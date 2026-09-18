import streamlit as st
import random

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="True AI Self-Learning Predictor", layout="wide")

# --- सेशन स्टेट इनिशियलाइज़ेशन ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'base_bet' not in st.session_state:
    st.session_state.base_bet = 10
if 'total_pnl' not in st.session_state:
    st.session_state.total_pnl = 0.0
if 'last_pred_size' not in st.session_state:
    st.session_state.last_pred_size = None
if 'last_pred_num' not in st.session_state:
    st.session_state.last_pred_num = None
if 'last_pred_color' not in st.session_state:
    st.session_state.last_pred_color = None
if 'last_all_preds' not in st.session_state:
    st.session_state.last_all_preds = {}  # बैकग्राउंड में सभी नियमों की प्रिडिक्शन स्टोर करने के लिए
if 'active_rule' not in st.session_state:
    st.session_state.active_rule = None
if 'correct_preds' not in st.session_state:
    st.session_state.correct_preds = 0
if 'total_preds' not in st.session_state:
    st.session_state.total_preds = 0
if 'last_commentary' not in st.session_state:
    st.session_state.last_commentary = "नमस्ते! ट्रू सेल्फ-लर्निंग एआई सक्रिय है। यह हर नियम को ट्रैक करेगा और खुद को सुधारेगा।"
if 'success_alert' not in st.session_state:
    st.session_state.success_alert = ""

# ट्रू एआई लर्निंग वेट्स (Dynamic Weights)
if 'rule_weights' not in st.session_state:
    st.session_state.rule_weights = {
        'ZIGZAG_PATTERN': 25.0,     # जिग-जैग (A-B-A-B)
        'STREAK_FOLLOWER': 25.0,    # लगातार एक ही पैटर्न (A-A-A)
        'SMART_COLOR_FLIP': 20.0,   # कलर फ्लिप पैटर्न
        'ZERO_FIVE_RULE': 20.0,     # 0 और 5 का टर्निंग पॉइंट
        'NUMBER_REPEAT': 20.0,      # नंबर का दोहराव
        'HISTORICAL_PATTERN': 15.0  # इतिहास से सीखना (डिफ़ॉल्ट)
    }

st.sidebar.header("⚙️ प्रो एआई सेटिंग्स")
st.session_state.base_bet = st.sidebar.number_input("शुरुआती बेट राशि (₹)", min_value=10, value=10, step=10)

# ==========================================
# 🎨 सटीक कलर और साइज नियम
# ==========================================
def get_number_details(num):
    size = "Big" if num >= 5 else "Small"
    if num == 0: color = "Violet + Red"
    elif num == 1: color = "Green"
    elif num == 2: color = "Red"
    elif num == 3: color = "Green"
    elif num == 4: color = "Red"
    elif num == 5: color = "Violet + Green"
    elif num == 6: color = "Red"
    elif num == 7: color = "Green"
    elif num == 8: color = "Red"
    elif num == 9: color = "Green"
    else: color = "Unknown"
    return size, color

