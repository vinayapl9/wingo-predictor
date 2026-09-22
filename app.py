import streamlit as st

st.set_page_config(page_title="Ultimate Pro Predictor (Final)", layout="wide")

# ==========================================================
# 🔢 Niyam 1: 100% Sothik Color ebong Size Mapping
# ==========================================================
NUMBER_MAP = {
    0: ("Small", "Violet + Red"),
    1: ("Small", "Green"),
    2: ("Small", "Red"),
    3: ("Small", "Green"),
    4: ("Small", "Red"),
    5: ("Big",   "Violet + Green"),
    6: ("Big",   "Red"),
    7: ("Big",   "Green"),
    8: ("Big",   "Red"),
    9: ("Big",   "Green"),
}

def num_size(n):  return NUMBER_MAP[n][0]
def num_color(n): return NUMBER_MAP[n][1]

def get_base_color(color_str):
    if "Red" in color_str: return "Red"
    if "Green" in color_str: return "Green"
    return "Unknown"

# Apnar screenshot theke neya 89 ti actual number (Pre-loaded History)
PRELOADED_NUMS = [
    5, 2, 6, 4, 1, 2, 1, 9, 1, 1, 3, 7, 7, 2, 6, 6, 1, 2, 0, 4, 7, 2, 3, 3, 3, 
    7, 9, 3, 7, 4, 3, 1, 8, 9, 9, 4, 2, 9, 5, 1, 0, 5, 4, 0, 7, 8, 3, 0, 2, 5, 
    5, 7, 3, 5, 2, 3, 2, 6, 3, 8, 1, 9, 3, 7, 6, 4, 8, 0, 1, 8, 2, 4, 7, 7, 2, 
    7, 6, 5, 0, 8, 5, 8, 3, 0, 3, 2, 8, 2, 5
]

# ==========================================================
# 🗂️ Session State
# ==========================================================
def init_state():
    if 'history' not in st.session_state:
        st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in PRELOADED_NUMS]
    if 'level' not in st.session_state: st.session_state.level = 1
    if 'base_bet' not in st.session_state: st.session_state.base_bet = 10
    if 'total_pnl' not in st.session_state: st.session_state.total_pnl = 0.0
    if 'last_pred_size' not in st.session_state: st.session_state.last_pred_size = None
    if 'last_base_thought' not in st.session_state: st.session_state.last_base_thought = None
    if 'last_mode' not in st.session_state: st.session_state.last_mode = "DIRECT"
    if 'direct_score' not in st.session_state: st.session_state.direct_score = 10
    if 'opposite_score' not in st.session_state: st.session_state.opposite_score = 5
    if 'alert' not in st.session_state: st.session_state.alert = ""
    if 'commentary' not in st.session_state: st.session_state.commentary = "Script ready. Apnar 89 ti pre-loaded number history te ache."

init_state()

def rerun():
    try: st.rerun()
    except AttributeError: st.experimental_rerun()

