# SPDX-License-Identifier: Apache-2.0
"""Regression for https://github.com/aboutcode-org/scancode-toolkit/issues/4229.

A C++ source comment uses a compact "Author:" field followed by a dotted
name. The copyright detector should identify the author, not discard it.
"""
import pytest

from cluecode.copyrights import AuthorDetection
from cluecode.copyrights import detect_copyrights_from_lines


@pytest.mark.parametrize('field', [
    'Author:Frankie.Chu',
    'Author: Frankie.Chu',
    'author:Frankie.Chu',
    'Authors:Frankie.Chu',
    'Author:\tFrankie.Chu',
])
def test_cpp_compact_author_line_issue_4229(field):
    numbered_lines = [
        (1, "//  Date:9 April,2012"),
        (2, f"//  {field}"),
    ]
    detections = list(
        detect_copyrights_from_lines(
            numbered_lines,
            include_copyrights=False,
            include_holders=False,
            include_authors=True,
        )
    )
    authors = [(d.author, d.start_line, d.end_line)
               for d in detections if isinstance(d, AuthorDetection)]
    assert authors == [('Frankie.Chu', 2, 2)]


@pytest.mark.parametrize('line', [
    '// Frankie.Chu',
    '// License:License.Txt',
    '// NotAuthor:Frankie.Chu',
])
def test_dotted_token_without_author_field_is_not_an_author(line):
    detections = list(detect_copyrights_from_lines([(1, line)]))
    assert not [d for d in detections if isinstance(d, AuthorDetection)]


def test_compact_author_field_with_spaced_name():
    detections = list(detect_copyrights_from_lines([(1, '// Author:John Smith')]))
    assert [d.author for d in detections if isinstance(d, AuthorDetection)] == ['John Smith']
