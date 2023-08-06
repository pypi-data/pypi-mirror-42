Overview
--------

This is a CLI tool that can list open pull requests and post them somewhere,
mainly Slack. This is useful to help a team stay on top of pull request
reviews.

It is configurable, supports multiple publishers, and makes it easy to write
your own publishers.

```bash
pip install pr-publisher
```

note: This is NOT a bot, it is NOT a Slack plugin, and it does NOT support
updating pull requests in any way from the command line.

Please report any issues or feature requests [on Github](https://github.com/pglass/pr-publisher/issues)

Usage
-----

This installs a script called `pr-publisher`,

```bash
pr-publisher --help
```

Arguments are supplied with CLI options, or environment variables. See the
`--help` output or below for available options.

### Basic usage

The tool needs a Github personal access token with `repo` and `read:org` permissions.

```
[x] repo
[ ] admin:org
    [ ] write:org
    [x] read:org
```

(note: It will try to read branch protection settings to determine the required
checks for the repository. I forget if an additional permission is required
for this)

Provide the token either by CLI option, or environment variable.

| Flag                 | Env Var        | Example                        |
| -----                | -----          | -----                          |
| `--github-org`       | `GITHUB_ORG`   | `pglbutt`                      |
| `--github-token`     | `GITHUB_TOKEN` |                                |
| `--github-url`       | `GITHUB_URL`   | `https://github.<company>.com` |
| `--include-wip`      |                |                                |
| `--users`            |                | `pglass,hotpie`                |
| `--approvals-needed` |                | `2`                            |
| `--show-labels`      |                |                                |

Currently, the Github organization is required. Open pull requests will be
discovered from all repositories in the org. Optionally, that list can be
filtered down to those owned by specific Github usernames.

Github enterprise is supported. Just provide your Github enterprise url with
the `--github-url` (however, I have not tested 2fa).

```bash
### Using flags
pr-publisher --github-org my-org --github-token <token> table slack
```

```bash
### Using environment variables
export GITHUB_TOKEN=<token>
export GITHUB_ORG=my-org
pr-publisher --users pglass,hotpie table slack
```

By default, PRs with titles that contain "wip" (case-insensitive) are ignored.
Use the `--include-wip` flag if you wish to include those.

### Publishers

The script accepts a list of publisher names. Currently there are two publishers

- `table`: prints the list of pull requests in a table to stdout
- `slack`: posts the list of pull requests to slack

Each publisher specified will be run and will publish the list of open pull
requests.

```bash
### Run the "table" publisher
pr-publisher <options> table

### Run both the "table" and "slack" publishers
pr-publisher <options> table slack
```

### Slack publisher

The slack publisher requires a slack url and token. Currently, the Slack
Jenkins CI integration url is the only tested and known working webhook url.

Below is a full list of options,

| Flag                                 | Env Var                            | Example                                              |
| -----                                | -----                              | -----                                                |
| `--slack-token`                      | `SLACK_TOKEN`                      |                                                      |
| `--slack-url`                        | `SLACK_URL`                        | `https://<team>.slack.com/services/hooks/jenkins-ci` |
| `--slack-channel`                    | `SLACK_CHANNEL`                    | `#my-team`                                           |
| `--slack-approved-emoji`             | `SLACK_APPROVED_EMOJI`             | `:+1:`                                               |
| `--slack-changes-requested-emoji`    | `SLACK_CHANGES_REQUESTED_EMOJI`    | `:-1:`                                               |
| `--slack-status-check-success-emoji` | `SLACK_STATUS_CHECK_SUCCESS_EMOJI` | `:white_check_mark:`                                 |
| `--slack-status-check-pending-emoji` | `SLACK_STATUS_CHECK_PENDING_EMOJI` | `:grey_question:`                                    |
| `--slack-status-check-failed-emoji`  | `SLACK_STATUS_CHECK_FAILED_EMOJI`  | `:x:`                                                |

- The slack channel is optional. If not supplied, the slack message is sent to
the channel associated with the token.
- All emojis default to the empty string and can be plain text strings if you like
- The "approved" and "changes requested" emojis are used to display pull request
approvals.  If your team requires a minimum number of approvals for a pull request,
you should supply the `--approvals-needed` flag to display how many more approvals
are needed.


Custom Publishers
-----------------

There are two basic steps for a writing your own custom publisher,

- Subclass `BasePublisher` when creating your publisher class
- Register your publisher with `Main`

[Here's a basic example](examples/custom_publisher.py). You create your
publisher class, add any cli args you like, and then implement the publish
method.

```python
"""Example of a custom publisher"""
from pr_publisher.publishers.base import BasePublisher
from pr_publisher.main import Main


class CustomPublisher(BasePublisher):

    @classmethod
    def add_cli_arguments(cls, parser):
        # All publisher cli args should be optional. (A user may only care to
        # run a single publisher, and doesn't want to supply values for the
        # rest of the publishers)
        parser.add_argument("--some-chat-url", default=None)

    def __init__(self, args):
        super(CustomPublisher, self).__init__(args)

        if not args.some_chat_url:
            raise Exception("--some-chat-url is required")

    def publish(self, publish_entries):
        for entry in publish_entries:
            # Just printing, for the sake of this example.
            # see pr_publisher.entry.PublishEntry for all available fields.
            print("{}\n  {}".format(entry.pr.title, entry.pr.html_url))


def main():
    # Register the publisher before we run the program
    Main.register_publisher("some-chat", CustomPublisher)

    # Run the program
    Main().run()


if __name__ == "__main__":
    main()
```

You now have your publisher hooked up. You should see the new CLI arguments
show up for the `some-chat` publisher, as well as CLI args for all other
registered publishers (but this is truncated for the example).

```bash
$ python custom_publisher.py -h
...

positional arguments:
  {table,slack,some-chat}
                        List of publishers to run

optional arguments:
  -h, --help            show this help message and exit
  ...
  --some-chat-url SOME_CHAT_URL
```

To run your publisher, specify the publisher name (`some-chat` on the command
line.

```bash
$ python custom_publisher.py ... --some-chat-url 'http://chat.example.com' --users pglass some-chat
Logging in...
Collecting info...
Publishing with CustomPublisher
Fixing some bug
  https://github.com/pglass/pr-publisher/pull/2
Fixing another bug
  https://github.com/pglass/pr-publisher/pull/5
Adding some feature
  https://github.com/pglass/pr-publisher/pull/6
```