# ==========================================================
# 🧠 Strict Rules Engine (Niyam 2 theke 6)
# ==========================================================
def strict_rule_engine():
    history = st.session_state.history
    nums = [h["number"] for h in history]
    sizes = [h["size"] for h in history]
    colors = [h["color"] for h in history]

    last_num = nums[-1]
    last_size = sizes[-1]
    last_color = colors[-1]
    prev_color = colors[-2]

    base_pred = None
    rule_used = ""

    # Niyam 6: Number Repeat
    if nums[-1] == nums[-2]:
        found = False
        for i in range(len(nums)-2, 0, -1):
            if nums[i] == nums[i-1] and i+1 < len(sizes):
                base_pred = sizes[i+1]
                rule_used = f"Niyam 6: Number {last_num} repeat hoyeche (History onujayi '{base_pred}')"
                found = True
                break
        if not found:
            base_pred = last_size
            rule_used = "Niyam 6: Number repeat (Trend follow)"

    # Niyam 5: 0 ba 5 er Turning Point
    elif last_num in [0, 5]:
        found = False
        for i in range(len(nums)-2, -1, -1):
            if nums[i] == last_num and i+1 < len(sizes):
                base_pred = sizes[i+1]
                rule_used = f"Niyam 5: {last_num} er turning point (History onujayi '{base_pred}')"
                found = True
                break
        if not found:
            base_pred = "Small" if last_num == 0 else "Big"
            rule_used = f"Niyam 5: {last_num} er default niyam"

    # Niyam 4: Color Flip (Color Change)
    elif get_base_color(prev_color) != get_base_color(last_color):
        base_pred = "Small" if last_size == "Big" else "Big"
        rule_used = f"Niyam 4: Color change hoyeche -> Size reverse"

    # Niyam 3: Zig-Zag Pattern
    elif sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
        base_pred = "Small" if last_size == "Big" else "Big"
        rule_used = "Niyam 3: Zig-zag pattern -> Size reverse"

    # Niyam 2: Streak (Lagaatar)
    elif sizes[-1] == sizes[-2]:
        base_pred = last_size
        rule_used = f"Niyam 2: Streak pattern -> '{last_size}' k follow kora holo"

    # Default
    else:
        base_pred = last_size
        rule_used = "Default: Current flow k follow kora holo"

    # ==========================================================
    # 🎯 Niyam 7: Direct vs Opposite Hack
    # ==========================================================
    if st.session_state.opposite_score > st.session_state.direct_score:
        final_size = "Small" if base_pred == "Big" else "Big"
        mode = "OPPOSITE (Ulto)"
    else:
        final_size = base_pred
        mode = "DIRECT (Sidha)"

    cands = [n for n in nums[-30:] if num_size(n) == final_size]
    if cands:
        final_num = max(set(cands), key=cands.count)
    else:
        final_num = 7 if final_size == 'Big' else 2
        
    final_color = num_color(final_num)

    return final_size, final_num, final_color, rule_used, mode, base_pred

# ==========================================================
# 🖥️ UI ebong Dashboard
# ==========================================================
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.base_bet = st.number_input("Shuruwati Bet (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    
    st.markdown("---")
    if st.button("🔄 Session Reset Korun", use_container_width=True):
        st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in PRELOADED_NUMS]
        st.session_state.total_pnl = 0.0
        st.session_state.level = 1
        st.session_state.direct_score = 10
        st.session_state.opposite_score = 5
        st.session_state.alert = "✅ Session reset hoyeche (Pre-loaded data abar esheche)!"
        rerun()

st.title("🎯 Ultimate Pro Predictor (Final Script)")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 Live Prediction")

    if len(st.session_state.history) >= 3:
        p_size, p_num, p_col, p_rule, p_mode, p_base = strict_rule_engine()
        
        st.session_state.last_pred_size = p_size
        st.session_state.last_base_thought = p_base
        st.session_state.last_mode = p_mode

        box_color = "#17a2b8" if "DIRECT" in p_mode else "#fd7e14"
        bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">Mode: {p_mode}</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">Color: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">Level {st.session_state.level}/8 &nbsp;•&nbsp; Bet: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.write(f"**Lagu Niyam:** {p_rule}")
        st.write(f"**Score Tracker:** Direct Score ({st.session_state.direct_score}) | Opposite Score ({st.session_state.opposite_score})")

    st.markdown("### 💬 Mentor Feedback")
    st.info(st.session_state.commentary)

with col_right:
    st.markdown("### 🔄 Notun Result Din")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    st.write("Number Select Korun (0-9):")
    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("Notun Number", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ Submit Korun", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        bet = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        if st.session_state.last_pred_size is not None:
            # Mode tracker update
            if st.session_state.last_base_thought == act_size:
                st.session_state.direct_score = min(20, st.session_state.direct_score + 2)
                st.session_state.opposite_score = max(0, st.session_state.opposite_score - 1)
            else:
                st.session_state.opposite_score = min(20, st.session_state.opposite_score + 3) # Ulto k catch korar jonno besi penalty
                st.session_state.direct_score = max(0, st.session_state.direct_score - 2)

            # Win / Loss check
            if act_size == st.session_state.last_pred_size:
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1
                st.session_state.commentary = f"🎯 Shandar win! Game er trend sothik dhorte perechi."
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.commentary = "⚠️ 8 Level puron hoyeche. Level 1 theke abar shuru."
                else:
                    st.session_state.commentary = f"📉 Prediction fail. Mode score update hoyeche."

        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 100:
            st.session_state.history.pop(0)

        st.session_state.alert = f"✅ Submit hoyeche: #{live_num} ({act_size} / {act_color})"
        rerun()

    st.markdown("### 📊 Performance")
    m1, m2 = st.columns(2)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("Level", f"L-{st.session_state.level}/8")
