"""Pipeline helpers for producing a baseline forecast."""

from __future__ import annotations

from dataclasses import dataclass

from stock_predictor.indicators import (
    exponential_moving_average,
    relative_strength_index,
    simple_moving_average,
)
from stock_predictor.models import LinearTrendModel, fit_linear_trend


@dataclass(frozen=True)
class ForecastResult:
    model: LinearTrendModel
    forecast: float
    sma: float
    ema: float
    rsi: float


def build_features(prices: list[float], window: int) -> tuple[float, float, float]:
    sma_values = simple_moving_average(prices, window)
    ema_values = exponential_moving_average(prices, window)
    rsi_values = relative_strength_index(prices, window)
    return sma_values[-1], ema_values[-1], rsi_values[-1]


def generate_forecast(prices: list[float], window: int = 14) -> ForecastResult:
    """Generate a baseline forecast using a linear trend model."""
    model = fit_linear_trend(prices)
    forecast = model.predict(len(prices))
    sma, ema, rsi = build_features(prices, window)
    return ForecastResult(model=model, forecast=forecast, sma=sma, ema=ema, rsi=rsi)
