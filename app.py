import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Pro Volatility Matrix Predictor", layout="wide")

# ==========================================================
# 🔢 100% सटीक नंबर और साइज मैपिंग
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

def base_color(c):
    if "Red" in c: return "Red"
    if "Green" in c: return "Green"
    return "Unknown"

# ==========================================================
# 🗂️ सेशन स्टेट इनिशियलाइज़ेशन
# ==========================================================
def init_state():
    defaults = {
        "history": [],
        "level": 1,
        "base_bet": 10,
        "total_pnl": 0.0,
        "pnl_curve": [],
        "last_pred_size": None,
        "last_pred_num": None,
        "active_indicators": {},
        "correct": 0,
        "total": 0,
        "commentary": "प्रो वोलैटिलिटी मैट्रिक्स इंजन सक्रिय है। यह बाजार के उतार-चढ़ाव को माप रहा है।",
        "alert": "",
        # हर नियम का अपना लाइव स्कोर (Self-Correction Weights)
        "indicator_weights": {
            "STREAK": 25.0,
            "ZIGZAG": 25.0,
            "COLOR_FLIP": 20.0,
            "NUMBER_REPEAT": 20.0,
            "ZERO_FIVE": 15.0
        }
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def rerun():
    try: st.rerun()
    except AttributeError: st.experimental_rerun()

# ==========================================================
# 🧠 एडवांस्ड वोलैटिलिटी और इंडिकेटर इंजन
# ==========================================================
def volatility_matrix_engine():
    history = st.session_state.history
    if len(history) < 3:
        return "Big", 5, "Violet + Green", 50, "बिल्डअप मोड (डाटा कम है)", "Normal"

    nums = [h["number"] for h in history]
    sizes = [h["size"] for h in history]
    colors = [h["color"] for h in history]

    last_size = sizes[-1]
    last_num = nums[-1]

    signals = {}

    # 1. Streak Indicator
    streak_count = 0
    for s in reversed(sizes):
        if s == last_size: streak_count += 1
        else: break
    if streak_count >= 2:
        signals["STREAK"] = (last_size, min(90, 50 + streak_count * 10))

    # 2. Zigzag Indicator
    if sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
        opp_size = "Small" if last_size == "Big" else "Big"
        signals["ZIGZAG"] = (opp_size, 75)

    # 3. Color Flip Indicator
    if len(colors) >= 2 and base_color(colors[-1]) != base_color(colors[-2]):
        opp_size = "Small" if last_size == "Big" else "Big"
        signals["COLOR_FLIP"] = (opp_size, 65)

    # 4. Number Repeat Indicator
    if len(nums) >= 2 and nums[-1] == nums[-2]:
        signals["NUMBER_REPEAT"] = (last_size, 70)

    # 5. Zero / Five Indicator
    if last_num in [0, 5]:
        z_pred = "Small" if last_num == 0 else "Big"
        signals["ZERO_FIVE"] = (z_pred, 60)

    # वोलैटिलिटी (시장 अस्थिरता) कैलकुलेशन
    recent_changes = sum(1 for i in range(1, len(sizes[-10:])) if sizes[-10:][i] != sizes[-10:][i-1])
    volatility = "High (खतरनाक / अस्थिर)" if recent_changes >= 7 else "Normal (सामान्य ट्रेंड)"

    # वेटेड स्कोरिंग सिस्टम (जिंदा स्कोर के आधार पर फैसला)
    big_score = 0.0
    small_score = 0.0
    active_sigs = []

    for ind, (pred_sz, base_conf) in signals.items():
        weight = st.session_state.indicator_weights.get(ind, 10.0)
        score = weight * (base_conf / 100.0)
        active_sigs.append(f"{ind}({pred_sz})")
        if pred_sz == "Big":
            big_score += score
        else:
            small_score += score

    # अगर कोई सिग्नल नहीं मिला तो पिछले ट्रेंड को फॉलो करें
    if not signals:
        final_size = last_size
        confidence = 55
        logic_desc = "कोई मजबूत पैटर्न नहीं — पिछले फ्लो का अनुसरण।"
    else:
        if big_score >= small_score:
            final_size = "Big"
            confidence = int(55 + min(35, (big_score - (small_score or 1)) * 10))
        else:
            final_size = "Small"
            confidence = int(55 + min(35, (small_score - (big_score or 1)) * 10))
        logic_desc = f"सक्रिय इंडिकेटर्स: {', '.join(active_sigs)}"

    # नंबर चयन
    cands = [n for n in nums[-30:] if num_size(n) == final_size]
    if cands:
        final_num = max(set(cands), key=cands.count)
    else:
        final_num = 7 if final_size == 'Big' else 2
    final_color = num_color(final_num)

    st.session_state.active_indicators = signals
    return final_size, final_num, final_color, confidence, logic_desc, volatility

# ==========================================================
# 🖥️ UI और डैशबोर्ड
# ==========================================================
with st.sidebar:
    st.header("⚙️ रिस्क मैनेजमेंट सेटिंग्स")
    st.session_state.base_bet = st.number_input("शुरुआती बेट (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    
    st.markdown("---")
    if st.button("🔄 सेशन रीसेट करें", use_container_width=True):
        init_state()
        st.session_state.history = []
        st.session_state.total_pnl = 0.0
        st.session_state.alert = "✅ सेशन रीसेट हो गया है!"
        rerun()

st.title("🎯 Pro Volatility Matrix Predictor")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 लाइव मैट्रिक्स प्रिडिक्शन")

    if len(st.session_state.history) >= 3:
        p_size, p_num, p_col, p_conf, p_logic, p_vol = volatility_matrix_engine()
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num

        box_color = "#dc3545" if "High" in p_vol else "#28a745"
        bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">मार्केट वोलैटिलिटी: {p_vol}</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">रंग: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">लेवल {st.session_state.level}/8 &nbsp;•&nbsp; सुझाई गई बेट: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.progress(p_conf / 100)
        st.write(f"**सिस्टम कॉन्फिडेंस:** {p_conf}%")
        st.caption(f"**मैट्रिक्स लॉजिक:** {p_logic}")

        with st.expander("📊 इंडिकेटर वेट्स (सेल्फ-लर्निंग स्कोर)", expanded=False):
            df_w = pd.DataFrame(list(st.session_state.indicator_weights.items()), columns=["इंडिकेटर", "स्कोर"]).sort_values("स्कोर", ascending=False)
            st.dataframe(df_w, use_container_width=True, hide_index=True)

    else:
        st.warning("⚠️ विश्लेषण के लिए कम से कम 3 नंबर दर्ज करें।")

    st.markdown("### 💬 मेंटोर फीडबैक और चेतावनियाँ")
    st.info(st.session_state.commentary)

    if st.session_state.pnl_curve:
        st.markdown("### 📈 P/L ग्राफ")
        st.line_chart(st.session_state.pnl_curve)

with col_right:
    st.markdown("### 📥 ऐतिहासिक डेटा दर्ज करें")
    batch = st.text_area("नंबर कॉमा से डालें:", height=70, placeholder="जैसे: 5,8,7,2,0,9")
    if st.button("🚀 डेटा लोड करें", use_container_width=True):
        try:
            raw = [int(x.strip()) for x in batch.split(",") if x.strip().isdigit() and 0 <= int(x.strip()) <= 9]
            if len(raw) >= 3:
                st.session_state.history = [{"number": n, "size": num_size(n), "color": num_color(n)} for n in raw[-80:]]
                st.session_state.alert = f"✅ {len(raw)} नंबर लोड हो गए।"
                rerun()
            else:
                st.error("कम से कम 3 नंबर चाहिए।")
        except:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें (लाइव फीडबैक)")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"mat_btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("नया आया हुआ नंबर (0-9)", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ रिजल्ट सबमिट करें", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        bet = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        if st.session_state.last_pred_size is not None:
            st.session_state.total += 1
            
            # सेल्फ-करेक्शन: जो इंडिकेटर सही थे उनका वजन बढ़ाओ, जो गलत थे उनका घटाओ
            for ind, (pred_sz, _) in st.session_state.active_indicators.items():
                if pred_sz == act_size:
                    st.session_state.indicator_weights[ind] = min(50.0, st.session_state.indicator_weights[ind] + 2.0)
                else:
                    st.session_state.indicator_weights[ind] = max(5.0, st.session_state.indicator_weights[ind] - 2.0)

            if act_size == st.session_state.last_pred_size:
                st.session_state.correct += 1
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1
                st.session_state.commentary = "🎯 शानदार विन! मैट्रिक्स ने सही पैटर्न पकड़ा। लेवल 1 पर रीसेट।"
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.commentary = "⚠️ 8 लेवल पूरे हुए। सुरक्षा के लिए लेवल 1 पर रीसेट कर दिया गया है। थोड़ी देर गेम रोकें।"
                else:
                    st.session_state.commentary = f"📉 प्रिडिक्शन फेल। इंडिकेटर स्कोर रीकैलिब्रेट कर दिए गए हैं। लेवल {st.session_state.level} सक्रिय।"
        else:
            st.session_state.commentary = "पहला रिजल्ट दर्ज हो गया।"

        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 80:
            st.session_state.history.pop(0)

        st.session_state.pnl_curve.append(round(st.session_state.total_pnl, 2))
        st.session_state.alert = f"✅ दर्ज: #{live_num} ({act_size} / {act_color})"
        rerun()

    st.markdown("### 📊 परफॉरमेंस स्टैट्स")
    m1, m2, m3 = st.columns(3)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("लेवल", f"L-{st.session_state.level}/8")
    acc = (st.session_state.correct / st.session_state.total * 100) if st.session_state.total else 0
    m3.metric("सटीकता", f"{acc:.1f}%")
