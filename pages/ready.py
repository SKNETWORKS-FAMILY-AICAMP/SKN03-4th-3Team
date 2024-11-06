import streamlit as st
import streamlit.components.v1 as components

# 페이지 제목 및 CSS 스타일 추가
st.markdown("""
    <style>
        .custom-title {
            font-size: 40px;
        }
        .custom-subheader {
            font-size: 20px;
            color: #333;
        }
        .car-image {
            position: fixed;
            bottom: 10px;
            width: 100px;
            transition: right 0.5s;
            z-index: 1;
        }
        .goal-image {
            position: fixed;
            bottom: 10px;
            left: 330px;
            width: 100px;
            z-index: 1;
        }
        .road {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50px;
            background-color: gray;
            z-index: 0;
        }
    </style>
""", unsafe_allow_html=True)

# 사용자 정의 제목 및 서브헤더
st.markdown('<h1 class="custom-title">🚗 운전면허 필기 시험 준비물 리스트</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="custom-subheader"> - 운전면허를 준비하는 당신을 위한 체크 리스트!</h2>', unsafe_allow_html=True)

# 준비물 목록 및 체크박스
items = [
    {"name": "신분증", "description": "본인 확인을 위한 필수 신분증입니다.", "image": "https://cdn.pixabay.com/photo/2013/03/29/13/38/contact-97574_1280.png"},
    {"name": "컬러사진 3매", "description": "운전 면허증에 들어갈 컬러사진 3매입니다.", "image": "https://cdn.pixabay.com/photo/2018/09/03/11/51/pictures-3651039_1280.png"},
    {"name": "응시표", "description": "시험을 응시하기 위한 응시표입니다.", "image": "https://cdn.pixabay.com/photo/2016/10/04/13/05/name-1714231_1280.png"},
    {"name": "응시료", "description": "운전면허 시험 응시를 위한 비용입니다.", "image": "https://cdn.pixabay.com/photo/2017/10/08/19/35/money-2831248_1280.png"},
    {"name": "신체검사 증명서", "description": "신체 검사를 통과했음을 증명하는 문서입니다.", "image": "https://cdn.pixabay.com/photo/2018/04/12/04/26/blood-pressure-3312513_1280.png"},
]

st.markdown("""
    <style>
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# 체크박스 및 설명 표시
checked_count = 0  # 선택된 체크박스 개수 추적
for index, item in enumerate(items):
    with st.expander(item["name"], expanded=False):
        st.markdown(f"""
        <div class="center-content">
            <img src="{item["image"]}" alt="{item["name"]}" style="width:200px;">
            <p>{item["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.checkbox("준비 완료", key=f"{item['name']}_{index}"):
            checked_count += 1
            components.html("""
                <div id="scroll-target"></div>
                <script>
                    document.getElementById('scroll-target').scrollIntoView({behavior: "smooth"});
                </script>
            """, height=0, width=0)

# 자동차 위치 계산 (오른쪽에서 왼쪽으로 이동)
car_position = checked_count * 17  # 오른쪽에서 왼쪽으로 이동하도록 설정
st.markdown(f"""
    <div class="road"></div>
    <img src="https://cdn.pixabay.com/photo/2016/04/01/11/11/automobile-1300239_1280.png" 
         class="car-image" alt="Car Illustration" style="right: {car_position}%; width: 100px;">
    <img src="https://cdn-icons-png.flaticon.com/512/2739/2739801.png" 
         class="goal-image" alt="Goal Illustration">
""", unsafe_allow_html=True)

# 모든 체크박스가 선택되었는지 확인
if checked_count == len(items):
    st.success("모든 준비가 다 되었네요! 시험 잘 보고 오세요! 🏁")
else:
    st.write("모든 준비물이 완료되었나요? 안전하게 운전하세요! 🚦")
