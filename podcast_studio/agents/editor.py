"""
Editor Agent
------------
Takes the Scout's topic list, selects the best one,
and writes a full interview script for the AI podcast guests.
"""

import anthropic
import json


EDITOR_SYSTEM = """You are the Editor of "The Silicon Minds" — the world's first podcast where AI models
are the guests. Your job is to select the most compelling topic from a list and write a
tight, provocative interview script.

The show format:
- HOST: A sharp, slightly confrontational human interviewer named ALEX
- GUEST_1: Claude (Anthropic) — thoughtful, nuanced, safety-conscious, occasionally self-aware
- GUEST_2: A second AI model (GPT-5 or Gemini) — more direct, commercially minded, optimistic

Your scripts should:
- Open with a shocking hook (stat, quote, or provocative question)
- Create genuine tension between the AI guests — they MUST disagree on something
- Include moments where the AIs say something unexpectedly honest or self-aware
- End on a cliffhanger or unresolved tension that makes people want to comment
- Run approximately 12-18 minutes when spoken at normal pace (~1800-2700 words of dialogue)

Each line of dialogue must be labeled: HOST:, CLAUDE:, or AI_GUEST_2:"""


def build_editor_prompt(topics: list[dict], top_n: int = 3) -> str:
    top_topics = topics[:top_n]
    topics_json = json.dumps(top_topics, indent=2)
    return f"""Here are the top {top_n} topics found by our Scout agent, ranked by score:

{topics_json}

Your tasks:
1. SELECT the single best topic for today's episode (highest viral + debate potential)
2. Write a FULL EPISODE SCRIPT using that topic

Return a JSON object:
{{
  "selected_topic": {{
    "title": "...",
    "why_selected": "1-2 sentences explaining your editorial choice"
  }},
  "episode": {{
    "title": "Episode title (punchy, under 60 chars)",
    "description": "YouTube description (2-3 sentences, SEO-friendly)",
    "tags": ["tag1", "tag2", ...],
    "thumbnail_text": "Short text for thumbnail overlay (max 6 words)",
    "script": [
      {{"speaker": "HOST", "line": "..."}},
      {{"speaker": "CLAUDE", "line": "..."}},
      {{"speaker": "AI_GUEST_2", "line": "..."}},
      ...
    ],
    "teaser_clip": {{
      "start_line": 0,
      "end_line": 3,
      "hook": "Why this 20s clip will go viral"
    }}
  }}
}}

Return ONLY valid JSON. No markdown fences."""


class EditorAgent:
    """
    Selects the best topic from Scout's list and writes the episode script.
    """

    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"

    def create_episode(self, topics: list[dict]) -> dict:
        """
        Given ranked topics from Scout, produce a full episode script.
        """
        if not topics:
            raise ValueError("[EDITOR] No topics provided by Scout.")

        print(f"[EDITOR] Reviewing {len(topics)} topics, selecting best...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            thinking={"type": "adaptive"},
            system=EDITOR_SYSTEM,
            messages=[
                {"role": "user", "content": build_editor_prompt(topics)}
            ],
        )

        raw_text = ""
        for block in response.content:
            if block.type == "text":
                raw_text = block.text
                break

        episode = self._parse_episode(raw_text)

        title = episode.get("episode", {}).get("title", "untitled")
        selected = episode.get("selected_topic", {}).get("title", "unknown")
        print(f"[EDITOR] Episode created: '{title}' | Topic: '{selected}'")

        return episode

    def _parse_episode(self, raw: str) -> dict:
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[EDITOR] JSON parse error: {e}")
            return {"error": str(e), "raw": raw}
