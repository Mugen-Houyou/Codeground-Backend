import pytest
from datetime import datetime, timedelta, timezone

from src.app.domain.match.schemas.match_schemas import MatchingUserInfo
from src.app.domain.match.utils.matcher import (
    pop_median_user,
    force_match,
    greedy_matching,
    hungarian_matching,
    filtering_gap,
)


def make_user(uid: int, mmr: float, rd: float = 0, wait: int = 0) -> MatchingUserInfo:
    return MatchingUserInfo(
        id=uid,
        mmr=mmr,
        rd=rd,
        joined_at=datetime.now(timezone.utc) - timedelta(seconds=wait),
    )


def test_pop_median_user():
    users = [make_user(1, 1000), make_user(2, 1200), make_user(3, 1100)]
    median, rest = pop_median_user(users)
    assert median.id == 3
    assert {u.id for u in rest} == {1, 2}


def test_force_match():
    hard = make_user(1, 1500)
    waiting = [make_user(2, 1400), make_user(3, 1600), make_user(4, 1550)]
    victim = force_match(hard, waiting)
    assert victim.id == 4


def test_greedy_matching_even():
    users = [make_user(i, 1000 + i * 10) for i in range(4)]
    pairs, waiting = greedy_matching(users)
    assert len(pairs) == 2
    assert not waiting


def test_hungarian_matching_simple():
    users = [make_user(i, 1000 + i * 10) for i in range(4)]
    pairs, waiting = hungarian_matching(users)
    ids = sorted([sorted([a.id, b.id]) for a, b in pairs])
    assert ids == [[0, 1], [2, 3]]
    assert not waiting


def test_filtering_gap():
    a = make_user(1, 1000)
    b = make_user(2, 1020)
    c = make_user(3, 1000)
    d = make_user(4, 1100)
    pairs = [(a, b), (c, d)]
    matched, waiting = filtering_gap(pairs)
    assert (a, b) in matched
    assert c in waiting and d in waiting