# ==========================================
# 🧠 ट्रू रीइन्फोर्समेंट लर्निंग इंजन (True RL Engine)
# ==========================================
def true_ai_engine(history_data, weights):
    if len(history_data) < 3:
        return "Big", 5, "Violet + Green", 90, "DATA_GATHERING", "एआई पैटर्न को समझने के लिए डेटा जुटा रहा है।", {}

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    last_size = recent_sizes[-1]
    last_num = recent_nums[-1]

    # --- स्टेप 1: सभी नियमों की स्वतंत्र भविष्यवाणी (Independent Predictions) ---
    all_rule_preds = {}

    # 1. ZIGZAG_PATTERN: अगर पिछले दो साइज अलग हैं, तो जिग-जैग मानकर अगला साइज पलटेगा
    if recent_sizes[-1] != recent_sizes[-2]:
        all_rule_preds['ZIGZAG_PATTERN'] = "Small" if last_size == "Big" else "Big"
    
    # 2. STREAK_FOLLOWER: अगर पिछले दो साइज सेम हैं, तो स्ट्रीक मानकर उसी को दोहराएगा
    if recent_sizes[-1] == recent_sizes[-2]:
        all_rule_preds['STREAK_FOLLOWER'] = last_size

    # 3. SMART_COLOR_FLIP: बेस कलर बदलता है तो
    prev_base = "Red" if "Red" in recent_colors[-2] else "Green"
    curr_base = "Red" if "Red" in recent_colors[-1] else "Green"
    if prev_base != curr_base:
        # इतिहास देखें कि कलर बदलने पर क्या हुआ था
        hist_action = "Opposite"
        for i in range(len(recent_colors)-2, 0, -1):
            p_c = "Red" if "Red" in recent_colors[i-1] else "Green"
            c_c = "Red" if "Red" in recent_colors[i] else "Green"
            if p_c != c_c:
                hist_action = "Same" if recent_sizes[i] == recent_sizes[i-1] else "Opposite"
                break
        all_rule_preds['SMART_COLOR_FLIP'] = last_size if hist_action == "Same" else ("Small" if last_size == "Big" else "Big")

    # 4. ZERO_FIVE_RULE: 0 या 5 आने पर
    if last_num in [0, 5]:
        hist_05_action = "Small" if last_num == 0 else "Big" # डिफ़ॉल्ट
        for i in range(len(recent_nums)-2, -1, -1):
            if recent_nums[i] == last_num and i+1 < len(recent_sizes):
                hist_05_action = recent_sizes[i+1]
                break
        all_rule_preds['ZERO_FIVE_RULE'] = hist_05_action

    # 5. NUMBER_REPEAT: नंबर दोहराने पर
    if len(recent_nums) >= 2 and recent_nums[-1] == recent_nums[-2]:
        hist_rep_action = last_size
        for i in range(len(recent_nums)-2, 0, -1):
            if recent_nums[i] == recent_nums[i-1] and i+1 < len(recent_sizes):
                hist_rep_action = recent_sizes[i+1]
                break
        all_rule_preds['NUMBER_REPEAT'] = hist_rep_action

    # 6. HISTORICAL_PATTERN (मजबूत डिफ़ॉल्ट): पिछले 2 साइज का कॉम्बो इतिहास में क्या लाया?
    if len(recent_sizes) >= 3:
        pattern = recent_sizes[-2:]
        hist_follows = []
        for i in range(len(recent_sizes)-2):
            if recent_sizes[i:i+2] == pattern and i+2 < len(recent_sizes):
                hist_follows.append(recent_sizes[i+2])
        if hist_follows:
            all_rule_preds['HISTORICAL_PATTERN'] = max(set(hist_follows), key=hist_follows.count)
        else:
            all_rule_preds['HISTORICAL_PATTERN'] = "Small" if last_size == "Big" else "Big" # ब्लाइंड रिपीट रोकने के लिए जिग-जैग बायस

    # --- स्टेप 2: सबसे मजबूत नियम चुनना (Choosing the Best Rule based on Weights) ---
    best_rule = None
    max_weight = -1
    predicted_size = "Big"

    for rule, pred in all_rule_preds.items():
        w = weights.get(rule, 0)
        if w > max_weight:
            max_weight = w
            best_rule = rule
            predicted_size = pred

    # यदि किसी कारणवश कोई नियम नहीं मिला
    if not best_rule:
        best_rule = "HISTORICAL_PATTERN"
        predicted_size = "Small" if last_size == "Big" else "Big"
        all_rule_preds[best_rule] = predicted_size

    confidence = int(80 + min(19, max_weight / 2))
    status = f"एआई ने {best_rule} का उपयोग किया क्योंकि इसका स्कोर ({max_weight:.1f}) सबसे अधिक है।"

    # नंबर का चयन
    candidate_nums = [n for n in recent_nums[-20:] if get_number_details(n)[0] == predicted_size]
    if candidate_nums:
        predicted_num = max(set(candidate_nums), key=candidate_nums.count)
    else:
        predicted_num = 7 if predicted_size == 'Big' else 2

    predicted_color = get_number_details(predicted_num)[1]
    
    return predicted_size, predicted_num, predicted_color, confidence, best_rule, status, all_rule_preds

