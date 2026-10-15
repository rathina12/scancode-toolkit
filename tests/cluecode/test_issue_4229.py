# SPDX-License-Identifier: Apache-2.0
"""Regression for https://github.com/aboutcode-org/scancode-toolkit/issues/4229.

A C++ source comment uses a compact "Author:" field followed by a dotted
name. The copyright detector should identify the author, not discard it.
"""
from cluecode.copyrights import AuthorDetection
from cluecode.copyrights import detect_copyrights_from_lines


def test_cpp_compact_author_line_issue_4229():
    numbered_lines = [
        (1, "//  Date:9 April,2012"),
        (2, "//  Author:Frankie.Chu"),
    ]
    detections = list(
        detect_copyrights_from_lines(
            numbered_lines,
            include_copyrights=False,
            include_holders=False,
            include_authors=True,
        )
    )
    authors = [d.author for d in detections if isinstance(d, AuthorDetection)]
    assert any("Frankie.Chu" in name for name in authors), authors
