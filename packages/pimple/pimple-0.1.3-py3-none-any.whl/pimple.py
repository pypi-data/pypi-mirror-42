"""
pimple
--------

usage: pimple.py [-h] TEST_DIR

positional arguments:
  TEST_DIR    The test directory to search

optional arguments:
  -h, --help  show this help message and exit
"""

import argparse
import re
import textwrap
from collections import namedtuple
from pathlib import Path


# Regular expressions
TEST_FUNC = re.compile(
    r"""
    def             # def statement
    [ ]             # space
    (
        test_       # any function beginning with 'test_"
        \w*         # the remaining name of the function
    )
    \(              # opening paren for args
        [\w,= ]*    # args
    \):\n           # closing paren, colon, newline
    \s*\"{3}        # opening 3 quotes
    (
        [^"]*       # the docstring (any character that is not a quote)
    )
    \"{3}           # closing 3 quotes
    """,
    re.VERBOSE,
)


# Named tuples for collecting data
TestModule = namedtuple("TestModule", "name, functions")
TestFunction = namedtuple("TestFunction", "name, docstring")


def flush_left(text: str) -> str:
    """Remove leading whitespace from each line."""
    lines = text.split("\n")
    lines = [line.lstrip() for line in lines]
    return "\n".join(lines)


def format_rst(modules: list) -> str:
    """Format the test case docstrings for reStructuredText."""
    output = flush_left(
        """Test cases
           ==========
        """
    )
    for module in modules:
        output += textwrap.dedent(
            f"""
            {module.name}
            {"":-<{len(module.name)}}
            """
        )
        for function in module.functions:
            output += flush_left(
                f"""
                {function.name}
                {"":"<{len(function.name)}}

                {function.docstring}
                """
            )
    return output


def main():
    """Recurse through the given directory and compile a summary of test cases found."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "test_dir", metavar="TEST_DIR", type=str, help="The test directory to search"
    )
    args = parser.parse_args()

    modules = []
    test_dir = Path(args.test_dir)
    test_files = test_dir.glob("**/test_*.py")
    for test_file in test_files:
        test_funcs = []
        with open(test_file, "r") as f:
            lines = f.read()
            funcs = TEST_FUNC.findall(lines)
            for func in funcs:
                test_funcs.append(TestFunction(*func))
        modules.append(TestModule(name=str(test_file), functions=test_funcs))

    with open("testcase_summary.rst", "w") as f:
        f.write(format_rst(modules))


if __name__ == "__main__":
    main()
