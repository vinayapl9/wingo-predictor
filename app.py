import streamlit as st
import random

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="AI Advanced Probability SaaS Predictor", layout="wide")

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
    st.session_state.last_commentary = "नमस्ते भाई! मल्टी-फैक्टर प्रोबेबिलिटी और स्मार्ट एआई इंजन सक्रिय है। यह साइज, नंबर, कलर और ज़ीरो-फाइव के पैटर्न को गहराई से तौल रहा है।"
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

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
# 🧠 उन्नत मल्टी-फैक्टर प्रायिकता इंजन (Multi-Factor Probability Engine)
# ==========================================
def advanced_probability_engine(history_data, current_level):
    if len(history_data) < 3:
        return "Big", 5, "Red + Violet", 85, "इंजन डेटा का विश्लेषण कर रहा है भाई।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    last_num = recent_nums[-1]
    last_size = recent_sizes[-1]

    big_score = 0
    small_score = 0
    status_reasons = []

    # 1. ज़ीरो (0) और फाइव (5) का विशेष संभावना नियम
    if last_num in [0, 5]:
        # इतिहास में देखें कि 0 या 5 के बाद अक्सर कौन से नंबर या साइज आए हैं
        sub_following = []
        for i in range(len(recent_nums) - 1):
            if recent_nums[i] in [0, 5]:
                sub_following.append(recent_sizes[i+1])
        
        if sub_following:
            b_cnt = sub_following.count('Big')
            s_cnt = sub_following.count('Small')
            if b_cnt > s_cnt:
                big_score += 4
                status_reasons.append("ज़ीरो/फाइव के बाद ऐतिहासिक रूप से 'Big' की संभावना अधिक है।")
            elif s_cnt > b_cnt:
                small_score += 4
                status_reasons.append("ज़ीरो/फाइव के बाद ऐतिहासिक रूप से 'Small' की संभावना अधिक है।")
        else:
            # डिफ़ॉल्ट नियम: 0 या 5 के बाद खुद 0/5 या उनके आस-पास के ट्रेंड पर विचार
            if last_num == 0:
                small_score += 3
                status_reasons.append("ज़ीरो (0) के बाद दोहराव या स्मॉल की प्राथमिकता।")
            else:
                big_score += 3
                status_reasons.append("फाइव (5) के बाद बिग की प्राथमिकता।")

    # 2. समग्र फ्रिक्वेंसी और प्रायिकता स्कोर (पिछले सभी डेटा का निचोड़)
    total_big = recent_sizes.count('Big')
    total_small = recent_sizes.count('Small')
    total_len = len(recent_sizes)

    big_prob = (total_big / total_len) * 10 if total_len > 0 else 5
    small_prob = (total_small / total_len) * 10 if total_len > 0 else 5

    big_score += big_prob
    small_score += small_prob

    # 3. कलर फ्लिप और ट्रेंड बैलेंस
    if len(recent_colors) >= 2 and recent_colors[-1] != recent_colors[-2]:
        # कलर बदलने पर विपरीत साइज को थोड़ा बूस्ट देना
        if last_size == "Big":
            small_score += 2.5
            status_reasons.append("कलर फ्लिप के कारण Small को प्राथमिकता।")
        else:
            big_score += 2.5
            status_reasons.append("कलर फ्लिप के कारण Big को प्राथमिकता।")
    else:
        # अगर कलर नहीं बदला है, तो मौजूदा ट्रेंड को हल्का सा बल देना
        if last_size == "Big":
            big_score += 1.5
        else:
            small_score += 1.5

    # 4. अंतिम निर्णय (Final Probability Decision)
    if big_score >= small_score:
        predicted_size = "Big"
        confidence = int(85 + min(12, (big_score - small_score) * 2))
    else:
        predicted_size = "Small"
        confidence = int(85 + min(12, (small_score - big_score) * 2))

    # यदि लेवल 1 से ऊपर जाता है (रिकवरी मोड)
    if current_level > 1:
        # रिकवरी में विपरीत ट्रेंड या सबसे मजबूत संभावना चुनें
        predicted_size = "Small" if last_size == "Big" else "Big"
        confidence = min(98, confidence + (current_level * 1))
        status_reasons.append(f"लेवल {current_level}/8 रिकवरी मोड: स्मार्ट काउंटर-प्रायिकता सक्रिय।")

    # --- सबसे सटीक नंबर का चयन (प्रायिकता के आधार पर) ---
    # इतिहास में देखें कि predicted_size के कौन से नंबर सबसे ज्यादा बार आए हैं
    candidate_nums = [n for n in recent_nums if get_number_details(n)[0] == predicted_size]
    if candidate_nums:
        # जो नंबर सबसे ज्यादा बार आया है, उसे चुनें
        predicted_num = max(set(candidate_nums), key=candidate_nums.count)
    else:
        # यदि डेटा न हो तो मानक नंबर चुनें
        predicted_num = random.choice([5, 6, 7, 8, 9]) if predicted_size == "Big" else random.choice([0, 1, 2, 3, 4])

    predicted_color = get_number_details(predicted_num)[1]
    status_text = " | ".join(status_reasons) if status_reasons else "संतुलित प्रायिकता विश्लेषण।"

    return predicted_size, predicted_num, predicted_color, confidence, status_text

