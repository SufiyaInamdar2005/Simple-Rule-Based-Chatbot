import os
import sys
from datetime import datetime

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")


class LLM:
    def __init__(self):
        key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=key) if anthropic and key else None

    @property
    def enabled(self):
        return self.client is not None

    def _now(self, timezone):
        try:
            return datetime.now(ZoneInfo(timezone)) if timezone and ZoneInfo else datetime.now().astimezone()
        except Exception:
            return datetime.now().astimezone()

    def ask(self, messages, user_name=None, timezone=None):
        now = self._now(timezone).strftime("%A, %d %B %Y, %I:%M %p %Z")
        system = (
            "You are PyBot, an expert assistant. Answer any question accurately, clearly and "
            "concisely. For maths and logic show the key steps. For code give working, idiomatic "
            "code in triple-backtick fences. If you are unsure or lack live data (news, prices, "
            "weather), say so instead of guessing. Use plain text without markdown headings or "
            f"bold. Current date and time: {now}."
        )
        if user_name:
            system += f" The user's name is {user_name}."
        try:
            response = self.client.messages.create(
                model=MODEL, max_tokens=1500, system=system, messages=messages
            )
            return "".join(b.text for b in response.content if b.type == "text").strip() or None
        except Exception as exc:
            print(f"LLM error: {exc}", file=sys.stderr)
            return None
