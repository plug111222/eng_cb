import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Get the API key securely from environment variables
client = OpenAI(api_key=os.getenv("CHAT_KEY"))

# --- Predefined knowledge base for the chatbot ---
knowledge = [
    "Campus 'Match High School' has an average engagement score of approximately 3.66.",
    "Campus 'Match Middle School' has an average engagement score of approximately 3.81.",
    "Campus 'Match Community Day' has an average engagement score of approximately 3.84.",
    "Campus 'School Central Office' has an average engagement score of approximately 4.19.",
    "Role 'Teacher' has an average engagement score of approximately 3.74.",
    "Role 'Associate Teacher' has an average engagement score of approximately 3.79.",
    "Role 'School Leader' has an average engagement score of approximately 3.79.",
    "Role 'School Staff' has an average engagement score of approximately 3.81.",
    "Role 'Network Staff' has an average engagement score of approximately 4.23.",
    "Age group '21–29' has an average engagement score of approximately 3.72.",
    "Age group '30–39' has an average engagement score of approximately 3.83.",
    "Age group '40–49' has an average engagement score of approximately 3.91.",
    "Gender 'female' has an average engagement score of approximately 3.80.",
    "Gender 'male' has an average engagement score of approximately 3.90.",
    "Race 'White' has an average engagement score of approximately 3.79.",
    "Race 'Black or African American' has an average engagement score of approximately 3.89.",
    "Race 'Hispanic or Latino' has an average engagement score of approximately 4.00.",
    "Tenure group '3–5 yrs' has an average engagement score of approximately 3.56.",
    "Tenure group '5–10 yrs' has an average engagement score of approximately 3.68.",
    "Tenure group '1–3 yrs' has an average engagement score of approximately 3.79.",
    "Tenure group '<1 yr' has an average engagement score of approximately 3.89.",
    "22.0% of staff are categorized as 'Engaged'.",
    "9.5% of staff are categorized as 'Actively Disengaged'.",
    "68.4% of staff are categorized as 'Not Engaged'."
]

# --- Homepage with simple input form ---
@app.route("/")
def index():
    return render_template_string('''
    <!doctype html>
    <html>
        <head>
            <title>Staff Engagement Chatbot</title>
            <style>
                body { font-family: Arial; padding: 30px; }
                input, button { font-size: 16px; padding: 10px; }
                input { width: 80%; }
                #response { margin-top: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>📊 Staff Engagement Chatbot</h2>
            <p>Ask a question about school engagement trends:</p>
            <form id="chat-form">
                <input type="text" id="question" placeholder="Type your question...">
                <button type="submit">Ask</button>
            </form>
            <div id="response"></div>
            <script>
                document.getElementById('chat-form').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    const question = document.getElementById('question').value;
                    const res = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question })
                    });
                    const data = await res.json();
                    document.getElementById('response').innerText = data.answer;
                });
            </script>
        </body>
    </html>
    ''')

# --- Chatbot logic endpoint ---
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "")
    prompt = (
        "You are a school data summary chatbot. Respond only using general trends. "
        "Do not reference individual-level data.\n\n"
        "Knowledge base:\n" +
        "\n".join(knowledge) +
        f"\n\nUser: {user_question}\nChatbot:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return jsonify({"answer": answer})

# --- Start the Flask app ---
if __name__ == "__main__":
    app.run(debug=True)
