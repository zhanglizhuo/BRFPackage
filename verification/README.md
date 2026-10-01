# Archived prepare-verification logs

Raw output of

```
python scripts/compute_prepare_hashes.py --verify
```

## Current state (canonical content hash)

| log | interpreter | OK | MISMATCH | ERROR |
|---|---|---|---|---|
| `prepare_verify_py313.txt` | CPython 3.13.11 (numpy 2.4.4, pandas 2.3.3) | 51 | 0 | 0 |
| `prepare_verify_py38.txt` | CPython 3.8.20 (numpy 1.24.3, pandas 2.0.3) | 36 | 0 | 15 |

`MISMATCH` is 0 on both. The 15 errors on 3.8 are missing optional readers in
that deliberately minimal environment (9 `sklearn`, 3 `kagglehub`, and one each
of `scipy`, `pyreadstat`, `openpyxl`); 36 + 15 = 51. They are installation
state, not hash disagreement.

## Why the legacy log exists

`prepare_verify_py38_legacy.txt` is the same command under the previous
implementation and shows `10 OK / 27 MISMATCH / 15 ERROR`. It is kept because it
is the evidence for the change that produced the current scheme.

`compute_prepare_sha256` used to hash the bytes `numpy.save()` emits. That is a
hash of a serialisation, not of the data. `groups` is an `object`-dtype array,
so `numpy.save` pickles it, and the pickled byte stream is not stable across
interpreters. For `abalone`, `X` and `y` were element-for-element equal across
3.8 and 3.13 (`np.array_equal` `True`, max absolute difference `0.0`, same shape,
same `float64` dtype), yet the digests differed because the serialised `groups`
array was 8663 bytes on 3.8 and 8646 on 3.13 (`ec91fc24...` vs `98b59954...`).
The dtype and element type (`str`) matched on both sides and
`pickle.DEFAULT_PROTOCOL` was 4 on both, so the difference was in the encoding
rather than in protocol selection.

The function now reduces each array to an explicitly declared dtype, its shape,
and its raw bytes, so the digest depends on the values only.

## Reproducing the 3.8 run

Python 3.8 is not in the base environment:

```
conda create -n py38chk python=3.8 -y
conda activate py38chk
pip install --no-deps dist/benchmark_reliability-0.3.1-py3-none-any.whl
conda install numpy            # 1.24.3, last numpy supporting 3.8
pip install pandas==2.0.3      # last pandas supporting 3.8
```

scikit-learn, scipy, matplotlib, openml, kagglehub, pyreadstat and openpyxl
were left uninstalled, which accounts for all 15 errors and affects none of the
36 verifications.