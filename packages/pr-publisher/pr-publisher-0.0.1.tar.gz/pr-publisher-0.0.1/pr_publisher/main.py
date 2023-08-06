import logging

import configargparse
import github3

from pr_publisher.entry import PublishEntry
from pr_publisher.publishers.slack import SlackPublisher
from pr_publisher.publishers.table import TablePublisher


class Main:

    PUBLISHERS = {"table": TablePublisher, "slack": SlackPublisher}

    def __init__(self, args=None):
        self.args = args or self.parse_args()
        if self.args.debug:
            logging.basicConfig(level=logging.DEBUG)

        self.gh = self.authenticate()
        self.publishers = self.select_publishers(self.args)

    @classmethod
    def parse_args(cls):
        parser = configargparse.ArgParser(
            description="A CLI for publishing a list of open pull requests from Github.\n"
        )
        parser.add_argument("--debug", '-d', action='store_true')
        parser.add_argument("--github-url", default=None, env_var="GITHUB_URL")
        parser.add_argument(
            "--github-org",
            required=True,
            env_var="GITHUB_ORG",
            help="The Github Org where your repos live",
        )
        parser.add_argument(
            "--github-token",
            required=True,
            env_var="GITHUB_TOKEN",
            help='A Github token. Should have "repo" and "read:org" perms',
        )
        parser.add_argument(
            "publishers",
            default="table",
            nargs="+",
            choices=tuple(Main.PUBLISHERS.keys()),
            help="List of publishers to run",
        )
        parser.add_argument(
            "--include-wip",
            action="store_true",
            help="Include WIP pull requests"
        )
        # TODO: support filtering by users in a team
        parser.add_argument(
            "--users",
            default=None,
            help="Only list PRs in the org, opened by these users",
        )
        parser.add_argument(
            "--approvals-needed",
            default=None,
            type=int,
            help="(optional) The number of approvals needed for merge",
        )

        parser.add_argument(
            "--show-labels",
            default=False,
            action="store_true",
            help="Have the publisher display labels",
        )

        for publisher_cls in cls.PUBLISHERS.values():
            publisher_cls.add_cli_arguments(parser)

        return parser.parse_args()

    @classmethod
    def register_publisher(cls, name, publisher_cls):
        if name in cls.PUBLISHERS:
            raise Exception("Publisher name '{}' already used".format(name))
        cls.PUBLISHERS[name] = publisher_cls

    @classmethod
    def select_publishers(cls, args):
        return [cls.PUBLISHERS[key](args) for key in args.publishers]

    def authenticate(self):
        print("Logging in...")
        if self.args.github_url:
            return github3.enterprise_login(
                url=self.args.github_url, token=self.args.github_token
            )
        return github3.login(token=self.args.github_token)

    def run(self):
        print("Collecting info...")
        org = self.gh.organization(self.args.github_org)
        repos = org.repositories()
        prs = self.collect_pull_requests(repos)

        entries = []
        for pr in prs:
            # Ignore WIP pull requests by default
            # TODO: Look at labels as well
            if not self.args.include_wip and "wip" in pr.title.lower():
                continue

            # optionally, ignore PRs not from a specified list of users
            if self.args.users and pr.user.login not in self.args.users:
                continue

            # get all the fields
            pr = pr.refresh()

            approvals = self.collect_undismissed_approvals(list(pr.reviews()))

            entries.append(PublishEntry(self.args, pr, approvals))

        entries.sort(key=lambda x: -x.age_since_update)

        for publisher in self.publishers:
            print("Publishing with {}".format(publisher.__class__.__name__))
            publisher.publish(entries)

    def collect_pull_requests(self, repos, state="open"):
        return [pr for repo in repos for pr in repo.pull_requests(state=state)]

    def collect_undismissed_approvals(self, reviews):
        """
        This returns a list of reviews, which are the latest undismissed
        approvals (or disapprovals) for each user.

        Pull requests have a list of reviews. Each review state can be,

        - APPROVED
        - DISMISSED
        - REQUEST_CHANGES
        - COMMENTED
        - PENDING
            Pending is for unsubmitted reviews. Only the current user's
            pending reviews will be visible.

        A single user can have multiple reviews on the PR (e.g. approve,
        dismiss, then approve again). So walk through reviews in order,
        maintaining the the latest APPROVED or REQUEST_CHANGES review for each
        user that does not have a subsequent dismissal.
        """
        approvals_by_user = {}

        # Assuming they are sorted by time
        for review in reviews:
            user_key = review.user.login

            # Ignore reviews that don't approve or disapprove
            if review.state in ["COMMENTED", "PENDING"]:
                continue
            elif review.state == "DISMISSED":
                # Could a user approve twice over the life of a PR, and then
                # dismiss the first approval, but not the second??
                #
                # I think the Github UI just dismisses the latest approval.
                try:
                    del approvals_by_user[user_key]
                except KeyError:
                    pass
            elif review.state in ["APPROVED", "REQUEST_CHANGES"]:
                approvals_by_user[user_key] = review

        return sorted(approvals_by_user.values(), key=lambda r: r.submitted_at)
