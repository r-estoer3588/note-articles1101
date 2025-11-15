# Plush Image Generation — Quick Start (Windows PowerShell)

This repo includes `tools/generate_plush_image.py` to create a hyper-cute plush puppy image from a high-quality prompt. It supports OpenAI (text-to-image) and Stability AI (SDXL text-to-image, image-to-image with a reference).

## 1) Install dependencies

```powershell
pip install -r ..\requirements.txt
```

## 2) Choose a backend and set an API key

- OpenAI
  ```powershell
  $env:OPENAI_API_KEY = "sk-..."
  ```
- Stability AI
  ```powershell
  $env:STABILITY_API_KEY = "..."
  ```

If no key is set, the script runs in dry-run and saves the final prompt next to the output path.

## 3) Run

- OpenAI text-to-image
  ```powershell
  python .\generate_plush_image.py --backend openai --out ..\outputs\plush_openai.png
  ```

- Stability SDXL text-to-image
  ```powershell
  python .\generate_plush_image.py --backend stability --out ..\outputs\plush_sdxl.png --seed 1234
  ```

- Stability image-to-image with a motif
  ```powershell
  python .\generate_plush_image.py --backend stability --image ..\prompt\motif.png --out ..\outputs\plush_i2i.png
  ```

The default prompt is stored at `../prompt/plush_puppy_prompt.txt`. You can edit it and re-run.

## Notes
- Output sidecar JSON records the prompt, backend, and timestamp for reproducibility.
- Size is 1024x1024 by default. Adjust backends or the script if needed.
