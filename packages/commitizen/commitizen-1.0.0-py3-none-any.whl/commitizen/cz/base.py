import os
import sys
import logging
from commitizen import cmd
from abc import ABCMeta, abstractmethod
from tempfile import NamedTemporaryFile
from questionary import prompt

logger = logging.getLogger(__name__)


class BaseCommitizen(metaclass=ABCMeta):
    @abstractmethod
    def questions(self):
        """Questions regarding the commit message.

        Must have 'whaaaaat' format.
        More info: https://github.com/finklabs/whaaaaat/

        :rtype: list
        """

    @abstractmethod
    def message(self, answers):
        """Format your git message.

        :param answers: Use answers
        :type answers: dict

        :rtype: string
        """

    def commit(self, message: str):
        f = NamedTemporaryFile("wb", delete=False)
        f.write(message.encode("utf-8"))
        f.close()

        c = cmd.run(f"git commit -a -F {f.name}")
        print(c.out or c.err)

        os.unlink(f.name)
        return c

    def example(self):
        """Example of the commit message.

        :rtype: string
        """
        raise NotImplementedError("Not Implemented yet")

    def schema(self):
        """Schema definition of the commit message.

        :rtype: string
        """
        raise NotImplementedError("Not Implemented yet")

    def info(self):
        """Information about the standardized commit message.

        :rtype: string
        """
        raise NotImplementedError("Not Implemented yet")

    def show_example(self, *args, **kwargs):
        logger.info(self.example())

    def show_schema(self, *args, **kwargs):
        logger.info(self.schema())

    def show_info(self, *args, **kwargs):
        logger.info(self.info())

    def run(self, *args, **kwargs):
        questions = self.questions()
        answers = prompt(questions)
        logger.debug("Answers:\n %s", answers)
        m = self.message(answers)
        logger.debug("Commit message generated:\n %s", m)

        c = self.commit(m)

        if c.err:
            logger.warning(c.err)
            sys.exit(1)

        if "nothing added" not in c.out:
            logger.info("Commit successful!")

        sys.exit(0)
