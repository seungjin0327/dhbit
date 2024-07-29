import streamlit as st
import pandas as pd

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
st.set_page_config(page_title="비트코인 양방향 전략 계산기", layout="wide")

# 세션 상태 초기화
if "initial_price" not in st.session_state:
    st.session_state.initial_price = ""
if "price_range" not in st.session_state:
    st.session_state.price_range = 300
if "first_entry_amount" not in st.session_state:
    st.session_state.first_entry_amount = 300

# 앱 제목
st.title("비트코인 양방향 전략 계산기")

# 레이아웃 설정
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("첫 진입 가격 입력")
    
    # 가격 표시
    st.text_input("첫 진입 가격", value=st.session_state.initial_price, key="price_display", disabled=True)
    
    # 숫자 버튼 생성
    cols = st.columns(3)
    for i in range(9):
        if cols[i % 3].button(str(i + 1), key=f"btn_{i+1}"):
            st.session_state.initial_price += str(i + 1)
    
    # 마지막 줄 버튼
    col1_1, col1_2, col1_3 = st.columns(3)
    if col1_1.button("C"):
        st.session_state.initial_price = ""
    if col1_2.button("0"):
        st.session_state.initial_price += "0"
    if col1_3.button("⌫"):
        st.session_state.initial_price = st.session_state.initial_price[:-1]
    
    if st.button("가격 설정"):
        try:
            initial_price = int(st.session_state.initial_price.replace(",", ""))
            st.session_state.initial_price = f"{initial_price:,}"
            st.success(f"첫 진입 가격이 {st.session_state.initial_price}으로 설정되었습니다.")
        except ValueError:
            st.error("유효한 숫자를 입력해주세요.")

with col2:
    st.subheader("가격 범위 및 포지션 설정")
    
    # 가격 범위 설정
    col2_1, col2_2, col2_3 = st.columns([1,3,1])
    with col2_1:
        if st.button("-", key="minus_button"):
            st.session_state.price_range = max(50, st.session_state.price_range - 50)
    with col2_2:
        st.session_state.price_range = st.number_input("가격 범위 (포인트)", value=st.session_state.price_range, step=50)
    with col2_3:
        if st.button("+", key="plus_button"):
            st.session_state.price_range += 50
    
    # 첫 진입 금액 설정
    st.write("첫 진입 금액")
    col2_4, col2_5, col2_6 = st.columns([1,3,1])
    with col2_4:
        if st.button("-", key="minus_entry_button"):
            st.session_state.first_entry_amount = max(50, st.session_state.first_entry_amount - 50)
    with col2_5:
        st.session_state.first_entry_amount = st.number_input("첫 진입 금액", value=st.session_state.first_entry_amount, step=50)
    with col2_6:
        if st.button("+", key="plus_entry_button"):
            st.session_state.first_entry_amount += 50

    # 첫 진입 포지션 선택
    initial_position = st.selectbox("첫 진입 포지션", ["롱", "숏"])

# 계산 버튼
if st.button("계산", use_container_width=True):
    try:
        initial_price = int(st.session_state.initial_price.replace(",", ""))
        prices, positions = calculate_prices(initial_price, st.session_state.price_range, initial_position)
        entry_amounts = calculate_entry_amounts(st.session_state.first_entry_amount)
        
        df = pd.DataFrame({
            "회차": range(1, 7),
            "포지션": positions,
            "가격": prices,
            "진입금액": entry_amounts
        })
        
        st.success("계산이 성공적으로 완료되었습니다.")
        
        st.dataframe(
            df.style
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

    except ValueError:
        st.error("유효한 가격을 입력해주세요.")

# 사용 방법 안내
st.markdown("""
### 사용 방법:
1. **비트코인 첫 진입 가격**을 계산기 스타일의 입력기를 사용하여 입력하세요.
2. "가격 설정" 버튼을 클릭하여 입력한 가격을 확정하세요.
3. **가격 범위**를 '+' 또는 '-' 버튼을 사용하여 50단위로 조절하세요.
4. **첫 진입 금액**을 설정하세요.
5. **첫 진입 포지션**을 선택하세요. (롱 또는 숏)
6. **계산** 버튼을 클릭하세요.
7. 결과 테이블에서 각 회차별 포지션, 가격, 진입금액을 확인하세요.
""")
