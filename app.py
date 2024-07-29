import streamlit as st
import pandas as pd

# 상수 정의
DEFAULT_PRICE_RANGE = 300
DEFAULT_FIRST_ENTRY_AMOUNT = 300

# 회차별 진입 금액 계산 함수
def calculate_entry_amounts(first_entry):
    return [first_entry, first_entry*2, first_entry*3, first_entry*6, first_entry*8, first_entry*12]

# 가격 계산 함수
def calculate_prices(initial_price, price_range, initial_position):
    prices = [initial_price]
    positions = [initial_position]
    
    for i in range(1, 6):
        if initial_position == "롱":
            price = initial_price if i % 2 == 0 else initial_price - price_range
            position = "롱" if i % 2 == 0 else "숏"
        else:
            price = initial_price if i % 2 == 0 else initial_price + price_range
            position = "숏" if i % 2 == 0 else "롱"
        
        prices.append(round(price))
        positions.append(position)
    
    return prices, positions

# Streamlit 앱 설정
st.set_page_config(page_title="비트코인 양방향 전략", layout="wide")

# 앱 제목
st.title("비트코인 양방향 전략")

# 탭 생성
tab1, tab2 = st.tabs(["입력", "결과"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("가격 설정")
        initial_price = st.number_input("첫 진입 가격", min_value=0, step=100, format="%d", value=10000)
        price_range = st.slider("가격 범위", min_value=50, max_value=1000, value=DEFAULT_PRICE_RANGE, step=50)
    
    with col2:
        st.subheader("진입 설정")
        first_entry_amount = st.number_input("첫 진입 금액", min_value=50, step=50, value=DEFAULT_FIRST_ENTRY_AMOUNT)
        initial_position = st.selectbox("첫 진입 포지션", ["롱", "숏"])

    if st.button("계산", use_container_width=True):
        try:
            prices, positions = calculate_prices(initial_price, price_range, initial_position)
            entry_amounts = calculate_entry_amounts(first_entry_amount)
            
            df = pd.DataFrame({
                "회차": range(1, 7),
                "포지션": positions,
                "가격": prices,
                "진입금액": entry_amounts
            })
            
            st.session_state.result = df
            st.success("계산이 성공적으로 완료되었습니다.")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {str(e)}")

with tab2:
    if 'result' in st.session_state:
        st.dataframe(
            st.session_state.result.style
            .format({
                "가격": "{:,}",
                "진입금액": "{:,}"
            })
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('color', 'black'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('text-align', 'center')]},
            ]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("입력 탭에서 계산을 진행해주세요.")

# 사용 방법 안내
st.markdown("""
### 사용 방법:
1. '입력' 탭에서 **첫 진입 가격**을 입력하세요.
2. **가격 범위**를 슬라이더를 사용하여 조절하세요.
3. **첫 진입 금액**을 설정하세요.
4. **첫 진입 포지션**을 선택하세요. (롱 또는 숏)
5. **계산** 버튼을 클릭하세요.
6. '결과' 탭으로 이동하여 각 회차별 포지션, 가격, 진입금액을 확인하세요.
""")
