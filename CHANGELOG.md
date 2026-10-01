# Changelog

## 0.3.3 (2026-10-01)

- **Fix: the version chain was broken in 0.3.2.** The 0.3.0 entry records the chain as unified across `pyproject.toml`, `setup.py`, `CITATION.cff`, `brf.__version__` and the bundled registry manifest, but 0.3.2 updated only `pyproject.toml` and `brf.__version__`, leaving `setup.py` and `CITATION.cff` at 0.3.0. A reader inspecting either file would have seen a different version from the one reported at runtime and from the one on PyPI. The bundled manifest carries the registry version (2.1), which is a separate quantity and is unchanged.
- **Fix: 21 of the 51 dataset cards had an empty `task.type`.** The cards split the field into `type` and `target`, and the 21 affected cards recorded only `target` (for example `binary (Graduate/Dropout)` or `ordinal 3-class (Low/Medium/High)`), so the value was present in prose but absent from the typed field the schema defines. All 51 now carry a `type` consistent with the corresponding source module's `task`. No count changes: the regression/classification split is 40/11 and is read from the source modules, which already agreed.
- `MANIFEST.in` referenced `sn-nature.bst` and `sn-mathphys-num.bst`, which live in the Scientific Data manuscript directory and not in this package. The patterns matched nothing and setuptools skipped them silently, so twine check passed regardless. Removed.
- `version_policy.yaml`: the mm_tba entry attributed the figshare HTTP 403 to requiring a proxy in mainland China, which was not verified and may not be the cause. It now records what was actually observed, that the metadata endpoint returned 403 when checked on 2026-10-01, and that a cached extraction from a successful 2026-09-12 fetch is present.

## 0.3.2 (2026-10-01)

- **Fix: `mm_tba` file-level SHA-256 could never be reproduced.** The source's `download()` returns the cache root, and the figshare archive unpacks a full research code release alongside the data: `Teacher_Action_Detection/my_mmaction` (1919 files), yolo `dense_proposals_*.pkl` files, and 51 `__pycache__` `.pyc` files. The directory hash therefore covered 2666 files of which `prepare()` reads 419, and the `.pyc` bytes depend on when and under which interpreter they were written, so any reader recomputing the digest saw MISMATCH. `DatasetSource.hash_scope()` is a new hook that limits a directory digest to the files a loader consumes; `mm_tba` uses it to cover `metadata.xlsx` plus the 418 transcript and GPT-report files. Its recorded digest is regenerated over that scope.
- **Fix: the dataset cards and policy files the Data Descriptor points to were not installable.** The manuscript names `registry/cards/`, `registry/taxonomy.yaml` and `registry/version_policy.yaml` as artefacts a reader can obtain, but `[tool.setuptools.package-data]` listed only `manifest.yaml`, `registry_v2.1.json` and `prepare_hashes.json`, so those three paths did not exist in an installed wheel. All 51 cards and both YAML files are now packaged; the wheel grows from 72 to 125 files.

## 0.3.1 (2026-09-30)

- **Fix: the bundled `prepare_hashes.json` was the v2.0 (35-dataset) file.** The copy shipped inside the package still carried the frozen 35-entry cohort, and 30 of its 35 hashes conflicted with the registry's v2.1 values, so `brf registry verify` scored 5/51 instead of 51/51 against the installed package. Replaced with the 51-entry v2.1 file from `BRFRegistry/registry/prepare_hashes.json`.
- **Fix: `prepare_hashes.json` is now packaged.** It was absent from `[tool.setuptools.package-data]`, so the layer-2 prepared-array check that the Data Descriptor reports was unreachable from an installed wheel. `brf/registry/verify.py` already resolved the path relative to the package directory; it now ships.
- `download()` offline-cache fallback for `kdd_cup_2010` (rglob prior extract) and `student_dropout` (extra CSV reuse), matching the Track A 2026-09-24 re-run behaviour. No effect on data or results.

## 0.3.0 (2026-09-11)

- Registry v2.1: 51 unique datasets (25 educational + 26 cross-domain: health, finance, environment, energy, transportation, systems); 58 entries incl. 7 alt-grouping views
- BRF results: 42 Reliable / 9 Void / 0 Fragile (pisa2015 re-sourced to the official OECD PUF 2026-09-14: Void -> Reliable)
- Version chain unified at 0.3.0 (pyproject.toml, setup.py, CITATION.cff, `brf.__version__`, bundled registry manifest)
- Bundled registry manifest synced to v2.1 (was v1.5)
- `brf` now exposes a queryable `brf.__version__`
- CITATION.cff preferred citation updated to the published BehaviorAudit (Scientific Reports, DOI 10.1038/s41598-026-69629-6)

## 0.2.1 (2026-07-01)

- Context-aware recommendations in `analyzer.recommend()`

## 0.2.0 (2026-07-01)

- `analyzer.diagnose()`, `analyzer.rank()`, `analyzer.recommend()`

## 0.1.6 (2026-07-01)

- Registry integrated into the `brf` package with the `brf registry` CLI
- SHA-256 checksum verification
- JOSS software paper drafted

## 0.1.5 (2026-06-30)

- Add result interpretation table to README (Reliable / Fragile / Void)
- Clean up README for PyPI audience

## 0.1.4 (2026-06-30)

- Rewrite README: remove internal research planning, focus on users

## 0.1.3 (2026-06-30)

- Fix all non-ASCII chars in README for PyPI compatibility

## 0.1.2 (2026-06-30)

- Fix non-ASCII chars in description field for PyPI
- Fix README em dashes

## 0.1.1 (2026-06-30)

- Fix em dash encoding issue in pyproject.toml description

## 0.1.0 (2026-06-30)

- Initial PyPI release
- Core BRF metrics: B (Baseline Gain), I (Instability), N (Null Separability), M (Metadata Sufficiency)
- Phase embedding: S = N - I, E = B + M
- Classification: Reliable / Fragile / Void
- Visualization: phase diagram plot
- Export: JSON, LaTeX
- 50 unit tests