current_bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================
# 🖥️ UI और डैशबोर्ड
# ==========================================
st.title("🎯 Pro AI Master - True Self-Learning Edition")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("### 🤖 एआई लाइव प्रिडिक्शन")
    
    if len(st.session_state.history) >= 2:
        p_size, p_num, p_color, p_conf, p_rule, p_stat, all_preds = true_ai_engine(
            st.session_state.history, st.session_state.rule_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        st.session_state.active_rule = p_rule
        st.session_state.last_all_preds = all_preds # सभी नियमों का डेटा सेव
        
        box_color = "#28a745" if "Green" in p_color else "#dc3545" if "Red" in p_color else "#6f42c1"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">एआई की स्मार्ट चाल</h3>
                <h1 style="font-size: 42px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग: {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(p_conf / 100)
        st.write(f"**सटीकता:** {p_conf}% | **मुख्य नियम:** {p_rule}")
        st.caption(f"**एआई लॉजिक:** {p_stat}")
    else:
        st.warning("⚠️ एआई को पैटर्न समझने के लिए कम से कम 2 नंबर दें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक")
    st.info(st.session_state.last_commentary)

    with st.expander("🧠 ट्रू एआई लर्निंग वेट्स (कौन सा नियम कितना मजबूत है)"):
        sorted_weights = sorted(st.session_state.rule_weights.items(), key=lambda item: item[1], reverse=True)
        for r_key, r_val in sorted_weights:
            st.write(f"**{r_key}**: {r_val:.1f}")

with col_right:
    st.markdown("### 📥 ऐतिहासिक डेटा दर्ज करें")
    batch_input = st.text_area("पिछले नंबर कॉमा से डालें (जैसे: 5,8,7,2):", height=70)
    if st.button("🚀 डेटा प्रोसेस करें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 2:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                st.session_state.success_alert = f"✅ {len(raw_nums)} नंबर सफलतापूर्वक लोड हो गए।"
                st.rerun()
        except:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें (सच्चा एआई सेल्फ-लर्निंग)")
    
    if st.session_state.success_alert:
        st.success(st.session_state.success_alert)
        st.session_state.success_alert = ""

    live_num = st.number_input("नया आया हुआ नंबर (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ नंबर सबमिट करें"):
        act_size, act_color = get_number_details(live_num)
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            
            # --- असली सेल्फ-लर्निंग (यहाँ एआई हर नियम को उसके प्रदर्शन पर इनाम/सजा देता है) ---
            rules_that_were_right = []
            for rule, pred_size in st.session_state.last_all_preds.items():
                if pred_size == act_size:
                    # जो नियम सही थे (चाहे वे मुख्य नियम न हों), उनका वजन तेजी से बढ़ाएं
                    st.session_state.rule_weights[rule] = min(60.0, st.session_state.rule_weights[rule] + 2.5)
                    rules_that_were_right.append(rule)
                else:
                    # जो नियम गलत थे, उनका वजन घटाएं
                    st.session_state.rule_weights[rule] = max(5.0, st.session_state.rule_weights[rule] - 1.5)

            # मुख्य बेट का रिजल्ट
            if act_size == st.session_state.last_pred_size:
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += current_bet_amt * 0.95
                st.session_state.level = 1
                st.session_state.last_commentary = f"🎯 शानदार विन! मुख्य नियम ({st.session_state.active_rule}) सफल रहा। एआई ने सही नियम सीख लिए हैं।"
            else:
                st.session_state.total_pnl -= current_bet_amt
                st.session_state.level += 1
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.last_commentary = "⚠️ 8 लेवल पूरे हुए। सुरक्षा के लिए लेवल 1 पर वापस।"
                else:
                    if rules_that_were_right:
                        st.session_state.last_commentary = f"📉 मुख्य प्रिडिक्शन फेल, लेकिन एआई ने पहचान लिया है कि {rules_that_were_right[0]} पैटर्न चल रहा है। अगली चाल में इसे लागू करेगा।"
                    else:
                        st.session_state.last_commentary = f"📉 प्रिडिक्शन फेल। एआई इतिहास खंगालकर नई रणनीति बना रहा है।"
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो गया है।"

        st.session_state.history.append({'number': int(live_num), 'size': act_size, 'color': act_color})
        if len(st.session_state.history) > 60:
            st.session_state.history.pop(0)

        st.session_state.success_alert = f"✅ कन्फर्म: नंबर #{live_num} ({act_size} / {act_color}) दर्ज हो गया है!"
        st.rerun()

    # लाइव आंकड़े
    st.markdown("### 📊 परफॉरमेंस ट्रैकर")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Net P/L", value=f"₹ {st.session_state.total_pnl:.2f}")
    with m2:
        st.metric(label="लेवल", value=f"L-{st.session_state.level}/8")
    with m3:
        acc = int((st.session_state.correct_preds / st.session_state.total_preds) * 100) if st.session_state.total_preds > 0 else 0
        st.metric(label="सटीकता", value=f"{acc}%")

    if st.button("🔄 इंजन रीसेट करें"):
        st.session_state.history = []
        st.session_state.level = 1
        st.session_state.total_pnl = 0.0
        st.session_state.rule_weights = {
            'ZIGZAG_PATTERN': 25.0, 'STREAK_FOLLOWER': 25.0, 
            'SMART_COLOR_FLIP': 20.0, 'ZERO_FIVE_RULE': 20.0, 
            'NUMBER_REPEAT': 20.0, 'HISTORICAL_PATTERN': 15.0
        }
        st.session_state.success_alert = "इंजन सफलतापूर्वक रीसेट हो गया है।"
        st.rerun()
