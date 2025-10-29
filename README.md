InkMath – Draw Math. Get Answers.
=================================

OpenCV-powered whiteboard that converts hand-drawn math (equations, integrals, annotated triangles) into solutions rendered live on an Answer Board. Runs locally in VS Code; no Docker, no cloud.

✨ Features
----------

- Handwritten → LaTeX OCR (pix2tex) with local model auto-download
- Algebra: solve, simplify, factor; systems (2×2)
- Calculus: definite/indefinite integrals with SymPy + numeric fallback
- Geometry: triangle solver with right-angle detection & angle labels
- Smooth drawing, undo/redo, eraser, box-select, clear, grid overlay
- Answer Board with LaTeX rendering and step-by-step hints

1) Quick Start
--------------

Prereqs: Python 3.10+, Git, VS Code recommended.

```bash
git clone <your-repo-url>
cd inkmath
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# First run downloads the OCR model (~100–200MB)
python src/run.py
```

macOS: The first time, grant Screen/Files access if prompted (no keyboard control required).
GPU: Set models.device: cuda in ~/.inkmath/config.yaml if you have a working PyTorch CUDA setup.

2) How To Use
-------------

### Canvas Basics

- P Pen · E Eraser · B Box-Select · M Move
- Ctrl+Z / Ctrl+Y Undo/Redo · C Clear · R Recognize
- Toggle Grid (G), Theme (T)

### Equations

1. Write: x^2 - 5x + 6 = 0
2. Box-select → press R
3. Answer Board shows roots, factorization, and optional steps.

### Integrals

1. Draw ∫ with optional bounds: ∫_0^1 x^2 dx or ∫ sin(x) dx
2. Box-select (or rely on auto detection) → R
3. See exact symbolic result; definite integrals also show numeric value.

### Triangles

1. Draw a triangle with straight strokes.
2. Label two or more values (e.g., a=3, b=4, ∠C=90° or add a small square at the right angle).
3. Box-select the triangle + labels → R
4. Answer Board returns the missing side/angles, area, perimeter.

Without a right-angle or an angle value, two sides alone are insufficient and the app will tell you what’s missing.

3) Configuration
----------------

First run creates ~/.inkmath/config.yaml. Example:

```yaml
canvas:
  width: 1280
  height: 720
  bg_color: white
  smoothing: true
ocr:
  engine: pix2tex      # or trocr
  debounce_ms: 600
  min_confidence: 0.40
models:
  device: cpu          # or cuda
  pix2tex_path: ~/.inkmath/models/pix2tex
solve:
  timeout_ms_symbolic: 800
  numeric_fallback: true
render:
  dpi: 160
  font_size: 14
  theme: dark
logging:
  level: INFO
  to_file: true
```

### CLI overrides

```bash
python src/run.py --engine pix2tex --device cpu --theme dark
```

4) File Structure
-----------------

```
src/
  run.py                # entry point
  core/                 # config, bootstrap, logging
  ink/                  # drawing & shape heuristics
  ocr/                  # pix2tex / trocr engines + normalization
  nl/                   # LaTeX → SymPy
  solve/                # algebra, calculus, triangle solvers
  render/               # LaTeX → image, answer board
  ui/                   # hotkeys, sidebar
tests/                  # unit & smoke tests
```

5) Troubleshooting
------------------

- OCR mistakes (1 vs l, 0 vs O): Box-select smaller regions; write a bit larger; ensure good contrast.
- Integrals failing: Ensure dx is present for indefinite integrals; for definite, include bounds (_a^b).
- Triangle unsolvable: Provide a right-angle mark or at least one angle value.
- Performance: Switch models.device to cuda or reduce canvas size.
- Model download blocked: Pre-download models and place them under ~/.inkmath/models; set paths in config.

6) Development
--------------

Lint/typecheck/tests:

```bash
ruff check
mypy src
pytest -q
```

Run with logs:

```bash
INKMATH_LOG=DEBUG python src/run.py
```

7) Security & Privacy
---------------------

- Models and configs live under ~/.inkmath.
- No cloud calls. Your ink stays local.
- Optional local CSV metrics if enabled in config.

8) License
---------

MIT. See LICENSE.

9) Roadmap (optional)
---------------------

- Multi-expression layout understanding
- Step-by-step derivations via rule-engine
- Save/load boards and sessions
