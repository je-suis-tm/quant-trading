import importlib.util
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

SCRIPT = ROOT / 'Dual Thrust backtest.py'


def load_dual_thrust():
    # The script changes directory on import, which fails on machines
    # without a D: drive, so we neutralise os.chdir while loading it.
    original_chdir = os.chdir
    os.chdir = lambda *args, **kwargs: None
    try:
        spec = importlib.util.spec_from_file_location(
            'dual_thrust', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        os.chdir = original_chdir
    return module


def make_minute_data(days=7, start='2018-06-01'):
    frames = []
    for day in range(days):
        idx = pd.date_range(pd.Timestamp(start) + pd.Timedelta(days=day),
                            periods=13 * 60, freq='min')
        price = 1.32 + 0.001 * np.sin(np.arange(len(idx)) / 30) + 0.0001 * (day + 1)
        frames.append(pd.DataFrame({'price': price}, index=idx))
    df = pd.concat(frames)
    df['date'] = df.index
    return df


def test_min2day_builds_daily_ohlc():
    dual = load_dual_thrust()
    df = make_minute_data()

    intraday = dual.min2day(df, 'price', 2018, 6, 5)

    assert len(intraday) == 7
    session = df.loc['2018-06-01 03:00:00':'2018-06-01 12:00:00']
    assert intraday['open'].iloc[0] == pytest.approx(session['price'].iloc[0])
    assert intraday['close'].iloc[0] == pytest.approx(session['price'].iloc[-1])
    assert intraday['high'].iloc[0] == pytest.approx(session['price'].max())
    assert intraday['low'].iloc[0] == pytest.approx(session['price'].min())


def test_signal_generation_completes_and_clears_positions():
    dual = load_dual_thrust()
    df = make_minute_data()

    intraday = dual.min2day(df, 'price', 2018, 6, 5)
    signals = dual.signal_generation(df, intraday, 0.5, 'price', 5)

    assert not signals.empty
    # every day ends flat, so all positions are cleared at the close
    per_day = signals['signals'].groupby(signals.index.date).sum()
    assert (per_day == 0).all()
