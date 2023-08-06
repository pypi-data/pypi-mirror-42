import datetime
import pandas as pd
import xarray as xr
from pytradecli.client import Client
import jpxtime3
from .data import N225DerivativesData
from .io import N225Serializer


def save_ds_n225fop(dt=datetime.datetime.now(), freq="5min"):
    serializer = N225Serializer(dt)
    if serializer.get_file_path().exists():
        ext_ds = serializer.load_ds()
        start = ext_ds["t0"].values[-1]
    else:
        start = jpxtime3.SessionTime(dt).opening_time_ns
    
    ts = pd.date_range(start, dt, freq=freq)
    ts = ts[ts.map(jpxtime3.is_open) != 0]
    cli = Client()
    df = [cli.get("N225FOP", date=t) for t in ts]
    ds = [N225DerivativesData(d).to_ds() for d in df if d is not None]
    concat_ds = xr.concat(ds, dim="t0")
    serializer.serialize(concat_ds)


if __name__ == "__main__":
    pass
