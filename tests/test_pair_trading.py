import pandas as pd

from conftest import load_script_module


class FakeModel:
    def __init__(self):
        self.resid = pd.Series([-1.0, 1.0, -1.0, 1.0])

    def predict(self, X):
        if hasattr(X, "iloc") and getattr(X, "shape", (0, 0))[1] == 2:
            return X.iloc[:, 1]
        return X


def always_cointegrated(X, Y):
    return True, FakeModel()


def test_pair_trading_enters_on_positive_zscore_breakout():
    module = load_script_module("Pair trading backtest.py")
    index = pd.date_range("2020-01-01", periods=8, freq="D")

    asset1 = pd.DataFrame({"Close": [10, 11, 12, 13, 14, 15, 16, 17]}, index=index)
    asset2 = pd.DataFrame({"Close": [10, 11, 12, 13, 17, 15, 13, 17]}, index=index)

    signals = module.signal_generation(asset1, asset2, always_cointegrated, bandwidth=4)

    assert signals.loc[index[4], "signals1"] == 1


def test_pair_trading_stays_flat_after_reversion_and_keeps_legs_opposite():
    module = load_script_module("Pair trading backtest.py")
    index = pd.date_range("2020-01-01", periods=8, freq="D")

    asset1 = pd.DataFrame({"Close": [10, 11, 12, 13, 14, 15, 16, 17]}, index=index)
    asset2 = pd.DataFrame({"Close": [10, 11, 12, 13, 17, 15, 13, 17]}, index=index)

    signals = module.signal_generation(asset1, asset2, always_cointegrated, bandwidth=4)

    assert signals.loc[index[5], "signals1"] == 0
    assert signals["signals2"].equals(-signals["signals1"])
    assert signals["positions2"].fillna(0).equals(-signals["positions1"].fillna(0))
