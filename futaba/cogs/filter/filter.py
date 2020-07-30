#
# cogs/filter/filter.py
#
# futaba - A Discord Mod bot for the Programming server
# Copyright (c) 2017-2020 Jake Richardson, Ammon Smith, jackylam5
#
# futaba is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import logging
import re

from confusable_homoglyphs import confusables

from futaba.str_builder import StringBuilder

logger = logging.getLogger(__name__)

__all__ = ["UNICODE_SPACES_REGEX", "Filter"]

UNICODE_SPACES_REGEX = re.compile(
    "".join(
        (
            "[",
            "\u0020\u00a0\u1680",
            "\u180e\u2000\u2001",
            "\u2002\u2003\u2004",
            "\u2005\u2006\u2006",
            "\u2007\u2008\u2009",
            "\u200a\u200b\u202f",
            "\u205f\u3000\ufeff",
            "]",
        )
    )
)


class Filter:
    __slots__ = ("text", "regex")

    def __init__(self, text):
        logger.info("Creating filter regular expression from %r", text)
        groups = confusables.is_confusable(text, greedy=True)
        if groups:
            pattern = Filter.build_regex(text, groups)
        else:
            pattern = re.escape(text)

        logger.debug("Generated pattern: %r", pattern)

        self.text = text
        self.regex = re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def build_regex(text, groups):
        # Build similar character tree
        chars = {}
        pattern = StringBuilder()
        for group in groups:
            pattern.write("[")
            char = group["character"]
            pattern.write(re.escape(char))
            for homoglyph in group["homoglyphs"]:
                pattern.write(re.escape(homoglyph["c"]))
            pattern.write("]")
            chars[char] = str(pattern)
            pattern.clear()

        # Create pattern
        for char in text:
            pattern.write(chars.get(char, char))

        return str(pattern)

    def matches(self, content):
        contents = (content, UNICODE_SPACES_REGEX.sub("", content))

        return bool(any(map(self.regex.search, contents)))

    def __hash__(self):
        return hash(self.text) ^ 0x2C6F024ED28

    def __eq__(self, other):
        return (
            isinstance(self, Filter)
            and isinstance(other, Filter)
            and self.text == other.text
        )
