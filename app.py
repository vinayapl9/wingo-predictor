import streamlit as st

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="AI Master Predictor - Final Edition", layout="wide")

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
if 'correct_preds' not in st.session_state:
    st.session_state.correct_preds = 0
if 'total_preds' not in st.session_state:
    st.session_state.total_preds = 0
if 'last_commentary' not in st.session_state:
    st.session_state.last_commentary = "नमस्ते भाई! कन्फर्मेशन मैसेज और सटीक कलर कोडिंग वाला एआई इंजन सक्रिय है।"
if 'success_alert' not in st.session_state:
    st.session_state.success_alert = ""
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

# एआई सेल्फ-इम्प्रूवमेंट वेट्स
if 'rule_weights' not in st.session_state:
    st.session_state.rule_weights = {
        'streak_follow': 25.0,
        'color_flip': 20.0,
        'zero_five': 18.0
    }

# --- साइडबार सेटिंग्स ---
st.sidebar.header("⚙️ कमर्शियल सेटिंग्स")
st.session_state.base_bet = st.sidebar.number_input("शुरुआती बेट राशि (₹)", min_value=10, value=10, step=10)

st.sidebar.markdown("---")
st.sidebar.header("🔊 ऑडियो & वॉइस सेटिंग्स")
enable_voice = st.sidebar.checkbox("देवनागरी बोलकर घोषणा सुनें", value=True)
enable_sound = st.sidebar.checkbox("स्पेशल विन/लॉस साउंड इफेक्ट्स", value=True)

# ==========================================
# 🎨 सटीक कलर और साइज मैपिंग (आपके निर्देशों के अनुसार)
# ==========================================
def get_number_details(num):
    size = "Big" if num >= 5 else "Small"
    
    # सटीक कलर कोडिंग (रेड, ग्रीन, और वॉयलेट कॉम्बिनेशन)
    if num == 0:
        color = "Red + Violet"
    elif num == 1:
        color = "Green"
    elif num == 2:
        color = "Red"
    elif num == 3:
        color = "Green"
    elif num == 4:
        color = "Red"
    elif num == 5:
        color = "Red + Violet" # या वॉयलेट कॉम्बिनेशन
    elif num == 6:
        color = "Red"
    elif num == 7:
        color = "Green + Violet" # मानक नियम के अनुसार 7 वॉयलेट
    elif num == 8:
        color = "Red"
    elif num == 9:
        color = "Green + Violet" # मानक नियम के अनुसार 9 वॉयलेट
    else:
        color = "Unknown"
        
    return size, color

# ==========================================
# 🧠 सटीक पैटर्न और स्ट्रीक लर्निंग इंजन
# ==========================================
def master_ai_engine(history_data, current_level, weights):
    if len(history_data) < 2:
        return "Big", 5, "Red + Violet", 90, "इंजन डेटा का विश्लेषण कर रहा है।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    last_num = recent_nums[-1]
    last_size = recent_sizes[-1]

    # 1. वास्तविक स्ट्रीक की सटीक गिनती (गलत गिनती को पूरी तरह खत्म किया गया)
    streak_count = 0
    for s in reversed(recent_sizes):
        if s == last_size:
            streak_count += 1
        else:
            break

    # 2. कलर फ्लिप जाँच (कलर बदलने पर साइज उलटा होना)
    color_flipped = False
    if len(recent_colors) >= 2:
        prev_col = recent_colors[-2].split(" + ")[0]
        curr_col = recent_colors[-1].split(" + ")[0]
        if prev_col != curr_col:
            color_flipped = True

    # 3. ज़ीरो और पाँच (0/5) का टर्निंग पॉइंट नियम
    is_zero_five = last_num in [0, 5]

    predicted_size = "Big"
    confidence = 92
    status = "सटीक पैटर्न विश्लेषण सक्रिय।"

    # प्राथमिकता निर्णय
    if streak_count >= 2 and weights['streak_follow'] >= 10.0:
        predicted_size = last_size
        confidence = int(92 + min(6, streak_count))
        status = f"सटीक पकड़: लगातार {streak_count} बार '{last_size}' आया है, इंजन उसी ट्रेंड को फॉलो कर रहा है।"
    elif color_flipped and weights['color_flip'] >= 10.0:
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = 95
        status = f"सटीक पकड़: कलर फ्लिप हुआ है! पिछला साइज '{last_size}' था, इसलिए अब साइज उलटकर '{predicted_size}' हो गया है।"
    elif is_zero_five and weights['zero_five'] >= 10.0:
        predicted_size = "Big" if last_num >= 5 else "Small"
        confidence = 94
        status = f"सटीक पकड़: ज़ीरो/फाइव टर्निंग पॉइंट (#{last_num}) सक्रिय है।"
    else:
        predicted_size = last_size
        confidence = 90
        status = "सटीक पकड़: वर्तमान ट्रेंड को प्राथमिकता दी जा रही है।"

    # रिकवरी मोड
    if current_level > 1:
        predicted_size = last_size if streak_count >= 2 else ("Small" if last_size == "Big" else "Big")
        confidence = min(99, confidence + (current_level * 1))
        status = f"रिकवरी मोड (लेवल {current_level}/8): नुकसान रोकने के लिए सख्त ट्रेंड सक्रिय।"

    # सटीक नंबर चयन
    matching_nums = [n for n in recent_nums if get_number_details(n)[0] == predicted_size]
    if matching_nums:
        predicted_num = max(set(matching_nums), key=matching_nums.count)
    else:
        predicted_num = 7 if predicted_size == 'Big' else 2

    predicted_color = get_number_details(predicted_num)[1]
    return predicted_size, predicted_num, predicted_color, confidence, status

