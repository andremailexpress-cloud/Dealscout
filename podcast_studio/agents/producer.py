"""
Producer Agent
--------------
Takes the Editor's episode script and prepares it for production:
- Formats dialogue for TTS (ElevenLabs-ready)
- Assigns voice IDs per speaker
- Generates the teaser clip script
- Writes metadata files for YouTube upload
- Outputs a production package
"""

import json
import os
from datetime import datetime
from pathlib import Path


# ElevenLabs voice IDs (replace with your actual voice IDs)
VOICE_MAP = {
    "HOST":        "21m00Tcm4TlvDq8ikWAM",   # Rachel — crisp, professional
    "CLAUDE":      "AZnzlk1XvdvUeBnXmlld",   # Domi — warm, thoughtful
    "AI_GUEST_2":  "ErXwobaYiN019PkySvjV",   # Antoni — direct, confident
}

# Speaker display names for captions/overlays
DISPLAY_NAMES = {
    "HOST":       "Alex (Host)",
    "CLAUDE":     "Claude · Anthropic",
    "AI_GUEST_2": "GPT-5 · OpenAI",
}


class ProducerAgent:
    """
    Prepares the episode for production. Outputs a full production package.
    """

    def __init__(self, output_dir: str = "podcast_studio/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def produce(self, episode_data: dict) -> dict:
        """
        Takes Editor output → returns production package dict + writes files.
        """
        episode = episode_data.get("episode", {})
        selected_topic = episode_data.get("selected_topic", {})

        if not episode:
            raise ValueError("[PRODUCER] No episode data in Editor output.")

        title = episode.get("title", "untitled_episode")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = self._slugify(title)
        episode_id = f"{timestamp}_{slug}"

        print(f"[PRODUCER] Producing episode: {title}")

        # Build TTS script — one entry per line of dialogue
        tts_script = self._build_tts_script(episode.get("script", []))

        # Build teaser TTS (20-second clip)
        teaser_info = episode.get("teaser_clip", {})
        teaser_script = self._build_teaser(
            episode.get("script", []),
            teaser_info.get("start_line", 0),
            teaser_info.get("end_line", 3),
        )

        # YouTube metadata
        yt_metadata = {
            "title": episode.get("title", ""),
            "description": episode.get("description", ""),
            "tags": episode.get("tags", []),
            "thumbnail_text": episode.get("thumbnail_text", ""),
            "category": "Science & Technology",
        }

        # Full production package
        package = {
            "episode_id": episode_id,
            "topic": selected_topic,
            "metadata": yt_metadata,
            "tts_script": tts_script,
            "teaser_script": teaser_script,
            "voice_map": VOICE_MAP,
            "display_names": DISPLAY_NAMES,
            "raw_script": episode.get("script", []),
            "produced_at": datetime.now().isoformat(),
        }

        # Write files
        self._write_package(episode_id, package)
        self._write_readable_script(episode_id, episode.get("script", []), title)

        print(f"[PRODUCER] Package ready → output/{episode_id}/")
        return package

    def _build_tts_script(self, script: list[dict]) -> list[dict]:
        """Convert script lines to TTS-ready format with voice IDs."""
        tts = []
        for i, line in enumerate(script):
            speaker = line.get("speaker", "HOST")
            tts.append({
                "index": i,
                "speaker": speaker,
                "display_name": DISPLAY_NAMES.get(speaker, speaker),
                "voice_id": VOICE_MAP.get(speaker, VOICE_MAP["HOST"]),
                "text": line.get("line", ""),
                "pause_after_ms": self._calc_pause(speaker, line.get("line", "")),
            })
        return tts

    def _build_teaser(self, script: list[dict], start: int, end: int) -> list[dict]:
        """Extract the teaser clip lines (for the 20-second social media cut)."""
        clip = script[start:end + 1]
        return self._build_tts_script(clip)

    def _calc_pause(self, speaker: str, line: str) -> int:
        """Estimate pause duration (ms) after a line based on content."""
        if line.endswith("?"):
            return 800   # question — let it land
        if speaker == "HOST":
            return 400
        if len(line) > 200:
            return 600   # longer thought — breath
        return 300

    def _write_package(self, episode_id: str, package: dict) -> None:
        """Write full JSON production package."""
        ep_dir = self.output_dir / episode_id
        ep_dir.mkdir(parents=True, exist_ok=True)

        pkg_path = ep_dir / "production_package.json"
        with open(pkg_path, "w", encoding="utf-8") as f:
            json.dump(package, f, indent=2, ensure_ascii=False)

        # Separate YouTube metadata file
        meta_path = ep_dir / "youtube_metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(package["metadata"], f, indent=2, ensure_ascii=False)

        # Separate TTS script
        tts_path = ep_dir / "tts_script.json"
        with open(tts_path, "w", encoding="utf-8") as f:
            json.dump(package["tts_script"], f, indent=2, ensure_ascii=False)

        # Teaser script
        teaser_path = ep_dir / "teaser_script.json"
        with open(teaser_path, "w", encoding="utf-8") as f:
            json.dump(package["teaser_script"], f, indent=2, ensure_ascii=False)

    def _write_readable_script(self, episode_id: str, script: list[dict], title: str) -> None:
        """Write a human-readable .txt version of the script."""
        ep_dir = self.output_dir / episode_id
        script_path = ep_dir / "script.txt"

        lines = [f"EPISODE: {title}", "=" * 60, ""]
        for line in script:
            speaker = line.get("speaker", "")
            display = DISPLAY_NAMES.get(speaker, speaker)
            text = line.get("line", "")
            lines.append(f"{display}:")
            lines.append(f"  {text}")
            lines.append("")

        with open(script_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert title to filename-safe slug."""
        import re
        slug = text.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "_", slug)
        return slug[:50]
