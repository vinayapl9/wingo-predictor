import streamlit as st

st.set_page_config(page_title="Pro Predictor (Max 4-Level Safe Mode)", layout="wide")

# ==========================================================
# 🔢 100% सटीक कलर और साइज मैपिंग
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

# प्री-लोडेड 89 नंबर इतिहास
PRELOADED_NUMS = [
    5, 2, 6, 4, 1, 2, 1, 9, 1, 1, 3, 7, 7, 2, 6, 6, 1, 2, 0, 4, 7, 2, 3, 3, 3, 
    7, 9, 3, 7, 4, 3, 1, 8, 9, 9, 4, 2, 9, 5, 1, 0, 5, 4, 0, 7, 8, 3, 0, 2, 5, 
    5, 7, 3, 5, 2, 3, 2, 6, 3, 8, 1, 9, 3, 7, 6, 4, 8, 0, 1, 8, 2, 4, 7, 7, 2, 
    7, 6, 5, 0, 8, 5, 8, 3, 0, 3, 2, 8, 2, 5
]

# ==========================================================
# 🗂️ सेशन स्टेट
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
    if 'commentary' not in st.session_state: st.session_state.commentary = "सेफ मोड एक्टिव है। अधिकतम रिस्क केवल 4 लेवल तक सीमित है।"

init_state()

def rerun():
    try: st.rerun()
    except AttributeError: st.experimental_rerun()

# ==========================================================
# 🧠 स्ट्रिक्ट रूल इंजन (Max 4-Level Safety Logic के साथ)
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

    # लेवल 4 पर सुरक्षा के लिए स्पेशल डीप इतिहास चेक
    if st.session_state.level == 4:
        # अगर लेवल 4 पर हैं, तो पिछले 3 परिणामों का मजबूत पैटर्न देखा जाएगा
        recent_trend = sizes[-3:]
        if recent_trend.count("Big") >= 2:
            base_pred = "Big"
            rule_used = "सेफ्टी लेवल 4: पिछले रुझान के आधार पर Big को प्राथमिकता दी गई"
        else:
            base_pred = "Small"
            rule_used = "सेफ्टी लेवल 4: पिछले रुझान के आधार पर Small को प्राथमिकता दी गई"
    else:
        # सामान्य नियम (1 से 3 लेवल के लिए)
        if nums[-1] == nums[-2]:
            found = False
            for i in range(len(nums)-2, 0, -1):
                if nums[i] == nums[i-1] and i+1 < len(sizes):
                    base_pred = sizes[i+1]
                    rule_used = f"नियम 6: नंबर {last_num} दोहराया गया (इतिहास के अनुसार '{base_pred}')"
                    found = True
                    break
            if not found:
                base_pred = last_size
                rule_used = "नियम 6: नंबर दोहराव (ट्रेंड फॉलो)"

        elif last_num in [0, 5]:
            found = False
            for i in range(len(nums)-2, -1, -1):
                if nums[i] == last_num and i+1 < len(sizes):
                    base_pred = sizes[i+1]
                    rule_used = f"नियम 5: {last_num} का टर्निंग पॉइंट (इतिहास के अनुसार '{base_pred}')"
                    found = True
                    break
            if not found:
                base_pred = "Small" if last_num == 0 else "Big"
                rule_used = f"नियम 5: {last_num} का डिफ़ॉल्ट नियम"

        elif get_base_color(prev_color) != get_base_color(last_color):
            base_pred = "Small" if last_size == "Big" else "Big"
            rule_used = "नियम 4: कलर चेंज हुआ -> साइज पलट गया"

        elif sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
            base_pred = "Small" if last_size == "Big" else "Big"
            rule_used = "नियम 3: जिग-जैग पैटर्न -> साइज पलट गया"

        elif sizes[-1] == sizes[-2]:
            base_pred = last_size
            rule_used = f"नियम 2: स्ट्रीक पैटर्न -> '{last_size}' फॉलो किया"

        else:
            base_pred = last_size
            rule_used = "डिफ़ॉल्ट: मौजूदा फ्लो फॉलो किया"

    # ==========================================================
    # 🎯 ऑपोज़िट / हाइब्रिड मोड
    # ==========================================================
    if st.session_state.opposite_score > st.session_state.direct_score:
        final_size = "Small" if base_pred == "Big" else "Big"
        mode = "OPPOSITE (उल्टा)"
    else:
        final_size = base_pred
        mode = "DIRECT (सीधा)"

    cands = [n for n in nums[-30:] if num_size(n) == final_size]
    if cands:
        final_num = max(set(cands), key=cands.count)
    else:
        final_num = 7 if final_size == 'Big' else 2
        
    final_color = num_color(final_num)

    return final_size, final_num, final_color, rule_used, mode, base_pred

