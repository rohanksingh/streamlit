import streamlit as st    
import numpy as np        

st.set_page_config(page_title="Bond Price-Yield Calculator", layout="centered")
st.title("Bond price vs Yield Calculator")

st.sidebar.header("Bond Parameters")
face_value= st.sidebar.number_input("Face Value ($)", min_value=100, max_value=10000, value=1000, step=100)
coupon_rate= st.sidebar.number_input("Annual Coupon Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)/100
maturity_years = st.sidebar.slider("Year to Maturity", 1,30, 10)
market_yield= st.sidebar.slider("Market Yield to maturity (%)", 0.0, 20.0, 5.0, step=0.1)/100
payment_frequency= st.sidebar.selectbox("Coupon Frequency", ["Annual", "Semi-Annual", "Quartetly"])


# Frequency mapping

freq_map= {"Annual": 1, "Semi-Annual": 2, "Quarterly": 4}
freq= freq_map[payment_frequency]

# Bond Pricing formula

def calculate_bond_price(face, coupon, years, ytm, freq):
    n_periods= years * freq
    coupon_payment= face * coupon /freq
    discount_factors = [(1+ytm/ freq) ** t for t in range(1, n_periods +1)]
    pv_coupons = sum([coupon_payment / df for df in discount_factors])
    pv_face= face / ((1+ ytm /freq) ** n_periods)
    return pv_coupons + pv_face

price= calculate_bond_price(face_value, coupon_rate, maturity_years, market_yield, freq)

st.write("## Bond Price Calculation")
st.metric(label= "Calculated Bond Price", value=f"${price:,.2F}")

st.write("___")
st.write("### Explanation")
st.markdown(f"""
- **Face Value**: ${face_value:,.0f}
- **Coupon Rate**: {coupon_rate * 100:.2f}%
- **Maturity**: {maturity_years} years
- **Market Yield**: {market_yield * 100:.2f}%
- **Coupon Frequency**: {payment_frequency})
> **Note**: As market yield increases, bond price decreases — and vice versa. This app uses discounted cash flow valuation.
""")