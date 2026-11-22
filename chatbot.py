import random
import re
import unicodedata
from datetime import datetime

MAX_INPUT_LENGTH = 500
MATCH_THRESHOLD = 0.65

INTENTS = {
    "farewell": {
        "words": ["bye", "goodbye", "exit", "quit", "cya", "goodnight", "farewell"],
        "phrases": ["see you", "see ya", "take care", "good night", "talk later"],
        "responses": ["Goodbye{n}! Have a great day.", "Bye{n}! Talk to you soon.",
                      "See you later{n}. Take care!"],
    },
    "greeting": {
        "weight": 0.5,
        "words": ["hi", "hello", "hey", "hola", "howdy", "greetings", "yo", "hii", "heya"],
        "phrases": ["good morning", "good afternoon", "good evening"],
        "responses": ["Hello{n}! How can I help you?", "Hi there{n}! What can I do for you?",
                      "Hey{n}! Nice to see you."],
    },
    "how_are_you": {
        "words": [],
        "phrases": ["how are you", "how are u", "how r u", "how do you do", "whats up",
                    "how is it going", "hows it going", "how are things", "how you doing"],
        "responses": ["I am doing great, thanks for asking{n}! How about you?",
                      "All systems running smoothly{n}. How are you?"],
    },
    "thanks": {
        "words": ["thanks", "thank", "thx", "thankyou", "appreciate", "cheers"],
        "phrases": ["thank you", "many thanks"],
        "responses": ["You are welcome{n}!", "Happy to help{n}!", "Anytime{n}!"],
    },
    "time": {
        "words": ["time", "clock"],
        "phrases": ["what time", "current time", "tell me the time"],
        "responses": ["The current time is {time}."],
    },
    "date": {
        "words": ["date", "calendar"],
        "phrases": ["what day", "todays date", "what is today", "which day",
                    "day is it", "current date", "whats today"],
        "responses": ["Today is {date}."],
    },
    "weather": {
        "words": ["weather", "temperature", "forecast", "rain", "raining"],
        "phrases": [],
        "responses": ["I cannot check live weather, but a weather app or website will "
                      "give you an accurate forecast."],
    },
    "bot_name": {
        "words": [],
        "phrases": ["your name", "who are you", "what are you", "who made you",
                    "introduce yourself"],
        "responses": ["I am PyBot, a simple rule-based chatbot built with Python."],
    },
    "user_name": {
        "words": [],
        "phrases": ["my name", "who am i", "know my name"],
        "responses": ["__USER_NAME__"],
    },
    "help": {
        "words": ["help", "assist", "assistance", "support", "commands", "options", "menu"],
        "phrases": ["what can you do", "how do you work", "what do you know"],
        "responses": ["I can: greet you, tell the time and date, tell a joke, remember your "
                      "name (say 'my name is ...'), and chat politely. Type 'bye' or 'exit' "
                      "to leave."],
    },
    "joke": {
        "words": ["joke", "jokes", "funny", "laugh", "humor"],
        "phrases": ["make me laugh", "cheer me up"],
        "responses": ["Why do programmers prefer dark mode? Because light attracts bugs.",
                      "There are 10 kinds of people: those who understand binary and those who do not.",
                      "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'"],
    },
}

FALLBACKS = [
    "Sorry, I did not understand that. Could you rephrase it?",
    "Hmm, I am not sure what you mean. Try asking about the time, date, or a joke.",
    "I do not know that one yet. Type 'help' to see what I can do.",
]

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKD", text[:MAX_INPUT_LENGTH])
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def squeeze(word):
    return re.sub(r"(.)\1+", r"\1", word)


