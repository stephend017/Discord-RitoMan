import os
from discord_ritoman.utils import create_logger


def test_create_logger():
    """
    tests that create logger works correctly
    """

    logger = create_logger(__file__)
    logger.info("test")

    # date not included cause it changes
    expected = "[INFO] [test_utils.py:test_create_logger(11)]: test\n"

    fp = open(f"{__file__}.log", "r")
    actual = fp.read()[26:]  # remove the date
    fp.close()

    # cleanup
    os.remove(f"{__file__}.log")

    assert expected == actual