# ==========================================================
# 🖥️ UI और डैशबोर्ड
# ==========================================================
with st.sidebar:
    st.header("⚙️ सेटिंग्स (Max 4-Level)")
    st.session_state.base_bet = st.number_input("शुरुआती बेट (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    
    st.markdown("---")
    if st.button("🔄 सेशन रीसेट करें", use_container_width=True):
        st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in PRELOADED_NUMS]
        st.session_state.total_pnl = 0.0
        st.session_state.level = 1
        st.session_state.direct_score = 10
        st.session_state.opposite_score = 5
        st.session_state.alert = "✅ सेशन रीसेट हो गया है!"
        rerun()

st.title("🎯 Pro Predictor (Max 4-Level Safe Mode)")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 लाइव प्रिडिक्शन")

    if len(st.session_state.history) >= 3:
        p_size, p_num, p_col, p_rule, p_mode, p_base = strict_rule_engine()
        
        st.session_state.last_pred_size = p_size
        st.session_state.last_base_thought = p_base
        st.session_state.last_mode = p_mode

        box_color = "#17a2b8" if "DIRECT" in p_mode else "#fd7e14"
        # मार्टिंगेल केवल 4 लेवल तक ही कैलकुलेट होगा (Base, Base*2, Base*4, Base*8)
        current_safe_level = min(4, st.session_state.level)
        bet_amt = st.session_state.base_bet * (2 ** (current_safe_level - 1))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">मोड: {p_mode}</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">रंग: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">लेवल {st.session_state.level}/4 (Max Safe) &nbsp;•&nbsp; बेट: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.write(f"**लागू नियम:** {p_rule}")
        st.write(f"**सुरक्षा स्थिति:** अधिकतम लेवल सीमा 4 पर सेट है।")

    st.markdown("### 💬 मेंटोर फीडबैक")
    st.info(st.session_state.commentary)

with col_right:
    st.markdown("### 🔄 नया रिजल्ट दर्ज करें")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    st.write("नंबर चुनें (0-9):")
    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("नया नंबर", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ सबमिट करें", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        current_safe_level = min(4, st.session_state.level)
        bet = st.session_state.base_bet * (2 ** (current_safe_level - 1))

        if st.session_state.last_pred_size is not None:
            if st.session_state.last_base_thought == act_size:
                st.session_state.direct_score = min(20, st.session_state.direct_score + 2)
                st.session_state.opposite_score = max(0, st.session_state.opposite_score - 1)
            else:
                st.session_state.opposite_score = min(20, st.session_state.opposite_score + 3)
                st.session_state.direct_score = max(0, st.session_state.direct_score - 2)

            if act_size == st.session_state.last_pred_size:
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1 # जीतते ही लेवल 1 पर वापस
                st.session_state.commentary = "🎯 शानदार विन! सुरक्षित रूप से लेवल 1 पर रीसेट हो गया है।"
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                
                # --- सख्त 4 लेवल कैप नियम ---
                if st.session_state.level > 4:
                    st.session_state.level = 1 # लेवल 4 पार होते ही बिना बड़ा रिस्क लिए सीधे लेवल 1 पर रीसेट!
                    st.session_state.commentary = "🛡️ सेफ़्टी ट्रिगर: लेवल 4 पार हो गया था! बड़े नुकसान से बचने के लिए लेवल 1 पर रीसेट कर दिया गया है।"
                else:
                    st.session_state.commentary = f"📉 प्रिडिक्शन फेल। सुरक्षित रिकवरी के लिए लेवल {st.session_state.level}/4 सक्रिय।"

        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 100:
            st.session_state.history.pop(0)

        st.session_state.alert = f"✅ दर्ज: #{live_num} ({act_size} / {act_color})"
        rerun()

    st.markdown("### 📊 परफॉरमेंस")
    m1, m2 = st.columns(2)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("सुरक्षित लेवल", f"L-{st.session_state.level}/4")
