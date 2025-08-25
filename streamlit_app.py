# streamlit 라이브러리를 st라는 별칭으로 가져옵니다.
import streamlit as st

# --- 페이지 설정 ---
# 웹페이지의 제목, 아이콘, 레이아웃을 설정합니다.
# layout="centered"는 콘텐츠를 중앙에 정렬해줍니다.
st.set_page_config(page_title="나의 취향 공유 페이지", page_icon="💖", layout="centered")

# --- 앱 제목 ---
# st.title()을 사용하여 웹 앱에 큰 제목을 표시합니다.
st.title("💖 나의 취향을 공유합니다!")

# --- 사용자 입력 섹션 ---
# st.subheader()로 작은 소제목을 추가하여 각 섹션을 구분합니다.
st.subheader("내 정보 입력하기 ✏️")

# st.columns()를 사용하여 화면을 두 개의 열로 나눕니다.
# 이렇게 하면 입력 필드를 더 깔끔하게 정렬할 수 있습니다.
col1, col2 = st.columns(2)

# 첫 번째 열에 입력 필드를 배치합니다.
with col1:
    # st.text_input() : 사용자로부터 텍스트를 입력받는 위젯입니다.
    name = st.text_input("닉네임", placeholder="예: 열정적인 탐험가")
    favorite_food = st.text_input("최애 음식", placeholder="예: 떡볶이")

# 두 번째 열에 입력 필드를 배치합니다.
with col2:
    # st.text_input() 위젯을 계속 사용합니다.
    favorite_hobby = st.text_input("최애 취미", placeholder="예: 코딩, 독서")
    favorite_song = st.text_input("최애 노래", placeholder="예: 아이유 - 밤편지")

# st.text_area() : 여러 줄의 텍스트를 입력받을 때 사용합니다.
mbti_reason = st.text_area("나를 자유롭게 표현해보세요!", placeholder="자신의 성격, 최근 관심사, 좋아하는 이유 등을 자유롭게 적어주세요. (100자 이내)")

# --- 공유 페이지 생성 버튼 ---
# st.button() : 클릭 가능한 버튼을 생성합니다.
# 사용자가 이 버튼을 누르면, if 구문 안의 코드가 실행됩니다.
if st.button("공유 페이지 생성하기 ✨"):
    
    # 모든 입력 필드가 채워졌는지 확인합니다.
    if name and favorite_food and favorite_hobby and favorite_song and mbti_reason:
        st.divider() # 콘텐츠를 구분하는 가로선을 추가합니다.

        # --- 결과 출력 섹션 ---
        st.subheader(f"🎉 '{name}'님의 취향 페이지가 생성되었어요!")
        
        # st.markdown()을 사용하여 텍스트에 서식을 적용합니다. (굵게, 이탤릭 등)
        # f-string을 사용하여 입력받은 변수를 문자열 안에 포함시킵니다.
        st.markdown(f"**- 최애 음식 🍔:** {favorite_food}")
        st.markdown(f"**- 최애 취미 🎨:** {favorite_hobby}")
        st.markdown(f"**- 최애 노래 🎵:** {favorite_song}")
        
        # st.expander() : 클릭하면 내용이 펼쳐지는 접이식 섹션을 만듭니다.
        with st.expander("나의 한마디 엿보기 👀"):
            st.write(mbti_reason)
        
        # st.success() : 성공 메시지를 초록색 상자에 표시합니다.
        st.success("아래 페이지를 캡처해서 친구들에게 공유해보세요!")
        
        # st.balloons() : 화면에 풍선이 날아가는 재미있는 효과를 추가합니다.
        st.balloons()

    else:
        # st.error() : 필수 항목이 누락되었을 때 사용자에게 알려주는 오류 메시지를 표시합니다.
        st.error("앗! 모든 항목을 입력해야 페이지를 생성할 수 있어요. 😥")