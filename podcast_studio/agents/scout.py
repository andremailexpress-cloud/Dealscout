"""
Scout Agent
-----------
Searches the web for the hottest current AI topics.
Returns a ranked list of potential episode subjects.
"""

import anthropic
import json


SCOUT_SYSTEM = """You are the Scout for a viral AI podcast called "The Silicon Minds".
Your job is to find the most provocative, controversial, and newsworthy topics in AI right now.

You look for:
- Major AI controversies or debates (companies vs regulators, AI safety arguments)
- Surprising AI breakthroughs or failures
- AI vs jobs news with real numbers
- AI consciousness / rights debates
- Feuds between AI labs or researchers
- AI misuse or concerning deployments
- Viral AI demos or experiments

For each topic you find, score it:
- VIRAL_POTENTIAL: 1-10 (how likely to get shares/clicks)
- CONTROVERSY: 1-10 (how much debate it sparks)
- FRESHNESS: 1-10 (how current and not overdone)
- PODCAST_FIT: 1-10 (how well AI guests can debate it)

Return exactly 5 topics as a JSON array."""


SCOUT_PROMPT = """Search for the top trending and most controversial AI news stories right now.
Focus on stories from the last 7 days. Find stories that would make people STOP scrolling.

Return a JSON array with exactly 5 topics, each structured as:
{
  "title": "Short punchy topic title",
  "summary": "2-3 sentence summary of the story",
  "controversy": "What makes this divisive or shocking",
  "debate_angle": "The key question AI models could argue about",
  "sources": ["source 1", "source 2"],
  "scores": {
    "viral_potential": 0,
    "controversy": 0,
    "freshness": 0,
    "podcast_fit": 0,
    "total": 0
  }
}

Return ONLY valid JSON. No markdown, no explanation."""


class ScoutAgent:
    """
    Scours the web for hot AI topics using Claude + web_search.
    """

    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"

    def find_topics(self) -> list[dict]:
        """
        Run the scout: search web, return ranked topic list.
        """
        print("[SCOUT] Searching for hot AI topics...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SCOUT_SYSTEM,
            tools=[
                {"type": "web_search_20260209", "name": "web_search"},
            ],
            messages=[
                {"role": "user", "content": SCOUT_PROMPT}
            ],
        )

        # Extract the final text block (after tool use)
        raw_text = ""
        for block in response.content:
            if block.type == "text":
                raw_text = block.text
                break

        topics = self._parse_topics(raw_text)
        topics = self._rank_topics(topics)

        print(f"[SCOUT] Found {len(topics)} topics. Top: {topics[0]['title'] if topics else 'none'}")
        return topics

    def _parse_topics(self, raw: str) -> list[dict]:
        """Parse JSON from Claude's response, tolerating minor formatting issues."""
        raw = raw.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        try:
            data = json.loads(raw)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            print(f"[SCOUT] JSON parse error: {e}")
            return []

    def _rank_topics(self, topics: list[dict]) -> list[dict]:
        """Sort topics by total score descending. Fill missing scores."""
        for t in topics:
            scores = t.get("scores", {})
            if "total" not in scores or scores["total"] == 0:
                scores["total"] = sum([
                    scores.get("viral_potential", 0),
                    scores.get("controversy", 0),
                    scores.get("freshness", 0),
                    scores.get("podcast_fit", 0),
                ])
            t["scores"] = scores

        return sorted(topics, key=lambda x: x["scores"].get("total", 0), reverse=True)
