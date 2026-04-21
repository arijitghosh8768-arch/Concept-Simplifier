import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Config
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "meta/llama-3.1-8b-instruct"

# ---------- ROBUST LOCAL FALLBACK (Bullet Points) ----------
FALLBACK_EXPLANATIONS = {
    "firewall": "- A firewall acts like a security guard for your network.\n- It checks all incoming and outgoing internet traffic.\n- If something looks dangerous or unauthorized, it blocks it.\n- Real-world example: Like a bouncer at a club checking IDs at the door.",
    "phishing": "- Phishing is a trick where hackers pretend to be a trusted company.\n- They send fake emails or texts to steal your passwords or money.\n- Real-world example: Like a digital 'fishing' hook trying to catch your secrets.\n- Always check the sender's email address carefully.",
    "sql injection": "- SQL Injection is when a hacker types malicious code into a website form.\n- This code tricks the database into revealing secret data like passwords.\n- Real-world example: Like giving a teacher a note that says 'Give me everyone's grades'.",
    "ransomware": "- Ransomware is malware that locks your computer files.\n- It demands money (a ransom) to give you the unlock key.\n- Real-world example: Like a digital kidnapper holding your family photos for money.\n- Never pay – restore your files from a backup instead.",
    "trojan horse": "- A Trojan Horse is malware disguised as a fun game or useful app.\n- Once you open it, it secretly attacks your system or spies on you.\n- Real-world example: Based on the ancient Greek story of the wooden horse hiding soldiers.",
    "vpn": "- VPN stands for Virtual Private Network – it creates a secure 'tunnel'.\n- It hides your real location and encrypts your internet activity.\n- Real-world example: Like sending a letter in a locked safe instead of an open envelope.\n- Great for staying safe on public Wi-Fi.",
    "blockchain": "- Blockchain is a digital ledger that stores data in linked 'blocks'.\n- Once data is written, it cannot be changed or deleted by anyone.\n- Real-world example: Like a shared notebook where everyone can see entries, but no one has an eraser.",
    "zero trust": "- A security model that assumes every user and device is a threat by default.\n- It requires continuous verification for every single access request.\n- Real-world example: Like a building where you must show your ID at every single door.",
    "zero-day exploit": "- A zero-day exploit is a security hole that hackers find before the maker knows about it.\n- Developers have 'zero days' to fix it before it is used for attacks.\n- Real-world example: Like a secret back door into a bank that even the bank manager doesn't know exists."
}

def get_local_explanation(topic: str) -> str:
    """Return a bulleted explanation from the local database."""
    topic_clean = topic.lower().strip()
    # Exact match or partial match
    if topic_clean in FALLBACK_EXPLANATIONS:
        return FALLBACK_EXPLANATIONS[topic_clean]
    for key, value in FALLBACK_EXPLANATIONS.items():
        if key in topic_clean or topic_clean in key:
            return value
    # Generic fallback if not in DB
    return f"- '{topic.capitalize()}' is a key concept in technology and security.\n- It involves protecting data or improving how systems communicate.\n- (Note: Connect to the API for a more detailed, real-time explanation.)"

def simplify_with_nvidia(topic: str) -> str:
    """Attempt NVIDIA API call with automatic local fallback on failure."""
    if not NVIDIA_API_KEY or NVIDIA_API_KEY == "your_nvidia_api_key_here":
        return get_local_explanation(topic)

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Explain the following concept in very simple English for a 12-year-old. 
Use **bullet points** (one per line, starting with a dash -). Keep it to 3-5 bullet points. 
Include a simple real-world example as one of the bullet points.

Concept: {topic}

Simple explanation (bullet points):"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 250
    }

    try:
        response = requests.post(NVIDIA_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        # Seamlessly fallback to local DB on any error (503, Timeout, Network)
        return get_local_explanation(topic)

@app.route("/", methods=["GET", "POST"])
def home():
    explanation = ""
    topic = ""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if topic:
            explanation = simplify_with_nvidia(topic)
    return render_template("index.html", explanation=explanation, topic=topic)

@app.route("/api/simplify", methods=["POST"])
def api_simplify():
    """Endpoint for AJAX calls"""
    data = request.get_json()
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    result = simplify_with_nvidia(topic)
    return jsonify({"explanation": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
