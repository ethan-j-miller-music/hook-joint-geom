# AGENT.MD — Codex Task Plan for hook-joint-geom

> Goal: Improve project quality without changing the mathematical intent.
> Scope: tests, docstrings/comments, documentation structure (README + docs/).
> Non-goals: no algorithmic redesign, no new features beyond tests/docs.

## 0. Working rules (must follow)

1. **Do not change the math** in `core.py` unless a bug is proven by tests.
2. Keep `core.py` as **single source of truth**. `HookJoint` is a wrapper/delegator only.
3. Prefer **relative imports** within the package.
4. Any change that affects public API must be justified and minimized.
5. All new/changed files must be formatted cleanly and pass tests.
6. If you must change behavior, add a regression test demonstrating the bug first.

---

## 1) Add core tests (create `tests/`), prioritize cross-validation

### 1.1 Create test scaffold
- Add `tests/` directory.
- Use `pytest` (preferred).
- Add minimal `pytest.ini` or `pyproject.toml` test config if needed.

### 1.2 Required tests (cross-validation focus)
> The package exposes mappings between angles (θx, θy), direction vector n ∈ S², and tendon rope lengths.

Implement tests that verify:

#### A) Angle ↔ Direction round-trip consistency
1. Randomly sample a set of valid angles `(theta_x, theta_y)` within safe ranges (avoid singular boundaries initially).
2. Compute `n = direction_from_angles(theta_x, theta_y)`.
3. Compute `(theta_x2, theta_y2) = angles_from_direction(n, ...)`.
4. Recompute `n2 = direction_from_angles(theta_x2, theta_y2)`.
5. Assert:
   - `||n - n2||` small (e.g., `<= 1e-9` or appropriate tolerance).
   - `n` is unit length (within tolerance) OR explicitly normalize and check.
6. Add tests around **poles/branch selection** using `pole_theta_x` where applicable:
   - Pick a direction near the singular/pole and assert the chosen solution is consistent by comparing `n` round-trip, not raw angles.

#### B) Rope lengths consistency: (angles → lengths) vs (direction → lengths)
1. Build a representative `TendonParams` fixture (phis 120° spacing; plausible r/h).
2. For random `(theta_x, theta_y)`:
   - `l1 = rope_lengths_from_angles(theta_x, theta_y, params=...)`
   - `n  = direction_from_angles(theta_x, theta_y)`
   - `l2 = rope_lengths_from_direction(n, params=..., eps=..., pole_theta_x=...)`
3. Assert `l1` and `l2` are close (within tolerance).

#### C) HookJoint wrapper delegates correctly
For each wrapper method in `HookJoint`, confirm output matches the corresponding `core.*` function using the same inputs (including eps/pole_theta_x/params). This is a “no duplication” safeguard.

#### D) Input robustness sanity checks
- Ensure functions tolerate non-unit `n` inputs if documented as allowed (normalize inside).
- Ensure error behavior is consistent (raise with clear message) for invalid shapes (e.g., n not length-3).
- Keep these tests aligned with current design intent (do not invent new semantics).

### 1.3 Test coverage targets (pragmatic)
- At least one param fixture + multiple randomized tests with fixed RNG seed.
- Ensure tests run fast (< 1–2 seconds).
- Add `tox` optional only if it’s already in use; otherwise skip.

### 1.4 How to run
- Ensure `pytest -q` passes locally.
- If CI exists, add a minimal workflow (optional; only if repo already has GitHub Actions).

---

## 2) Fill docstrings and important comments (without clutter)

### 2.1 Docstring standard
- Use concise, engineering-style docstrings:
  - Purpose (1 sentence)
  - Args: types + meaning
  - Returns: type + meaning
  - Notes: coordinate conventions, normalization, branches, eps usage
  - Raises: for invalid inputs
- Keep docstrings aligned with existing API names and meanings.

### 2.2 Where docstrings are mandatory
- All public functions exported in `__init__.py`
- `core.py` core mapping functions
- `HookJoint` class and its public methods
- `TendonParams` dataclass (fields explained)

### 2.3 Comments
- Add comments only where they prevent misuse:
  - coordinate frame assumptions
  - branch selection / singular behavior
  - why `eps` exists
- Avoid redundant narration (“now we compute x”).

---

## 3) Restructure documentation: README (user-facing) + docs/ (theory/design)

### 3.1 README.md must be short and user-facing
Keep README focused on:
- What the package does (1–2 paragraphs)
- Installation:
  - `pip install -e .` (dev)
  - `pip install git+https://...@<tag>` (from GitHub)
- Quickstart example (minimal runnable snippet)
- API overview (list of key functions/classes)
- Minimal “Conventions” section (only the must-know points)
- Links to detailed docs in `docs/`

Avoid:
- long derivations
- deep theory blocks
- excessive internal architecture discussion

### 3.2 Create `docs/` 
Use `docs/` directory unless repo already uses `doc/`.
Add at least:

1. `docs/conventions.md`
   - coordinate frame definition
   - angle definitions (θx, θy)
   - direction vector definition and sign conventions
   - normalization policy and tolerances

2. `docs/mapping-theory.md`
   - the mathematical mapping overview
   - notes about singularities/poles
   - how `pole_theta_x` affects inverse mapping branch choice

3. `docs/design-notes.md`
   - “minimum & local coordinate system principle”
   - layering:
     - `core.py` procedural truth
     - `HookJoint` wrapper
   - why relative imports, why frozen dataclasses, etc.

Optional:
- `docs/examples.md` for extended usage
- `docs/validation.md` summarizing what tests verify

### 3.3 Documentation quality bar
- Use clear headings and bullet points.
- Include equations if helpful, but keep them readable.
- No contradictions with code behavior; update docs if behavior differs.

---

## 4) Deliverables checklist

- [ ] `tests/` added with pytest-based tests covering A/B/C/D above
- [ ] `pytest -q` passes
- [ ] Public docstrings added/updated
- [ ] README rewritten to be concise, with links to docs
