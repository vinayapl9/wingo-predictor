import streamlit as st

st.set_page_config(page_title="Strict Rule-Based Predictor", layout="wide")

# ==========================================================
# 🔢 नियम 1: 100% सटीक कलर और साइज मैपिंग (आपके अनुसार)
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

# ==========================================================
# 🗂️ सेशन स्टेट (डेटा और मेमोरी)
# ==========================================================
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'base_bet' not in st.session_state: st.session_state.base_bet = 10
if 'total_pnl' not in st.session_state: st.session_state.total_pnl = 0.0
if 'last_pred_size' not in st.session_state: st.session_state.last_pred_size = None
if 'last_base_thought' not in st.session_state: st.session_state.last_base_thought = None
if 'last_mode' not in st.session_state: st.session_state.last_mode = "DIRECT"
if 'direct_score' not in st.session_state: st.session_state.direct_score = 5
if 'opposite_score' not in st.session_state: st.session_state.opposite_score = 5
if 'alert' not in st.session_state: st.session_state.alert = ""
if 'commentary' not in st.session_state: st.session_state.commentary = "नमस्ते! स्ट्रिक्ट रूल इंजन सक्रिय है। यह केवल आपके नियमों पर चलेगा।"

def rerun():
    try: st.rerun()
    except AttributeError: st.experimental_rerun()

# ==========================================================
# 🧠 नियम 2 से 6: स्ट्रिक्ट रूल इंजन (कोई AI फालतू दिमाग नहीं)
# ==========================================================
def strict_rule_engine():
    history = st.session_state.history
    if len(history) < 3:
        return "Big", 5, "Violet + Green", "इतिहास जुटा रहा है...", "DIRECT", "Big"

    nums = [h["number"] for h in history]
    sizes = [h["size"] for h in history]
    colors = [h["color"] for h in history]

    last_num = nums[-1]
    last_size = sizes[-1]
    last_color = colors[-1]
    prev_color = colors[-2]

    base_pred = None
    rule_used = ""

    # नियम 6: नंबर दोहराव (सबसे बड़ी प्राथमिकता)
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
            rule_used = f"नियम 6: नंबर दोहराव (इतिहास नहीं मिला, मौजूदा ट्रेंड लागू)"

    # नियम 5: 0 या 5 का टर्निंग पॉइंट
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
            rule_used = f"नियम 5: {last_num} का डिफ़ॉल्ट नियम लागू"

    # नियम 4: कलर चेंज (कलर फ्लिप)
    elif get_base_color(prev_color) != get_base_color(last_color):
        base_pred = "Small" if last_size == "Big" else "Big"
        rule_used = f"नियम 4: कलर चेंज हुआ ({get_base_color(prev_color)} से {get_base_color(last_color)}) -> साइज पलट गया"

    # नियम 3: जिग-जैग पैटर्न (A-B-A)
    elif sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
        base_pred = "Small" if last_size == "Big" else "Big"
        rule_used = "नियम 3: जिग-जैग पैटर्न डिटेक्ट हुआ -> साइज पलट गया"

    # नियम 2: स्ट्रीक (लगातार पैटर्न)
    elif sizes[-1] == sizes[-2]:
        base_pred = last_size
        rule_used = f"नियम 2: स्ट्रीक पैटर्न -> '{last_size}' लगातार चल रहा है, ट्रेंड फॉलो किया"

    # अगर कोई नियम नहीं लगा
    else:
        base_pred = last_size
        rule_used = "कोई खास नियम नहीं: पिछले रिजल्ट को फॉलो किया"

    # ==========================================================
    # 🎯 नियम 7: ऑपोज़िट / हाइब्रिड हैक (डायरेक्ट vs ऑपोज़िट)
    # ==========================================================
    if st.session_state.opposite_score > st.session_state.direct_score:
        final_size = "Small" if base_pred == "Big" else "Big"
        mode = "OPPOSITE (उल्टा)"
    else:
        final_size = base_pred
        mode = "DIRECT (सीधा)"

    # नंबर चुनना: जो साइज आया है, उसके अनुसार इतिहास से नंबर देना
    cands = [n for n in nums[-20:] if num_size(n) == final_size]
    if cands:
        final_num = max(set(cands), key=cands.count)
    else:
        final_num = 7 if final_size == 'Big' else 2
        
    final_color = num_color(final_num)

    return final_size, final_num, final_color, rule_used, mode, base_pred

