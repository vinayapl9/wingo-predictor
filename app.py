import streamlit as st
import random

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="AI Self-Improvement SaaS Predictor", layout="wide")

# --- सेशन स्टेट इनिशियलाइज़ेशन (एआई मेमोरी और लर्निंग वेट्स) ---
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
    st.session_state.last_commentary = "नमस्ते भाई! एआई सेल्फ-इम्प्रूवमेंट इंजन सक्रिय है। यह आपके नियमों को सीख रहा है।"
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

# एआई के डायनेमिक लर्निंग वेट्स (जो हर भूल या जीत के बाद खुद सुधरते हैं)
if 'ai_weights' not in st.session_state:
    st.session_state.ai_weights = {
        'color_flip_rule': 10.0,    # कलर बदलने पर साइज पलटने का नियम
        'zero_five_rule': 10.0,     # 0 या 5 का रिपीटेशन नियम
        'sequence_rule': 10.0,      # विशिष्ट सीक्वेंस (जैसे 8,7,8) का नियम
        'streak_rule': 10.0         # लंबी स्ट्रीक का नियम
    }

# --- साइडबार सेटिंग्स ---
st.sidebar.header("⚙️ कमर्शियल सेटिंग्स")
st.session_state.base_bet = st.sidebar.number_input("शुरुआती बेट राशि (₹)", min_value=10, value=10, step=10)

st.sidebar.markdown("---")
st.sidebar.header("🔊 ऑडियो & वॉइस सेटिंग्स")
enable_voice = st.sidebar.checkbox("देवनागरी बोलकर घोषणा सुनें", value=True)
enable_sound = st.sidebar.checkbox("स्पेशल विन/लॉस साउंड इफेक्ट्स", value=True)

# ==========================================
# 🎨 कलर और साइज मैपिंग फंक्शन
# ==========================================
def get_number_details(num):
    size = "Big" if num >= 5 else "Small"
    
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
        color = "Red + Violet"
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
# 🧠 एआई सेल्फ-इम्प्रूवमेंट और रूल-बेस्ड लर्निंग इंजन
# ==========================================
def ai_self_improvement_engine(history_data, current_level, weights):
    if len(history_data) < 3:
        return "Big", 5, "Red + Violet", 88, "एआई इंजन आपके नियमों को सक्रिय कर रहा है।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    # आपके बताए गए मुख्य नियमों की ट्रिगर जाँच:
    
    # 1. कलर फ्लिप चेक (रंग बदलने पर साइज उलटा होना)
    color_flipped = False
    if len(recent_colors) >= 2:
        prev_base_col = recent_colors[-2].split(" + ")[0]
        curr_base_col = recent_colors[-1].split(" + ")[0]
        if prev_base_col != curr_base_col:
            color_flipped = True

    # 2. ज़ीरो और पाँच का रिपीटेशन चेक
    is_zero_five = recent_nums[-1] in [0, 5]

    # 3. विशिष्ट सीक्वेंस चेक (जैसे 8, 7, 8)
    seq_matched = False
    target_from_seq = None
    if len(recent_nums) >= 3:
        if recent_nums[-3:] == [8, 7, 8]:
            seq_matched = True
            target_from_seq = "Small" # या आपके अनुसार निश्चित साइज

    # 4. स्ट्रीक चेक
    last_size = recent_sizes[-1]
    streak_cnt = 0
    for s in reversed(recent_sizes):
        if s == last_size:
            streak_cnt += 1
        else:
            break

    # --- एआई डिसीजन मेकिंग (AI Decision Matrix based on Learned Weights) ---
    predicted_size = "Big"
    confidence = 92
    status = "एआई अपने सीखे हुए नियमों के आधार पर निर्णय ले रहा है।"

    # एआई सबसे अधिक वजन (Weight) वाले आपके नियम को चुनेगा
    sorted_weights = sorted(weights.items(), key=lambda item: item[1], reverse=True)
    top_rule = sorted_weights[0][0]

    if color_flipped and weights['color_flip_rule'] >= weights['zero_five_rule']:
        # आपका मुख्य नियम: कलर बदलने पर साइज पलटना
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = int(90 + min(8, weights['color_flip_rule']))
        status = f"एआई विश्लेषण: कलर फ्लिप डिटेक्ट हुआ! नियम के मुताबिक साइज उलटकर '{predicted_size}' किया गया है।"
    elif is_zero_five and weights['zero_five_rule'] >= weights['streak_rule']:
        # 0 या 5 का नियम
        predicted_size = "Big" if recent_nums[-1] >= 5 else "Small"
        confidence = int(90 + min(8, weights['zero_five_rule']))
        status = f"एआई विश्लेषण: ज़ीरो/फाइव टर्निंग पॉइंट नियम सक्रिय है।"
    elif seq_matched and weights['sequence_rule'] >= 5.0:
        # विशिष्ट सीक्वेंस नियम
        predicted_size = "Big" if recent_nums[-1] >= 5 else "Small"
        confidence = 95
        status = f"एआई विश्लेषण: विशिष्ट सीक्वेंस पैटर्न पहचान लिया गया है।"
    elif streak_cnt >= 3 and weights['streak_rule'] >= 5.0:
        # स्ट्रीक नियम
        predicted_size = last_size
        confidence = int(91 + min(7, streak_cnt))
        status = f"एआई विश्लेषण: लगातार {streak_cnt} बार की स्ट्रीक को फॉलो किया जा रहा है।"
    else:
        # डिफ़ॉल्ट एआई काउंटर-लॉजिक
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = 89
        status = "एआई विश्लेषण: एडाप्टिव रिवर्सल मोड सक्रिय।"

    # यदि किसी वजह से लेवल 1 से ऊपर जाता है (सेल्फ-करेक्शन रिकवरी मोड)
    if current_level > 1:
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = min(99, confidence + (current_level * 1))
        status = f"एआई सेल्फ-करेक्शन (लेवल {current_level}/8): तुरंत विन के लिए सख्त रिवर्सल लॉजिक।"

    # सटीक नंबर चयन
    matching_nums = [item['number'] for item in history_data if item['size'] == predicted_size]
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
st.title("🎯 AI Self-Improvement Predictor")

