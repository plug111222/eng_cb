from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

# --- Flask app setup ---
app = Flask(__name__)
client = OpenAI(api_key="OPENAI_API_KEY"
# --- Knowledge base ---
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

# --- Route for homepage UI ---
@app.route("/")
def index():
    return render_template_string('''
    <!doctype html>
    <html>
        <head>
            <title>Engagement Chatbot</title>
            <style>
                body { font-family: Arial; margin: 40px; }
                input[type=text] { width: 80%; padding: 10px; }
                button { padding: 10px 20px; }
                #response { margin-top: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>📊 Staff Engagement Chatbot</h2>
            <p>Ask a question about engagement trends:</p>
            <form id="chat-form">
                <input type="text" id="question" placeholder="Type your question here...">
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

# --- API endpoint to handle questions ---
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    prompt = (
        "You are a data summary chatbot for a school engagement dashboard. "
        "Use only generalized summaries from staff-wide results. Never reveal individual data.\n\n"
        "Here is your reference knowledge:\n" +
        "\n".join(knowledge) +
        f"\n\nNow respond to the following question:\nUser: {user_question}\nChatbot:"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=200
    )
    return jsonify({"answer": response.choices[0].message.content.strip()})

# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)
