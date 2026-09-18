import streamlit as st

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="AI Pro Master Predictor - Smart History Edition", layout="wide")

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
    st.session_state.last_commentary = "नमस्ते! प्रो मॉडल सक्रिय है। स्मार्ट कलर-फ्लिप और नंबर रिपीटेशन डिटेक्टर चालू है।"
if 'success_alert' not in st.session_state:
    st.session_state.success_alert = ""
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

# ट्रू एआई लर्निंग वेट्स (DEFAULT_FLOW शामिल किया गया है)
if 'rule_weights' not in st.session_state:
    st.session_state.rule_weights = {
        'NUMBER_REPEAT': 32.0,      
        'STREAK_FOLLOWER': 28.0,    
        'SMART_COLOR_FLIP': 22.0,   
        'ZIGZAG_PATTERN': 18.0,     
        'ZERO_FIVE_RULE': 15.0,      
        'DEFAULT_FLOW': 10.0        # KeyError से बचने के लिए इसे जोड़ा गया है
    }

# --- साइडबार सेटिंग्स ---
st.sidebar.header("⚙️ प्रो एआई सेटिंग्स")
st.session_state.base_bet = st.sidebar.number_input("शुरुआती बेट राशि (₹)", min_value=10, value=10, step=10)
enable_voice = st.sidebar.checkbox("देवनागरी बोलकर घोषणा सुनें", value=True)
enable_sound = st.sidebar.checkbox("स्पेशल विन/लॉस साउंड इफेक्ट्स", value=True)

