from flask import Flask, request, jsonify, render_template
from src.chatbot import OpenAIChat
from src.database_operations import Database
from src.chatbot_custom import CustomLLM

app = Flask(__name__, template_folder="templates")

chatbot = OpenAIChat()
db = Database()
chatbot_custom = CustomLLM()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    db.connect()
    user_message = request.json.get("message", "")
    messages = db.get_chat_history(1)
    bot_response = chatbot.generate_response(user_message, messages)

    db.insert_llm_logger(user_message, bot_response, 1)
    db.disconnect()
    return jsonify({"message": bot_response})  # Return bot response as JSON


@app.route("/get_response_custom", methods=["POST"])
def get_response_custom():
    user_message = request.json.get("message", "")
    messages = db.get_chat_history(1)
    bot_response = chatbot_custom.generate_response(user_message, messages)
    db.insert_llm_logger(user_message, bot_response, 1)
    db.disconnect()
    return jsonify({"message": bot_response})  # Return bot response as JSON


@app.route("/get_snippets", methods=["POST"])
def get_snippets():
    db.connect()
    user_id = request.json.get("user_id", "")
    snippets = db.get_snippets(user_id)
    db.disconnect()
    return snippets


@app.route("/delete_snippet", methods=["POST"])
def delete_snippet():
    db.connect()
    response_id = request.json.get("response_id", "")
    result = db.delete_snippet(response_id)
    db.disconnect()
    return result


@app.route("/edit_snippet", methods=["POST"])
def edit_snippet():
    db.connect()
    response_id = request.json.get("response_id", "")
    snippet = request.json.get("snippet_content", "")
    result = db.edit_snippet(response_id, snippet)
    db.disconnect()
    return result


@app.route("/test_code", methods=["POST"])
def test_snippet():
    snippet = request.json.get("code", "")
    lines = snippet.split("\n")
    if lines[0].strip().lower().startswith("python"):
        modified_snippet = "\n".join(lines[1:])
    else:
        modified_snippet = snippet
    print(modified_snippet)
    response = chatbot.test_snippet(modified_snippet)
    if response:
        return jsonify({"success": "True"})
    else:
        return jsonify({"fail": "True"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
