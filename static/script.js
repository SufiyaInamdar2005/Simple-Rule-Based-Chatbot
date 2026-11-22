const log = document.getElementById("log");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = form.querySelector("button");
const chips = document.getElementById("chips");
const modeEl = document.getElementById("mode");
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
let ended = false;
let busy = false;

function renderBot(el, text) {
  text.split("```").forEach((part, i) => {
    if (i % 2) {
      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = part.replace(/^[\w+#-]*\n/, "").replace(/\n$/, "");
      pre.appendChild(code);
      el.appendChild(pre);
    } else if (part.trim()) {
      const span = document.createElement("span");
      span.textContent = part.trim();
      el.appendChild(span);
    }
  });
}

function addMessage(text, who) {
  const el = document.createElement("div");
  el.className = `msg msg--${who}`;
  if (who === "bot") renderBot(el, text);
  else el.textContent = text;
  log.appendChild(el);
  log.scrollTop = log.scrollHeight;
}

function setLocked(state) {
  input.disabled = sendBtn.disabled = state;
  if (!state) input.focus();
}

function showTyping() {
  const el = document.createElement("div");
  el.className = "msg msg--bot typing";
  el.setAttribute("aria-label", "PyBot is typing");
  el.innerHTML = "<i></i><i></i><i></i>";
  log.appendChild(el);
  log.scrollTop = log.scrollHeight;
  return el;
}

async function send(text) {
  text = text.trim();
  if (ended || busy || !text) return;
  busy = true;
  addMessage(text, "user");
  input.value = "";
  setLocked(true);
  const typing = showTyping();
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, timezone }),
    });
    const data = await res.json();
    typing.remove();
    if (!res.ok) throw new Error(data.error || "Request failed");
    addMessage(data.reply, "bot");
    if (data.done) {
      ended = true;
      addMessage("Chat ended. Press “New chat” to start again.", "bot");
    }
  } catch (err) {
    typing.remove();
    addMessage("Something went wrong reaching the server. Please try again.", "bot");
  } finally {
    busy = false;
    setLocked(ended);
  }
}

async function restart() {
  try { await fetch("/reset", { method: "POST" }); } catch (err) {}
  ended = false;
  log.innerHTML = "";
  setLocked(false);
  addMessage("Hi! I’m PyBot. Ask me anything, or type “bye” to finish.", "bot");
}

async function loadStatus() {
  try {
    const data = await (await fetch("/status")).json();
    modeEl.textContent = data.ai ? "AI mode" : "Offline mode";
  } catch (err) {
    modeEl.textContent = "Offline mode";
  }
}

form.addEventListener("submit", (e) => { e.preventDefault(); send(input.value); });
chips.addEventListener("click", (e) => { if (e.target.tagName === "BUTTON") send(e.target.textContent); });
document.getElementById("restart").addEventListener("click", restart);

restart();
loadStatus();
