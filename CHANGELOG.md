# Changelog

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
