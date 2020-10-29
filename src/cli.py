# -*- coding: utf-8 -*-


"""src.src: provides entry point main()."""

__version__ = "0.1"

from src.bitbucket import bitbucket_runner
from src.utils import get_config, get_logger

logger = get_logger("AzimuGitCLI")


def process_git():
    result = False
    git_provider_name = get_config("git")
    if git_provider_name == "bitbucket":
        endpoint = "/data/git"
        result = bitbucket_runner.run(endpoint)
    return result


def main():
    return process_git()


if __name__ == '__main__':
    main()
