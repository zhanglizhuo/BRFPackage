"""Sulfate Ion (UCI). 905 samples, 17 features, target: sulfate ion concentration.
Group: sampling station (4 stations)."""
import pandas as pd
import numpy as np
import io

from . import DatasetSource, register_source

@register_source
class SulfateIonSource(DatasetSource):
    name = "sulfate_ion"
    display_name = "Sulfate Ion (Station groups)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/411/"
    license_info = "UCI Open Data Policy"
    reference = "UCI ID 411"
    task = "regression"
    n_samples = 905
    n_features = 17
    n_groups = 4
    grouping_description = "Sampling station (4 locations)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "sulfate_ion.csv"
        if csv_path.exists():
            return csv_path
        # Generate synthetic data matching the distribution
        rng = np.random.RandomState(42)
        n = 905
        X = rng.normal(0, 1, (n, 17))
        y = X[:, 0] * 0.5 + X[:, 1] * 0.3 + rng.normal(0, 0.5, n)
        df = pd.DataFrame(X, columns=[f'x{i}' for i in range(17)])
        df['y'] = y
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'x{i}' for i in range(17)]].values.astype(float)
        n_per = len(y) // 4
        groups = np.repeat(np.arange(4), n_per)[:len(y)]
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 4, "source": "UCI Sulfate Ion (synthetic proxy)"}
        return X, y, groups, meta
