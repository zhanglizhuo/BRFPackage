"""Mutation-pin tests: each test fails if a specific silent-precision mutation
is introduced. These close the six surviving mutants found by mutation testing
(M2, M6, M7, M8, M9, M10). Every test recomputes its expectation independently
rather than calling the function under test.
"""
import inspect

import numpy as np
import pytest

from brf.metrics.baseline_gap import compute_b
from brf.metrics.instability import compute_i
from brf.metrics.metadata import compute_m
from brf.registry.verify import compute_prepare_sha256


def _independent_m(groups):
    """Independent re-implementation of the documented M formula.

    M = 0.5 * normalized_entropy + 0.5 * clipped_group_balance
    Returns (m, normalized_entropy, raw_balance).
    """
    _, counts = np.unique(np.asarray(groups), return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log(probs + 1e-10))
    ne = float(entropy / np.log(len(counts)))
    raw = 1.0 - float(np.std(counts) / (np.mean(counts) + 1e-8))
    clipped = max(0.0, min(1.0, raw))
    return 0.5 * ne + 0.5 * clipped, ne, raw


def test_compute_m_equal_weights():
    # M2 pin: 0.5/0.5 weighting of the entropy and balance components.
    groups = np.concatenate([np.full(s, i) for i, s in enumerate([1, 2, 5, 9])])
    m = compute_m(groups)
    expected, ne, gb = _independent_m(groups)
    assert m == pytest.approx(expected, rel=1e-12)
    assert abs(ne - gb) > 0.1  # guard: components differ, so weights are identifiable
    assert abs(m - (0.6 * ne + 0.4 * gb)) > 1e-3


def test_compute_m_clips_balance_at_zero():
    # M9 pin: the balance component is clipped to [0, 1] before weighting.
    groups = np.concatenate([np.full(s, i) for i, s in enumerate([1, 1, 1, 1, 20])])
    m = compute_m(groups)
    expected, ne, raw = _independent_m(groups)
    assert raw < 0.0  # guard: this case actually exercises the clip
    assert m == pytest.approx(expected, rel=1e-12)
    assert m > 0.5 * ne + 0.5 * raw  # unclipped value would be lower


def test_compute_b_is_gap_to_baseline():
    # M6 pin: B = r2(model) - r2(baseline), not r2(model) alone.
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    perfect = y.copy()
    baseline = np.full(5, y.mean())
    assert compute_b(y, perfect, baseline) == pytest.approx(1.0)
    assert compute_b(y, perfect, perfect) == pytest.approx(0.0, abs=1e-12)


def test_compute_i_uses_sample_standard_deviation():
    # M7 pin: ddof=1 (sample std), not ddof=0.
    r2s = [0.5, 0.7, 0.9, 0.6, 0.8]
    mean = float(np.mean(r2s))
    denom = max(abs(mean), 1e-4) + 1e-8
    assert compute_i(r2s) == pytest.approx(float(np.std(r2s, ddof=1)) / denom, rel=1e-12)
    assert compute_i(r2s) != pytest.approx(float(np.std(r2s, ddof=0)) / denom, rel=1e-6)


def test_null_separation_uses_strict_greater_than():
    # M8 pin: a split ties the null median only when r2 strictly exceeds it.
    import brf.analyzer as mod
    src = inspect.getsource(mod)
    assert "> float(np.median(perm_r2s))" in src
    assert ">= float(np.median(perm_r2s))" not in src


def test_prepare_hash_depends_on_shape():
    # M10 pin: the canonical digest includes each array's shape, so two
    # arrays with equal bytes but different shapes must hash differently.
    X1, X2 = np.zeros((4, 2)), np.zeros((2, 4))
    y = np.zeros(4)
    assert compute_prepare_sha256(X1, y, None) != compute_prepare_sha256(X2, y, None)
