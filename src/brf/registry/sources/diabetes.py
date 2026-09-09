"""Diabetes (UCI). 442 samples, 10 features, target: diabetes progression rate 1 year.
Group: sex (Male/Female)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class DiabetesSource(DatasetSource):
    name = "diabetes"
    display_name = "Diabetes (Sex groups)"
    version = "1.0"
    source_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3605048/"
    license_info = "CC BY 4.0"
    reference = "Efron et al. (2009); UCI Diabetes"
    task = "regression"
    n_samples = 442
    n_features = 10
    n_groups = 2
    grouping_description = "Sex (Male/Female)"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "diabetes.csv"
        if csv_path.exists():
            return csv_path
        url = "https://raw.githubusercontent.com/selva86/datasets/master/diabetes.csv"
        resp = urllib.request.urlopen(url, timeout=30)
        df = pd.read_csv(io.StringIO(resp.read().decode()))
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df.drop(columns=["y"]).values.astype(float)
        groups = (df["sex"].values == "Male").astype(int) if "sex" in df.columns else np.ones(len(y), dtype=int)
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "UCI Diabetes"}
        return X, y, groups, meta


import io