# ==========================================================
# 🖥️ UI और सेटिंग्स
# ==========================================================
with st.sidebar:
    st.header("⚙️ सेटिंग्स")
    st.session_state.base_bet = st.number_input("शुरुआती बेट (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    
    st.markdown("---")
    if st.button("🔄 पूरा सेशन रीसेट करें", use_container_width=True):
        st.session_state.history = []
        st.session_state.total_pnl = 0.0
        st.session_state.level = 1
        st.session_state.direct_score = 5
        st.session_state.opposite_score = 5
        st.session_state.alert = "✅ सेशन रीसेट हो गया है!"
        rerun()

st.title("🎯 Strict Rule-Based Predictor (100% आपके नियम)")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 लाइव प्रिडिक्शन")

    if len(st.session_state.history) >= 3:
        p_size, p_num, p_col, p_rule, p_mode, p_base = strict_rule_engine()
        
        st.session_state.last_pred_size = p_size
        st.session_state.last_base_thought = p_base
        st.session_state.last_mode = p_mode

        box_color = "#17a2b8" if p_mode == "DIRECT (सीधा)" else "#fd7e14"
        bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">मोड: {p_mode}</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">रंग: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">लेवल {st.session_state.level}/8 &nbsp;•&nbsp; बेट: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.write(f"**लागू नियम:** {p_rule}")
        st.write(f"**स्कोर ट्रैकर:** सीधा मोड ({st.session_state.direct_score}) | उल्टा मोड ({st.session_state.opposite_score})")

    else:
        st.warning("⚠️ पैटर्न समझने के लिए कम से कम 3 नंबर दर्ज करें।")

    st.markdown("### 💬 अलर्ट और फीडबैक")
    st.info(st.session_state.commentary)


with col_right:
    st.markdown("### 📥 पुराना डेटा डालें (कॉमा लगाकर)")
    batch = st.text_area("", height=70, placeholder="जैसे: 5,8,7,2,0,9")
    if st.button("🚀 डेटा प्रोसेस करें", use_container_width=True):
        try:
            raw = [int(x.strip()) for x in batch.split(",") if x.strip().isdigit() and 0 <= int(x.strip()) <= 9]
            if len(raw) >= 3:
                st.session_state.history = []
                for n in raw[-80:]:
                    st.session_state.history.append({"number": n, "size": num_size(n), "color": num_color(n)})
                st.session_state.alert = f"✅ {len(raw)} नंबर लोड हो गए।"
                rerun()
            else:
                st.error("कम से कम 3 नंबर चाहिए।")
        except Exception:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 नया रिजल्ट दर्ज करें")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    st.write("आया हुआ नंबर चुनें:")
    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("नया नंबर (0-9)", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ सबमिट करें", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        bet = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        if st.session_state.last_pred_size is not None:
            # --- नियम 7: सीधा/उल्टा हैक अपडेट ---
            if st.session_state.last_base_thought == act_size:
                st.session_state.direct_score = min(10, st.session_state.direct_score + 1)
                st.session_state.opposite_score = max(0, st.session_state.opposite_score - 1)
            else:
                st.session_state.opposite_score = min(10, st.session_state.opposite_score + 1)
                st.session_state.direct_score = max(0, st.session_state.direct_score - 1)

            # --- विन/लॉस चेकिंग ---
            if act_size == st.session_state.last_pred_size:
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1
                st.session_state.commentary = f"🎯 शानदार विन! गेम के ट्रेंड को सही पकड़ा। लेवल 1 पर रीसेट।"
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.commentary = "⚠️ 8 लेवल पूरे हुए। लेवल 1 पर वापस।"
                else:
                    st.session_state.commentary = f"📉 प्रिडिक्शन फेल। मोड स्कोर अपडेट हो गया है, अगली चाल तैयार है।"
        else:
            st.session_state.commentary = "पहला परिणाम दर्ज हुआ।"

        # इतिहास में जोड़ें
        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 80:
            st.session_state.history.pop(0)

        st.session_state.alert = f"✅ दर्ज: #{live_num} ({act_size} / {act_color})"
        rerun()

    st.markdown("### 📊 परफॉरमेंस")
    m1, m2 = st.columns(2)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("लेवल", f"L-{st.session_state.level}/8")
