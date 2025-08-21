import streamlit as st
import random
import time
import pandas as pd

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="Mouse Aim Practice", layout="wide")

# --- 게임 상태 초기화 함수 ---
def initialize_game():
    """게임을 초기화하거나 재시작할 때 호출되는 함수"""
    # st.session_state: Streamlit 앱의 세션을 관리하는 객체로, 앱이 재실행되어도 값을 유지합니다.
    st.session_state.score = 0
    st.session_state.misses = 0 # 빗나간 클릭 횟수
    st.session_state.game_over = False
    st.session_state.game_started = True
    st.session_state.start_time = time.time() # 게임 시작 시간 기록
    
    # 게임 난이도 관련 상태 변수
    st.session_state.grid_size = 4 # 초기 그리드 크기 (4x4)
    st.session_state.fake_targets_count = 0 # 가짜 타겟 수
    
    # 리더보드가 없으면 초기화
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = pd.DataFrame(columns=["Player", "Score", "Time (s)", "CPS"])

    # 첫 타겟 위치 생성
    generate_new_target()

def generate_new_target():
    """새로운 타겟과 가짜 타겟의 위치를 랜덤으로 생성하는 함수"""
    grid_size = st.session_state.grid_size
    
    # 모든 가능한 위치 생성
    all_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)]
    
    # 이미 타겟이 있는 위치는 제외
    if 'target_pos' in st.session_state:
        all_positions.remove(st.session_state.target_pos)

    # 샘플링할 총 타겟 수 (진짜 1개 + 가짜)
    total_targets_to_place = 1 + st.session_state.fake_targets_count
    
    # 만약 모든 칸이 타겟으로 채워질 경우를 대비한 예외 처리
    if len(all_positions) < total_targets_to_place:
        # 이 경우, 게임을 더 어렵게 만들거나 종료시킬 수 있습니다. 여기서는 단순히 타겟을 재배치합니다.
        all_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)]

    # 랜덤으로 위치 샘플링
    new_positions = random.sample(all_positions, total_targets_to_place)
    
    # 첫 번째 위치는 진짜 타겟으로 설정
    st.session_state.target_pos = new_positions[0]
    # 나머지는 가짜 타겟으로 설정
    st.session_state.fake_targets_pos = new_positions[1:]


# --- 게임 로직 함수 ---
def update_difficulty():
    """점수와 시간에 따라 게임 난이도를 조절하는 함수"""
    score = st.session_state.score
    
    # 점수가 10점 오를 때마다 그리드 크기 증가 (타겟이 작아지는 효과)
    if 10 <= score < 20:
        st.session_state.grid_size = 5
    elif score >= 20:
        st.session_state.grid_size = 6
    
    # 점수가 25점 이상이면 가짜 타겟 등장 시작
    if score >= 25:
        # 5점마다 가짜 타겟 1개씩 추가
        st.session_state.fake_targets_count = min(5, (score - 20) // 5)


def handle_target_click():
    """타겟을 성공적으로 클릭했을 때 호출되는 함수"""
    st.session_state.score += 1
    update_difficulty() # 난이도 업데이트
    generate_new_target() # 새로운 타겟 생성

def handle_fake_target_click():
    """가짜 타겟을 클릭했을 때 호출되는 함수"""
    st.session_state.score = max(0, st.session_state.score - 2) # 점수 2점 차감
    st.session_state.misses += 1
    generate_new_target() # 페널티 후 타겟 위치 변경

def handle_miss_click():
    """허공을 클릭했을 때(st.button으로 시뮬레이션) 호출되는 함수"""
    st.session_state.score = max(0, st.session_state.score - 1) # 점수 1점 차감
    st.session_state.misses += 1


# --- UI 렌더링 함수 ---
st.title("🎯 Mouse Aim Practice")

# 게임 시작 전 화면
if 'game_started' not in st.session_state or not st.session_state.game_started:
    st.session_state.game_started = False
    st.header("게임 방법")
    st.write("""
    1. 'Start Game' 버튼을 눌러 게임을 시작하세요.
    2. 화면에 나타나는 빨간색 타겟(🔴)을 최대한 빠르고 정확하게 클릭하세요.
    3. 타겟을 맞출 때마다 1점을 얻고, 빗나가거나 가짜 타겟을 누르면 점수가 차감됩니다.
    4. 점수가 높아질수록 타겟이 작아지고, 가짜 타겟이 나타나 난이도가 상승합니다.
    5. 'Stop Game' 버튼을 눌러 게임을 종료하고 리더보드에 점수를 등록할 수 있습니다.
    """)
    if st.button("Start Game", key="start"):
        initialize_game()
        st.rerun() # 앱을 즉시 새로고침하여 게임 화면을 보여줌
        
# 게임 오버 화면
elif st.session_state.game_over:
    total_time = st.session_state.end_time - st.session_state.start_time
    st.header("Game Over!")
    st.subheader(f"최종 점수: {st.session_state.final_score}")
    st.subheader(f"플레이 시간: {total_time:.2f} 초")
    st.subheader(f"빗나간 횟수: {st.session_state.misses}")

    # 리더보드에 이름 입력
    with st.form("leaderboard_form"):
        player_name = st.text_input("리더보드에 등록할 이름을 입력하세요", max_chars=10)
        submitted = st.form_submit_button("점수 등록")
        
        if submitted and player_name:
            # CPS (Clicks Per Second) 계산
            cps = st.session_state.final_score / total_time if total_time > 0 else 0
            
            new_score = pd.DataFrame([{
                "Player": player_name, 
                "Score": st.session_state.final_score, 
                "Time (s)": round(total_time, 2),
                "CPS": round(cps, 2)
            }])
            
            st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, new_score], ignore_index=True)
            # CPS가 높은 순으로 정렬
            st.session_state.leaderboard = st.session_state.leaderboard.sort_values(by="CPS", ascending=False).reset_index(drop=True)
            st.success(f"{player_name}님의 점수가 등록되었습니다!")
    
    if st.button("Play Again", key="play_again"):
        st.session_state.game_started = False # 시작 화면으로 돌아가기
        st.rerun()

