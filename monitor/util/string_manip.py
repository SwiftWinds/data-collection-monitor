
import re
import unittest

CAMEL_KEBAB_RE = re.compile(r'(?!^)(?=[A-Z])')


def camel_kebab(s: str, sep: str = '-') -> str:
    """
    Convert the passed string from ``camelCase`` or ``PascalCase``
    to ``kebab-case``. Assumes that every new capital letter constitutes a new
    word.
    """
    return CAMEL_KEBAB_RE.sub(sep, s).lower()


class TestFunctional(unittest.TestCase):
    def test_camel_kebab(self):
        camel = 'aStringInCamelCase'
        pascal = 'AStringInPascalCase'
        self.assertEqual('', camel_kebab(''))
        self.assertEqual('foo', camel_kebab('foo'))
        self.assertEqual('a-string-in-camel-case', camel_kebab(camel))
        self.assertEqual('a-string-in-pascal-case', camel_kebab(pascal))

        self.assertEqual('a_string_in_pascal_case', camel_kebab(pascal, '_'))
