# Validation Scope

Test coverage focuses on consistency and delegation rather than redesigning formulas.

## Cross-validation checks

- angle -> direction -> angle -> direction round-trips
- rope lengths from angles vs rope lengths from direction
- pole branch behavior validated by reconstructed direction consistency

## Wrapper behavior checks

- every public `HookJoint` method is compared against matching `core.py` function output
- guards against accidental duplication or drift in wrapper methods

## Input robustness checks

- non-unit direction vectors accepted and normalized internally
- invalid direction shape and zero vector produce clear `ValueError`
