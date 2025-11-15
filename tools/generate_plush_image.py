#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a hyper-cute plush puppy image from a high-quality prompt
using an API backend.

- Supports: OpenAI (gpt-image-1, text-to-image), Stability AI (SDXL,
    text-to-image; image-to-image if --image)
- If no API key is available, --dry-run saves the prompt next to the
    output image path.

Usage (PowerShell example):
  # Set one of the API keys before running
  # $env:OPENAI_API_KEY = "sk-..."  or  $env:STABILITY_API_KEY = "..."
    # python tools/generate_plush_image.py \
    #   --backend openai --out outputs/plush.png

Dependencies:
  - requests (for Stability REST)
  - openai (only when using --backend openai)

This script is safe to run without keys: it validates args and writes the
final prompt for inspection.
"""

import argparse
import base64
import json
import os
import pathlib
import sys
from datetime import datetime
from typing import Optional

DEFAULT_PROMPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "prompt"
    / "plush_puppy_prompt.txt"
)
DEFAULT_OUTPUT = (
    pathlib.Path(__file__).resolve().parents[1] / "outputs" / "plush_puppy.png"
)
DEFAULT_NEGATIVE = (
    "lowres, blur, overexposed, harsh shadows, extra limbs, deformed face, "
    "open seams, plastic look, wet fur, dirty background, text, watermark, "
    "logo, excessive saturation, gritty, toy eyes too reflective"
)


def read_prompt_text() -> str:
    if DEFAULT_PROMPT_PATH.exists():
        return DEFAULT_PROMPT_PATH.read_text(encoding="utf-8")
    # Fallback inline if file missing
    parts = [
        "ultra-soft long-fur plush puppy sitting neatly with both feet",
        "together, front-facing, childlike innocent and playful expression;",
        "gentle pastel yellow as the primary color; hyper-detailed",
        "fibers, fluffy tactile realism, soft diffused studio lighting,",
        "warm and cozy mood, pure white seamless background, soft shadows,",
        "photorealistic plush texture, studio quality, centered composition,",
        "front camera angle.",
    ]
    return " ".join(parts)


def ensure_parent_dir(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_bytes(path: pathlib.Path, data: bytes) -> None:
    ensure_parent_dir(path)
    path.write_bytes(data)


def save_prompt_sidecar(
    out_path: pathlib.Path,
    prompt: str,
    backend: str,
    negative: Optional[str],
) -> None:
    meta = {
        "backend": backend,
        "created": datetime.utcnow().isoformat() + "Z",
        "prompt": prompt,
        "negative": negative or "",
    }
    sidecar = out_path.with_suffix(out_path.suffix + ".json")
    ensure_parent_dir(sidecar)
    sidecar.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run_openai(prompt: str, out_path: pathlib.Path) -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Use --backend stability or --dry-run."
        )
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "openai package is not installed. Run: pip install openai"
        ) from e

    client = OpenAI(api_key=api_key)
    # gpt-image-1 supports text-to-image; size 1024 recommended
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )
    b64 = result.data[0].b64_json
    img = base64.b64decode(b64)
    save_bytes(out_path, img)


def run_stability(
    prompt: str,
    out_path: pathlib.Path,
    negative: Optional[str],
    image_path: Optional[pathlib.Path],
    seed: Optional[int],
) -> None:
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "STABILITY_API_KEY is not set. Use --backend openai or --dry-run."
        )

    import requests  # type: ignore

    headers = {"Authorization": f"Bearer {api_key}"}

    engine = "stable-diffusion-xl-1024-v1-0"
    if image_path:
        # Image-to-Image endpoint
        url = f"https://api.stability.ai/v1/generation/{engine}/image-to-image"
        with open(image_path, "rb") as f:
            files = {"init_image": (image_path.name, f, "image/png")}
            data = {
                "image_strength": 0.35,  # keep motif but allow plush rendering
                "cfg_scale": 5.0,
                "samples": 1,
                "steps": 35,
                "seed": seed or 0,
                "text_prompts[0][text]": prompt,
                "text_prompts[0][weight]": 1.0,
            }
            if negative:
                data["text_prompts[1][text]"] = negative
                data["text_prompts[1][weight]"] = -1.0
            resp = requests.post(
                url, headers=headers, files=files, data=data, timeout=120
            )
    else:
        # Text-to-Image endpoint
        url = f"https://api.stability.ai/v1/generation/{engine}/text-to-image"
        from typing import Any, Dict, List

        text_prompts: List[Dict[str, Any]] = [{"text": prompt, "weight": 1}]
        if negative:
            text_prompts.append({"text": negative, "weight": -1})

        payload: Dict[str, Any] = {
            "text_prompts": text_prompts,
            "cfg_scale": 5.0,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 35,
            "seed": seed or 0,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=120)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Stability API error: {resp.status_code} "
            f"{resp.text[:300]}"
        )

    data = resp.json()
    # v1 returns artifacts with base64
    from typing import Any, List, Dict, cast
    art = cast(List[Dict[str, Any]], data.get("artifacts", []))
    if not art:
        raise RuntimeError("No artifacts returned from Stability API")
    from typing import Optional, cast
    image_b64_opt = cast(Optional[str], art[0].get("base64"))
    if not image_b64_opt:
        raise RuntimeError("No base64 image content in Stability response")
    img = base64.b64decode(image_b64_opt)
    save_bytes(out_path, img)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate plush puppy image via OpenAI or Stability API"
        )
    )
    parser.add_argument(
        "--backend", choices=["openai", "stability"], default=None,
        help="API backend to use",
    )
    parser.add_argument(
        "--out", type=str, default=str(DEFAULT_OUTPUT),
        help="Output image path (.png)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Seed for reproducibility"
    )
    parser.add_argument(
        "--image", type=str, default=None,
        help=(
            "Optional reference image path (used for Stability image-to-image)"
        ),
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Do not call API; write prompt and exit 0",
    )

    args = parser.parse_args()

    out_path = pathlib.Path(args.out)
    prompt_text = read_prompt_text()

    # Extract EN section if present; otherwise use entire text
    # We keep JP for context but pass EN to models primarily.
    use_prompt = None
    if "[EN]" in prompt_text:
        try:
            en_part = prompt_text.split("[EN]")[1]
            if "[NEGATIVE]" in en_part:
                en_part = en_part.split("[NEGATIVE]")[0]
            use_prompt = en_part.strip()
        except Exception:
            use_prompt = prompt_text.strip()
    else:
        use_prompt = prompt_text.strip()

    negative = DEFAULT_NEGATIVE

    # Auto-select backend if not specified
    backend = args.backend
    if backend is None:
        if os.getenv("OPENAI_API_KEY"):
            backend = "openai"
        elif os.getenv("STABILITY_API_KEY"):
            backend = "stability"
        else:
            backend = "openai"  # default; falls back to dry-run if no key

    # Dry-run if no keys
    no_keys = (
        not os.getenv("OPENAI_API_KEY") and not os.getenv("STABILITY_API_KEY")
    )
    if args.dry_run or no_keys:
        ensure_parent_dir(out_path)
        save_prompt_sidecar(out_path, use_prompt, backend, negative)
        # Also save a .prompt.txt for convenience
        out_txt = out_path.with_suffix(".prompt.txt")
        out_txt.write_text(
            use_prompt + "\n\n[NEGATIVE]\n" + (negative or ""),
            encoding="utf-8",
        )
        print("[DRY-RUN] Saved prompt sidecar:", out_txt)
        if no_keys:
            print(
                "No API key detected. Set OPENAI_API_KEY or STABILITY_API_KEY "
                "to generate the image."
            )
        return 0

    try:
        if backend == "openai":
            run_openai(use_prompt, out_path)
        elif backend == "stability":
            ref_img = pathlib.Path(args.image) if args.image else None
            if ref_img and not ref_img.exists():
                raise FileNotFoundError(
                    f"Reference image not found: {ref_img}"
                )
            run_stability(use_prompt, out_path, negative, ref_img, args.seed)
        else:
            raise ValueError(f"Unsupported backend: {backend}")
    except Exception as e:
        # On error, still save prompt for reproducibility
        save_prompt_sidecar(out_path, use_prompt, backend, negative)
        print(f"Generation failed: {e}", file=sys.stderr)
        return 2

    save_prompt_sidecar(out_path, use_prompt, backend, negative)
    print(f"Image saved to: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
