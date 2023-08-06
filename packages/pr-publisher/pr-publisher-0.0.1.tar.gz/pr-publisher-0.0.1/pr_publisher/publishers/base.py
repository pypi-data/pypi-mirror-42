class BasePublisher(object):

    @classmethod
    def add_cli_arguments(cls, parser):
        """Sub-classes may implement this to add CLI arguments"""
        pass

    def __init__(self, args):
        self.args = args

    def publish(self, publish_entries):
        """
        Sub-classes must implement this to publish the list of pull requests

        :param publish_entries: A list of PublishEntry objects, each
            representing a single pull request
        """
        raise NotImplementedError
