"""Greedy non-maximum suppression for polygon deduplication (Algorithm 3.1).

Polygons are sorted by area, largest first. Each polygon is compared with every
polygon already retained; if its overlap, measured as a fraction of the smaller
polygon's area, reaches the threshold tau, it is discarded as a duplicate.

    overlap(p, q) = area(p ∩ q) / min(area(p), area(q))

In the West Dean data the overlap distribution was bimodal (true duplicates
93-100 %, adjacent fields under 5 %), so tau = 0.5 separated the two cleanly.
Cleaning removed 28 duplicate Farm polygons and 212.6 ha of double counting.
"""

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from shapely.geometry.base import BaseGeometry


@dataclass(frozen=True)
class DuplicateRecord:
    """Audit-trail entry: which polygon was dropped, what it duplicated, by how much."""

    dropped_id: str
    kept_id: str
    overlap: float


def overlap_fraction(p: BaseGeometry, q: BaseGeometry) -> float:
    """Intersection area as a fraction of the smaller polygon's area."""
    smaller = min(p.area, q.area)
    if smaller == 0:
        return 0.0
    return p.intersection(q).area / smaller


def deduplicate(
    polygons: Iterable[Tuple[str, BaseGeometry]],
    tau: float = 0.5,
) -> Tuple[List[Tuple[str, BaseGeometry]], List[DuplicateRecord]]:
    """Return (retained polygons, audit trail of removed duplicates).

    ``polygons`` is an iterable of (id, geometry) pairs in a projected,
    metre-based CRS (the project used British National Grid, EPSG:27700).
    """
    if not 0 < tau < 1:
        raise ValueError("tau must lie in (0, 1)")

    ordered: Sequence[Tuple[str, BaseGeometry]] = sorted(
        polygons, key=lambda item: item[1].area, reverse=True
    )
    retained: List[Tuple[str, BaseGeometry]] = []
    audit: List[DuplicateRecord] = []

    for pid, geom in ordered:
        duplicate_of = None
        for kid, kept in retained:
            ov = overlap_fraction(geom, kept)
            if ov >= tau:
                duplicate_of = DuplicateRecord(pid, kid, round(ov, 4))
                break
        if duplicate_of is None:
            retained.append((pid, geom))
        else:
            audit.append(duplicate_of)
    return retained, audit
