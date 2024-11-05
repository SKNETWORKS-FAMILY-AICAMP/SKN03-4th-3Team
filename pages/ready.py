import streamlit as st

# 페이지 제목
# CSS 스타일을 추가하여 제목을 조정
st.markdown("""
    <style>
        .custom-title {
            font-size: 40px; /* 제목 크기 */
        }
        .custom-subheader {
            font-size: 20px; /* 서브헤더 크기 */
            color: #333; /* 연한 검은색 (약간 회색) */
        }
        .car-image {
            position: fixed; /* 고정 위치 */
            bottom: 10px; /* 아래쪽에서의 간격 */
            right: 10px; /* 오른쪽에서의 간격 */
            width: 200px; /* 이미지 크기 조정 (필요시) */
            z-index: 1; /* 다른 요소 아래에 표시되도록 설정 */
        }
    </style>
""", unsafe_allow_html=True)

# 사용자 정의 제목
st.markdown('<h1 class="custom-title">🚗 운전면허 필기 시험 준비물 리스트</h1>', unsafe_allow_html=True)
# 사용자 정의 서브헤더
st.markdown('<h2 class="custom-subheader"> - 운전면허를 준비하는 당신을 위한 체크 리스트!</h2>', unsafe_allow_html=True)

# 준비물 목록
items = [
    {"name": "신분증", "description": "본인 확인을 위한 필수 신분증입니다.", "image": "https://cdn.pixabay.com/photo/2013/03/29/13/38/contact-97574_1280.png"},
    {"name": "컬러사진 3매", "description": "운전 면허증에 들어갈 컬러사진 3매입니다.", "image": "https://cdn.pixabay.com/photo/2018/09/03/11/51/pictures-3651039_1280.png"},
    {"name": "응시표", "description": "시험을 응시하기 위한 응시표입니다.", "image": "https://cdn.pixabay.com/photo/2016/10/04/13/05/name-1714231_1280.png"},
    {"name": "응시료", "description": "운전면허 시험 응시를 위한 비용입니다.", "image": "https://cdn.pixabay.com/photo/2017/10/08/19/35/money-2831248_1280.png"},
    {"name": "신체검사 증명서", "description": "신체 검사를 통과했음을 증명하는 문서입니다.", "image": "https://cdn.pixabay.com/photo/2018/04/12/04/26/blood-pressure-3312513_1280.png"},
]

# CSS 스타일을 추가하여 expander 안의 콘텐츠를 중앙 정렬
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
for item in items:
    with st.expander(item["name"], expanded=False):
        # 이미지와 설명을 중앙에 배치
        st.markdown(f"""
        <div class="center-content">
            <img src="{item["image"]}" alt="{item["name"]}" style="width:200px;">
            <p>{item["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("준비 완료", key=item["name"])

# 오른쪽 하단에 자동차 일러스트 삽입
st.markdown(f'<img src="https://cdn.pixabay.com/photo/2016/04/01/11/11/automobile-1300239_1280.png" class="car-image" alt="Car Illustration">', unsafe_allow_html=True)

# 모든 체크박스가 선택되었는지 확인
if all(st.session_state.get(item["name"], False) for item in items):
    st.success("모든 준비가 다 되었네요! 시험 잘 보고 오세용 ㅎvㅎ")
else:
    st.write("모든 준비물이 완료되었나요? 안전하게 운전하세요! 🚦")
