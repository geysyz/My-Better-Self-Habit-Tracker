from datetime import date

from habit_tracker.excuse import ExcusedPeriod, ExcusePolicy

TODAY = date(2026, 11, 10)
policy = ExcusePolicy()


def check(start, end, existing=(), reason="Trip"):
    return policy.validate(start, end, reason, TODAY, list(existing))


def test_valid_period_accepted():
    assert check(date(2026, 11, 11), date(2026, 11, 12)) is None

def test_end_before_start_rejected():
    assert "End date" in check(date(2026, 11, 12), date(2026, 11, 11))

def test_too_far_in_future_rejected():
    assert "future" in check(date(2026, 12, 20), date(2026, 12, 21))

def test_too_far_in_past_rejected():
    assert "past" in check(date(2026, 11, 6), date(2026, 11, 7))

def test_three_days_back_accepted():
    assert check(date(2026, 11, 7), date(2026, 11, 8)) is None

def test_longer_than_14_days_rejected():
    assert "14 days" in check(date(2026, 11, 10), date(2026, 11, 25))

def test_exactly_14_days_accepted():
    assert check(date(2026, 11, 10), date(2026, 11, 23)) is None

def test_overlap_rejected():
    existing = [ExcusedPeriod(1, date(2026, 11, 10), date(2026, 11, 12), "Trip")]
    assert "overlaps" in check(date(2026, 11, 12), date(2026, 11, 14), existing)

def test_empty_reason_rejected():
    assert "Reason" in check(date(2026, 11, 11), date(2026, 11, 12), reason="  ")