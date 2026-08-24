# AGENTS

## Project snapshot
- This repository is a small Python/OpenCV prototype for image processing.
- The main implementation lives in [limelighttest.py](limelighttest.py).
- There is no package manifest, build system, or automated test suite in this repo.
- The script depends on `opencv-python` and `numpy` being installed in the local Python environment.

## Working conventions
- Keep edits small and focused on the image-processing workflow.
- Prefer self-contained logic in the existing script unless the project clearly expands beyond one file.
- Avoid hardcoded machine-specific paths when possible; if a path is required, make it explicit and configurable.
- Preserve the current OpenCV/NumPy patterns unless a change is required for correctness or clarity.
- When debugging image processing, validate the input image and the mask/contour pipeline before changing algorithmic behavior.

## Local commands
- Run the project directly:
  - `python limelighttest.py`
- If you need to confirm the environment:
  - `python -c "import cv2, numpy; print(cv2.__version__)"`

## Guidance for AI coding agents
- Treat this repo as a prototype, not a library or app with a formal release pipeline.
- Prefer minimal, readable changes over refactors.
- If adding dependencies or new files, document the reason clearly because the repo does not currently define a project structure or tooling.
- Keep behavior predictable for image input/output and avoid hidden assumptions about local machine setup.

## AI feature and vision work
- This repository is centered on computer-vision processing, so AI-feature work should stay aligned with OpenCV/NumPy patterns rather than introducing unrelated application frameworks.
- Prefer improving the current image pipeline in [limelighttest.py](limelighttest.py) over creating new abstractions, services, or multi-file architecture unless the feature clearly requires it.
- For vision tasks, make masks, contours, thresholds, and transformations explicit and easy to inspect; avoid hidden state or undocumented preprocessing.
- When adding feature logic, validate against the repo's sample images and keep outputs deterministic for the same input image.
- Avoid adding heavy ML tooling, model registries, or packaging conventions unless the task explicitly requires them; this repo currently behaves like a lightweight prototype, not a full AI product.
- If a change affects the image pipeline, document the expected input/output behavior clearly in the code or adjacent notes because there is no larger test or docs structure to rely on.
