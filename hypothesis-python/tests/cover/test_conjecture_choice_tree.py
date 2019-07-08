# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

from random import Random

import hypothesis.strategies as st
from hypothesis import given
from hypothesis.internal.compat import hrange
from hypothesis.internal.conjecture.choicetree import ChoiceTree


def exhaust(f):
    tree = ChoiceTree()

    random = Random(0)

    results = []
    while not tree.exhausted:
        tree.step(random, lambda chooser: results.append(f(chooser)))
    return results


@given(st.lists(st.integers()))
def test_can_enumerate_a_shallow_set(ls):
    results = exhaust(lambda chooser: chooser.choose(ls))

    assert sorted(results) == sorted(ls)


def test_can_enumerate_a_nested_set():
    @exhaust
    def nested(chooser):
        i = chooser.choose(hrange(10))
        j = chooser.choose(hrange(10), condition=lambda j: j > i)
        return (i, j)

    assert sorted(nested) == [(i, j) for i in hrange(10) for j in hrange(i + 1, 10)]


def test_can_enumerate_empty():
    @exhaust
    def empty(chooser):
        return 1

    assert empty == [1]
