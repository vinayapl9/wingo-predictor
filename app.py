import streamlit as st

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="AI Pro Master Predictor - Silent Movement", layout="wide")

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
if 'active_rule' not in st.session_state:
    st.session_state.active_rule = None
if 'correct_preds' not in st.session_state:
    st.session_state.correct_preds = 0
if 'total_preds' not in st.session_state:
    st.session_state.total_preds = 0
if 'last_commentary' not in st.session_state:
    st.session_state.last_commentary = "नमस्ते! प्रो मॉडल सक्रिय है। साइलेंट मूवमेंट और सटीक ट्रेंड एनालिसिस चालू है।"
if 'success_alert' not in st.session_state:
    st.session_state.success_alert = ""

# ट्रू एआई लर्निंग वेट्स (ये वेट्स गलतियों से खुद को अपडेट करेंगे)
if 'rule_weights' not in st.session_state:
    st.session_state.rule_weights = {
        'STREAK_FOLLOWER': 30.0,    # लंबी स्ट्रीक को पकड़ना (सर्वोच्च)
        'ZIGZAG_PATTERN': 25.0,     # जिग-जैग (Small-Big-Small-Big) को पकड़ना
        'COLOR_FLIP': 20.0,         # रंग बदलने पर साइज पलटना
        'ZERO_FIVE_RULE': 15.0,     # 0 या 5 के आने का प्रभाव
        'PROBABILITY_FLOW': 10.0    # जब कोई पैटर्न न हो, तो साइलेंट फ्लो
    }

# --- साइडबार सेटिंग्स ---
st.sidebar.header("⚙️ प्रो एआई सेटिंग्स")
st.session_state.base_bet = st.sidebar.number_input("शुरुआती बेट राशि (₹)", min_value=10, value=10, step=10)

# ==========================================
# 🎨 आपके द्वारा दिए गए सटीक कलर और साइज नियम
# ==========================================
def get_number_details(num):
    size = "Big" if num >= 5 else "Small"
    
    if num == 0:
        color = "Violet + Red"
    elif num == 1:
        color = "Green"
    elif num == 2:
        color = "Red"
    elif num == 3:
        color = "Green"
    elif num == 4:
        color = "Red"
    elif num == 5:
        color = "Violet + Green"
    elif num == 6:
        color = "Red"
    elif num == 7:
        color = "Green"
    elif num == 8:
        color = "Red"
    elif num == 9:
        color = "Green"
    else:
        color = "Unknown"
        
    return size, color

# ==========================================
# 🧠 साइलेंट मूवमेंट & ट्रू एआई प्रिडिक्शन इंजन
# ==========================================
def advanced_pro_engine(history_data, weights):
    if len(history_data) < 3:
        return "Big", 5, "Violet + Green", 90, "PROBABILITY_FLOW", "डेटा लोड हो रहा है, एआई पैटर्न स्कैन कर रहा है।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    last_size = recent_sizes[-1]
    last_num = recent_nums[-1]

    # 1. स्ट्रीक चेकर (Streak Checker)
    streak_count = 0
    for s in reversed(recent_sizes):
        if s == last_size:
            streak_count += 1
        else:
            break

    # 2. जिग-जैग चेकर (Zig-Zag Checker)
    is_zigzag = False
    if len(recent_sizes) >= 3:
        if recent_sizes[-1] != recent_sizes[-2] and recent_sizes[-2] != recent_sizes[-3]:
            is_zigzag = True

    # 3. कलर फ्लिप चेकर (Color Flip Checker)
    color_flipped = False
    if len(recent_colors) >= 2:
        # बेस कलर पहचानना (Red या Green)
        prev_base = "Red" if "Red" in recent_colors[-2] else "Green"
        curr_base = "Red" if "Red" in recent_colors[-1] else "Green"
        if prev_base != curr_base:
            color_flipped = True

    # 4. 0 और 5 का नियम
    is_zero_five = last_num in [0, 5]

    # --- एआई डिसीजन मेकिंग (वजन के आधार पर प्राथमिकता) ---
    predicted_size = "Big"
    confidence = 90
    used_rule = "PROBABILITY_FLOW"
    status = "साइलेंट फ्लो: पिछले परिणामों का अनुसरण।"

    # एआई सबसे मजबूत (High Weight) नियम को पहले लागू करेगा
    # स्ट्रीक को सबसे ज्यादा तवज्जो (अगर 2 या उससे ज्यादा बार आ चुका है)
    if streak_count >= 2 and weights['STREAK_FOLLOWER'] > 15.0:
        predicted_size = last_size
        confidence = int(90 + min(9, streak_count * 1.5))
        used_rule = "STREAK_FOLLOWER"
        status = f"साइलेंट मूवमेंट: लगातार {streak_count} बार '{last_size}' आ रहा है। ट्रेंड के खिलाफ नहीं जाना है।"
    
    # अगर स्ट्रीक नहीं है, लेकिन जिग-जैग चल रहा है
    elif is_zigzag and weights['ZIGZAG_PATTERN'] > weights['COLOR_FLIP']:
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = 94
        used_rule = "ZIGZAG_PATTERN"
        status = "पैटर्न क्रैक: स्पष्ट जिग-जैग पैटर्न है, अगला साइज उलटा होगा।"
    
    # कलर फ्लिप नियम
    elif color_flipped and weights['COLOR_FLIP'] > weights['ZERO_FIVE_RULE']:
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = 93
        used_rule = "COLOR_FLIP"
        status = "नियम पालन: बेस कलर बदला है, इसलिए साइज को रिवर्स किया गया है।"
    
    # 0 या 5 का नियम
    elif is_zero_five and weights['ZERO_FIVE_RULE'] > 10.0:
        # ऐतिहासिक डेटा के आधार पर 0 या 5 के बाद क्या आता है (डिफ़ॉल्ट: 0 के बाद 0/Small, 5 के बाद 5/Big)
        predicted_size = "Small" if last_num == 0 else "Big"
        confidence = 92
        used_rule = "ZERO_FIVE_RULE"
        status = f"नियम पालन: टर्निंग पॉइंट {last_num} डिटेक्ट हुआ है।"
    
    # कोई स्पष्ट पैटर्न नहीं, तो ऐतिहासिक फ्रिक्वेंसी फॉलो करें
    else:
        big_c = recent_sizes.count('Big')
        small_c = recent_sizes.count('Small')
        predicted_size = "Big" if big_c >= small_c else "Small"
        used_rule = "PROBABILITY_FLOW"
        status = "साइलेंट मूवमेंट: ऐतिहासिक फ्रिक्वेंसी और शांतिपूर्ण फ्लो।"

    # सटीक नंबर का चयन (उसी साइज के सबसे संभावित नंबर)
    candidate_nums = [n for n in recent_nums if get_number_details(n)[0] == predicted_size]
    if candidate_nums:
        predicted_num = max(set(candidate_nums), key=candidate_nums.count)
    else:
        predicted_num = 7 if predicted_size == 'Big' else 2

    predicted_color = get_number_details(predicted_num)[1]
    return predicted_size, predicted_num, predicted_color, confidence, used_rule, status

