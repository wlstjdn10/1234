import streamlit as st
import requests
from datetime import datetime, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="오성중 급식 앱",
    page_icon="🍱",
    layout="centered"
)

# -----------------------------
# 학교 정보
# -----------------------------
API_KEY = "여기에_발급받은_API_KEY_넣기"

ATPT_OFCDC_SC_CODE = "B10"   # 서울특별시교육청
SD_SCHUL_CODE = "7010536"   # 학교 코드 (예시)

# -----------------------------
# 함수
# -----------------------------
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

        meal = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        calories = data['mealServiceDietInfo'][1]['row'][0]['CAL_INFO']

        meal = meal.replace("<br/>", "\n")

        return meal, calories

    except:
        return None, None


# -----------------------------
# 제목
# -----------------------------
st.title("🍱 오성중 급식 앱")
st.caption("오늘의 점심 메뉴를 확인해보세요!")

# -----------------------------
# 날짜 선택
# -----------------------------
selected_date = st.date_input(
    "날짜 선택",
    datetime.now()
)

formatted_date = selected_date.strftime("%Y%m%d")

# -----------------------------
# 급식 가져오기
# -----------------------------
meal, calories = get_meal(formatted_date)

# -----------------------------
# 화면 출력
# -----------------------------
if meal:
    st.success("급식 정보를 불러왔어요!")

    st.subheader("📅 선택한 날짜")
    st.write(selected_date.strftime("%Y년 %m월 %d일"))

    st.subheader("🍽️ 점심 메뉴")
    st.text(meal)

    st.subheader("🔥 칼로리")
    st.write(calories)

else:
    st.error("급식 정보가 없습니다.")

# -----------------------------
# 주간 급식 보기
# -----------------------------
st.divider()
st.subheader("🗓️ 이번 주 급식")

today = datetime.now()

for i in range(5):
    day = today + timedelta(days=i)
    date_str = day.strftime("%Y%m%d")

    meal, _ = get_meal(date_str)

    with st.expander(day.strftime("%m월 %d일 (%a)")):
        if meal:
            st.text(meal)
        else:
            st.write("급식 없음")
