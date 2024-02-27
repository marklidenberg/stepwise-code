import re
import textwrap

from stepwise_code.clean_test_string import clean_test_string
from stepwise_code.repeat_symbol_split import repeat_symbol_split


def format_steps(text: str, line_comment_symbol: str = "#") -> str:
    """Format code steps."""

    def _substitutor(match: re.Match, text: str) -> str:
        # - Extract

        (
            spaces1,
            dashes,
            spaces2,
            text,
        ) = match.groups()  # sample comment: (spaces1) # (spaces2) (dashes, like ----) (spaces3) (text)

        # - Strip

        text = text.strip()

        # - Make title

        text = text[0].upper() + text[1:]

        # - Remove trailing dots

        text = re.sub(r"[\.]*$", "", text)

        # - Return

        return f"\n{spaces1}{line_comment_symbol} {repeat_symbol_split('-', len(dashes))} {text.strip()}\n\n"

    empty_line = rf"(?:[ ]*\n)"
    pattern = rf"^{empty_line}*([ ]*){re.escape(line_comment_symbol)} (-+)([ ]+)([^\n]+){empty_line}*"
    return re.sub(
        pattern=pattern,
        repl=lambda match: _substitutor(match, text=text),
        string=text,
        flags=re.MULTILINE,
    )


# fmt: off

def test():
    text1 = """
    # - Step 1
    a = 1
    # -- Sub-step 1
    b = 2
    # -- Sub-step 2
    c = 3
    """

    text2 = """
    # - Step 1

    a = 1

    # -- Sub-step 1

    b = 2

    # -- Sub-step 2

    c = 3
    """

    assert clean_test_string(format_steps(text1)) == clean_test_string(text2)

# fmt: on

if __name__ == "__main__":
    test()
