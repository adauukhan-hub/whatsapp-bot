from flask import Flask, request
import requests

app = Flask(__name__)

# --- YAHAN APNI KEYS DALO ---
WHATSAPP_TOKEN = "Yahan Apni IP Key / Access Token Dalo"
PHONE_NUMBER_ID = "Yahan Phone Number ID Dalo"
VERIFY_TOKEN = "learning123"

# Aap ke sare contacts yahan save honge
ALL_CONTACTS = set()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # WhatsApp verification ke liye
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Wrong Token"

    if request.method == "POST":
        data = request.json
        try:
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                msg_body = entry['messages'][0]['text']['body']
                from_number = entry['messages'][0]['from']

                # Naya number list me add karo
                ALL_CONTACTS.add(from_number)
                print(f"Total Contacts: {len(ALL_CONTACTS)}")

                # --- AGENT KA JAWAB ---
                reply_text = f"As-salamu Alaikum! 👋\n\nMain Learning Time Bot hun. Aap ne kaha: '{msg_body}'\n\nMe aap ki kya madad kar sakta hun?"

                # Jawab bhejo
                url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
                payload = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {"body": reply_text}
                }
                requests.post(url, headers=headers, json=payload)

        except Exception as e:
            print(e)
        return "OK", 200

if __name__ == "__main__":
    app.run(port=10000)