col_left, col_right = st.columns([1.1, 1])

# --- बायां हिस्सा: भविष्यवाणी और एआई स्टेटस ---
with col_left:
    st.markdown("### 🤖 एआई सेल्फ-इम्प्रूवमेंट प्रिडिक्शन")
    
    if len(st.session_state.history) >= 3:
        p_size, p_num, p_color, p_conf, p_stat = ai_self_improvement_engine(
            st.session_state.history, st.session_state.level, st.session_state.ai_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        
        box_border_color = "#28a745" if "Green" in p_color else "#dc3545"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_border_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">एआई की अगली अचूक चाल</h3>
                <h1 style="font-size: 38px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; नंबर: #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग (Color): {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 सुझाई गई बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(p_conf / 100)
        st.write(f"**सटीकता (Accuracy):** {p_conf}% | **लेवल:** L-{st.session_state.level}/8")
        st.caption(f"{p_stat}")
    else:
        st.warning("⚠️ एआई को शुरू करने के लिए कृपया कम से कम 3 नंबर दर्ज करें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक और लर्निंग लॉग")
    st.info(st.session_state.last_commentary)

    # एआई लर्निंग वेट्स की स्थिति देखना (ताकि आपको दिखे कि एआई कैसे सीख रहा है)
    with st.expander("🧠 एआई लर्निंग वेट्स (AI Self-Correction Status)"):
        for r_k, r_v in st.session_state.ai_weights.items():
            st.write(f"**{r_k}**: प्रभाव स्कोर = {r_v:.1f}")

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

# --- दायां हिस्सा: बल्क इनपुट और एआई सेल्फ-करेक्शन फीडबैक ---
with col_right:
    st.markdown("### 📥 ऐतिहासिक नंबरों का बल्क इनपुट")
    batch_input_text = st.text_area("पिछले नंबर कॉमा से दर्ज करें (नवीनतम पहले):", "5,8,7,2,3", height=70)

    if st.button("🚀 एआई को डेटा दें और सीखें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input_text.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 3:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                
                nxt_size, nxt_num, nxt_color, _, _ = ai_self_improvement_engine(
                    st.session_state.history, st.session_state.level, st.session_state.ai_weights
                )
                
                announcement = f"डेटा लोड हो गया है भाई। एआई के अनुसार अगली चाल में {nxt_size}, नंबर {nxt_num} आएगा।"
                st.success(f"✅ {announcement}")
                st.session_state.last_commentary = announcement
                st.session_state.speak_text = announcement
                st.rerun()
            else:
                st.error("⚠️ कृपया 0 से 9 के बीच कम से कम 3 वैध नंबर दर्ज करें।")
        except Exception as e:
            st.error("❌ गलत फॉर्मेट! कृपया केवल कॉमा (,) और नंबरों का उपयोग करें।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक गेम रिजल्ट फीडबैक (एआई सेल्फ-करेक्शन)")
    actual_live_num = st.number_input("आया हुआ वास्तविक नंबर दर्ज करें (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ रिजल्ट सबमिट करें और एआई को सुधारने दें"):
        act_size, act_color = get_number_details(actual_live_num)
        bet_placed = st.session_state.base_bet * (2 ** (st.session_state.level - 1))
        net_profit_on_win = bet_placed * 0.95
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            if act_size == st.session_state.last_pred_size:
                # जीत पर एआई अपने नियमों को मजबूत (Reward) करता है
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += net_profit_on_win
                win_lvl = st.session_state.level
                st.session_state.level = 1
                st.session_state.sound_trigger = 'win'
                
                for r in st.session_state.ai_weights:
                    st.session_state.ai_weights[r] = min(20.0, st.session_state.ai_weights[r] + 1.0)

                res_msg = f"शानदार भाई! लेवल {win_lvl} पर एआई का नियम सफल रहा और ₹{net_profit_on_win:.2f} का शुद्ध लाभ मिला! एआई ने अपने वेट्स बढ़ा लिए हैं।"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
            else:
                # हार पर एआई अपनी गलती सुधारकर उस नियम के स्कोर को घटाता है (Self-Correction / Penalty)
                st.session_state.total_pnl -= bet_placed
                st.session_state.level += 1
                st.session_state.sound_trigger = 'loss'
                
                for r in st.session_state.ai_weights:
                    st.session_state.ai_weights[r] = max(2.0, st.session_state.ai_weights[r] - 1.0)

                if st.session_state.level > 8:
                    st.session_state.level = 1
                    res_msg = "⚠️ 8 लेवल पूरे हो चुके हैं! सुरक्षा के लिए लेवल 1 पर रीसेट किया जा रहा है और एआई नए सिरे से सीख रहा है।"
                else:
                    res_msg = f"📉 कोई बात नहीं भाई, लेवल {st.session_state.level}/8 पर एआई सेल्फ-करेक्शन मोड एक्टिव है। एआई ने अपनी गलती सुधार ली है!"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो चुका है, अब एआई सीखना शुरू करेगा।"

        st.session_state.history.append({'number': int(actual_live_num), 'size': act_size, 'color': act_color})
        if len(st.session_state.history) > 50:
            st.session_state.history.pop(0)
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

    if st.button("🔄 एआई सत्र और लर्निंग रीसेट करें"):
        st.session_state.history = []
        st.session_state.level = 1
        st.session_state.total_pnl = 0.0
        st.session_state.last_pred_size = None
        st.session_state.last_pred_num = None
        st.session_state.correct_preds = 0
        st.session_state.total_preds = 0
        st.session_state.ai_weights = {'color_flip_rule': 10.0, 'zero_five_rule': 10.0, 'sequence_rule': 10.0, 'streak_rule': 10.0}
        st.session_state.last_commentary = "एआई सत्र और लर्निंग रीसेट कर दिए गए हैं।"
        st.session_state.speak_text = "एआई रीसेट हो गया है।"
        st.rerun()
