import pytest

from ionex_formatter.formatter import (
    IonexFile,
    UnknownFormatingError,
    UnknownFormatSpecifier,
)


def test_1():
    formatter = IonexFile()
    with pytest.raises(UnknownFormatingError):
        formatter._verify_formatted(10.0, "I", "1", 2, 0)


def test_2():
    formatter = IonexFile()
    formatter.add_comment("123")


def test_3():
    formatter = IonexFile()
    with pytest.raises(UnknownFormatSpecifier):
        formatter.format_header_line()
