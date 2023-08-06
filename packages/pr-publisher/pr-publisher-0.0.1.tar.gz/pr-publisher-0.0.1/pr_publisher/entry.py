from collections import Counter
from datetime import datetime, timezone

NOW = datetime.utcnow().replace(tzinfo=timezone.utc)


class PublishEntry:
    """
    Each of these represents one pull request.

    This is a place to prep a PR with extra data for publishers to use.
    """

    class StatusCheck:
        """
        Helps facilitate cross-referencing of executed checks on the pull
        request with the repositories required checks.
        """

        def __init__(self, name, is_required, obj=None):
            self.name = name
            self.is_required = is_required
            self._obj = obj
            if not self._obj:
                self.state = "expected"
            else:
                self.state = self._obj.state

    def __init__(self, args, pr, approvals):
        self.args = args
        self.pr = pr
        self.issue = pr.issue()
        self.approvals = approvals

        self.age_since_creation = NOW - pr.created_at
        self.age_since_update = NOW - pr.updated_at

        self.age_since_creation_in_days = (
            self.age_since_creation.days + self.age_since_creation.seconds / (24 * 3600)
        )
        self.age_since_update_in_days = (
            self.age_since_update.days + self.age_since_update.seconds / (24 * 3600)
        )

        # https://developer.github.com/v4/enum/mergestatestatus/
        self.mergeable_state = pr.mergeable_state

        c = Counter([x.state for x in approvals])
        self.approval_count = c["APPROVED"]
        self.request_changes_count = c["REQUEST_CHANGES"]
        assert self.approval_count + self.request_changes_count == len(approvals)

        self.approvals_needed_count = None
        if self.args.approvals_needed:
            self.approvals_needed_count = self.args.approvals_needed

        self._required_status_check_names = self._get_required_status_checks()
        self._current_status_checks = self._get_status_checks()

        self.status_checks = {
            name: self.StatusCheck(name, is_required=True)
            for name in self._required_status_check_names
        }
        for check in self._current_status_checks:
            name = check.context
            is_required = name in self.status_checks
            self.status_checks[name] = self.StatusCheck(name, is_required, check)

        self.label_names = [x.name for x in self.issue.labels()]

        self.action_string = self._get_action_string()

    def _get_required_status_checks(self):
        base_branch = self.pr.repository.branch(self.pr.base.ref)
        # NOTE: there's an "enforcement_level" we could respect. This seems
        # to be set to "everyone" for our repos.
        return base_branch.original_protection["required_status_checks"]["contexts"]

    def _get_status_checks(self):
        commits = list(self.pr.commits())
        status = commits[-1].status()
        return status.statuses

    def _get_action_string(self):
        # Want to know
        #  1. Does it need rebase?
        #  2. Does it need reviews?
        #  3. Are checks passing?
        #     - Grab latest commit for the PR
        #     - Grab status checks for the commit
        #     - Cross reference status checks with those required, since
        #       there may be required checks that haven't run yet.
        parts = []
        if self.mergeable_state in ["dirty", "behind"]:
            parts.append("needs rebase")

        passing_count = len(
            [
                x
                for x in self.status_checks.values()
                if x.is_required and x.state == "success"
            ]
        )
        total_count = len([x for x in self.status_checks.values() if x.is_required])
        if passing_count < total_count:
            parts.append(f"{passing_count}/{total_count} required checks passed")

        if self.request_changes_count > 0:
            parts.append("changes requested")

        # Optional, based on CLI args
        if (self.approvals_needed_count and self.approval_count < self.approvals_needed_count):
            parts.append(f"needs {2 - self.approval_count} approval(s)")
        return ", ".join(parts)
