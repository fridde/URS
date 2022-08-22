"""
Tools
=====
Running all tools that URS has to offer.
"""


import logging

from analytics.frequencies import GenerateFrequencies
from analytics.wordcloud import GenerateWordcloud

from praw_scrapers.live_scrapers.livestream import Livestream

from praw_scrapers.static_scrapers.basic import RunBasic
from praw_scrapers.static_scrapers.comments import RunComments
from praw_scrapers.static_scrapers.redditor import RunRedditor
from praw_scrapers.static_scrapers.subreddit import RunSubreddit

from praw_scrapers.utils.validation import Validation

from utils.cli import (
    CheckCli,
    Parser
)
from utils.titles import MainTitle
from utils.utilities import DateTree

class Run():
    """
    Methods to call CLI and all tools.
    """

    def __init__(self, reddit):
        """
        Initialize variables used in instance methods:

            self._reddit: Reddit instance
            self._args: argparse Namespace object
            self._parser: argparse ArgumentParser object

        Calls a private method:

            self._introduce_then_args()

        Parameters
        ----------
        reddit: PRAW Reddit object

        Returns
        -------
        None
        """

        self._reddit = reddit
        self._args, self._parser = self._introduce_then_args()
        
    def _introduce_then_args(self):
        """
        Print title, then run checks for CLI args and PRAW credentials.

        Calls previously defined public methods:

            MainTitle.title()

            Parser().parse_args()
            CheckCli().check_args()

        Parameters
        ----------
        None

        Returns
        -------
        args: Namespace
            argparse Namespace object
        parser: ArgumentParser
            argparse ArgumentParser object
        """

        MainTitle.title()

        args, parser = Parser().parse_args()
        CheckCli().check_args(args)

        return args, parser

    def run_urs(self):
        """
        Switch for running all URS tools.

        Calls previously defined public methods:

            PRAW validation:

                Validation.validate_user()

            PRAW scrapers:

                RunSubreddit.run()
                RunRedditor.run()
                RunComments.run()
                RunBasic.run()

            PRAW livestream scrapers:

                Livestream.stream()
            
            Analytical tools:

                GenerateFrequencies.generate()
                GenerateWordcloud.generate()
        """

        if self._args.check:
            """
            Run rate limit check.
            """

            logging.info("RUNNING API CREDENTIALS CHECK.")
            logging.info("")

            Validation.validate_user(self._parser, self._reddit)

        elif self._args.tree:
            """
            Display visual directory tree for a date (default is the current date).
            """

            DateTree.display_tree(self._args.tree)

        elif self._args.subreddit or self._args.redditor or self._args.comments or self._args.basic:
            """
            Run PRAW scrapers.
            """
            
            Validation.validate_user(self._parser, self._reddit)

            if self._args.subreddit:
                RunSubreddit.run(self._args, self._parser, self._reddit)
            if self._args.redditor:
                RunRedditor.run(self._args, self._parser, self._reddit)
            if self._args.comments:
                RunComments.run(self._args, self._parser, self._reddit)
            elif self._args.basic:
                RunBasic.run(self._args, self._parser, self._reddit)

        elif self._args.live_subreddit or self._args.live_redditor:
            """
            Run PRAW livestream scrapers.
            """

            Validation.validate_user(self._parser, self._reddit)
            Livestream.stream(self._args, self._reddit)
        
        elif self._args.frequencies or self._args.wordcloud:
            """
            Run analytical tools.
            """

            if self._args.frequencies:
                GenerateFrequencies.generate(self._args)
            if self._args.wordcloud:
                GenerateWordcloud.generate(self._args)
