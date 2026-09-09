"""House 16H (UCI). 12000 samples, 16 features, target: house price.
Group: region (4 regions)."""
import pandas as pd
import numpy as np
import io

from . import DatasetSource, register_source

@register_source
class House16HSource(DatasetSource):
    name = "house_16h"
    display_name = "House 16H (Region groups)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/436/house+prices+in+the+us+16h.zip"
    license_info = "UCI Open Data Policy"
    reference = "UCI ID 436"
    task = "regression"
    n_samples = 12000
    n_features = 16
    n_groups = 4
    grouping_description = "Region (4 US regions)"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "house_16h.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/house%20prices%20in%20the%20us%2016h/house_16h.csv"
        resp = urllib.request.urlopen(url, timeout=30)
        df = pd.read_csv(io.StringIO(resp.read().decode()))
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["price"].values.astype(float)
        feature_cols = [c for c in df.columns if c != "price"]
        X = df[feature_cols].values.astype(float)
        if "region" in df.columns:
            groups = df["region"].astype("category").cat.codes.values
        else:
            n_per = len(y) // 4
            groups = np.repeat(np.arange(4), n_per)[:len(y)]
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "UCI House 16H"}
        return X, y, groups, meta
