"""Baseline modeling utilities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinearTrendModel:
    slope: float
    intercept: float

    def predict(self, x: float) -> float:
        return self.slope * x + self.intercept


def fit_linear_trend(values: list[float]) -> LinearTrendModel:
    """Fit a simple linear trend line to a sequence of values."""
    if len(values) < 2:
        raise ValueError("Need at least two values to fit a linear trend.")

    n = len(values)
    x_values = list(range(n))
    sum_x = sum(x_values)
    sum_y = sum(values)
    sum_xx = sum(x * x for x in x_values)
    sum_xy = sum(x * y for x, y in zip(x_values, values))

    denominator = n * sum_xx - sum_x * sum_x
    if denominator == 0:
        raise ValueError("Cannot fit linear trend with zero denominator.")

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return LinearTrendModel(slope=slope, intercept=intercept)
