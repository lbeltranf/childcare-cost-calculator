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
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
        box-sizing: border-box;
    }
    
    .main > div {
        height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        padding: 1rem !important;
        box-sizing: border-box;
    }
    
    header, footer, .stDeployButton, .st-emotion-cache-1wbqy5l,
    .viewerBadge_link__qRIco, .stActionButton, [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    .title-section {
        flex-shrink: 0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: clamp(24px, 4vw, 36px) !important;
        font-weight: 800 !important;
        margin: 0 0 0.5rem 0 !important;
    }
    
    .description-text {
        font-size: clamp(12px, 1.5vw, 16px);
        line-height: 1.4;
        color: #444;
        margin-bottom: 1rem;
    }
    
    .policies-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }
    
    .policies-grid {
        flex: 1;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        min-height: 0;
    }
    
    .policy-section {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 0;
    }
    
    .policy-title {
        font-size: clamp(14px, 2vw, 18px);
        font-weight: 600;
        margin-bottom: 0.5rem;
        flex-shrink: 0;
    }
    
    .slider-container {
        flex: 1;
        display: flex;
        align-items: center;
        min-height: 40px;
    }
    
    .cost-text {
        font-size: clamp(12px, 1.8vw, 16px);
        background-color: #ffecec;
        border: 2px solid #ff4d4d;
        color: #a00000;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin-top: 0.5rem;
        flex-shrink: 0;
    }
    
    .total-box {
        background-color: #fff3f3;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #ffcccc;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        flex-shrink: 0;
        margin-top: 1rem;
    }
    
    .total-text {
        font-size: clamp(18px, 3vw, 28px);
        color: #a00000;
        font-weight: bold;
        margin: 0;
    }
    
    .stSlider > div[data-baseweb="slider"] {
        padding: 8px 0;
    }
    
    .stSlider .css-14e1a1c {
        height: 28px !important;
    }
    
    .stSlider .css-1c5i8h5 {
        width: 14px !important;
        height: 14px !important;
        border-radius: 7px !important;
        background-color: #d22 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    
    .stSlider .css-1c5i8h5:hover {
        box-shadow: 0 0 0 3px rgba(210, 34, 34, 0.2);
    }
    
    /* Responsive adjustments */
    @media (max-height: 600px) {
        .main > div { padding: 0.5rem !important; }
        .policies-grid { gap: 0.5rem; }
        .policy-section { padding: 0.75rem; }
    }
    
    @media (max-width: 768px) {
        .policies-grid { 
            grid-template-columns: 1fr; 
            gap: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Create layout structure
st.markdown('<div class="title-section">', unsafe_allow_html=True)
st.title("Public Policy Cost Dashboard")
st.markdown("""
<div class="description-text">
    Use the interactive sliders below to model projected costs associated with various public policy options.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main container for policies and total
st.markdown('<div class="policies-container">', unsafe_allow_html=True)

# Create grid layout manually
st.markdown('<div class="policies-grid">', unsafe_allow_html=True)

individual_costs = {}

# Process policies in pairs for grid layout
for i in range(0, len(policies), 2):
    # First policy
    policy1 = policies[i]
    
    domain_min = policy1["domain_min"]
    domain_max = policy1["domain_max"]
    step = policy1["step"]
    
    min_cost = evaluate_function(policy1["function"], domain_min)
    max_cost = evaluate_function(policy1["function"], domain_max)
    
    if min_cost == 0:
        start_val = domain_min
    elif max_cost == 0:
        start_val = domain_max
    else:
        start_val = domain_min
    
    if domain_min > domain_max:
        domain_min, domain_max = domain_max, domain_min
        step = abs(step)
    
    st.markdown('<div class="policy-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="policy-title">{policy1["name"]}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    val1 = st.slider(
        label="",
        min_value=domain_min,
        max_value=domain_max,
        step=step,
        value=start_val,
        key=f"slider_{i}",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    cost1 = evaluate_function(policy1["function"], val1)
    rounded_cost1 = round_cost(cost1)
    individual_costs[policy1["name"]] = rounded_cost1
    
    st.markdown(
        f'<div class="cost-text">Estimated Cost: <b>${rounded_cost1:,.0f}</b></div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Second policy (if exists)
    if i + 1 < len(policies):
        policy2 = policies[i + 1]
        
        domain_min2 = policy2["domain_min"]
        domain_max2 = policy2["domain_max"]
        step2 = policy2["step"]
        
        min_cost2 = evaluate_function(policy2["function"], domain_min2)
        max_cost2 = evaluate_function(policy2["function"], domain_max2)
        
        if min_cost2 == 0:
            start_val2 = domain_min2
        elif max_cost2 == 0:
            start_val2 = domain_max2
        else:
            start_val2 = domain_min2
        
        if domain_min2 > domain_max2:
            domain_min2, domain_max2 = domain_max2, domain_min2
            step2 = abs(step2)
        
        st.markdown('<div class="policy-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="policy-title">{policy2["name"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        val2 = st.slider(
            label="",
            min_value=domain_min2,
            max_value=domain_max2,
            step=step2,
            value=start_val2,
            key=f"slider_{i+1}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        cost2 = evaluate_function(policy2["function"], val2)
        rounded_cost2 = round_cost(cost2)
        individual_costs[policy2["name"]] = rounded_cost2
        
        st.markdown(
            f'<div class="cost-text">Estimated Cost: <b>${rounded_cost2:,.0f}</b></div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close policies-grid

# Total cost section
total_cost = sum(individual_costs.values())

st.markdown(
    f'''
    <div class="total-box">
        <div class="total-text">Total Estimated Cost: ${total_cost:,.0f}</div>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)  # Close policies-container
