# -*- coding: utf-8 -*-


"""src.src: provides entry point main()."""

__version__ = "0.1"


from src.bitbucket import bitbucket_runner
from src.utils import get_config, get_logger

logger = get_logger("AzimuGitCLI")


def process_git():
    git_provider_name = get_config("git")
    if git_provider_name == "bitbucket":
        endpoint = "/data/git"
        bitbucket_runner.run(endpoint)


def main():
    process_git()


if __name__ == '__main__':
    main()
