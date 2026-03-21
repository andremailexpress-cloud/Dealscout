"""
Podcast Studio Pipeline
-----------------------
Orchestrates the full Scout → Editor → Producer flow.

Usage:
    python -m podcast_studio.pipeline

Or import and call:
    from podcast_studio.pipeline import run_pipeline
    package = run_pipeline()
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from .agents import ScoutAgent, EditorAgent, ProducerAgent


load_dotenv()


def run_pipeline(
    api_key: str | None = None,
    output_dir: str | None = None,
) -> dict:
    """
    Run the full pipeline:
      1. Scout   → find hot AI topics
      2. Editor  → select best topic, write script
      3. Producer → format for TTS + YouTube

    Returns the full production package dict.
    """
    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set.")

    out_dir = output_dir or str(
        Path(__file__).parent / "output"
    )

    print("\n" + "=" * 60)
    print("  THE SILICON MINDS — Episode Production Pipeline")
    print("=" * 60 + "\n")

    # ── Step 1: Scout ──────────────────────────────────────────
    scout = ScoutAgent(api_key=key)
    topics = scout.find_topics()

    if not topics:
        raise RuntimeError("[PIPELINE] Scout returned no topics. Aborting.")

    print(f"\n[PIPELINE] Scout found {len(topics)} topics:")
    for i, t in enumerate(topics, 1):
        score = t.get("scores", {}).get("total", 0)
        print(f"  {i}. [{score:>3}] {t.get('title', '?')}")

    # ── Step 2: Editor ─────────────────────────────────────────
    editor = EditorAgent(api_key=key)
    episode_data = editor.create_episode(topics)

    if "error" in episode_data:
        raise RuntimeError(f"[PIPELINE] Editor failed: {episode_data['error']}")

    # ── Step 3: Producer ───────────────────────────────────────
    producer = ProducerAgent(output_dir=out_dir)
    package = producer.produce(episode_data)

    # ── Summary ────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  PRODUCTION COMPLETE")
    print("=" * 60)
    print(f"  Episode ID : {package['episode_id']}")
    print(f"  Title      : {package['metadata']['title']}")
    print(f"  Topic      : {package['topic'].get('title', '?')}")
    print(f"  Lines      : {len(package['raw_script'])}")
    print(f"  Output     : {out_dir}/{package['episode_id']}/")
    print("=" * 60 + "\n")

    return package


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="The Silicon Minds — AI Podcast Production Pipeline"
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Directory to write episode files (default: podcast_studio/output)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print pipeline steps without calling the API"
    )
    args = parser.parse_args()

    if args.dry_run:
        print("[DRY RUN] Pipeline stages:")
        print("  1. ScoutAgent  → web_search → ranked topics JSON")
        print("  2. EditorAgent → select topic → write episode script JSON")
        print("  3. ProducerAgent → TTS script + YouTube metadata + readable script")
        return

    package = run_pipeline(output_dir=args.output_dir)

    # Print teaser to terminal
    teaser = package.get("teaser_script", [])
    if teaser:
        print("\n── TEASER CLIP (20s) ──────────────────────────────────")
        for line in teaser:
            print(f"  {line['display_name']}: {line['text']}")
        print("───────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
