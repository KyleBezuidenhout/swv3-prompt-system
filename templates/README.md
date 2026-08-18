# Layer templates — NOT YET WRITTEN

Two templates belong here; both are open items (see README "Current status"):

- **`workspace-prompt.md`** — the scaffold a business fills in: house style, industry context, tightened tier rules. Must respect the lint gate rules (docs/implementation-guide.md §6): may tighten tiers, never loosen; ≤ ~2k tokens.
- **`user-prompt.md`** — the scaffold for an operator's personal custom instructions. ≤ ~1k tokens.

When writing them, follow the contract's own craft rules (reasons attached, no compliance theater, calibrate by example) and the corpus finding that banned-phrase lists and worked examples beat adjectives. The templates are customer-facing product surface — design them with the same care as the contract.