# ==========================================
# 🎨 सटीक कलर और साइज नियम
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
# 🧠 एडवांस्ड हिस्टोरिकल प्रिडिक्शन इंजन
# ==========================================
def smart_history_engine(history_data, weights):
    if len(history_data) < 3:
        return "Big", 5, "Violet + Green", 90, "DATA_GATHERING", "एआई पैटर्न को समझने के लिए डेटा जुटा रहा है।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    last_size = recent_sizes[-1]
    last_num = recent_nums[-1]

    # 1. नंबर रिपीटेशन
    is_num_repeat = False
    repeat_hist_action = "Same"
    if len(recent_nums) >= 2 and recent_nums[-1] == recent_nums[-2]:
        is_num_repeat = True
        for i in range(len(recent_nums)-2, 0, -1):
            if recent_nums[i] == recent_nums[i-1]:
                if i+1 < len(recent_sizes):
                    repeat_hist_action = "Same" if recent_sizes[i+1] == recent_sizes[i] else "Opposite"
                break

    # 2. स्मार्ट कलर फ्लिप
    color_flipped = False
    color_flip_hist_action = "Opposite"
    if len(recent_colors) >= 2:
        prev_base = "Red" if "Red" in recent_colors[-2] else "Green"
        curr_base = "Red" if "Red" in recent_colors[-1] else "Green"
        if prev_base != curr_base:
            color_flipped = True
            for i in range(len(recent_colors)-2, 0, -1):
                p_c = "Red" if "Red" in recent_colors[i-1] else "Green"
                c_c = "Red" if "Red" in recent_colors[i] else "Green"
                if p_c != c_c:
                    if recent_sizes[i] == recent_sizes[i-1]:
                        color_flip_hist_action = "Same"
                    else:
                        color_flip_hist_action = "Opposite"
                    break

    # 3. स्ट्रीक चेकर
    streak_count = 0
    for s in reversed(recent_sizes):
        if s == last_size:
            streak_count += 1
        else:
            break

    # 4. जिग-जैग चेकर
    is_zigzag = False
    if len(recent_sizes) >= 3:
        if recent_sizes[-1] != recent_sizes[-2] and recent_sizes[-2] != recent_sizes[-3]:
            is_zigzag = True

    # --- एआई डिसीजन मेकिंग ---
    predicted_size = "Big"
    confidence = 90
    used_rule = "DEFAULT_FLOW"
    status = "शांत प्रवाह: एआई पिछले रुझानों का विश्लेषण कर रहा है।"

    if is_num_repeat and weights.get('NUMBER_REPEAT', 0) > 15.0:
        predicted_size = last_size if repeat_hist_action == "Same" else ("Small" if last_size == "Big" else "Big")
        confidence = 96
        used_rule = "NUMBER_REPEAT"
        status = f"सुपर क्रैक: नंबर {last_num} रिपीट हुआ है! इतिहास के अनुसार एआई ने '{repeat_hist_action}' पैटर्न चुना है।"
    
    elif streak_count >= 3 and weights.get('STREAK_FOLLOWER', 0) > weights.get('SMART_COLOR_FLIP', 0):
        predicted_size = last_size
        confidence = int(90 + min(9, streak_count * 1.5))
        used_rule = "STREAK_FOLLOWER"
        status = f"साइलेंट मूवमेंट: {streak_count} बार '{last_size}' आ चुका है, स्ट्रीक को टूटने नहीं देना है।"
    
    elif color_flipped and weights.get('SMART_COLOR_FLIP', 0) > weights.get('ZIGZAG_PATTERN', 0):
        predicted_size = last_size if color_flip_hist_action == "Same" else ("Small" if last_size == "Big" else "Big")
        confidence = 94
        used_rule = "SMART_COLOR_FLIP"
        status = f"स्मार्ट क्रैक: कलर बदला है! इतिहास बताता है कि इस स्थिति में साइज '{color_flip_hist_action}' रहता है।"
    
    elif is_zigzag and weights.get('ZIGZAG_PATTERN', 0) > weights.get('ZERO_FIVE_RULE', 0):
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = 93
        used_rule = "ZIGZAG_PATTERN"
        status = "पैटर्न क्रैक: जिग-जैग चल रहा है, अगला साइज रिवर्स होगा।"
    
    elif last_num in [0, 5] and weights.get('ZERO_FIVE_RULE', 0) > 10.0:
        predicted_size = "Small" if last_num == 0 else "Big"
        confidence = 91
        used_rule = "ZERO_FIVE_RULE"
        status = f"टर्निंग पॉइंट: {last_num} के बाद ऐतिहासिक नियम लागू किया गया है।"
    
    else:
        predicted_size = last_size
        status = "कंटिन्यूएशन: मौजूदा फ्लो को बनाए रखा गया है।"

    # सटीक नंबर का चयन
    candidate_nums = [n for n in recent_nums if get_number_details(n)[0] == predicted_size]
    if candidate_nums:
        predicted_num = max(set(candidate_nums), key=candidate_nums.count)
    else:
        predicted_num = 7 if predicted_size == 'Big' else 2

    predicted_color = get_number_details(predicted_num)[1]
    return predicted_size, predicted_num, predicted_color, confidence, used_rule, status

