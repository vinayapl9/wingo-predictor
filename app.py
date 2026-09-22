import streamlit as st
from collections import Counter

st.set_page_config(page_title="Adaptive Momentum Predictor", layout="wide")

# ==========================================================
# 🔢 Number Mapping
# ==========================================================
NUMBER_MAP = {
    0: ("Small", "Violet + Red"), 1: ("Small", "Green"),
    2: ("Small", "Red"), 3: ("Small", "Green"),
    4: ("Small", "Red"), 5: ("Big", "Violet + Green"),
    6: ("Big", "Red"), 7: ("Big", "Green"),
    8: ("Big", "Red"), 9: ("Big", "Green"),
}
def num_size(n): return NUMBER_MAP[n][0]
def num_color(n): return NUMBER_MAP[n][1]

# User ke naye 98 real numbers ka data (A11 se A20)
REAL_DATA = [
    2, 9, 2, 5, 1, 9, 4, 8, 6, 4, 3, 4, 9, 5, 7, 6, 8, 5, 8, 7, 7, 2, 0, 2, 1, 5, 
    2, 1, 6, 1, 3, 8, 9, 9, 6, 7, 3, 4, 7, 0, 3, 5, 9, 6, 0, 1, 9, 6, 2, 8, 8, 3, 
    1, 2, 5, 2, 7, 0, 4, 9, 0, 8, 8, 7, 1, 7, 6, 2, 6, 5, 1, 2, 6, 3, 4, 0, 2, 7, 
    9, 3, 7, 1, 4, 2, 7, 6, 4, 1, 0, 9, 3, 0, 3, 0, 9, 4, 9, 4
]

def init_state():
    if 'history' not in st.session_state:
        st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in REAL_DATA]
    if 'level' not in st.session_state: st.session_state.level = 1
    if 'base_bet' not in st.session_state: st.session_state.base_bet = 10
    if 'total_pnl' not in st.session_state: st.session_state.total_pnl = 0.0
    if 'last_pred_size' not in st.session_state: st.session_state.last_pred_size = None
    if 'alert' not in st.session_state: st.session_state.alert = ""

init_state()

# ==========================================================
# 🧠 Adaptive Momentum Engine (Works in all conditions)
# ==========================================================
def adaptive_engine():
    history = st.session_state.history
    sizes = [h["size"] for h in history]
    nums = [h["number"] for h in history]
    
    if len(sizes) < 5:
        return "Big", 5, "Violet + Green", "Need more data..."

    last_size = sizes[-1]
    
    # Check Trend Strength
    trend_count = 0
    for s in reversed(sizes):
        if s == last_size: trend_count += 1
        else: break
        
    # Check Chop (ZigZag) Strength
    chop_count = 0
    for i in range(1, min(6, len(sizes))):
        if sizes[-i] != sizes[-(i+1)]: chop_count += 1
        else: break

    # Logic Decision
    if chop_count >= 2:
        final_size = "Small" if last_size == "Big" else "Big"
        logic_used = f"Choppy Market Detected ({chop_count} flips). Betting on Reversal."
    elif trend_count >= 2:
        final_size = last_size
        logic_used = f"Strong Trend Detected ({trend_count} in a row). Following Momentum."
    else:
        # Fallback: Check last 10 frequency
        recent_10 = sizes[-10:]
        counts = Counter(recent_10)
        final_size = "Big" if counts["Big"] >= counts["Small"] else "Small"
        logic_used = "No clear pattern. Following recent highest frequency."

    # Number Pick
    cands = [n for n in nums[-40:] if num_size(n) == final_size]
    final_num = max(set(cands), key=cands.count) if cands else (7 if final_size == 'Big' else 2)
    final_color = num_color(final_num)

    return final_size, final_num, final_color, logic_used

# ==========================================================
# 🖥️ User Interface
# ==========================================================
with st.sidebar:
    st.header("⚙️ Settings (Max 4-Level)")
    st.session_state.base_bet = st.number_input("Base Bet (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    if st.button("🔄 Hard Reset", use_container_width=True):
        st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in REAL_DATA]
        st.session_state.total_pnl = 0.0
        st.session_state.level = 1
        st.session_state.alert = "✅ Naye 98 numbers ke sath session reset ho gaya!"
        st.rerun()

st.title("🎯 Ultimate Adaptive Predictor (Any Condition)")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 Live Engine")
    if len(st.session_state.history) >= 5:
        p_size, p_num, p_col, p_logic = adaptive_engine()
        st.session_state.last_pred_size = p_size
        
        current_safe_level = min(4, st.session_state.level)
        bet_amt = st.session_state.base_bet * (2 ** (current_safe_level - 1))
        
        box_color = "#17a2b8" if p_size == "Big" else "#fd7e14"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">Next Target</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">Color: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">Level {current_safe_level}/4 (Safe Mode) &nbsp;•&nbsp; Bet: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)
        st.info(f"**Current Market Logic:** {p_logic}")
    else:
        st.warning("Gathering data...")

with col_right:
    st.markdown("### 🔄 Enter Result")
    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("Number Input", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ Submit", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        current_safe_level = min(4, st.session_state.level)
        bet = st.session_state.base_bet * (2 ** (current_safe_level - 1))

        if st.session_state.last_pred_size:
            if act_size == st.session_state.last_pred_size:
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1 
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                if st.session_state.level > 4:
                    st.session_state.level = 1 

        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 150:
            st.session_state.history.pop(0)

        st.session_state.alert = f"✅ Added: #{live_num} ({act_size})"
        st.rerun()

    st.markdown("### 📊 Live Performance")
    m1, m2 = st.columns(2)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("Current Level", f"L-{min(4, st.session_state.level)}/4")