def edit_distance(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[-1][-1]


WORD_INDEX = {}
SQUEEZED_INDEX = {}
for _intent, _rule in INTENTS.items():
    for _w in _rule["words"]:
        WORD_INDEX.setdefault(_w, []).append(_intent)
        SQUEEZED_INDEX.setdefault(squeeze(_w), []).append(_intent)


def match_word(token):
    if token in WORD_INDEX:
        return WORD_INDEX[token], 1.0
    if squeeze(token) in SQUEEZED_INDEX:
        return SQUEEZED_INDEX[squeeze(token)], 0.9
    n = len(token)
    if n < 4:
        return [], 0.0
    allowed = 1 if n < 8 else 2
    for word, intents in WORD_INDEX.items():
        if len(word) < 4 or abs(len(word) - n) > allowed:
            continue
        dist = edit_distance(token, word)
        if n == 4:
            ok = dist == 1 and sorted(token) == sorted(word)
        else:
            ok = dist <= allowed
        if ok:
            return intents, 0.7
    return [], 0.0


def match_intent(cleaned, exclude=()):
    scores = {}
    for intent, rule in INTENTS.items():
        for phrase in rule["phrases"]:
            if re.search(rf"\b{re.escape(phrase)}\b", cleaned):
                scores[intent] = scores.get(intent, 0) + 1.5 * len(phrase.split())
    for token in cleaned.split():
        intents, score = match_word(token)
        for intent in intents:
            scores[intent] = scores.get(intent, 0) + score
    best, best_score = None, 0.0
    for intent in INTENTS:
        if intent in exclude:
            continue
        raw = scores.get(intent, 0)
        score = raw * INTENTS[intent].get("weight", 1.0)
        if raw >= MATCH_THRESHOLD and score > best_score:
            best, best_score = intent, score
    return best


NAME_STOPWORDS = {"is", "not", "a", "the", "what", "who", "your", "my"}
NAME_PATTERN = re.compile(r"\b(?:my name is|my name's|call me|i am called)\s+([A-Za-z][A-Za-z'\-]{1,24})",
                          re.IGNORECASE)


FILLERS = {"please", "a", "lot", "so", "much", "very", "you", "u", "there", "everyone", "all",
           "again", "now", "then", "just", "really", "for", "that", "it", "bot", "pybot",
           "good", "morning", "afternoon", "evening", "night", "friend"}
QUICK_INTENTS = {"farewell", "greeting", "thanks"}
PHRASE_WORDS = {name: {w for p in rule["phrases"] for w in p.split()} for name, rule in INTENTS.items()}
MAX_HISTORY = 20


class Chatbot:
    def __init__(self, llm=None):
        self.user_name = None
        self.fallback_streak = 0
        self.llm = llm
        self.history = []

    def remember_name(self, user_input):
        m = NAME_PATTERN.search(user_input or "")
        if m and m.group(1).lower() not in NAME_STOPWORDS:
            self.user_name = m.group(1).capitalize()
            return True
        return False

    def quick_reply(self, user_input):
        cleaned = clean_text(user_input)
        tokens = cleaned.split()
        if not tokens or len(tokens) > 5:
            return None
        intent = match_intent(cleaned)
        if intent not in QUICK_INTENTS:
            return None
        for token in tokens:
            intents, _ = match_word(token)
            if intent not in intents and token not in FILLERS and token not in PHRASE_WORDS[intent]:
                return None
        return self._fmt(random.choice(INTENTS[intent]["responses"])), intent == "farewell"

    def _store(self, user_input, reply, done):
        self.history += [{"role": "user", "content": user_input},
                         {"role": "assistant", "content": reply}]
        del self.history[:-MAX_HISTORY]
        return reply, done

    def reply(self, user_input, timezone=None):
        user_input = (user_input or "").strip()
        quick = self.quick_reply(user_input)
        if quick:
            return self._store(user_input, *quick)
        if self.remember_name(user_input) and len(clean_text(user_input).split()) <= 5:
            return self._store(user_input, f"Nice to meet you, {self.user_name}!", False)
        if self.llm and self.llm.enabled:
            messages = self.history + [{"role": "user", "content": user_input}]
            answer = self.llm.ask(messages, self.user_name, timezone)
            if answer:
                return self._store(user_input, answer, False)
        return self._store(user_input, *self.respond(user_input))

    def _fmt(self, text):
        now = datetime.now()
        return (text.replace("{n}", f", {self.user_name}" if self.user_name else "")
                    .replace("{time}", now.strftime("%I:%M %p").lstrip("0"))
                    .replace("{date}", now.strftime("%A, %d %B %Y")))

    def respond(self, user_input):
        cleaned = clean_text(user_input)
        if not cleaned:
            return "Please type something and I will do my best to help.", False

        if self.remember_name(user_input):
            self.fallback_streak = 0
            return f"Nice to meet you, {self.user_name}!", False

        intent = match_intent(cleaned)
        if intent == "farewell" and not self.quick_reply(user_input):
            intent = match_intent(cleaned, exclude=("farewell",))
        if intent is None:
            self.fallback_streak += 1
            reply = FALLBACKS[min(self.fallback_streak - 1, len(FALLBACKS) - 1)]
            return reply, False

        self.fallback_streak = 0
        reply = random.choice(INTENTS[intent]["responses"])
        if reply == "__USER_NAME__":
            reply = (f"Your name is {self.user_name}." if self.user_name else
                     "I do not know your name yet. Tell me: 'my name is ...'")
        return self._fmt(reply), intent == "farewell"


def main():
    from llm import LLM
    llm = LLM()
    bot = Chatbot(llm)
    mode = "AI mode" if llm.enabled else "offline mode"
    print(f"PyBot ({mode}): Hi! Ask me anything. Type 'bye' or 'exit' to leave.")
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nPyBot: Goodbye!")
            break
        reply, done = bot.reply(user_input)
        print(f"PyBot: {reply}")
        if done:
            break


if __name__ == "__main__":
    main()
