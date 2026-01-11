from flask import Flask, request, jsonify, render_template_string
import requests
import os

API_KEY = "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"  # type your key manually

SYSTEM_PROMPT = "You are Sam GPT, a friendly and intelligent chatbot. Talk casually and clearly. No NSFW, no hate."

app = Flask(__name__)
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sam GPT</title>
<style>
body { font-family: Arial; background: #f0f0f0; padding: 20px; }
#chat { max-width: 600px; margin: auto; }
.message { padding: 10px; margin: 5px 0; border-radius: 5px; }
.user { background: #d1e7dd; text-align: right; }
.bot { background: #fff3cd; text-align: left; }
input { width: 80%; padding: 10px; }
button { padding: 10px; }
</style>
</head>
<body>
<div id="chat"></div>
<input type="text" id="userInput" placeholder="Type a message">
<button onclick="sendMessage()">Send</button>
<script>
async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value;
    if(!message) return;
    addMessage(message,'user');
    input.value='';
    const res = await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});
    const data = await res.json();
    addMessage(data.reply,'bot');
}
function addMessage(msg,type){
    const chat=document.getElementById("chat");
    const div=document.createElement("div");
    div.textContent=msg;
    div.className="message "+type;
    chat.appendChild(div);
    chat.scrollTop=chat.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    messages.append({"role": "user", "content": user_input})

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model":"gpt-4o-mini","messages":messages}
    )
    data = response.json()
    reply = data["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
