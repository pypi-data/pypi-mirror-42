import pandas as pd
from . import utils
import ivolat3


class Trade:
    def __init__(self, ds, trade_df, t0=None):
        self.ds = ds
        self.trade_df = trade_df
        work_df = trade_df.copy()
        work_df.index = work_df.index.floor(freq="1min")

        if len(ds["t0"].values) == 0:
            work_ds = ds
        else:
            if t0:
                work_ds = ds.sel(t0=t0)
            else:
                work_ds = ds.sel(t0=ds["t0"].values[-1])

        if t0:
            work_df = work_df.loc[:t0]

        work_df[["maturity", "type", "strike"]] = work_df[
            ["maturity", "type", "strike"]
        ].fillna("")
        work_df["symbol"] = work_df[["maturity", "type", "strike"]].apply(
            lambda x: "".join(map(str, x)), axis=1
        )
        work_df["turnover"] = work_df["qty"] * work_df["price"]
        grouped_by_symbol = work_df.groupby("symbol")
        qty = grouped_by_symbol["qty"].sum()
        turnover = grouped_by_symbol["turnover"].sum()

        summary_df = pd.DataFrame(
            [], index=qty.index.values, columns=["maturity", "type", "strike", "price"]
        )
        for col in ["maturity", "type", "strike"]:
            summary_df[col] = summary_df.index.map(
                lambda x: utils.take_one_data(work_df.loc[work_df["symbol"] == x, col])
            )
        summary_df["price"] = summary_df.apply(
            lambda x: self.get_price_from_ds(
                work_ds, str(x["maturity"]), x["type"], x["strike"]
            ),
            axis=1,
        )
        summary_df["qty"] = qty
        summary_df["pl"] = (summary_df["qty"] * summary_df["price"]) - turnover
        summary_df["iv"] = summary_df.apply(
            lambda x: self.get_iv_from_ds(
                work_ds, x["maturity"], x["strike"], x["type"]
            ),
            axis=1,
        )
        summary_df[["delta", "gamma", "vega", "theta"]] = summary_df.apply(
            lambda x: self.calc_greeks(
                work_ds, x["qty"], x["maturity"], x["strike"], x["iv"], x["type"]
            ),
            axis=1,
        )
        self.summary_df = summary_df

        self.work_df = work_df

    def get_price_from_ds(self, ds, maturity, fop_type, strike=None):
        price = {"C": "interpolated_call", "P": "interpolated_put", "F": "price_fut"}[
            fop_type
        ]
        if fop_type == "F":
            return float(ds.sel(maturity=maturity)[price].values)
        else:
            return float(ds.sel(maturity=maturity, k=strike)[price].values)

    def get_iv_from_ds(self, ds, maturity, strike, fop_type):
        if fop_type == "F":
            return None
        else:
            return ds.sel(maturity=maturity, k=strike)["interpolated_iv"].values

    def calc_greeks(self, ds, qty, maturity, strike, iv, fop_type):
        maturity_ds = ds.sel(maturity=maturity)
        if fop_type == "F":
            delta, gamma, vega, theta = 1, 0, 0, 0
        else:
            s, r, q, t = (
                maturity_ds["s"].values,
                maturity_ds["r"].values,
                maturity_ds["q"].values,
                maturity_ds["t"].values,
            )
            delta = ivolat3.delta(s, strike, r, q, t, iv, fop_type)
            gamma = ivolat3.gamma(s, strike, r, q, t, iv)
            vega = ivolat3.vega(s, strike, r, q, t, iv)
            theta = ivolat3.theta(s, strike, r, q, t, iv, fop_type)
        return (
            pd.Series(
                [delta, gamma, vega, theta], index=["delta", "gamma", "vega", "theta"]
            )
            * qty
        )
