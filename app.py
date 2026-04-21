from flask import Flask, render_template, request

app = Flask(__name__)

# ========== STABLE LOCAL KNOWLEDGE BASE (No API) ==========
EXPLANATIONS = {
    "firewall": "- A firewall acts like a security guard for your computer.\n- It checks all incoming and outgoing internet traffic.\n- If something looks dangerous, it blocks it.\n- Example: Like a bouncer at a club who checks IDs and stops troublemakers.",
    
    "phishing": "- Phishing is a trick where scammers pretend to be a trusted company.\n- They send fake emails or messages asking for your password or credit card.\n- Example: An email that looks like it's from your bank saying 'click here to verify your account'.\n- Always check the sender's address before clicking links.",
    
    "sql injection": "- SQL Injection is when a hacker types malicious code into a website's search box or login form.\n- This tricks the website into giving away secret data from its database.\n- Example: Entering `' OR '1'='1` as a password might bypass login.\n- Websites prevent this by sanitizing user input.",
    
    "ransomware": "- Ransomware is malware that locks your files and demands money to unlock them.\n- It spreads through email attachments or fake downloads.\n- Example: A popup says 'Pay $500 in Bitcoin or lose all your photos'.\n- Never pay – restore from backups instead.",
    
    "trojan horse": "- A Trojan Horse is malware disguised as a useful or fun program.\n- Once installed, it can steal passwords, spy on you, or damage your system.\n- Example: A free game download that actually installs a keylogger.\n- Only download software from official websites.",
    
    "vpn": "- VPN stands for Virtual Private Network – it creates a secure tunnel for your internet data.\n- It hides your real location and encrypts what you do online.\n- Example: You can appear to be in another country to access blocked websites.\n- Useful on public Wi‑Fi to prevent snooping.",
    
    "blockchain": "- Blockchain is a digital ledger that stores data in linked 'blocks'.\n- Once data is added, it cannot be changed – very secure.\n- Example: Bitcoin uses blockchain to record every transaction.\n- Think of it as a shared notebook that everyone can see but no one can erase.",
    
    "routing information protocol": "- RIP (Routing Information Protocol) helps routers share information about network paths.\n- It tells routers the best way to send data from one computer to another.\n- RIP counts the number of 'hops' (router jumps) to find the shortest route.\n- Example: Like a GPS that calculates the fastest route by counting traffic lights.",
    
    "rip": "- RIP stands for Routing Information Protocol.\n- It's a simple protocol routers use to exchange network distance information.\n- It uses 'hop count' as its metric (max 15 hops).\n- Example: In a delivery network, RIP would choose the route with the fewest stops.",
    
    "zero-day exploit": "- A zero‑day exploit is a security hole that hackers find before the software maker knows about it.\n- 'Zero‑day' means the developer has zero days to fix it.\n- Example: A hacker discovers a bug in Windows and uses it to break into computers.\n- Regular updates help close these holes.",
    
    "zero trust": "- A security model that assumes every user and device is a threat by default.\n- It requires continuous verification for every single access request.\n- Real-world example: Like a building where you have to show your ID at every single door."
}

def get_explanation(topic):
    # Normalize input
    topic_lower = topic.lower().strip()
    # Remove common question words
    for prefix in ["what is ", "define ", "explain ", "tell me about ", "what's ", "what are "]:
        if topic_lower.startswith(prefix):
            topic_lower = topic_lower[len(prefix):]
    topic_lower = topic_lower.strip()
    
    # 1. Exact match
    if topic_lower in EXPLANATIONS:
        return EXPLANATIONS[topic_lower]
    
    # 2. Partial match
    for key, value in EXPLANATIONS.items():
        if key in topic_lower or topic_lower in key:
            return value
    
    # 3. Generic fallback
    return f"- '{topic}' is a concept in computer networking or technology.\n- It defines rules or methods for communication.\n- Example: Protocols like RIP, HTTP, or TCP/IP help systems work together."

@app.route("/", methods=["GET", "POST"])
def home():
    explanation = ""
    topic = ""
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if topic:
            explanation = get_explanation(topic)
    return render_template("index.html", explanation=explanation, topic=topic)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
