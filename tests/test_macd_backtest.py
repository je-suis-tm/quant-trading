import pandas as pd

from conftest import load_script_module


def test_macd_signal_generation_handles_basic_crossover():
    module = load_script_module("MACD Oscillator backtest.py")
    module.ma1 = 2
    module.ma2 = 3

    index = pd.date_range("2020-01-01", periods=5, freq="D")
    df = pd.DataFrame({"Close": [1.0, 2.0, 3.0, 2.0, 1.0]}, index=index)

    signals = module.signal_generation(df.copy(), module.macd)

    assert signals.loc[index[2], "signals"] == 1
    assert signals.loc[index[4], "signals"] == -1
