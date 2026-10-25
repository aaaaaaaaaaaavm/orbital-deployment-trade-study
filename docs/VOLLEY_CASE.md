# VOLLEY case and evidence boundary

Documentation cutoff: **25 October 2026**. This page aligns navigation with **VOLLEY-G5-ACR1**; it does not replace local example inputs or regenerate earlier results.

## Scope of this package

Two-body orbital and rigid-body screens; the local VOLLEY case is a historical regression input, not the current ACR1 mission campaign.

The reusable software is version **0.1.3**. Local cases, diagrams and figures use their committed inputs and sources. A diagram describes the software relationship; it is not an additional engineering result. Run the quick start in the [README](../README.md), then the stated local checks before changing inputs.

## Current engineering reference

[ACR1 source, results and reproduction](https://github.com/aaaaaaaaaaaavm/VOLLEY/tree/main/validation/acr1) identifies the corrected twelve-payload configuration: twelve nominal 4 kg 3U surrogates, guided lead-screw feed, a restrained transfer cradle and a captive reusable launch sled. The supported modeled range is **1–3 m/s**, with 3 m/s as the principal case. Eight native/STEP states and 154 accepted motion/refinement checks establish their declared computational geometry boundary.

The mass ledger is **149.55672 kg CAD dry + 7 kg electrical/control allowance = 156.55672 kg device mass**. Allowances are not measured installed equipment. These values and the current finite-force/circuit/mission outputs belong to ACR1. They are not outputs of this narrow package.

Original Gen5 speeds of 16.029 m/s and 12.448 m/s, older mass/fit failures and retained `reference/volley/` snapshots remain tied to their original configurations and source hashes. Where present, the `aa22a06` fixture is a dated source snapshot. No historical fixture is silently updated to ACR1. The separately selected FM08-R3 mixed 1U/3U subsystem and Gen6 studies retain their own identities.

## Navigation and reuse

[Main engineering record](https://github.com/aaaaaaaaaaaavm/VOLLEY) · [Labs alternatives](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) · [Academic thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) · [Paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)

The current license is **CC-BY-4.0**: [full text](../LICENSE), [attribution and scope](../NOTICE), [software citation](../CITATION.cff). Preserve source and third-party credits. Cite the local software version and exact inputs separately from the ACR1 engineering record. No physical prototype, measured performance, flight qualification or provider approval is established here.
