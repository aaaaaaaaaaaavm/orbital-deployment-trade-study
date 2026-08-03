# Contributing

I treat numerical outputs as engineering claims, not decoration. A change to `orbital_trade`
should include a limiting-case test, stated units, and an explanation of which assumption
changed. Do not replace an unfavourable result by changing a tolerance after the run.

The files under `reference/volley/` are a hashed source snapshot. Change them only by
rebuilding from a reviewed VOLLEY state and regenerating `SOURCE_MANIFEST.json`.

Before proposing a release, run:

```bash
python -m unittest discover -s tests -v
python tools/verify_repository.py
```