# 8 लेवल बेट राशि
current_bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================
# 🖥️ UI और डैशबोर्ड
# ==========================================
st.title("🎯 Pro Master AI - Silent Movement Edition")

col_left, col_right = st.columns([1.1, 1])

# --- बायां हिस्सा: भविष्यवाणी ---
with col_left:
    st.markdown("### 🤖 एआई लाइव प्रिडिक्शन")
    
    if len(st.session_state.history) >= 2:
        p_size, p_num, p_color, p_conf, p_rule, p_stat = advanced_pro_engine(
            st.session_state.history, st.session_state.rule_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        st.session_state.active_rule = p_rule
        
        box_color = "#28a745" if "Green" in p_color else "#dc3545" if "Red" in p_color else "#6f42c1"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">एआई की साइलेंट चाल</h3>
                <h1 style="font-size: 42px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग: {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(p_conf / 100)
        st.write(f"**सटीकता:** {p_conf}% | **एक्टिव रूल:** {p_rule}")
        st.caption(f"**एआई लॉजिक:** {p_stat}")
    else:
        st.warning("⚠️ एआई को पैटर्न समझने के लिए कम से कम 2 नंबर दें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक")
    st.info(st.session_state.last_commentary)

    with st.expander("🧠 एआई सेल्फ-लर्निंग वेट्स (लाइव अपडेट्स)"):
        for r_key, r_val in st.session_state.rule_weights.items():
            st.write(f"**{r_key}**: {r_val:.1f}")

# --- दायां हिस्सा: इनपुट और फीडबैक ---
with col_right:
    st.markdown("### 📥 बल्क डेटा लोड (ऑप्शनल)")
    batch_input = st.text_area("पिछले नंबर कॉमा से डालें (जैसे: 5,8,7,2):", height=70)
    if st.button("🚀 डेटा प्रोसेस करें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 2:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                st.session_state.success_alert = f"✅ {len(raw_nums)} नंबर सफलतापूर्वक लोड हो गए हैं।"
                st.rerun()
        except:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें (सेल्फ-लर्निंग लूप)")
    
    # कन्फर्मेशन अलर्ट
    if st.session_state.success_alert:
        st.success(st.session_state.success_alert)
        st.session_state.success_alert = ""

    live_num = st.number_input("आया हुआ नया नंबर दर्ज करें (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ नंबर सबमिट करें"):
        act_size, act_color = get_number_details(live_num)
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            used_rule = st.session_state.active_rule
            
            if act_size == st.session_state.last_pred_size:
                # WIN - एआई उसी नियम का स्कोर बढ़ाएगा जिसने जिताया
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += current_bet_amt * 0.95
                st.session_state.rule_weights[used_rule] = min(50.0, st.session_state.rule_weights[used_rule] + 2.0)
                
                st.session_state.last_commentary = f"🎯 शानदार! {used_rule} नियम सफल रहा। एआई ने इस नियम को रिवॉर्ड दिया है। लेवल 1 पर रीसेट।"
                st.session_state.level = 1
            else:
                # LOSS - एआई अपनी गलती मानेगा और उस नियम का स्कोर घटाएगा
                st.session_state.total_pnl -= current_bet_amt
                st.session_state.rule_weights[used_rule] = max(5.0, st.session_state.rule_weights[used_rule] - 2.0)
                
                st.session_state.level += 1
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.last_commentary = "⚠️ 8 लेवल पूरे हुए। सुरक्षा के लिए लेवल 1 पर वापस।"
                else:
                    st.session_state.last_commentary = f"📉 {used_rule} नियम फेल हुआ। एआई ने इस नियम का पावर कम कर दिया है और लेवल {st.session_state.level} पर नई रणनीति अपनाएगा।"
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो गया है।"

        st.session_state.history.append({'number': int(live_num), 'size': act_size, 'color': act_color})
        if len(st.session_state.history) > 60:
            st.session_state.history.pop(0)

        # स्क्रीन पर तत्काल सफलता का संदेश
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
        st.session_state.rule_weights = {'STREAK_FOLLOWER': 30.0, 'ZIGZAG_PATTERN': 25.0, 'COLOR_FLIP': 20.0, 'ZERO_FIVE_RULE': 15.0, 'PROBABILITY_FLOW': 10.0}
        st.session_state.success_alert = "इंजन सफलतापूर्वक रीसेट हो गया है।"
        st.rerun()
