import pytest
from website.views import allowed_file


def test_allowed_file():
    """Test the allowed filename verifier."""
    allowed_filenames = [
        "some_files.csv",
        "2840abc.csv",
        "25-qhat?.csv"
    ]
    prohibited_filenames = [
        "csv.jpg",
        "hacker_tool.sh",
        "Makefile",
        "hackIntoPPA.csv.c"
    ]

    for filename in allowed_filenames:
        assert allowed_file(filename) == True
    for filename in prohibited_filenames:
        assert allowed_file(filename) == False