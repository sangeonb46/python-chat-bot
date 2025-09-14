import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key=api_key)

# 앱 제목
st.title("🧠 Gemini 챗봇")

# 시스템 프롬프트 입력
system_prompt = st.text_input("원하는 챗봇의 유형을 입력하세요:", key="system_prompt")

# 세션 상태 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 대화 내역 전체 출력
if st.session_state.history:
    st.markdown("### 💬 이전 대화")
    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"사용자: {msg['content']}")
        else:
            st.markdown(f"AI: {msg['content']}")

# 사용자 입력 받기
user_input = st.text_input("You:", key="user_input")

if user_input:
    # 전체 메시지 구성
    history_text = ""
    for m in st.session_state.history:
        role = "사용자" if m["role"] == "user" else "AI"
        history_text += f"{role}: {m['content']}\n"

    contents = (
        f"[시스템]\n{system_prompt}\n\n"
        f"[대화]\n{history_text}사용자: {user_input}\nAI:"
    )

    # Gemini API 호출
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.7,
            ),
        )
        answer = getattr(response, "text", "") or "(빈 응답)"
    except Exception as e:
        answer = f"오류 발생: {str(e)}"

    # 대화 기록 저장
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": answer})

    # 페이지 새로고침 없이 바로 출력
    st.markdown(f"사용자: {user_input}")
    st.markdown(f"AI: {answer}")
