import streamlit as st
import sqlite3
import os
import bcrypt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="인공지능 교육 플랫폼", page_icon="🚀", layout="wide")

DB_FILE = "myproject.db"
def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            userid TEXT UNIQUE NOT NULL,
            passwd TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userid TEXT NOT NULL,
            q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, q5 INTEGER,
            q6 INTEGER, q7 INTEGER, q8 INTEGER, q9 INTEGER, q10 INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY(userid) REFERENCES users(userid)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 비밀번호 암호화 및 검증 함수
def hash_password(plain_pw: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_pw.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(plain_pw.encode('utf-8'), hashed_pw.encode('utf-8'))

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'userid' not in st.session_state:
    st.session_state['userid'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

def get_kst_now():
    return (datetime.utcnow() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

if not st.session_state['logged_in']:
    st.title('🔒 Welcome to my Webapp')
    tab_login, tab_signup = st.tabs(["로그인", "신규회원 가입"])
    
    with tab_login:
        st.subheader("로그인")
        login_id = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")
        
        if st.button("로그인 하기", type="primary"):
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE userid = ?", (login_id,)).fetchone()
            conn.close()
            
            if user and verify_password(login_pw, user['passwd']):
                st.session_state['logged_in'] = True
                st.session_state['userid'] = user['userid']
                st.session_state['username'] = user['username']
                st.success(f"🎉 {user['username']}님, 환영합니다!")
                st.rerun()
            else:
                st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")
                
    with tab_signup:
        st.subheader("신규 회원 등록")
        new_name = st.text_input("이름", key="join_name")
        new_id = st.text_input("아이디 (중복 불가)", key="join_id")
        new_pw = st.text_input("비밀번호", type="password", key="join_pw")
        
        if st.button("회원가입 완료"):
            if new_name and new_id and new_pw:
                try:
                    hashed_pw = hash_password(new_pw)
                    conn = get_db_connection()
                    conn.execute(
                        "INSERT INTO users (username, userid, passwd, created_at) VALUES (?, ?, ?, ?)",
                        (new_name, new_id, hashed_pw, get_kst_now())
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ 회원가입이 완료되었습니다! 로그인 탭에서 로그인을 진행해 주세요.")
                except sqlite3.IntegrityError:
                    st.error("❌ 이미 존재하는 아이디입니다. 다른 아이디를 입력해 주세요.")
            else:
                st.warning("⚠️ 모든 빈칸을 채워주세요.")
else:
    st.sidebar.title(f"👤 {st.session_state['username']}님")
    if st.sidebar.button("로그아웃", type="secondary"):
        st.session_state['logged_in'] = False
        st.session_state['userid'] = None
        st.session_state['username'] = None
        st.rerun()
        
    menu = st.sidebar.radio("메뉴 이동", ["메인 홈", "📋 AX 전환 학생 실태조사"])
    
    if menu == "메인 홈":
        st.title('This is my first webapp')
        st.write("---")
        urls=['https://www.youtube.com/watch?v=KR8ddnPjCtk','https://www.youtube.com/watch?v=Gv9_4yMHFhI','https://www.youtube.com/watch?v=MP8R6kBykzE']
        images=['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmhSNJGrrK7GNNwzYnikLsOrFAiKTX3xm06-UVMxCGwg&s=10']
        
        con1, con2 = st.columns((4,1))
        with con1:
            with st.expander('Content...'):
                for u in urls: st.video(u)
        with con2:
            with st.expander('Tips...'):
                st.image(images[0])

        con3, con4 = st.columns((4,1))
        with con3:
            with st.expander('Content...'):
                import pandas as pd
                if os.path.exists('./data.csv'):
                    df = pd.read_csv('./data.csv')
                    st.write(df)
                else:
                    st.info("💡 './data.csv' 파일이 없습니다. 데이터를 배치하면 여기에 테이블이 표시됩니다.")
        with con4:
            with st.expander('Tips...'):
                if os.path.exists('./ml.txt'):
                    with open('./ml.txt','r', encoding='UTF-8') as f:
                        st.markdown(f.read())
                else:
                    st.markdown("머신러닝 가이드가 곧 추가됩니다.")
                st.image(images[0])
                
    elif menu == "📋 AX 전환 학생 실태조사":
        st.title("📋 AX(AI 전환)에 따른 학생 인식 실태조사")
        st.markdown("본 설문은 교육 환경의 인공지능 전환(AX)에 대응하는 학생들의 인식을 파악하기 위한 조사입니다. (5점 리커트 척도)")
        
        questions = [
            "Q1. 학교 수업에서 AI가 적극적으로 도입되어야 한다고 생각한다.",
            "Q2. AI 보조도구는 나의 자기주도적 학습 능력을 향상시키는 데 기여한다.",
            "Q3. AI 기반 교육 프로그램의 도입은 학생 간의 교육 격차를 줄이는 데 도움이 될 것이다.",
            "Q4. 향후 AI 교육 서비스가 고도화된다면 기존 교사의 역할을 상당 부분 대체할 수 있다고 본다.",
            "Q5. 학교 및 공공 교육에서 제공하는 디지털 AI 도구의 데이터 보안을 신뢰한다.",
            "Q6. 인공지능 전환 과정에서 대면 협업 활동이나 인간적 상호작용이 약화될까 우려된다.",
            "Q7. AI 환경에 적응하기 위한 디지털 리터러시 역량을 기르는 데 학교 교육이 도움을 주고 있다.",
            "Q8. 미래 직업 및 진로 설계 과정에서 AX(AI 전환) 트렌드 분석이 필수적이라고 느낀다.",
            "Q9. AI가 생성해 주는 지식 정보나 평가 피드백 결과를 비판 없이 그대로 수용하는 경향이 있다.",
            "Q10. 전반적으로 AI 중심의 교육 패러다임 전환이 나의 미래 역량 강화에 긍정적인 영향을 줄 것이다."
        ]
        
        options = {5: "매우 그렇다", 4: "그렇다", 3: "보통이다", 2: "그렇지 않다", 1: "매우 그렇지 않다"}
        
        with st.form("survey_form"):
            responses = {}
            for idx, q in enumerate(questions, 1):
                st.markdown(f"##### {q}")
                responses[f"q{idx}"] = st.radio(
                    f"선택_{idx}", 
                    options=[1, 2, 3, 4, 5], 
                    format_func=lambda x: f"{x}점 ({options[x]})", 
                    horizontal=True, 
                    label_visibility="collapsed"
                )
                st.write("")
                
            submitted = st.form_submit_button("설문 제출하기", type="primary")
            if submitted:
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO inventory (userid, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (st.session_state['userid'], *[responses[f"q{i}"] for i in range(1, 11)], get_kst_now()))
                conn.commit()
                conn.close()
                st.success("🎉 설문 응답이 성공적으로 저장되었습니다. 참여해 주셔서 감사합니다!")
