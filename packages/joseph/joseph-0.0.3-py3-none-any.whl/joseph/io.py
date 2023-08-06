from abc import ABC, abstractmethod
import datetime
from pathlib import Path

import jpxtime3
import numpy as np
import pandas as pd
import xarray as xr


joseph_home = Path.home() / ".joseph"
joseph_cache = joseph_home / "cache"

if not joseph_home.exists():
    joseph_home.mkdir()
if not joseph_cache.exists():
    joseph_cache.mkdir()


class AbstractSerializer(ABC):
    @abstractmethod
    def get_file_path(self):
        pass

    @abstractmethod
    def load_ds(self):
        pass

    @abstractmethod
    def serialize(self):
        pass


class Serializer(AbstractSerializer):
    def __init__(self, t0=datetime.datetime.now()):
        self.t0 = t0

    def get_file_path(self):
        file_name = datetime.datetime.strftime(self.t0, "%Y%m%d.nc")
        return joseph_cache / file_name

    def load_ds(self, decode_times=True):
        file_path = self.get_file_path()
        if file_path.exists():
            ds = xr.open_dataset(file_path)
            if decode_times:
                ds["t0"] = np.vectorize(lambda x: pd.Timestamp(x, unit="s"))(
                    ds["t0"].values
                )
        else:
            ds = None
        return ds

    def serialize(self, ds):
        file_path = self.get_file_path()
        new_ds = ds.copy()
        new_ds["t0"] = new_ds["t0"].astype(int) / 1e9
        ext_ds = self.load_ds(decode_times=False)

        if ext_ds:
            ext_t0 = ext_ds["t0"].values
            if ext_t0.size == 1:
                ext_t0 = np.array(ext_t0)
            diff = np.setdiff1d(new_ds["t0"].values, ext_ds["t0"].values)
            if len(diff) == 0:
                return
            if len(diff) == 1:
                concat_ds = xr.concat([ext_ds, new_ds], dim="t0")
            else:
                concat_ds = xr.concat([ext_ds, new_ds.sel(t0=diff)], dim="t0")
            concat_ds.sortby("t0").to_netcdf(file_path)
        else:
            new_ds.to_netcdf(file_path)


class N225Serializer(Serializer):
    def get_file_path(self):
        dt = jpxtime3.get_nominal_trading_day(pd.to_datetime(self.t0))
        file_name = f"{dt:%Y%m%d}.nc"
        return joseph_cache / file_name
