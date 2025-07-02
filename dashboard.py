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
    html, body, [data-testid="stAppViewContainer"], .main {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }

    .main > div {
        height: 100vh !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        padding: 1% !important;
        box-sizing: border-box !important;
    }

    header > div:first-child, .stDeployButton, .st-emotion-cache-1wbqy5l,
    footer, .viewerBadge_link__qRIco, .stActionButton, [data-testid="stStatusWidget"] {
        display: none !important;
    }

    h1 {
        font-size: 3vw !important;
        font-weight: 800 !important;
        margin-bottom: 1% !important;
        flex-shrink: 0 !important;
    }

    .description-text {
        font-size: 1.2vw;
        line-height: 1.4;
        color: #444;
        margin-bottom: 2%;
        flex-shrink: 0;
    }

    hr {
        margin: 1% 0 !important;
        flex-shrink: 0 !important;
    }

    .policy-section {
        background-color: #f9f9f9;
        padding: 2%;
        border-radius: 1%;
        box-shadow: 0 0.1% 0.4% rgba(0, 0, 0, 0.05);
        text-align: center;
        position: relative;
        top: 3%;
        height: fit-content;
        margin-bottom: 2%;
    }

    .policy-title {
        font-size: 1.5vw;
        font-weight: 600;
        margin-bottom: 2%;
    }

    .cost-text {
        position: relative;
        top: -1.5%;
        font-size: 1.6vw;
        background-color: #ffecec;
        border: 0.2vw solid #ff4d4d;
        color: #a00000;
        padding: 1% 2%;
        border-radius: 1%;
        font-weight: 600;
        display: inline-block;
        margin-top: 1%;
    }

    .total-box {
        background-color: #fff3f3;
        padding: 3%;
        border-radius: 2%;
        border: 0.2vw solid #ffcccc;
        text-align: center;
        box-shadow: 0 0.2vw 0.8vw rgba(0, 0, 0, 0.1);
        margin-bottom: 0 !important;
        flex-shrink: 0 !important;
    }

    .total-text {
        font-size: 2.5vw;
        color: #a00000;
        font-weight: bold;
    }

    .stSlider > div[data-baseweb="slider"] {
        padding-top: 1.2%;
        padding-bottom: 1.2%;
    }

    .stSlider .css-14e1a1c {
        height: 3% !important;
    }

    .stSlider .css-1c5i8h5 {
        width: 1.5vw !important;
        height: 1.5vw !important;
        border-radius: 50% !important;
        background-color: #d22 !important;
        box-shadow: 0 0.1vw 0.4vw rgba(0,0,0,0.2);
    }

    .stSlider .css-1c5i8h5:hover {
        box-shadow: 0 0 0 0.4vw rgba(210, 34, 34, 0.2);
    }

    div[data-testid="column"] {
        height: fit-content !important;
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
