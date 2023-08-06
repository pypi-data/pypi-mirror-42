import requests

from pr_publisher.publishers.base import BasePublisher


class SlackPublisher(BasePublisher):
    """Posts a list of pull requests to slack"""

    MERGE_STATE_COLORS = {
        "behind": "warning",
        "blocked": "warning",
        "clean": "good",
        "dirty": "danger",
        "has_hooks": "good",
        "unstable": "warning",
    }

    @classmethod
    def add_cli_arguments(cls, parser):
        parser.add_argument(
            "--slack-token",
            default=None,
            env_var="SLACK_TOKEN",
            help='The slack token to use (required for "slack" publisher)',
        )
        parser.add_argument(
            "--slack-url",
            env_var="SLACK_URL",
            default=None,
            help='The Slack webhook url (required for "slack" publisher)',
        )
        parser.add_argument(
            "--slack-channel",
            default=None,
            env_var="SLACK_CHANNEL",
            help='Slack channel to post in (optional for "slack" publisher)',
        )
        parser.add_argument(
            "--slack-approved-emoji",
            default=None,
            env_var="SLACK_APPROVED_EMOJI",
            help="Emoji/character for pull requests approvals",
        )
        parser.add_argument(
            "--slack-changes-requested-emoji",
            default=None,
            env_var="SLACK_CHANGES_REQUESTED_EMOJI",
            help="Emoji/character for pull requests disapprovals",
        )
        parser.add_argument(
            "--slack-status-check-success-emoji",
            default=None,
            env_var="SLACK_STATUS_CHECK_SUCCESS_EMOJI",
            help="Emoji/character for a successful PR check",
        )
        parser.add_argument(
            "--slack-status-check-pending-emoji",
            default=None,
            env_var="SLACK_STATUS_CHECK_PENDING_EMOJI",
            help="Emoji/character for a pending PR check",
        )
        parser.add_argument(
            "--slack-status-check-failed-emoji",
            default=None,
            env_var="SLACK_STATUS_CHECK_FAILED_EMOJI",
            help="Emoji/character for a failed PR check",
        )

    def __init__(self, args):
        super(SlackPublisher, self).__init__(args)

        if not args.slack_token:
            raise Exception("--slack-token is required for SlackPublisher")

        self.session = requests.Session()
        self.session.headers = {"Content-type": "application/json"}
        self.session.params = {"token": args.slack_token}

        # Note: tested with the slack.com/services/hooks/jenkins-ci url
        # There are "incoming webhook" urls, as well as chat.postMessage
        # that may have differences in the specific request details.
        self.webhook_url = args.slack_url
        self.channel = args.slack_channel

        self.approved_emoji = args.slack_approved_emoji
        self.changes_requested_emoji = args.slack_changes_requested_emoji

        self.check_success_emoji = args.slack_status_check_success_emoji
        self.check_pending_emoji = args.slack_status_check_pending_emoji
        self.check_failed_emoji = args.slack_status_check_failed_emoji

    def publish(self, publish_entries):
        # TODO: message for no open pull requests
        payload = {
            "text": "Open pull requests",
            "attachments": list(map(self.get_attachment, publish_entries)),
        }
        if self.channel:
            payload["channel"] = self.channel

        resp = self.session.post(self.webhook_url, json=payload)
        if not resp.ok:
            raise Exception(
                "[{}] {} {}\n{}".format(
                    resp.status_code, resp.request.method, resp.request.url, resp.text
                )
            )

    def get_attachment(self, entry):
        return {
            "title": self._attachment_title(entry),
            "text": self._attachment_text(entry),
            "color": self._attachment_color(entry),
        }

    def _attachment_title(self, entry):
        return "[{}]{} {}".format(
            entry.pr.created_at.date(),
            self._emojis_for_approvals(entry),
            entry.pr.title,
        )

    def _attachment_text(self, entry):
        status_string = entry.mergeable_state
        if entry.action_string:
            status_string += ": " + entry.action_string

        result = "<{}|{}#{}> - {} days since last update {}\n{}".format(
            entry.pr.html_url,
            entry.pr.repository.full_name,
            entry.pr.number,
            round(entry.age_since_update_in_days),
            self._emojis_for_status_checks(entry),
            status_string,
        )

        if self.args.show_labels and entry.label_names:
            result += '\nlabels: ' + ', '.join(entry.label_names)
        return result

    def _attachment_color(self, entry):
        return self.MERGE_STATE_COLORS.get(entry.mergeable_state)

    def _emojis_for_approvals(self, entry):
        result = ""
        if self.approved_emoji:
            result += self.approved_emoji * entry.approval_count
        if self.changes_requested_emoji:
            result += self.changes_requested_emoji * entry.request_changes_count
        return result

    def _emojis_for_status_checks(self, entry):
        def status_to_emoji(chk):
            if chk.state == "success":
                return self.check_success_emoji if self.check_success_emoji else ""
            if chk.state == "failure":
                return self.check_failed_emoji if self.check_failed_emoji else ""
            return self.check_pending_emoji if self.check_pending_emoji else ""

        checks = sorted(entry.status_checks.values(), key=lambda chk: chk.state)
        if checks:
            return "".join(map(status_to_emoji, reversed(checks)))
        return ""
