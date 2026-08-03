# Contributing

A change to `orbital_trade` should state the reference frame, sign convention, units and
validity boundary. Include a limiting case or conservation test. Do not turn a geometry screen
into a conjunction claim by adding an assumed covariance and a precise-looking probability.

Commit subjects should describe the physical consequence. “Separate recoil magnitude from
deployment direction” is useful later; “update core.py” is not.

The files under `reference/volley/` are retained from VOLLEY commit `aa22a06`. Change them only
by selecting a later reviewed VOLLEY commit, copying its exact blobs and regenerating
`SOURCE_MANIFEST.json`.

Before proposing a release, run:

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```
