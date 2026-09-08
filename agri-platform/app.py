import streamlit as st
import pandas as pd
from pathlib import Path

from utils.auth import login


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="Agri Platform",
    page_icon="🌱",
    layout="wide"
)


# ==========================================
# 파일 경로
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
FARMS_FILE = BASE_DIR / "data" / "farms.csv"


# ==========================================
# 세션 초기화
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ==========================================
# 농장 데이터 불러오기
# ==========================================

def load_farms():

    if not FARMS_FILE.exists():

        return pd.DataFrame(
            columns=[
                "id",
                "owner_id",
                "farm_name",
                "region",
                "area",
                "crop_type",
                "description"
            ]
        )

    return pd.read_csv(FARMS_FILE)


# ==========================================
# 농장 등록
# ==========================================

def add_farm(
    owner_id,
    farm_name,
    region,
    area,
    crop_type,
    description
):

    farms = load_farms()

    if len(farms) == 0:
        new_id = 1
    else:
        new_id = int(farms["id"].max()) + 1

    new_farm = pd.DataFrame([{
        "id": new_id,
        "owner_id": owner_id,
        "farm_name": farm_name,
        "region": region,
        "area": area,
        "crop_type": crop_type,
        "description": description
    }])

    farms = pd.concat(
        [farms, new_farm],
        ignore_index=True
    )

    farms.to_csv(
        FARMS_FILE,
        index=False,
        encoding="utf-8-sig"
    )


# ==========================================
# 로그인 화면
# ==========================================

