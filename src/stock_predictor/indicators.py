"""Technical indicator calculations."""

from __future__ import annotations

from collections import deque


def simple_moving_average(prices: list[float], window: int) -> list[float]:
    """Calculate the simple moving average for a price series."""
    if window <= 0:
        raise ValueError("Window size must be positive.")
    if len(prices) < window:
        raise ValueError("Price series must be at least as long as the window.")

    sums: deque[float] = deque()
    total = 0.0
    averages: list[float] = []
    for price in prices:
        sums.append(price)
        total += price
        if len(sums) > window:
            total -= sums.popleft()
        if len(sums) == window:
            averages.append(total / window)
    return averages


def exponential_moving_average(prices: list[float], window: int) -> list[float]:
    """Calculate the exponential moving average for a price series."""
    if window <= 0:
        raise ValueError("Window size must be positive.")
    if len(prices) < window:
        raise ValueError("Price series must be at least as long as the window.")

    multiplier = 2 / (window + 1)
    ema_values: list[float] = []
    initial_sma = sum(prices[:window]) / window
    ema_values.append(initial_sma)
    for price in prices[window:]:
        ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])
    return ema_values


def relative_strength_index(prices: list[float], window: int = 14) -> list[float]:
    """Calculate the RSI for a price series."""
    if window <= 0:
        raise ValueError("Window size must be positive.")
    if len(prices) <= window:
        raise ValueError("Price series must be longer than the window.")

    gains: list[float] = []
    losses: list[float] = []
    for index in range(1, window + 1):
        delta = prices[index] - prices[index - 1]
        gains.append(max(delta, 0))
        losses.append(max(-delta, 0))

    average_gain = sum(gains) / window
    average_loss = sum(losses) / window
    rsi_values: list[float] = []

    for index in range(window + 1, len(prices)):
        delta = prices[index] - prices[index - 1]
        gain = max(delta, 0)
        loss = max(-delta, 0)
        average_gain = ((average_gain * (window - 1)) + gain) / window
        average_loss = ((average_loss * (window - 1)) + loss) / window
        if average_loss == 0:
            rsi = 100.0
        else:
            rs = average_gain / average_loss
            rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    return rsi_values
