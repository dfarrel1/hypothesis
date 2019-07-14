import pytest
import numpy as np

from hypothesis import seed, given, strategies as st
from hypothesis.searchstrategy.misc import SampledFromStrategy

from tests.common.debug import assert_no_examples, find_any, minimal

from hypothesis.errors import Frozen, InvalidArgument
from hypothesis.internal.compat import hbytes, hrange
from hypothesis.internal.conjecture.data import (
    MAX_DEPTH,
    ConjectureData,
    DataObserver,
    Overrun,
    Status,
    StopTest,
)
from hypothesis.searchstrategy.strategies import SearchStrategy


### reproduct old issue in 2030
def test_blacklisted_characters():
    bad_chars = u"te02тест49st"
    active_strategy = st.characters(
        min_codepoint=ord("0"), max_codepoint=ord("9"), blacklist_characters=bad_chars
    )
    assert "1" == minimal(active_strategy, lambda c: True)
    assert_no_examples(active_strategy, lambda c: c in bad_chars)

def test_integers():
    assert_no_examples(st.integers(0, 5), lambda x: False)

# def test_discarded_data_is_eventually_terminated():
#       data = ConjectureData.for_buffer(hbytes(100))
#       with pytest.raises(StopTest):
#          for _ in hrange(100):
#              data.start_example(1)
#              data.draw_bits(1)
#              data.stop_example(discard=True)

#       assert data.status == Status.INVALID

### something (whatever) that works
@given(lst=st.lists(st.integers(), min_size=5, max_size=10))
def test_sort_a_list_hypothesis(lst):
    new = sorted(list(lst))    
    assert sorted(lst) == new

### using custom strategy with sample_from
@given(st.lists(st.sampled_from(range(4)), unique=True))
def test_sampled_from_special(lst):
    # print('lst : {}'.format(lst))
    pass

### defeated special casing
@given(st.lists(st.sampled_from(range(4)), unique=True).map(lambda x: x))
def test_sampled_from_defeated(lst):
    # print('lst : {}'.format(lst))
    pass

### defeated special casing
@given(st.just(range(4)))
def test_sampled_from_strategy_class(lst):
    print('SampledFromStrategy(lst)')
    print(dir(SampledFromStrategy(lst)))
    # pass    