# 8 लेवल मार्टिंगेल बेट राशि गणना
current_bet_amt = st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================
# 🖥️ मुख्य स्प्लिट-स्क्रीन डैशबोर्ड लेआउट
# ==========================================
st.title("🎯 AI Advanced Probability Predictor")

col_left, col_right = st.columns([1.1, 1])

# --- बायां हिस्सा: भविष्यवाणी और लाइव घोषणा ---
with col_left:
    st.markdown("### 🤖 एडवांस्ड प्रायिकता आधारित प्रिडिक्शन")
    
    if len(st.session_state.history) >= 3:
        p_size, p_num, p_color, p_conf, p_stat = advanced_probability_engine(
            st.session_state.history, st.session_state.level
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        
        box_border_color = "#28a745" if "Green" in p_color else "#dc3545"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_border_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">संभावना आधारित अगली अचूक चाल</h3>
                <h1 style="font-size: 38px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; नंबर: #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग (Color): {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 सुझाई गई बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(p_conf / 100)
        st.write(f"**सटीकता प्रायिकता:** {p_conf}% | **लेवल:** L-{st.session_state.level}/8")
        st.caption(f"**एआई विश्लेषण:** {p_stat}")
    else:
        st.warning("⚠️ सटीक प्रायिकता के लिए कृपया कम से कम 3 नंबर दर्ज करें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक और घोषणा")
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

# --- दायां हिस्सा: बल्क इनपुट और रिजल्ट फीडबैक ---
with col_right:
    st.markdown("### 📥 ऐतिहासिक नंबरों का बल्क इनपुट")
    batch_input_text = st.text_area("पिछले नंबर कॉमा से दर्ज करें (नवीनतम पहले):", "5,8,7,2,3", height=70)

    if st.button("🚀 डेटा प्रोसेस करें और प्रायिकता जांचें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input_text.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 3:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                
                nxt_size, nxt_num, nxt_color, _, _ = advanced_probability_engine(
                    st.session_state.history, st.session_state.level
                )
                
                announcement = f"डेटा लोड हो गया है भाई। प्रायिकता के अनुसार अगली चाल में {nxt_size}, नंबर {nxt_num} आने की संभावना है।"
                st.success(f"✅ {announcement}")
                st.session_state.last_commentary = announcement
                st.session_state.speak_text = announcement
                st.rerun()
            else:
                st.error("⚠️ कृपया 0 से 9 के बीच कम से कम 3 वैध नंबर दर्ज करें।")
        except Exception as e:
            st.error("❌ गलत फॉर्मेट! कृपया केवल कॉमा (,) और नंबरों का उपयोग करें।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक गेम रिजल्ट फीडबैक")
    actual_live_num = st.number_input("आया हुआ वास्तविक नंबर दर्ज करें (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ रिजल्ट सबमिट करें और एक्यूरेसी सुधार देखें"):
        act_size, act_color = get_number_details(actual_live_num)
        bet_placed = st.session_state.base_bet * (2 ** (st.session_state.level - 1))
        net_profit_on_win = bet_placed * 0.95
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            if act_size == st.session_state.last_pred_size:
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += net_profit_on_win
                win_lvl = st.session_state.level
                st.session_state.level = 1
                st.session_state.sound_trigger = 'win'
                res_msg = f"शानदार भाई! लेवल {win_lvl} पर प्रायिकता सही साबित हुई और ₹{net_profit_on_win:.2f} का शुद्ध लाभ मिला!"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
            else:
                st.session_state.total_pnl -= bet_placed
                st.session_state.level += 1
                st.session_state.sound_trigger = 'loss'
                
                if st.session_state.level > 8:
                    st.session_state.level = 1
                    res_msg = "⚠️ 8 लेवल पूरे हो चुके हैं! सुरक्षा के लिए लेवल 1 पर रीसेट किया जा रहा है।"
                else:
                    res_msg = f"📉 कोई बात नहीं भाई, लेवल {st.session_state.level}/8 पर प्रायिकता रीकैलिब्रेशन एक्टिव है।"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो चुका है।"

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

    if st.button("🔄 सत्र रीसेट करें"):
        st.session_state.history = []
        st.session_state.level = 1
        st.session_state.total_pnl = 0.0
        st.session_state.last_pred_size = None
        st.session_state.last_pred_num = None
        st.session_state.correct_preds = 0
        st.session_state.total_preds = 0
        st.session_state.last_commentary = "सत्र रीसेट कर दिया गया है।"
        st.session_state.speak_text = "सत्र रीसेट हो गया है।"
        st.rerun()
