"""Behaviour of the Algorithm 3.1 reference implementation on synthetic polygons."""

import pytest
from shapely.affinity import translate
from shapely.geometry import box

from wcc_carbon.dedup import deduplicate, overlap_fraction


def test_identical_field_drawn_twice_is_removed():
    field = box(0, 0, 100, 100)
    redrawn = translate(field, 2, 0)  # same field, digitised slightly offset (98 % overlap)
    kept, audit = deduplicate([("F1", field), ("F1b", redrawn)])
    assert len(kept) == 1
    assert len(audit) == 1
    assert audit[0].overlap >= 0.93


def test_adjacent_fields_sharing_a_boundary_are_kept():
    a = box(0, 0, 100, 100)
    b = box(98, 0, 198, 100)  # 2 % sliver along the shared hedge line
    kept, audit = deduplicate([("A", a), ("B", b)])
    assert {pid for pid, _ in kept} == {"A", "B"}
    assert audit == []


def test_largest_polygon_is_the_one_retained():
    big = box(0, 0, 100, 100)
    small = box(10, 10, 60, 60)  # fully inside: overlap / min(area) = 1.0
    kept, audit = deduplicate([("small", small), ("big", big)])
    assert [pid for pid, _ in kept] == ["big"]
    assert audit[0].dropped_id == "small" and audit[0].kept_id == "big"


def test_overlap_is_measured_against_the_smaller_polygon():
    big = box(0, 0, 100, 100)
    small = box(0, 0, 10, 10)
    assert overlap_fraction(big, small) == pytest.approx(1.0)


def test_threshold_must_be_a_fraction():
    with pytest.raises(ValueError):
        deduplicate([("A", box(0, 0, 1, 1))], tau=1.5)