def login_page():

    st.title("🌱 Agri Platform")

    st.write(
        "농지 · 농작물 · 도매 · 스마트팜을 연결하는 농업 플랫폼"
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("로그인")

        email = st.text_input(
            "이메일"
        )

        password = st.text_input(
            "비밀번호",
            type="password"
        )

        if st.button(
            "로그인",
            use_container_width=True
        ):

            user = login(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                st.rerun()

            else:

                st.error(
                    "이메일 또는 비밀번호가 올바르지 않습니다."
                )


# ==========================================
# 농장주 대시보드
# ==========================================

def farmer_dashboard():

    user = st.session_state.user

    st.title("🌾 농장주 대시보드")

    st.write(
        f"안녕하세요, **{user['name']}**님!"
    )

    st.divider()

    farms = load_farms()

    # 현재 로그인한 농장주의 농지만 가져오기
    my_farms = farms[
        farms["owner_id"].astype(str)
        == str(user["id"])
    ]

    # --------------------------------------
    # 통계
    # --------------------------------------

    total_farms = len(my_farms)

    total_area = (
        my_farms["area"].sum()
        if len(my_farms) > 0
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "내 농지",
        f"{total_farms}개"
    )

    c2.metric(
        "총 농지 면적",
        f"{total_area:,.0f}평"
    )

    c3.metric(
        "재배 작물",
        my_farms["crop_type"].nunique()
        if len(my_farms) > 0
        else 0
    )

    st.divider()

    # ======================================
    # 내 농지
    # ======================================

    st.subheader("🏞️ 내 농지")

    if len(my_farms) == 0:

        st.info(
            "등록된 농지가 없습니다."
        )

    else:

        display_farms = my_farms[
            [
                "farm_name",
                "region",
                "area",
                "crop_type",
                "description"
            ]
        ].copy()

        display_farms.columns = [
            "농장 이름",
            "지역",
            "면적(평)",
            "재배 작물",
            "설명"
        ]

        st.dataframe(
            display_farms,
            use_container_width=True,
            hide_index=True
        )

    # ======================================
    # 농지 등록
    # ======================================

    st.subheader("➕ 농지 등록")

    with st.form("farm_register_form"):

        farm_name = st.text_input(
            "농장 이름",
            placeholder="예: 홍길동 농장"
        )

        region = st.text_input(
            "지역",
            placeholder="예: 충남 논산시"
        )

        area = st.number_input(
            "농지 면적 (평)",
            min_value=1,
            step=100
        )

        crop_type = st.selectbox(
            "주요 재배 작물",
            [
                "토마토",
                "딸기",
                "배추",
                "고추",
                "벼",
                "사과",
                "배",
                "기타"
            ]
        )

        description = st.text_area(
            "농지 설명",
            placeholder="농지에 대한 설명을 입력하세요."
        )

        submitted = st.form_submit_button(
            "농지 등록하기",
            use_container_width=True
        )

        if submitted:

            if not farm_name:
                st.error(
                    "농장 이름을 입력해주세요."
                )

            elif not region:
                st.error(
                    "지역을 입력해주세요."
                )

            else:

                add_farm(
                    owner_id=user["id"],
                    farm_name=farm_name,
                    region=region,
                    area=area,
                    crop_type=crop_type,
                    description=description
                )

                st.success(
                    "농지가 등록되었습니다! 🎉"
                )

                st.rerun()


# ==========================================
# 도매업자
# ==========================================

def wholesaler_dashboard():

    user = st.session_state.user

    st.title("🏪 도매업자 대시보드")

    st.write(
        f"안녕하세요, **{user['name']}**님!"
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("거래 가능 매물", "24건")
    c2.metric("거래 진행 중", "6건")
    c3.metric("추천 농장", "12곳")

    st.subheader("🍅 농작물 매물")

    crops = [
        ("토마토", "논산 ○○농장", "2,000kg", "3,500원/kg"),
        ("딸기", "부여 △△농장", "500kg", "11,500원/kg"),
        ("배추", "공주 □□농장", "5,000kg", "1,900원/kg")
    ]

    for i, crop in enumerate(crops):

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(4)

            c1.write(f"🌱 **{crop[0]}**")
            c2.write(crop[1])
            c3.write(crop[2])
            c4.write(crop[3])

            if st.button(
                "거래 신청",
                key=f"trade_{i}"
            ):

                st.success(
                    f"{crop[0]} 거래 신청이 완료되었습니다."
                )


# ==========================================
# 토지매매자
# ==========================================

def land_agent_dashboard():

    user = st.session_state.user

    st.title("🏞️ 토지매매자 대시보드")

    st.write(
        f"안녕하세요, **{user['name']}**님!"
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("등록 토지", "8개")
    c2.metric("판매 중", "5개")
    c3.metric("거래 완료", "3건")

    st.subheader("🏞️ 내 토지")

    lands = pd.DataFrame({
        "지역": [
            "논산시 ○○면",
            "부여군 △△면",
            "공주시 □□면"
        ],
        "면적": [
            "3,000평",
            "2,000평",
            "5,000평"
        ],
        "가격": [
            "2억 4,000만원",
            "1억 5,000만원",
            "3억 8,000만원"
        ],
        "상태": [
            "판매 중",
            "판매 중",
            "거래 완료"
        ]
    })

    st.dataframe(
        lands,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 앱 실행
# ==========================================

if not st.session_state.logged_in:

    login_page()

else:

    user = st.session_state.user

    # --------------------------------------
    # 사이드바
    # --------------------------------------

    with st.sidebar:

        st.title("🌱 Agri Platform")

        st.write(
            f"👤 {user['name']}"
        )

        role_names = {
            "farmer": "농장주",
            "wholesaler": "도매업자",
            "land_agent": "토지매매자"
        }

        st.caption(
            role_names.get(
                user["role"],
                user["role"]
            )
        )

        st.divider()

        if st.button(
            "로그아웃",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user = None

            st.rerun()

    # --------------------------------------
    # 역할별 화면
    # --------------------------------------

    if user["role"] == "farmer":

        farmer_dashboard()

    elif user["role"] == "wholesaler":

        wholesaler_dashboard()

    elif user["role"] == "land_agent":

        land_agent_dashboard()

    else:

        st.error(
            "등록되지 않은 사용자 역할입니다."
        )
