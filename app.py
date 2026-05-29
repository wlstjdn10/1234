import streamlit as st
import requests
from datetime import datetime, timedelta

# --------------------------------
# 기본 설정
# --------------------------------
st.set_page_config(
    page_title="오성고 급식 앱",
    page_icon="🍱",
    layout="centered"
)

# --------------------------------
# 학교 정보
# --------------------------------
API_KEY = "여기에_API_KEY_넣기"

# 대구광역시교육청
ATPT_OFCDC_SC_CODE = "D10"

# 오성고등학교 학교 코드
SD_SCHUL_CODE = "7240454"

# --------------------------------
# 급식 가져오기 함수
# --------------------------------
def get_meal(date):
    url = (
        f"https://open.neis.go.kr/hub/mealServiceDietInfo?"
        f"KEY={API_KEY}"
        f"&Type=json"
        f"&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}"
        f"&SD_SCHUL_CODE={SD_SCHUL_CODE}"
        f"&MLSV_YMD={date}"
    )

    response = requests.get(url)

    try:
        data = response.json()

        row = data["mealServiceDietInfo"][1]["row"][0]

        meal = row["DDISH_NM"]
        calories = row["CAL_INFO"]

        meal = meal.replace("<br/>", "\n")

        return meal, calories

    except:
        return None, None


# --------------------------------
# 제목
# --------------------------------
st.title("🍱 오성고 급식 앱")
st.caption("오늘의 점심 메뉴를 확인하세요!")

# --------------------------------
# 날짜 선택
# --------------------------------
selected_date = st.date_input(
    "날짜 선택",
    datetime.now()
)

formatted_date = selected_date.strftime("%Y%m%d")

# --------------------------------
# 급식 표시
# --------------------------------
meal, calories = get_meal(formatted_date)

if meal:
    st.success("급식 정보를 불러왔어요!")

    st.subheader("📅 날짜")
    st.write(selected_date.strftime("%Y년 %m월 %d일"))

    st.subheader("🍽️ 메뉴")
    st.text(meal)

    st.subheader("🔥 칼로리")
    st.write(calories)

else:
    st.error("급식 정보가 없습니다.")

# --------------------------------
# 이번 주 급식
# --------------------------------
st.divider()
st.subheader("🗓️ 이번 주 급식")

today = datetime.now()

for i in range(5):
    day = today + timedelta(days=i)

    date_str = day.strftime("%Y%m%d")

    meal, _ = get_meal(date_str)

    with st.expander(day.strftime("%m월 %d일")):
        if meal:
            st.text(meal)
        else:
            st.write("급식 없음")
