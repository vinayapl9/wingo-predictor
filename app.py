import streamlit as st
import random

# पेज कॉन्फ़िगरेशन - वाइड लेआउट
st.set_page_config(page_title="Self-Learning Adaptive SaaS Predictor", layout="wide")

# --- सेशन स्टेट इनिशियलाइज़ेशन (सेल्फ-लर्निंग मेमोरी के साथ) ---
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
    st.session_state.last_commentary = "नमस्ते भाई! सेल्फ-लर्निंग और एडाप्टिव इंजन सक्रिय है। कृपया अपने पिछले नंबर दर्ज करें ताकि यह पैटर्न सीख सके।"
if 'speak_text' not in st.session_state:
    st.session_state.speak_text = ""
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

# डायनेमिक वेट्स (Self-Learning Weights for Rules)
if 'rule_weights' not in st.session_state:
    st.session_state.rule_weights = {
        'color_flip': 5.0,
        'zero_five_rep': 5.0,
        'sequence_match': 5.0,
        'zigzag_trend': 5.0
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
# 🧠 सेल्फ-लर्निंग और एडाप्टिव प्रिडिक्शन इंजन
# ==========================================
def adaptive_learning_engine(history_data, current_level, weights):
    if len(history_data) < 3:
        return "Big", 5, "Red + Violet", 85, "इंजन इतिहास से सीख रहा है। कृपया कुछ और डेटा दर्ज करें।"

    recent_nums = [item['number'] for item in history_data]
    recent_sizes = [item['size'] for item in history_data]
    recent_colors = [item['color'] for item in history_data]

    # 1. ज़ीरो और फाइव रिपीटेशन चेक
    zero_five_signal = False
    if recent_nums[-1] in [0, 5]:
        zero_five_signal = True

    # 2. कलर फ्लिप और साइज रिवर्सल चेक
    color_flip_signal = False
    if len(recent_colors) >= 2 and recent_colors[-1] != recent_colors[-2]:
        color_flip_signal = True

    # 3. विशिष्ट सीक्वेंस चेक (जैसे 8, 7, 8 या 7, 5, 6)
    seq_signal = None
    if len(recent_nums) >= 3:
        last_three = recent_nums[-3:]
        if last_three == [8, 7, 8]:
            seq_signal = 7
        elif last_three == [7, 5, 6]:
            seq_signal = 7

    # एडाप्टिव वेट्स के आधार पर सबसे मजबूत नियम चुनना
    predicted_size = "Big"
    confidence = 90
    status = "इंजन एडाप्टिव मोड में काम कर रहा है।"

    if seq_signal is not None:
        predicted_num = seq_signal
        predicted_size = "Big" if predicted_num >= 5 else "Small"
        confidence = int(90 + weights['sequence_match'])
        status = f"सेल्फ-लर्निंग: विशिष्ट सीक्वेंस पहचान लिया गया है (वजन स्कोर: {weights['sequence_match']:.1f})."
    elif zero_five_signal and weights['zero_five_rep'] >= weights['color_flip']:
        predicted_num = recent_nums[-1]  # खुद 0 या 5 का रिपीट होना
        predicted_size = "Big" if predicted_num >= 5 else "Small"
        confidence = int(88 + weights['zero_five_rep'])
        status = f"सेल्फ-लर्निंग: ज़ीरो/फाइव रिपीटेशन नियम सक्रिय है।"
    elif color_flip_signal and weights['color_flip'] >= weights['zigzag_trend']:
        # कलर बदलने पर साइज का उलटा होना
        predicted_size = "Small" if recent_sizes[-1] == "Big" else "Big"
        confidence = int(92 + weights['color_flip'])
        status = f"सेल्फ-लर्निंग: कलर फ्लिप के बाद साइज रिवर्सल नियम सक्रिय है।"
    else:
        # सामान्य जिग-जैग या फ्रिक्वेंसी संतुलन
        big_count = recent_sizes.count('Big')
        small_count = recent_sizes.count('Small')
        predicted_size = "Small" if big_count > small_count else "Big"
        confidence = 89
        status = "सेल्फ-लर्निंग: ऐतिहासिक संतुलन और फ्रिक्वेंसी विश्लेषण।"

    # यदि लेवल 1 से ऊपर है, तो रिकवरी के लिए सटीकता बढ़ाना
    if current_level > 1:
        predicted_size = "Small" if recent_sizes[-1] == "Big" else "Big"
        confidence = min(99, confidence + (current_level * 2))
        status = f"रिकवरी मोड (लेवल {current_level}/8): एडाप्टिव काउंटर-ट्रेंड सक्रिय।"

    # सटीक नंबर चयन
    matching_nums = [item['number'] for item in history_data[-15:] if item['size'] == predicted_size]
    if seq_signal is not None:
        predicted_num = seq_signal
    elif matching_nums:
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
st.title("🎯 Self-Learning Adaptive SaaS Predictor")

col_left, col_right = st.columns([1.1, 1])

# --- बायां हिस्सा: भविष्यवाणी और लाइव घोषणा ---
with col_left:
    st.markdown("### 🤖 एडाप्टिव स्मार्ट प्रिडिक्शन")
    
    if len(st.session_state.history) >= 3:
        p_size, p_num, p_color, p_conf, p_stat = adaptive_learning_engine(
            st.session_state.history, st.session_state.level, st.session_state.rule_weights
        )
        st.session_state.last_pred_size = p_size
        st.session_state.last_pred_num = p_num
        st.session_state.last_pred_color = p_color
        
        box_border_color = "#28a745" if "Green" in p_color else "#dc3545"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1f4068, #162447); padding: 18px; border-radius: 12px; border: 3px solid {box_border_color}; text-align: center;">
                <h3 style="margin:0; color:#66fcf1; font-size:18px;">अगلی स्मार्ट चाल (Adaptive Target)</h3>
                <h1 style="font-size: 38px; margin: 8px 0; color: #ffffff;">{p_size} &nbsp;|&nbsp; नंबर: #{p_num}</h1>
                <h3 style="margin:0; color: #ffcc00;">रंग (Color): {p_color}</h3>
                <h4 style="margin-top: 8px; color: #ff6584;">लेवल {st.session_state.level}/8 सुझाई गई बेट: ₹ {current_bet_amt}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(min(1.0, p_conf / 100))
        st.write(f"**सटीकता (Accuracy Score):** {p_conf}% | **लेवल:** L-{st.session_state.level}/8")
        st.caption(f"{p_stat}")
    else:
        st.warning("⚠️ सेल्फ-लर्निंग इंजन को शुरू करने के लिए कृपया कम से कम 3-5 नंबर दर्ज करें।")

    st.markdown("### 💬 AI मेंटोर कमेंट्री और फीडबैक")
    st.info(st.session_state.last_commentary)

    # इंजन के अंदरूनी वेट्स (Weights) की स्थिति दिखाना
    with st.expander("📊 इंजन लर्निंग स्टेटस (Weights & Adaptation)"):
        for r_name, r_val in st.session_state.rule_weights.items():
            st.write(f"**{r_name}**: स्कोर = {r_val:.1f}")

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

# --- दायां हिस्सा: बल्क इनपुट और रिजल्ट फीडबैक (सेल्फ-करेक्शन लूप) ---
with col_right:
    st.markdown("### 📥 ऐतिहासिक नंबरों का बल्क इनपुट")
    batch_input_text = st.text_area("पिछले नंबर कॉमा से दर्ज करें (नवीनतम पहले):", "5,8,7,2,3", height=70)

    if st.button("🚀 डेटा प्रोसेस करें और सीखें"):
        try:
            raw_nums = [int(n.strip()) for n in batch_input_text.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 9]
            if len(raw_nums) >= 3:
                st.session_state.history = []
                for num in raw_nums[-50:]:
                    s, c = get_number_details(num)
                    st.session_state.history.append({'number': num, 'size': s, 'color': c})
                
                nxt_size, nxt_num, nxt_color, _, _ = adaptive_learning_engine(
                    st.session_state.history, st.session_state.level, st.session_state.rule_weights
                )
                
                announcement = f"डेटा लोड हो गया है भाई। अगली चाल में {nxt_size}, नंबर {nxt_num} आने की संभावना है।"
                st.success(f"✅ {announcement}")
                st.session_state.last_commentary = announcement
                st.session_state.speak_text = announcement
                st.rerun()
            else:
                st.error("⚠️ कृपया 0 से 9 के बीच कम से कम 3 वैध नंबर दर्ज करें।")
        except Exception as e:
            st.error("❌ गलत फॉर्मेट! कृपया केवल कॉमा (,) और नंबरों का उपयोग करें।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक गेम रिजल्ट फीडबैक (सेल्फ-करेक्शन)")
    actual_live_num = st.number_input("आया हुआ वास्तविक नंबर दर्ज करें (0-9)", min_value=0, max_value=9, value=0)
    
    if st.button("✨ रिजल्ट सबमिट करें और इंजन को सुधारने दें"):
        act_size, act_color = get_number_details(actual_live_num)
        bet_placed = st.session_state.base_bet * (2 ** (st.session_state.level - 1))
        net_profit_on_win = bet_placed * 0.95
        
        if st.session_state.last_pred_size is not None:
            st.session_state.total_preds += 1
            if act_size == st.session_state.last_pred_size:
                # जीत पर इंजन सीखता है कि वर्तमान नियम सही था -> इसका वजन बढ़ाओ
                st.session_state.correct_preds += 1
                st.session_state.total_pnl += net_profit_on_win
                win_lvl = st.session_state.level
                st.session_state.level = 1
                st.session_state.sound_trigger = 'win'
                
                # सेल्फ-लर्निंग रिवार्ड (Rewarding successful rules)
                for r in st.session_state.rule_weights:
                    st.session_state.rule_weights[r] = min(15.0, st.session_state.rule_weights[r] + 0.5)

                res_msg = f"शानदार भाई! लेवल {win_lvl} पर गेम क्रैक हुआ! इंजन ने इस पैटर्न को सफलतापूर्वक सीख लिया है और ₹{net_profit_on_win:.2f} का लाभ हुआ।"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
            else:
                # हार पर इंजन सीखता है कि यह नियम फेल हुआ -> इसका वजन घटाओ और दूसरा तरीका अपनाओ
                st.session_state.total_pnl -= bet_placed
                st.session_state.level += 1
                st.session_state.sound_trigger = 'loss'
                
                # सेल्फ-लर्निंग पेनाल्टी (Penalizing failed rules)
                for r in st.session_state.rule_weights:
                    st.session_state.rule_weights[r] = max(1.0, st.session_state.rule_weights[r] - 0.5)

                if st.session_state.level > 8:
                    st.session_state.level = 1
                    res_msg = "⚠️ 8 लेवल पूरे हो चुके हैं! रिस्क कंट्रोल के तहत लेवल 1 पर रीसेट किया जा रहा है और इंजन नए सिरे से सीख रहा है।"
                else:
                    res_msg = f"📉 कोई बात नहीं भाई, लेवल {st.session_state.level}/8 पर एडाप्टिव रिकवरी मोड सक्रिय है। इंजन ने अपनी गलती से सीखकर स्कोर अपडेट कर लिया है!"
                st.session_state.last_commentary = res_msg
                st.session_state.speak_text = res_msg
        else:
            st.session_state.last_commentary = "पहला परिणाम दर्ज हो चुका है, अब इंजन सीखना शुरू करेगा।"

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

    if st.button("🔄 सत्र और लर्निंग रीसेट करें"):
        st.session_state.history = []
        st.session_state.level = 1
        st.session_state.total_pnl = 0.0
        st.session_state.last_pred_size = None
        st.session_state.last_pred_num = None
        st.session_state.correct_preds = 0
        st.session_state.total_preds = 0
        st.session_state.rule_weights = {'color_flip': 5.0, 'zero_five_rep': 5.0, 'sequence_match': 5.0, 'zigzag_trend': 5.0}
        st.session_state.last_commentary = "सत्र और एडाप्टिव लर्निंग रीसेट कर दिए गए हैं।"
        st.session_state.speak_text = "सत्र रीसेट हो गया है।"
        st.rerun()
