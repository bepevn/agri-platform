import streamlit as st
import pandas as pd
from utils.auth import login

st.set_page_config(page_title="Agri Platform", page_icon="🌱", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

st.markdown("""
<style>
.main-title { font-size: 42px; font-weight: 700; }
.subtitle { font-size: 18px; color: gray; }
</style>
""", unsafe_allow_html=True)

def login_page():
    st.markdown('<div class="main-title">🌱 Agri Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">농지 · 농작물 · 도매 · 스마트팜을 연결하는 농업 플랫폼</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("로그인")
        email = st.text_input("이메일", placeholder="example@test.com")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인", use_container_width=True):
            user = login(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("이메일 또는 비밀번호가 올바르지 않습니다.")

def farmer_dashboard():
    user = st.session_state.user
    st.title("🌾 농장주 대시보드")
    st.write(f"안녕하세요, **{user['name']}**님!")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("보유 농지", "3개")
    c2.metric("재배 작물", "4종")
    c3.metric("판매 예정", "2건")
    c4.metric("배송 중", "1건")

    st.subheader("📈 주요 작물 시세")
    prices = pd.DataFrame({
        "작물": ["토마토", "배추", "딸기", "고추"],
        "가격": ["3,800원/kg", "2,100원/kg", "12,000원/kg", "7,200원/kg"]
    })
    st.dataframe(prices, use_container_width=True, hide_index=True)

    st.subheader("🏞️ 추천 농지")
    lands = pd.DataFrame({
        "지역": ["논산시 ○○면", "부여군 △△면", "공주시 □□면"],
        "면적": ["2,300평", "2,700평", "2,100평"],
        "가격": ["1억 8,000만원", "1억 9,500만원", "1억 7,000만원"]
    })
    st.dataframe(lands, use_container_width=True, hide_index=True)

def wholesaler_dashboard():
    user = st.session_state.user
    st.title("🏪 도매업자 대시보드")
    st.write(f"안녕하세요, **{user['name']}**님!")
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("거래 가능 매물", "24건")
    c2.metric("거래 진행 중", "6건")
    c3.metric("추천 농장", "12곳")

    st.subheader("🍅 농작물 매물")
    crops = [
        ("토마토", "논산 ○○농장", "2,000kg", "3,500원/kg"),
        ("딸기", "부여 △△농장", "500kg", "11,500원/kg"),
        ("배추", "공주 □□농장", "5,000kg", "1,900원/kg"),
    ]
    for i, (crop, farm, quantity, price) in enumerate(crops):
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"🌱 **{crop}**")
            c2.write(farm)
            c3.write(quantity)
            c4.write(price)
            if st.button("거래 신청", key=f"trade_{i}"):
                st.success(f"{crop} 거래 신청이 완료되었습니다.")

def land_agent_dashboard():
    user = st.session_state.user
    st.title("🏞️ 토지매매자 대시보드")
    st.write(f"안녕하세요, **{user['name']}**님!")
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("등록 토지", "8개")
    c2.metric("판매 중", "5개")
    c3.metric("거래 완료", "3건")

    st.subheader("🏞️ 내 토지")
    lands = pd.DataFrame({
        "지역": ["논산시 ○○면", "부여군 △△면", "공주시 □□면"],
        "면적": ["3,000평", "2,000평", "5,000평"],
        "가격": ["2억 4,000만원", "1억 5,000만원", "3억 8,000만원"],
        "상태": ["판매 중", "판매 중", "거래 완료"]
    })
    st.dataframe(lands, use_container_width=True, hide_index=True)

    st.subheader("➕ 토지 등록")
    with st.form("land_form"):
        region = st.text_input("지역")
        area = st.number_input("면적 (평)", min_value=0)
        price = st.number_input("판매 가격 (원)", min_value=0)
        description = st.text_area("토지 설명")
        submitted = st.form_submit_button("토지 등록")
        if submitted:
            st.success(f"{region} / {area}평 토지가 등록되었습니다.")

if not st.session_state.logged_in:
    login_page()
else:
    user = st.session_state.user
    with st.sidebar:
        st.title("🌱 Agri Platform")
        st.write(f"👤 {user['name']}")
        role_names = {"farmer": "농장주", "wholesaler": "도매업자", "land_agent": "토지매매자"}
        st.caption(role_names.get(user["role"], user["role"]))
        st.divider()
        if st.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    if user["role"] == "farmer":
        farmer_dashboard()
    elif user["role"] == "wholesaler":
        wholesaler_dashboard()
    elif user["role"] == "land_agent":
        land_agent_dashboard()
    else:
        st.error("등록되지 않은 사용자 역할입니다.")
