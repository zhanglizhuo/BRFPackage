# Changelog

## 0.3.5 (2026-10-03)

- **Fix: the `colleges_usnews` data source was pointing at a different dataset.** The source module and `registry_v2.1.json` both named `https://www.openml.org/data/download/22101655/colleges_usnews.arff` and both declared sha256 `699af407...`. Fetching that URL returns 97,148,755 bytes whose sha256 is exactly `699af407...` and whose header reads `Title: ACS Public Coverage Dataset` / `@RELATION ACSPublicCoverage` - the ACS Public Coverage data, not the College Scorecard table this dataset is named for. The only thing tying the URL to `colleges_usnews` is the filename it is served under. The card was already correct on both counts (`source.url = .../search?type=data&id=538`, `integrity.sha256 = c96a8f3e...`), so the two machine-readable records were the outliers and disagreed with their own card. The module now downloads `https://www.openml.org/d/538`, whose CSV digests to `c96a8f3e...`, the ARFF fallback branch was removed, and the JSON matches the card. Re-downloading did 538 through the OpenML API on 2026-10-03 produced a CSV byte-identical to the cached one, so no study number changes: N=1,204, p=31, 51 groups are unchanged and the paper's tables stand.
- **Fix: `registry_v2.1.json` carried the same wrong provenance as the module.** For `colleges_usnews` the JSON's `source_url` and `sha256` were a second copy of the ACS values above, not a mismatch against the module. All four machine-readable fields (`source_url` and `sha256`, in the module and in the JSON) now read `https://www.openml.org/d/538` and `c96a8f3e...`, agreeing with the card.
- **Fix: three dataset cards recorded the wrong feature counts.** `higher_ed` had `features.count = 31` against 30 columns; `law_school` had 10 against 7; `oulad` had 44 against 52, so two were inflated and one understated. Each card's count is now equal to `prepare()`'s column count and to `registry_v2.1.json`'s `n_features`, checked for all 51 datasets rather than for these three alone.
- **Fix: the distributions did not carry the license or the changelog.** Every wheel and sdist from 0.3.1 to 0.3.4 contained neither `LICENSE` nor `CHANGELOG.md`, although the metadata declares MIT. `MANIFEST.in` named only the verification files, and `pyproject.toml` set `license-files = []`, so setuptools dropped the license from the wheel and the manifest never picked it up for the sdist. The sdist now ships both files and the wheel ships `LICENSE`.
- The consistency suite is now nineteen checks across both trees. `check_card_source_agreement` read the cards' top-level `n_samples`/`n_groups`/`n_features` keys, but no card carries any of those keys, so every count comparison evaluated `None is not None` and silently did nothing while the check still reported PASS. It would not have caught the three count errors above. The counts are nested under `samples.count`, `grouping.count` and `features.count`; the check now reads those paths, treats a missing field as a failure, and also fails on an absent `task.type`. Its `task.type` comparison was working before this release, which is how 0.3.3's twenty-one empty types were found. A new check, `check_registry_json_values`, compares the *values* the other checks only verify structurally: for all fifty-one datasets, the source modules' `sha256` and `source_url` against the same fields in `registry_v2.1.json`, the cards' counts and task types against the JSON's, and each card's `integrity.sha256` against the JSON's `sha256`. It is the check releases 0.3.2-0.3.4 could not have passed: those wheels record one sha256 for `mm_tba` in the module and a different one in the JSON, and carry the three count errors above.
- **Fix: four descriptions misstated how their data is grouped or what task it runs.** `boston_housing` called its groups `region (4 regions)` and `(Region groups)`, but `prepare()` bins feature f5 into quartiles; `pollution` called them `station (10 stations)` / `Monitoring station (10 stations)` where `prepare()` bins feature f0 into deciles. The module docstrings, `display_name`, `grouping_description`, the cards and `registry_v2.1.json` now all say quartile bins of f5 (4 groups) and decile bins of f0 (10 groups). `college_scorecard`'s docstring, `grouping_description` and JSON entry claimed `State (59 groups)` against the code's `n_groups = 55` and now say 55 (the card carries no count and needed no change). `student_depression`'s notes asserted `Run as regression.` although the task is binary classification; the phrase is gone from the module, the card and the JSON. All four fixes are prose only: hashes, N, p, group counts and every number in the paper are unchanged.
- **Fix: the `climate_weather` docstring claimed 243 countries.** Running `prepare()` and taking `np.unique` on the groups yields 242, which is what `n_groups`, `grouping_description`, the card and `registry_v2.1.json` all already recorded; the module docstring was the single outlier and now reads `country (242)`.
- **Fix: the `real_estate` source URL was dead.** `https://archive.ics.uci.edu/static/public/477/real+estate+valuation.zip` returns HTTP 404 (checked 2026-10-04). UCI's canonical archive `https://archive.ics.uci.edu/static/public/477/real+estate+valuation+data+set.zip` returns 200 and contains `Real estate valuation data set.xlsx`, byte-identical (sha256 `597d72fc...`) to the file `download()` fetches from the legacy `/ml/machine-learning-databases/00477/` link, which is still alive. The canonical URL now appears in the source module, `registry_v2.1.json` and both cards; `download()` keeps the legacy link, so nothing executable changed: the recorded sha256, N=414 and all study numbers stand.
- The test suite ran only with `PYTHONPATH=src` exported. From the repository root, `python3 -m pytest tests/ -q` died with three collection errors (`ModuleNotFoundError: No module named 'brf'`), so a bare invocation of the documented command never reached the 50 tests. A `tests/conftest.py` now prepends `src/` to `sys.path`, and `MANIFEST.in` ships it with the sdist alongside the `test*.py` files; both invocation styles, and a bare `pytest tests/ -q` in the unpacked tarball, pass.
- **Fix: three dataset cards recorded stale or transposed `brf_compatibility` values.** `diabetes` (audited v2.1) carried its B value (0.5103) in the E field; the true E is B + M = 1.3617. `higher_ed` and `oulad` still carried their v1.5-era S/E values (and said so, via `audited_version: v1.5`) while the registry shipped v2.1 results. All three cards now record the v2.1 values from `registry_v2.1.json` verbatim and are labeled `audited_version: v2.1`. A new check, `check_brf_compatibility`, compares every card's S/E/class against the recorded results (tolerance 0.01 for S/E), so this class of error fails the suite instead of passing it.
- **Fix: `diagnose()` claimed "Strong group structure" for groupings with fewer than 5 groups.** `compute_m` measures the balance and entropy of the groups that exist and does not see how few there are, so a perfectly balanced 2-group split scores M near 1.0 and the old message presented that as strong group structure. The M >= 0.3 branches now report "group balance" instead of "group structure" and add the >=5-groups annotation caveat whenever 0 < groups < 5. Display text only: no stored metric changes.
- **Test coverage: six silent-precision mutations survived the pre-existing suite.** Mutation testing (10 mutants over the metric and registry code) was killed 4/10; the survivors were M-weighting (0.5/0.5), `compute_b` dropping the baseline subtraction, `compute_i` switching to ddof=0, the null-separation comparison flipping `>` to `>=`, the balance clip being removed, and the prepare hash dropping the shape from the digest. `tests/test_mutation_pins.py` adds one independent-recomputation test per mutant; the full mutant set is now killed 10/10 and the suite grew from 50 to 56 tests. A `[tool.pytest.ini_options]` section sets `testpaths = ["tests"]`, so a bare `pytest` at the repository root collects the project suite (56 passed) instead of ~94 collection errors from the vendored third-party test trees under `src/brf/registry/cache/`.

## 0.3.4 (2026-10-01)

- **Fix: `MANIFEST.in` still named two files that are not in this package.** The 0.3.3 entry said they had been removed; they had not, because the edit that was meant to remove them stopped early. `sn-nature.bst` and `sn-mathphys-num.bst` live in the Scientific Data manuscript directory, so both patterns matched nothing and setuptools skipped them silently. twine check reports on the built distribution rather than on whether the manifest is satisfiable, so it passed with the stale lines still present, and the 0.3.3 sdist shipped without those files. Removed.
- `scripts/check_consistency.py` is available from the repository tree alongside the package (see BRFRegistry). Fourteen checks across both trees: the version chain, package-data and MANIFEST.in patterns against real files, byte-level agreement of the registry trees, card fields against the source modules, the SHA coverage quoted in `version_policy.yaml`, and that every registry source parses. Exits non-zero on failure.

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
