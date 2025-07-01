import streamlit as st
import json
import math

with open("policies.json", "r") as f:
    policies = json.load(f)

def evaluate_function(expr, x_val):
    try:
        return eval(expr, {"x": x_val, "math": math})
    except Exception:
        return 0.0

def round_cost(value):
    return round(value / 100000) * 100000

st.set_page_config(page_title="Public Policy Cost Dashboard", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
    height: 1000vh;
    width: 1000vw;
    overflow: hidden !important;
    transform: scale(0.8);
    transform-origin: top left;
    padding: 0;
    margin: 0;
}
    @supports (-webkit-touch-callout: none) {
        html, body, [data-testid="stAppViewContainer"] {
            transform: scale(0.8);
            transform-origin: top left;
            width: 125%;
        }
    }
    @supports not (-webkit-touch-callout: none) {
        html, body, [data-testid="stAppViewContainer"] {
            zoom: 80%;
        }
    }
    @media not all and (min-resolution:.001dpcm) {
        @supports (-webkit-appearance:none) {
            html, body, [data-testid="stAppViewContainer"] {
                transform: scale(0.8);
                transform-origin: top left;
                width: 125%;
            }
        }
    }}
        zoom: 80%;
    }
    header > div:first-child, .stDeployButton, .st-emotion-cache-1wbqy5l {
        display: none !important;
    }
    footer, .viewerBadge_link__qRIco, .stActionButton, [data-testid="stStatusWidget"] {
        display: none !important;
    }
    h1 {
        font-size: 40px !important;
        font-weight: 800 !important;
        margin-bottom: 10px;
    }
    .description-text {
        font-size: 16px;
        line-height: 1.6;
        color: #444;
    }
    .policy-section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        position: relative;
        top: 35px;
    }
    .policy-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .cost-text {
        position: relative;
        top: -10px;
        font-size: 20px;
        background-color: #ffecec;
        border: 2px solid #ff4d4d;
        color: #a00000;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }
    .total-box {
        background-color: #fff3f3;
        padding: 30px;
        border-radius: 12px;
        border: 2px solid #ffcccc;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 40px;
    }
    .total-text {
        font-size: 32px;
        color: #a00000;
        font-weight: bold;
    }
    .stSlider > div[data-baseweb="slider"] {
        padding-top: 12px;
        padding-bottom: 12px;
    }
    .stSlider .css-14e1a1c {
        height: 36px !important;
    }
    .stSlider .css-1c5i8h5 {
        width: 16px !important;
        height: 16px !important;
        border-radius: 8px !important;
        background-color: #d22 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    .stSlider .css-1c5i8h5:hover {
        box-shadow: 0 0 0 4px rgba(210, 34, 34, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("Public Policy Cost Dashboard")

st.markdown("""
<div class="description-text">
    Use the interactive sliders below to model projected costs associated with various public policy options.
    Each change dynamically updates the estimated government expenditure.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

cols = st.columns(2)
individual_costs = {}

for i, policy in enumerate(policies):
    col = cols[i % 2]

    with col:
        domain_min = policy["domain_min"]
        domain_max = policy["domain_max"]
        step = policy["step"]

        min_cost = evaluate_function(policy["function"], domain_min)
        max_cost = evaluate_function(policy["function"], domain_max)

        if min_cost == 0:
            start_val = domain_min
        elif max_cost == 0:
            start_val = domain_max
        else:
            start_val = domain_min

        if domain_min > domain_max:
            domain_min, domain_max = domain_max, domain_min
            step = abs(step)

        with st.container():
            st.markdown("<div class='policy-section'>", unsafe_allow_html=True)
            st.markdown(f"<div class='policy-title'>{policy['name']}</div>", unsafe_allow_html=True)

            val = st.slider(
                label="",
                min_value=domain_min,
                max_value=domain_max,
                step=step,
                value=start_val,
                key=f"slider_{i}",
                label_visibility="collapsed"
            )

            cost = evaluate_function(policy["function"], val)
            rounded_cost = round_cost(cost)
            individual_costs[policy["name"]] = rounded_cost

            st.markdown(
                f"<div class='cost-text'>Estimated Cost: <b>${rounded_cost:,.0f}</b></div>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

total_cost = sum(individual_costs.values())

st.markdown(
    f"""
    <div class='total-box'>
        <div class='total-text'>Total Estimated Cost: ${total_cost:,.0f}</div>
    </div>
    """,
    unsafe_allow_html=True
)
