"""California Housing. 20640 samples, 8 features, target: median house value.
Group: ocean proximity (5 categories)."""
import pandas as pd
import numpy as np
import io

from . import DatasetSource, register_source

@register_source
class CaliforniaHousingSource(DatasetSource):
    name = "california_housing"
    display_name = "California Housing (Ocean proximity groups)"
    version = "1.0"
    source_url = "https://www.dcc.fc.up.pt/~ltorgo/REG/california.housing.asc"
    license_info = "Public domain"
    reference = "Torgo (2007); sklearn.datasets"
    task = "regression"
    n_samples = 20640
    n_features = 8
    n_groups = 5
    grouping_description = "Ocean proximity (5 categories)"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "california_housing.csv"
        if csv_path.exists():
            return csv_path
        url = "https://raw.githubusercontent.com/selva86/datasets/master/cal_housing.csv"
        resp = urllib.request.urlopen(url, timeout=30)
        df = pd.read_csv(io.StringIO(resp.read().decode()))
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["MedHouseVal"].values.astype(float)
        feature_cols = [c for c in df.columns if c != "MedHouseVal" and c != "OceanProximity"]
        X = df[feature_cols].values.astype(float)
        if "OceanProximity" in df.columns:
            groups = df["OceanProximity"].astype("category").cat.codes.values
        else:
            n_per = len(y) // 5
            groups = np.repeat(np.arange(5), n_per)[:len(y)]
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "California Housing"}
        return X, y, groups, meta
