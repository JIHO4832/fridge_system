import os
from flask import Flask, send_from_directory, request, jsonify
import google.generativeai as genai

app = Flask(__name__, static_folder="static")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/ai", methods=["POST"])
def ai_assistant():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"reply": "음성 명령을 인식하지 못했습니다."}), 400

    if not GEMINI_API_KEY:
        return jsonify({"reply": "Gemini API 키가 설정되지 않았습니다. Render 환경 변수(GEMINI_API_KEY)를 확인해 주세요."})

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"너는 스마트 냉장고의 친절한 AI 음성 비서야. 사용자의 다음 질문이나 명령에 짧고 명확하게 한국어로 답변해줘: {user_message}"
        response = model.generate_content(prompt)
        
        reply_text = response.text if response and response.text else "답변을 생성하지 못했습니다."
        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"reply": f"Gemini 통신 에러가 발생했습니다: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