current_bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================
# 🖥️ UI और डैशबोर्ड
# ==========================================
st.title("🎯 Pro Master AI - Smart History & Repeat Edition")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("### 🤖 एआई लाइव प्रिडिक्शन")
    
    if len(st.session_state.history) >= 2:
        p_size, p_num, p_color, p_conf, p_rule, p_stat = smart_history_engine(
            st.session_state.history, st.session_state.rule_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        st.session_state.active_rule = p_rule
        
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
        st.write(f"**सटीकता:** {p_conf}% | **एक्टिव रूल:** {p_rule}")
        st.caption(f"**एआई लॉजिक:** {p_stat}")
    else:
        st.warning("⚠️ एआई को पैटर्न समझने के लिए कम से कम 2 नंबर दें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक")
    st.info(st.session_state.last_commentary)

    with st.expander("🧠 एआई लर्निंग वेट्स (लाइव अपडेट्स)"):
        for r_key, r_val in st.session_state.rule_weights.items():
            st.write(f"**{r_key}**: {r_val:.1f}")

    # जावास्क्रिप्ट स्पीच/साउंड
    js_code = ""
    if enable_sound and st.session_state.sound_trigger:
        if st.session_state.sound_trigger == 'win':
            js_code += "try { const ctx = new (window.AudioContext || window.webkitAudioContext)(); const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.type = 'triangle'; osc.frequency.setValueAtTime(523.25, ctx.currentTime); osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1); gain.gain.setValueAtTime(0.2, ctx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5); osc.connect(gain); gain.connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime + 0.5); } catch(e) {}"
        elif st.session_state.sound_trigger == 'loss':
            js_code += "try { const ctx = new (window.AudioContext || window.webkitAudioContext)(); const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.type = 'sawtooth'; osc.frequency.setValueAtTime(220, ctx.currentTime); osc.frequency.setValueAtTime(185, ctx.currentTime + 0.15); gain.gain.setValueAtTime(0.2, ctx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4); osc.connect(gain); gain.connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime + 0.4); } catch(e) {}"
        st.session_state.sound_trigger = None

    if enable_voice and st.session_state.speak_text:
        clean_text = st.session_state.speak_text.replace("'", "").replace('"', "")
        js_code += f"if ('speechSynthesis' in window) {{ window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'hi-IN'; msg.rate = 0.95; window.speechSynthesis.speak(msg); }}"
        st.session_state.speak_text = ""

    if js_code:
        st.components.v1.html(f"<script>{js_code}</script>", height=0)

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
                st.session_state.success_alert = f"✅ {len(raw_nums)} नंबर सफलतापूर्वक लोड हो गए हैं।"
                st.rerun()
        except:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें (सेल्फ-लर्निंग)")
    
    if st.session_state.success_alert:
        st.success(st.session_state.success_alert)
        st.session_state.success_alert = ""

    live_num = st.number_input("नया आया हुआ नंबर (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ नंबर सबमिट करें"):
        act_size, act_color = get_number_details(live_num)
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            used_rule = st.session_state.active_rule
            
            if act_size == st.session_state.last_pred_size:
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += current_bet_amt * 0.95
                
                # सेफ चेकिंग: KeyError से बचने के लिए
                if used_rule in st.session_state.rule_weights:
                    st.session_state.rule_weights[used_rule] = min(50.0, st.session_state.rule_weights[used_rule] + 2.0)
                
                st.session_state.last_commentary = f"🎯 शानदार! {used_rule} नियम सफल रहा। लेवल 1 पर रीसेट।"
                st.session_state.speak_text = "शानदार विन"
                st.session_state.level = 1
                st.session_state.sound_trigger = 'win'
            else:
                st.session_state.total_pnl -= current_bet_amt
                
                # सेफ चेकिंग: KeyError से बचने के लिए
                if used_rule in st.session_state.rule_weights:
                    st.session_state.rule_weights[used_rule] = max(5.0, st.session_state.rule_weights[used_rule] - 2.0)
                
                st.session_state.level += 1
                st.session_state.sound_trigger = 'loss'
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    st.session_state.last_commentary = "⚠️ 8 लेवल पूरे हुए। लेवल 1 पर वापस।"
                else:
                    st.session_state.last_commentary = f"📉 {used_rule} नियम फेल हुआ। एआई ने रणनीति बदल ली है।"
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो गया है।"

        st.session_state.history.append({'number': int(live_num), 'size': act_size, 'color': act_color})
        if len(st.session_state.history) > 60:
            st.session_state.history.pop(0)

        st.session_state.success_alert = f"✅ कन्फर्म: नंबर #{live_num} ({act_size} / {act_color}) दर्ज हो गया है!"
        st.rerun()

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
        # DEFAULT_FLOW को रीसेट में भी शामिल किया गया है
        st.session_state.rule_weights = {'NUMBER_REPEAT': 32.0, 'STREAK_FOLLOWER': 28.0, 'SMART_COLOR_FLIP': 22.0, 'ZIGZAG_PATTERN': 18.0, 'ZERO_FIVE_RULE': 15.0, 'DEFAULT_FLOW': 10.0}
        st.session_state.success_alert = "इंजन सफलतापूर्वक रीसेट हो गया है।"
        st.rerun()
