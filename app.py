import json
from collections import Counter
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pro AI Predictor v3.1 - Rapid Hybrid", layout="wide")

# ==========================================================
# 🔢 100% सटीक नंबर -> साइज / कलर मैपिंग
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
    return "Violet"

# ==========================================================
# 🗂️ सेशन स्टेट (डेटा और मेमोरी)
# ==========================================================
def init_state():
    defaults = {
        "history": [],          
        "level": 1,
        "base_bet": 10,
        "total_pnl": 0.0,
        "pnl_curve": [],        
        "last_pred_size": None,
        "last_base_thought": None,
        "last_mode": None,
        "last_rule_preds": {},
        "consecutive_fails": 0, # रैपिड-स्विचिंग के लिए नया ट्रैकर
        "correct": 0,
        "total": 0,
        "commentary": "नमस्ते भाई! रैपिड हाइब्रिड एआई सक्रिय है। यह मोड में फंसेगा नहीं, तुरंत पलटी मारेगा।",
        "alert": "",
        "rule_weights": {
            "STREAK_FOLLOWER": 30.0,
            "NUMBER_REPEAT": 28.0,
            "ZIGZAG_PATTERN": 25.0,
            "SMART_COLOR_FLIP": 22.0,
            "ZERO_FIVE_RULE": 20.0,
            "HISTORICAL_PATTERN": 15.0
        },
        "mode_weights": {
            "DIRECT": 30.0,
            "OPPOSITE": 30.0
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
# 🧠 स्मार्ट रूल्स
# ==========================================================
def get_rule_predictions(nums, sizes, colors):
    preds = {}
    if len(sizes) < 3: return preds

    last_size = sizes[-1]
    last_num = nums[-1]

    # 1. स्ट्रीक
    if sizes[-1] == sizes[-2]:
        preds['STREAK_FOLLOWER'] = last_size

    # 2. जिग-जैग
    if sizes[-1] != sizes[-2]:
        preds['ZIGZAG_PATTERN'] = "Small" if last_size == "Big" else "Big"

    # 3. नंबर दोहराव
    if len(nums) >= 2 and nums[-1] == nums[-2]:
        hist_action = last_size
        for i in range(len(nums)-2, 0, -1):
            if nums[i] == nums[i-1] and i+1 < len(sizes):
                hist_action = sizes[i+1]
                break
        preds['NUMBER_REPEAT'] = hist_action

    # 4. स्मार्ट कलर फ्लिप
    pb = base_color(colors[-2])
    cb = base_color(colors[-1])
    if pb != cb:
        hist_action = "Opposite"
        for i in range(len(colors)-2, 0, -1):
            if base_color(colors[i-1]) != base_color(colors[i]):
                hist_action = "Same" if sizes[i] == sizes[i-1] else "Opposite"
                break
        preds['SMART_COLOR_FLIP'] = last_size if hist_action == "Same" else ("Small" if last_size == "Big" else "Big")

    # 5. 0/5 नियम
    if last_num in [0, 5]:
        hist_05_action = "Small" if last_num == 0 else "Big"
        for i in range(len(nums)-2, -1, -1):
            if nums[i] == last_num and i+1 < len(sizes):
                hist_05_action = sizes[i+1]
                break
        preds['ZERO_FIVE_RULE'] = hist_05_action

    # 6. हिस्टोरिकल
    pattern = sizes[-2:]
    hist_follows = [sizes[i+2] for i in range(len(sizes)-2) if sizes[i:i+2] == pattern]
    if hist_follows:
        preds['HISTORICAL_PATTERN'] = max(set(hist_follows), key=hist_follows.count)
    else:
        preds['HISTORICAL_PATTERN'] = "Small" if last_size == "Big" else "Big"

    return preds

# ==========================================================
# 🚀 रैपिड हाइब्रिड एआई इंजन
# ==========================================================
def hybrid_ai_engine():
    history = st.session_state.history
    if len(history) < 3:
        return "Big", 5, "Violet + Green", 90, "DATA_GATHERING", "DIRECT", "Big", "एआई सीख रहा है।"

    nums = [h["number"] for h in history]
    sizes = [h["size"] for h in history]
    colors = [h["color"] for h in history]

    rule_preds = get_rule_predictions(nums, sizes, colors)
    st.session_state.last_rule_preds = rule_preds

    best_rule = "HISTORICAL_PATTERN"
    max_weight = -1
    base_thought = "Big"

    for rule, pred in rule_preds.items():
        w = st.session_state.rule_weights.get(rule, 0)
        if w > max_weight:
            max_weight = w
            best_rule = rule
            base_thought = pred

    # हाइब्रिड डिसीजन (कौन सा मोड ज्यादा मजबूत है?)
    if st.session_state.mode_weights['OPPOSITE'] > st.session_state.mode_weights['DIRECT']:
        final_size = "Small" if base_thought == "Big" else "Big"
        mode = "OPPOSITE"
        stat = f"🔄 रिवर्स हैक: {best_rule} ने '{base_thought}' चुना था, लेकिन मोड के अनुसार '{final_size}' दिया।"
    else:
        final_size = base_thought
        mode = "DIRECT"
        stat = f"✅ सीधा फ्लो: {best_rule} के अनुसार '{base_thought}' ही सही है।"

    conf = min(98, int(85 + (max_weight / 2.5)))

    cands = [n for n in nums[-30:] if num_size(n) == final_size]
    if cands:
        final_num = max(set(cands), key=cands.count)
    else:
        final_num = 7 if final_size == 'Big' else 2
        
    final_color = num_color(final_num)

    return final_size, final_num, final_color, conf, best_rule, mode, base_thought, stat

# ==========================================================
# 🖥️ साइडबार और UI
# ==========================================================
with st.sidebar:
    st.header("⚙️ प्रो सेटिंग्स")
    st.session_state.base_bet = st.number_input("शुरुआती बेट (₹)", min_value=10, value=st.session_state.base_bet, step=10)
    
    st.markdown("---")
    if st.button("🔄 पूरा सेशन रीसेट करें", use_container_width=True):
        init_state()
        st.session_state.history = []
        st.session_state.total_pnl = 0.0
        st.session_state.pnl_curve = []
        st.session_state.alert = "✅ सेशन पूरी तरह रीसेट हो गया है!"
        rerun()

st.title("🎯 Pro Master AI v3.1 - Rapid Switcher")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("### 🤖 एआई लाइव प्रिडिक्शन")

    if len(st.session_state.history) >= 3:
        p_size, p_num, p_col, p_conf, p_rule, p_mode, p_base, p_stat = hybrid_ai_engine()
        
        st.session_state.last_pred_size = p_size
        st.session_state.last_base_thought = p_base
        st.session_state.last_mode = p_mode

        box_color = "#17a2b8" if p_mode == "DIRECT" else "#fd7e14"
        bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447); padding:20px; border-radius:14px; border:3px solid {box_color}; text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:18px;">मोड: {p_mode} | नियम: {p_rule}</h3>
            <h1 style="font-size:48px;margin:10px 0;color:#ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
            <h3 style="margin:0;color:#ffcc00;">रंग: {p_col}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">लेवल {st.session_state.level}/8 &nbsp;•&nbsp; बेट: ₹ {bet_amt}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.progress(p_conf / 100)
        c1, c2 = st.columns(2)
        c1.metric("सटीकता (Confidence)", f"{p_conf}%")
        c2.metric("डायनेमिक मोड", p_mode)
        st.caption(f"**लॉजिक:** {p_stat}")

        with st.expander("🧠 एआई लर्निंग वेट्स (नियमों की ताकत)", expanded=False):
            df_rules = pd.DataFrame(list(st.session_state.rule_weights.items()), columns=["नियम", "स्कोर"]).sort_values("स्कोर", ascending=False)
            st.dataframe(df_rules, use_container_width=True, hide_index=True)
            st.write(f"**स्विचर ट्रैकर:** DIRECT ({st.session_state.mode_weights['DIRECT']:.1f}) | OPPOSITE ({st.session_state.mode_weights['OPPOSITE']:.1f})")

    else:
        st.warning("⚠️ एआई को पैटर्न समझने के लिए कम से कम 3 नंबर दर्ज करें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक")
    st.info(st.session_state.commentary)

    if st.session_state.pnl_curve:
        st.markdown("### 📈 प्रॉफिट / लॉस चार्ट")
        st.line_chart(st.session_state.pnl_curve)

with col_right:
    st.markdown("### 📥 ऐतिहासिक डेटा डालें")
    batch = st.text_area("नंबर कॉमा (,) लगाकर डालें:", height=70, placeholder="जैसे: 5,8,7,2,0,9")
    if st.button("🚀 डेटा प्रोसेस करें", use_container_width=True):
        try:
            raw = [int(x.strip()) for x in batch.split(",") if x.strip().isdigit() and 0 <= int(x.strip()) <= 9]
            if len(raw) >= 3:
                st.session_state.history = []
                for n in raw[-80:]:
                    st.session_state.history.append({"number": n, "size": num_size(n), "color": num_color(n)})
                st.session_state.alert = f"✅ {len(raw)} नंबर लोड हो गए।"
                rerun()
        except Exception:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें (सेल्फ-लर्निंग)")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    st.write("नंबर चुनें:")
    cols = st.columns(5)
    for i in range(10):
        if cols[i%5].button(str(i), key=f"btn_{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input("नया नंबर (0-9)", min_value=0, max_value=9, value=st.session_state.get("pending_num", 0))

    if st.button("✨ नंबर सबमिट करें", type="primary", use_container_width=True):
        act_size = num_size(live_num)
        act_color = num_color(live_num)
        bet = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

        if st.session_state.last_pred_size is not None:
            st.session_state.total += 1
            
            # --- 1. नियम वेट अपडेट ---
            for rule, pred_s in st.session_state.last_rule_preds.items():
                if pred_s == act_size:
                    st.session_state.rule_weights[rule] = min(60.0, st.session_state.rule_weights[rule] + 2.0)
                else:
                    st.session_state.rule_weights[rule] = max(5.0, st.session_state.rule_weights[rule] - 1.5)

            # --- 2. रैपिड-स्विचिंग हाइब्रिड अपडेट ---
            mode_that_was_correct = "DIRECT" if st.session_state.last_base_thought == act_size else "OPPOSITE"
            mode_that_was_wrong = "OPPOSITE" if mode_that_was_correct == "DIRECT" else "DIRECT"

            # जो मोड सही साबित हुआ, उसे रिवॉर्ड दें और फेल काउंटर रीसेट करें
            st.session_state.mode_weights[mode_that_was_correct] = min(60.0, st.session_state.mode_weights[mode_that_was_correct] + 3.0)
            
            if act_size == st.session_state.last_pred_size:
                # यदि एआई की फाइनल प्रिडिक्शन सही थी
                st.session_state.consecutive_fails = 0
                st.session_state.correct += 1
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1
                st.session_state.commentary = f"🎯 शानदार विन! {st.session_state.last_mode} मोड और नियम एकदम सटीक बैठे।"
            else:
                # यदि एआई की फाइनल प्रिडिक्शन फेल हो गई
                st.session_state.consecutive_fails += 1
                st.session_state.total_pnl -= bet
                st.session_state.level += 1
                
                # शार्प पेनाल्टी: जो मोड फेल हुआ है, उसका वेट तेजी से घटाएं
                st.session_state.mode_weights[st.session_state.last_mode] -= 8.0 
                
                # अगर लगातार 2 बार फेल होता है, तो तुरंत फोर्स-स्विच कर दें
                if st.session_state.consecutive_fails >= 2:
                    st.session_state.mode_weights[mode_that_was_correct] += 15.0 # दूसरे मोड को भारी बूस्ट दें
                    st.session_state.consecutive_fails = 0
                    mode_msg = f" ⚠️ लगातार फेलियर के कारण एआई ने मोड को '{mode_that_was_correct}' पर पलट दिया है।"
                else:
                    mode_msg = " एआई ने वेट्स एडजस्ट कर लिए हैं।"

                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.commentary = "⚠️ 8 लेवल पूरे हुए। सुरक्षा के लिए लेवल 1 पर वापस।" + mode_msg
                else:
                    st.session_state.commentary = f"📉 प्रिडिक्शन फेल।" + mode_msg

            # ओवरफ्लो/अंडरफ्लो रोकना
            st.session_state.mode_weights['DIRECT'] = max(5.0, min(60.0, st.session_state.mode_weights['DIRECT']))
            st.session_state.mode_weights['OPPOSITE'] = max(5.0, min(60.0, st.session_state.mode_weights['OPPOSITE']))

        else:
            st.session_state.commentary = "पहला परिणाम दर्ज हुआ। एआई ने ट्रैकिंग शुरू कर दी है।"

        # इतिहास में जोड़ें
        st.session_state.history.append({"number": live_num, "size": act_size, "color": act_color})
        if len(st.session_state.history) > 80:
            st.session_state.history.pop(0)

        st.session_state.pnl_curve.append(round(st.session_state.total_pnl, 2))
        st.session_state.alert = f"✅ दर्ज: #{live_num} ({act_size} / {act_color})"
        rerun()

    st.markdown("### 📊 लाइव स्टैट्स")
    m1, m2, m3 = st.columns(3)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("लेवल", f"L-{st.session_state.level}/8")
    acc = (st.session_state.correct / st.session_state.total * 100) if st.session_state.total else 0
    m3.metric("सटीकता", f"{acc:.1f}%")