# 게임 진행 화면
else:
    # 상단 정보 표시 (점수, 시간, 종료 버튼)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric("Score", st.session_state.score)
    with col2:
        elapsed_time = time.time() - st.session_state.start_time
        st.metric("Time", f"{elapsed_time:.2f} s")
    with col3:
        if st.button("Stop Game", key="stop"):
            st.session_state.game_over = True
            st.session_state.end_time = time.time()
            st.session_state.final_score = st.session_state.score
            st.rerun()

    st.markdown("---")

    # 게임 그리드 생성
    # st.columns를 중첩하여 그리드를 만듭니다.
    grid_size = st.session_state.grid_size
    for r in range(grid_size):
        cols = st.columns(grid_size)
        for c in range(grid_size):
            with cols[c]:
                pos = (r, c)
                # 현재 위치가 진짜 타겟 위치인 경우
                if pos == st.session_state.target_pos:
                    if st.button("🔴", key=f"target_{r}_{c}", use_container_width=True):
                        handle_target_click()
                        st.rerun()
                # 현재 위치가 가짜 타겟 위치인 경우
                elif pos in st.session_state.fake_targets_pos:
                    if st.button("🔴", key=f"fake_{r}_{c}", use_container_width=True):
                        handle_fake_target_click()
                        st.rerun()
                # 빈 공간인 경우 (빗나감을 처리하기 위한 보이지 않는 버튼)
                else:
                    # 빈 버튼을 만들어 클릭을 감지합니다.
                    if st.button(" ", key=f"miss_{r}_{c}", use_container_width=True):
                        handle_miss_click()
                        # 미스 클릭 시에는 타겟을 재배치하지 않습니다.
                        st.rerun()

# 리더보드 표시
st.markdown("---")
st.header("🏆 Leaderboard")
st.write("리더보드는 CPS (Clicks Per Second)가 높은 순으로 정렬됩니다.")
# 리더보드가 비어있지 않으면 데이터프레임을 예쁘게 표시
if not st.session_state.get('leaderboard', pd.DataFrame()).empty:
    st.dataframe(st.session_state.leaderboard, use_container_width=True, hide_index=True)
else:
    st.info("아직 등록된 점수가 없습니다. 게임을 플레이하고 첫 번째 순위를 차지해보세요!")