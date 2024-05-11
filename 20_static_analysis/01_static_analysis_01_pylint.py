
# pylint <this script path>

from dataclasses import dataclass


# ------------------------------------------------------------------------------
# pylint
# 'pylint <this script path>'
# ------------------------------------------------------------------------------

@dataclass
class Author:
    cookbooks: list[str]


# pylint: W0613: Unused argument 'name' (unused-argument)
def find_author(name: str):
    return Author([])


# pylint: W0102: Dangerous default value [] as argument (dangerous-default-value)
def add_authors_cookbooks(author_name: str, cookbooks: list[str] = []) -> bool:
    author = find_author(author_name)
    if author is None:
        assert False, "Author does not exist"
    else:
        for cookbook in author.cookbooks:
            cookbooks.append(cookbook)
        return True
