import prettytable

from pr_publisher.publishers.base import BasePublisher


class TablePublisher(BasePublisher):
    """Prints pull requests in a table format to stdout"""

    def publish(self, publish_entries):
        fields = [
            "+1's",
            "merge state",
            "action needed",
            "title",
            "created",
            "updated",
            "days since update",
            "link",
        ]

        if self.args.show_labels:
            fields.append('labels')

        table = prettytable.PrettyTable(field_names=fields)

        for entry in publish_entries:
            row = [
                entry.approval_count if entry.approval_count > 0 else "-",
                entry.mergeable_state,
                entry.action_string,
                entry.pr.title,
                entry.pr.created_at.date(),
                entry.pr.updated_at.date(),
                round(entry.age_since_update_in_days),
                entry.pr.html_url,
            ]
            if self.args.show_labels:
                label_names = ' '.join(entry.label_names) if entry.label_names else ''
                row.append(label_names)

            table.add_row(row)
        print(table)