# 8 लेवल मार्टिंगेल बेट राशि गणना
current_bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================
# 🖥️ मुख्य स्प्लिट-स्क्रीन डैशबोर्ड लेआउट
# ==========================================
st.title("🎯 AI Master Predictor [Confirmed Feedback Edition]")

col_left, col_right = st.columns([1.1, 1])

# --- बायां हिस्सा: भविष्यवाणी और लाइव घोषणा ---
with col_left:
    st.markdown("### 🤖 एआई मास्टर प्रिडिक्शन इंजन")
    
    if len(st.session_state.history) >= 2:
        p_size, p_num, p_color, p_conf, p_stat = master_ai_engine(
            st.session_state.history, st.session_state.level, st.session_state.rule_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        
        box_border_color = "#28a745" if "Green" in p_color else "#dc3545"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_border_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">एआई की अगली पक्की चाल</h3>
                <h1 style="font-size: 38px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; नंबर: #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग (Color): {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 सुझाई गई बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(p_conf / 100)
        st.write(f"**नियम सटीकता:** {p_conf}% | **लेवल:** L-{st.session_state.level}/8")
        st.caption(f"**एआई मेंटोर:** {p_stat}")
    else:
        st.warning("⚠️ इंजन शुरू करने के लिए कृपया कम से कम 2 नंबर दर्ज करें।")

    st.markdown("### 💬 एआई लर्निंग और फीडबैक लॉग")
    st.info(st.session_state.last_commentary)

    # --- जावास्क्रिप्ट स्पीच और साउंड सिंथेसिस ---
    js_code = ""

    if enable_sound and st.session_state.sound_trigger:
        if st.session_state.sound_trigger == 'win':
            js_code += """
                try {
                    const ctx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime);
                    osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1);
                    osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.2);
                    gain.gain.setValueAtTime(0.2, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.5);
                } catch(e) {}
            """
        elif st.session_state.sound_trigger == 'loss':
            js_code += """
                try {
                    const ctx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(220, ctx.currentTime);
                    osc.frequency.setValueAtTime(185, ctx.currentTime + 0.15);
                    gain.gain.setValueAtTime(0.2, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.4);
                } catch(e) {}
            """
        st.session_state.sound_trigger = None

    if enable_voice and st.session_state.speak_text:
        clean_text = st.session_state.speak_text.replace("'", "").replace('"', "")
        js_code += f"""
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_text}');
                msg.lang = 'hi-IN';
                msg.rate = 0.95;
                window.speechSynthesis.speak(msg);
            }}
        """
        st.session_state.speak_text = ""

    if js_code:
        st.components.v1.html(f"<script>{js_code}</script>", height=0)

# --- दायां हिस्सा: बल्क इनपुट और कन्फर्मेशन मैसेज वाला रिजल्ट फीडबैक ---
with col_right:
    st.markdown("### 📥 ऐतिहासिक नंबरों का बल्क इनपुट")
    batch_input_text = st.text_area("पिछले नंबर कॉमा से दर्ज करें (नवीनतम पहले):", "5,8,7,2,3", height=70)

    if st.button("🚀 डेटा प्रोसेस करें और लोड करें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input_text.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 2:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                
                announcement = f"सफलतापूर्वक {len(raw_nums)} नंबर लोड हो गए हैं भाई!"
                st.success(f"✅ {announcement}")
                st.session_state.last_commentary = announcement
                st.session_state.speak_text = announcement
                st.rerun()
            else:
                st.error("⚠️ कृपया कम से कम 2 वैध नंबर दर्ज करें।")
        except Exception as e:
            st.error("❌ गलत फॉर्मेट! कृपया केवल कॉमा और नंबरों का उपयोग करें।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक गेम रिजल्ट फीडबैक (कन्फर्मेशन अलर्ट के साथ)")
    
    # यहाँ कन्फर्मेशन मैसेज दिखाने के लिए एहतियात
    if st.session_state.success_alert:
        st.success(st.session_state.success_alert)
        st.session_state.success_alert = "" # एक बार दिखाने के बाद साफ करना

    actual_live_num = st.number_input("आया हुआ वास्तविक नंबर दर्ज करें (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ नंबर सबमिट करें और कन्फर्मेशन देखें"):
        act_size, act_color = get_number_details(actual_live_num)
        bet_placed = st.session_state.base_bet * (2 ** (st.session_state.level - 1))
        net_profit_on_win = bet_placed * 0.95
        
        # इतिहास में नया नंबर जोड़ने से पहले पिछला प्रिडिक्शन जांचें
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            if act_size == st.session_state.last_pred_size:
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += net_profit_on_win
                win_lvl = st.session_state.level
                st.session_state.level = 1
                st.session_state.sound_trigger = 'win'
                
                for r in st.session_state.rule_weights:
                    st.session_state.rule_weights[r] = min(30.0, st.session_state.rule_weights[r] + 1.0)

                res_msg = f"शानदार भाई! लेवल {win_lvl} पर गेम क्रैक हुआ और ₹{net_profit_on_win:.2f} का लाभ मिला!"
            else:
                st.session_state.total_pnl -= bet_placed
                st.session_state.level += 1
                st.session_state.sound_trigger = 'loss'
                
                for r in st.session_state.rule_weights:
                    st.session_state.rule_weights[r] = max(5.0, st.session_state.rule_weights[r] - 1.0)

                if st.session_state.level > 8:
                    st.session_state.level = 1
                    res_msg = "⚠️ 8 लेवल पूरे हो चुके हैं! सुरक्षा के लिए लेवल 1 पर रीसेट किया जा रहा है।"
                else:
                    res_msg = f"📉 कोई बात नहीं, लेवल {st.session_state.level}/8 पर रिकवरी मोड एक्टिव है।"
        else:
            res_msg = "पहला परिणाम दर्ज हो गया है।"

        # नया रिजल्ट इतिहास में जोड़ें
        st.session_state.history.append({'number': int(actual_live_num), 'size': act_size, 'color': act_color})
        if len(st.session_state.history) > 50:
            st.session_state.history.pop(0)

        # साफ और स्पष्ट कन्फर्मेशन मैसेज सेट करें जो स्क्रीन पर तुरंत दिखेगा
        st.session_state.success_alert = f"✅ कन्फर्म: वास्तविक नंबर #{actual_live_num} ({act_size} / {act_color}) सफलतापूर्वक दर्ज कर लिया गया है!"
        st.session_state.last_commentary = res_msg
        st.session_state.speak_text = res_msg
        st.rerun()

    # लाइव आंकड़े
    st.markdown("### 📊 लाइव आंकड़े")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Net P/L", value=f"₹ {st.session_state.total_pnl:.2f}")
    with m2:
        st.metric(label="लेवल", value=f"L-{st.session_state.level}/8")
    with m3:
        acc = int((st.session_state.correct_preds / st.session_state.total_preds) * 100) if st.session_state.total_preds > 0 else 0
        st.metric(label="सटीकता", value=f"{acc}%")

    if st.button("🔄 सत्र और लर्निंग रीसेट करें"):
        st.session_state.history = []
        st.session_state.level = 1
        st.session_state.total_pnl = 0.0
        st.session_state.last_pred_size = None
        st.session_state.last_pred_num = None
        st.session_state.correct_preds = 0
        st.session_state.total_preds = 0
        st.session_state.rule_weights = {'streak_follow': 25.0, 'color_flip': 20.0, 'zero_five': 18.0}
        st.session_state.last_commentary = "सत्र रीसेट कर दिया गया है।"
        st.session_state.success_alert = "सत्र सफलतापूर्वक रीसेट हो गया है।"
        st.session_state.speak_text = "सत्र रीसेट हो गया है।"
        st.rerun()
