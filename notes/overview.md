# Issue 2036

## Issue Overview

**[2036]**(https://github.com/HypothesisWorks/hypothesis/issues/2036)

As of **[#2030]**(https://github.com/HypothesisWorks/hypothesis/issues/2036)
we have a special case for lists(sampled_from(...), unique=True)
that uses a custom strategy. Unfortunately this special casing is trivial to
defeat. e.g. lists(sampled_from(...).map(lambda x: x), unique=True) should
behave the same way but doesn't. It would be good to extend this support to
include arbitrary chains of maps and filters over sampled_from.

There are a couple of possible ways to do this, but I think the easiest would be
to extend the base SampledFrom strategy to have a transform function which takes
an element of the sample and either transforms it or raises an
UnsatisfiedAssumption (or returns a special value). The special case unique list
strategy could then call this transformed function directly.

## Current Behavior


`lists(sampled_from(...), unique=True)`

has been improved to run faster, or stop quicker (after 20 discards at attempting
to find a unique element)

`lists(sampled_from(...).map(lambda x: x), unique=True)`

does not run in the same efficient way.

## Desired Behavior

Arbitrary chains of maps and filters over sampled_from run performantly.

## Approach

Extend the base `SampledFrom` strategy to have a `transform` function 

`transform`
takes an element of the sample and either transforms it or raises an
`UnsatisfiedAssumption` 

`UniqueSampledListStrategy` then calls this transformed function
directly.

## Relevant Code

[`UniqueSampledListStrategy`][UniqueSampledListStrategy-Impl] is returned from `lists` strategy


[`class SampledFromStrategy(SearchStrategy)`][SampledFromStrategy]  which is the class containing the `sampled_from` method


**definition of stopping criteria that speeds up sampling performance**

[data.py - discards def][data-sampling-one]  
[data.py - stop example][data-sampling-two]


**example use of UnsatisfiedAssumption**

[`MappedSearchStrategy.do_draw`][mapped-search-strategy-do-draw]


```
    try:
        data.start_example(MAPPED_SEARCH_STRATEGY_DO_DRAW_LABEL)
        result = self.pack(data.draw(self.mapped_strategy))
        data.stop_example()
        return result
    except UnsatisfiedAssumption:
        data.stop_example(discard=True)
        if data.index == i:
            raise

raise UnsatisfiedAssumption()

```

--

[`UniqueSampledListStrategy`][UniqueSampledListStrategy]

[`utils.many.more`][utils.many.more]

```
class many(object):
    """Utility class for collections. Bundles up the logic we use for "should I
    keep drawing more values?" and handles starting and stopping examples in
    the right place.
    Intended usage is something like:
    elements = many(data, ...)
    while elements.more():
        add_stuff_to_result()
    """
```

<!-- ----------------------------------------- -->
<!-- LINKS -->

[UniqueSampledListStrategy-Impl]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/_strategies.py#L794-L801

[SampledFromStrategy]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/searchstrategy/misc.py#L67-L156

[data-sampling-one]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/internal/conjecture/data.py#L754

[data-sampling-two]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/internal/conjecture/data.py#L868

[mapped-search-strategy-do-draw]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/searchstrategy/strategies.py#L546-L559

[UniqueSampledListStrategy]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/searchstrategy/collections.py#L173

[utils.many.more]: https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis-python/src/hypothesis/internal/conjecture/utils.py#L347-L412