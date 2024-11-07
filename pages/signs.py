import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from dotenv import load_dotenv
import openai
import os

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# BLIP 모델과 프로세서 로드
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Streamlit 페이지 설정
st.set_page_config(page_title="교통 표지판 설명 생성기", page_icon="🚦")

# 채팅 기록을 세션 상태에 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 메인 페이지 타이틀과 설명
st.title("🚦 교통 표지판 설명 생성기")
st.subheader("이미지를 업로드하고 이미지에 대해 질문하세요.")

# 이미지 업로드 영역
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 업로드된 이미지가 있으면 세션 상태에 저장하고 표시
if uploaded_file:
    image = Image.open(uploaded_file)
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = image
        st.session_state.messages.append({"role": "user", "type": "image", "content": image})

# 이전 채팅 메시지와 이미지를 화면에 표시
for message in st.session_state.messages:
    if isinstance(message, dict) and "type" in message:
        if message["type"] == "text":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        elif message["type"] == "image":
            with st.chat_message("user"):
                st.image(message["content"], caption="업로드된 이미지", use_column_width=True)

# 사용자가 입력한 질문 받기
if prompt := st.chat_input("이미지에 대한 질문을 입력하세요..."):
    if uploaded_file is None:
        st.error("먼저 이미지를 업로드해주세요.")
    else:
        # 사용자가 입력한 질문을 채팅에 추가
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

        # BLIP 모델을 사용해 기본 설명 생성
        inputs = processor(images=st.session_state.uploaded_image, return_tensors="pt")
        out = model.generate(**inputs)
        blip_description = processor.decode(out[0], skip_special_tokens=True)

        # GPT 모델을 사용해 BLIP 설명을 확장하여 보다 세밀한 설명 생성
        gpt_prompt = (
            f"다음 이미지는 교통 표지판에 대한 설명입니다: '{blip_description}'. "
            f"이 설명을 기반으로 한국어로 더욱 구체적이고 세밀한 교통 표지판 설명을 생성하세요. "
            "특히 해당 표지판의 기능, 운전자에게 요구되는 행동, 그리고 주의 사항에 대해 포함하여 설명하세요."
        )

        # GPT-4 API 호출
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 교통 표지판에 대한 설명을 제공하는 도우미입니다."},
                {"role": "user", "content": gpt_prompt}
            ]
        )
        gpt_description = response.choices[0].message.content.strip()

        # GPT 설명을 채팅에 추가
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": gpt_description})

        # 결과를 화면에 표시 (이미지 없이 텍스트만)
        with st.chat_message("assistant"):
            st.markdown(gpt_description)
