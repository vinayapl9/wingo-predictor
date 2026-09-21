"""
Pro AI Predictor v2.0 — Silent Movement Edition (Upgraded)
----------------------------------------------------------
What's new vs v1:
  • Ensemble engine — 8 independent rule-detectors vote, weighted by their OWN live accuracy
  • Markov chains (order-1 and order-2) for real transition learning
  • Laplace-smoothed accuracy tracking (no wild swings on small samples)
  • Data-driven 0/5 rule (learns from YOUR history instead of hard-coded)
  • Recency-weighted frequency + Markov number picker
  • Confidence is now calibrated from vote margin AND rule agreement
  • Persistent state (export / import JSON)
  • P/L chart, size distribution, rule leaderboard
  • Bug fixes: prediction now works with 2+ numbers, bet amount syncs with level

⚠️  HONEST NOTE: Colour / size games are RNG-driven. No algorithm can
    guarantee wins. This tool improves *pattern structure and money
    management discipline* — it does NOT beat the house edge.
"""

import json
from collections import Counter
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pro AI Predictor v2", layout="wide")

# ==========================================================
# 🔢 NUMBER → SIZE / COLOUR MAP (as per your spec)
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

def base_color(n):
    """Pure Red / Green / Violet (ignores the mixed violet tag)."""
    if n in (1, 3, 7, 9): return "Green"
    if n in (2, 4, 6, 8): return "Red"
    return "Violet"

# ==========================================================
# ⚖️ BASE RULE WEIGHTS (accuracy multiplier is applied on top)
# ==========================================================
BASE_WEIGHTS = {
    "MARKOV_2":   22.0,
    "MARKOV_1":   18.0,
    "STREAK":     16.0,
    "ZIGZAG":     16.0,
    "COLOR_FLIP": 12.0,
    "MEAN_REVERT":10.0,
    "ZERO_FIVE":   8.0,
    "FREQUENCY":   8.0,
}

# ==========================================================
# 🧠 RULE DETECTORS
# Each returns (predicted_size, confidence_0_to_1) or None
# ==========================================================

def rule_streak(nums, sizes):
    if len(sizes) < 2:
        return None
    last, c = sizes[-1], 0
    for s in reversed(sizes):
        if s == last: c += 1
        else: break
    if c >= 4: return last, 0.85
    if c == 3: return last, 0.72
    if c == 2: return last, 0.58
    return None

def rule_zigzag(nums, sizes):
    if len(sizes) < 4: return None
    if sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3] and sizes[-3] != sizes[-4]:
        return ("Small" if sizes[-1] == "Big" else "Big"), 0.68
    if sizes[-1] != sizes[-2] and sizes[-2] != sizes[-3]:
        return ("Small" if sizes[-1] == "Big" else "Big"), 0.60
    return None

def rule_markov1(nums, sizes):
    """P(next size | last size)"""
    if len(sizes) < 10: return None
    last = sizes[-1]
    tr = Counter(b for a, b in zip(sizes[:-1], sizes[1:]) if a == last)
    tot = sum(tr.values())
    if tot < 5: return None
    best, cnt = tr.most_common(1)[0]
    p = cnt / tot
    if p < 0.54: return None
    return best, min(0.80, 0.45 + p * 0.4)

def rule_markov2(nums, sizes):
    """P(next size | last two sizes)"""
    if len(sizes) < 16: return None
    key = (sizes[-2], sizes[-1])
    tr = Counter(sizes[i + 2] for i in range(len(sizes) - 2)
                 if (sizes[i], sizes[i + 1]) == key)
    tot = sum(tr.values())
    if tot < 4: return None
    best, cnt = tr.most_common(1)[0]
    p = cnt / tot
    if p < 0.55: return None
    return best, min(0.85, 0.45 + p * 0.45)

def rule_color_flip(nums, sizes):
    eff = [base_color(n) for n in nums if base_color(n) in ("Red", "Green")]
    if len(eff) < 3: return None
    if eff[-1] != eff[-2] and eff[-2] != eff[-3]:
        return ("Small" if sizes[-1] == "Big" else "Big"), 0.62
    if eff[-1] != eff[-2]:
        return ("Small" if sizes[-1] == "Big" else "Big"), 0.55
    return None

def rule_zero_five(nums, sizes):
    """Learns from history: what usually follows a 0 or a 5?"""
    if len(nums) < 16: return None
    tr = Counter(b for a, b in zip(nums[:-1], sizes[1:]) if a in (0, 5))
    tot = sum(tr.values())
    if tot < 6: return None
    best, cnt = tr.most_common(1)[0]
    p = cnt / tot
    if p < 0.56: return None
    return best, min(0.78, p)

def rule_mean_revert(nums, sizes):
    if len(sizes) < 14: return None
    w = sizes[-12:]
    p = w.count("Big") / len(w)
    if p >= 0.75: return "Small", 0.62
    if p <= 0.25: return "Big",   0.62
    if p >= 0.67: return "Small", 0.56
    if p <= 0.33: return "Big",   0.56
    return None

def rule_frequency(nums, sizes):
    if len(sizes) < 14: return None
    w = sizes[-16:]
    p = w.count("Big") / len(w)
    if abs(p - 0.5) < 0.07: return None
    return ("Big" if p > 0.5 else "Small"), 0.50 + abs(p - 0.5) * 0.45

RULES = {
    "MARKOV_2":   rule_markov2,
    "MARKOV_1":   rule_markov1,
    "STREAK":     rule_streak,
    "ZIGZAG":     rule_zigzag,
    "COLOR_FLIP": rule_color_flip,
    "MEAN_REVERT":rule_mean_revert,
    "ZERO_FIVE":  rule_zero_five,
    "FREQUENCY":  rule_frequency,
}

# ==========================================================
# 🗂️ SESSION STATE
# ==========================================================
def init_state():
    defaults = {
        "history": [],          # [{'number':int, 'size':str, 'color':str, 'ts':str}]
        "level": 1,
        "base_bet": 10,
        "bet_mode": "Martingale (2x)",
        "total_pnl": 0.0,
        "pnl_curve": [],        # for the chart
        "last_pred": None,      # dict from run_engine()
        "last_fired": [],       # [{'rule':name,'size':str}]
        "rule_stats": {},       # {rule: {'wins':int,'trials':int}}
        "correct": 0,
        "total": 0,
        "commentary": "नमस्ते! प्रो इंजन v2 सक्रिय है। एन्सेम्बल + मार्कोव चेन तैयार है।",
        "alert": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def rerun():
    try: st.rerun()
    except AttributeError: st.experimental_rerun()

def eff_weight(rule):
    """Base weight × live-accuracy multiplier (Laplace smoothed)."""
    rs = st.session_state.rule_stats.get(rule, {"wins": 0, "trials": 0})
    acc = (rs["wins"] + 1) / (rs["trials"] + 2)   # 0..1, smoothed
    return BASE_WEIGHTS[rule] * (0.5 + acc), acc

# ==========================================================
# 🚀 THE ENSEMBLE ENGINE
# ==========================================================
def run_engine(history):
    nums  = [h["number"] for h in history]
    sizes = [h["size"]   for h in history]

    votes   = Counter()
    fired   = []
    details = []

    for name, fn in RULES.items():
        try:
            res = fn(nums, sizes)
        except Exception:
            res = None
        if not res:
            continue

        size, conf = res
        ew, acc    = eff_weight(name)
        score      = ew * conf
        votes[size] += score

        fired.append({"rule": name, "size": size})
        details.append({
            "Rule": name, "Pred": size, "Conf": conf, "Acc": acc,
            "Eff.Weight": ew, "Score": score,
        })

    # ---- fallback when nothing fires ----
    if not votes:
        if len(sizes) >= 5:
            p = sizes[-10:].count("Big") / len(sizes[-10:])
            pred = "Big" if p >= 0.5 else "Small"
        else:
            pred = "Big"
        confidence = 52.0
        margin = 0.0
        avg_conf = 0.5
    else:
        if len(votes) == 1:
            pred, margin = list(votes)[0], 1.0
        else:
            (pred, top), (_, second) = votes.most_common(2)
            margin = (top - second) / (top + second) if (top + second) else 0.0
        avg_conf = sum(d["Conf"] for d in details) / len(details)
        confidence = 52 + margin * 36 + (avg_conf - 0.55) * 32
        confidence = max(52.0, min(96.0, confidence))

    # ---- number picker (recency frequency + Markov) ----
    pred_num, num_probs = pick_number(nums, pred)
    pred_color = num_color(pred_num)

    details.sort(key=lambda d: -d["Score"])

    return {
        "size": pred,
        "number": pred_num,
        "color": pred_color,
        "confidence": round(confidence, 1),
        "margin": round(margin, 3),
        "fired": fired,
        "details": details,
        "num_probs": num_probs,
    }

def pick_number(nums, pred_size):
    """Blend recency-weighted frequency with a 1st-order Markov transition."""
    cands = [n for n in range(10) if num_size(n) == pred_size]

    # recency-weighted frequency
    freq = {n: 0.0 for n in cands}
    for i, n in enumerate(reversed(nums[-40:])):
        if n in freq:
            freq[n] += 0.94 ** i
    fsum = sum(freq.values()) or 1.0
    freq = {n: v / fsum for n, v in freq.items()}

    # markov from the last seen number
    mk = {n: 0.0 for n in cands}
    if len(nums) >= 6:
        last = nums[-1]
        tr = Counter(b for a, b in zip(nums[:-1], nums[1:]) if a == last)
        t = sum(tr.values())
        if t:
            mk = {n: tr.get(n, 0) / t for n in cands}

    combined = {n: 0.6 * freq[n] + 0.4 * mk[n] for n in cands}
    best = max(combined, key=combined.get)
    return best, combined

# ==========================================================
# 📚 LEARNING UPDATE (called after every real result)
# ==========================================================
def update_learning(fired, actual_size):
    for f in fired:
        rs = st.session_state.rule_stats.setdefault(f["rule"], {"wins": 0, "trials": 0})
        rs["trials"] += 1
        if f["size"] == actual_size:
            rs["wins"] += 1

# ==========================================================
# 💰 BET SIZING
# ==========================================================
def current_bet():
    if st.session_state.bet_mode.startswith("Flat"):
        return st.session_state.base_bet
    return st.session_state.base_bet * (2 ** (st.session_state.level - 1))

# ==========================================================
# 🖥️ SIDEBAR
# ==========================================================
with st.sidebar:
    st.header("⚙️ प्रो एआई सेटिंग्स")
    st.session_state.base_bet = st.number_input(
        "शुरुआती बेट राशि (₹)", min_value=10, value=st.session_state.base_bet,
        step=10, key="bet_input"
    )
    st.session_state.bet_mode = st.selectbox(
        "बेटिंग मोड", ["Martingale (2x)", "Flat Betting"],
        index=0 if st.session_state.bet_mode.startswith("Martingale") else 1
    )

    st.markdown("---")
    st.subheader("🎚️ रूल सेंसिटिविटी")
    st.caption("बेस वेट बदलें — लाइव सटीकता इस पर गुणा होती है।")
    for r in BASE_WEIGHTS:
        BASE_WEIGHTS[r] = st.slider(r, 0.0, 40.0, BASE_WEIGHTS[r], 0.5, key=f"w_{r}")

    st.markdown("---")
    st.subheader("💾 डेटा")
    export_payload = {
        "history": st.session_state.history,
        "rule_stats": st.session_state.rule_stats,
        "total_pnl": st.session_state.total_pnl,
        "level": st.session_state.level,
        "correct": st.session_state.correct,
        "total": st.session_state.total,
        "exported": datetime.now().isoformat(timespec="seconds"),
    }
    st.download_button(
        "⬇️ सेशन एक्सपोर्ट (JSON)",
        data=json.dumps(export_payload, ensure_ascii=False, indent=2),
        file_name=f"pro_ai_session_{datetime.now():%Y%m%d_%H%M}.json",
        mime="application/json",
    )
    uploaded = st.file_uploader("⬆️ सेशन इम्पोर्ट (JSON)", type=["json"])
    if uploaded is not None:
        try:
            data = json.load(uploaded)
            st.session_state.history    = data.get("history", [])
            st.session_state.rule_stats = data.get("rule_stats", {})
            st.session_state.total_pnl  = data.get("total_pnl", 0.0)
            st.session_state.level      = data.get("level", 1)
            st.session_state.correct    = data.get("correct", 0)
            st.session_state.total      = data.get("total", 0)
            st.session_state.alert = "✅ सेशन इम्पोर्ट सफल!"
            rerun()
        except Exception as e:
            st.error(f"इम्पोर्ट फेल: {e}")

    st.markdown("---")
    st.caption("⚠️ यह गेम RNG-आधारित है। कोई भी AI 100% सटीक भविष्यवाणी नहीं कर सकता। "
               "इसे केवल पैटर्न-एनालिसिस और मनी-मैनेजमेंट टूल की तरह इस्तेमाल करें।")

# ==========================================================
# 🎯 MAIN UI
# ==========================================================
st.title("🎯 Pro Master AI v2 — Silent Movement Edition")

col_left, col_right = st.columns([1.15, 1])

# ---------------- LEFT: PREDICTION ----------------
with col_left:
    st.markdown("### 🤖 एआई लाइव प्रिडिक्शन")

    if len(st.session_state.history) >= 2:
        result = run_engine(st.session_state.history)
        st.session_state.last_pred  = result
        st.session_state.last_fired = result["fired"]

        box_color = ("#28a745" if "Green" in result["color"]
                     else "#dc3545" if "Red" in result["color"]
                     else "#6f42c1")

        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1f4068,#162447);
                    padding:20px; border-radius:14px; border:3px solid {box_color};
                    text-align:center;">
            <h3 style="margin:0;color:#66fcf1;font-size:16px;letter-spacing:1px;">
                एआई की साइलेंट चाल
            </h3>
            <h1 style="font-size:46px;margin:10px 0;color:#ffffff;">
                {result['size']} &nbsp;|&nbsp; #{result['number']}
            </h1>
            <h3 style="margin:0;color:#ffcc00;">रंग: {result['color']}</h3>
            <h4 style="margin-top:10px;color:#ff6584;">
                लेवल {st.session_state.level}/8 &nbsp;•&nbsp; बेट: ₹ {current_bet()}
            </h4>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, result["confidence"] / 100))
        c1, c2, c3 = st.columns(3)
        c1.metric("सटीकता", f"{result['confidence']}%")
        c2.metric("वोट मार्जिन", f"{result['margin']*100:.0f}%")
        c3.metric("सक्रिय रूल्स", len(result["fired"]))

        with st.expander("🔍 रूल-बाय-रूल वोट ब्रेकडाउन", expanded=True):
            if result["details"]:
                df = pd.DataFrame(result["details"])
                df["Conf"] = (df["Conf"] * 100).round(0).astype(int).astype(str) + "%"
                df["Acc"]  = (df["Acc"]  * 100).round(0).astype(int).astype(str) + "%"
                df["Eff.Weight"] = df["Eff.Weight"].round(1)
                df["Score"] = df["Score"].round(2)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("अभी कोई रूल ट्रिगर नहीं हुआ — फॉलबैक प्रोबेबिलिटी इस्तेमाल हो रही है।")

        with st.expander("🎲 नंबर प्रोबेबिलिटी डिस्ट्रिब्यूशन"):
            probs = result["num_probs"]
            if probs:
                pdf = pd.DataFrame(
                    {"नंबर": list(probs.keys()),
                     "प्रोबेबिलिटी": [round(v * 100, 2) for v in probs.values()]}
                ).sort_values("नंबर")
                st.bar_chart(pdf.set_index("नंबर"))
    else:
        st.warning("⚠️ एआई को पैटर्न सीखने के लिए कम से कम 2 नंबर दर्ज करें।")

    st.markdown("### 💬 एआई मेंटोर फीडबैक")
    st.info(st.session_state.commentary)

    # ------- Rule leaderboard -------
    with st.expander("🧠 एआई सेल्फ-लर्निंग लीडरबोर्ड"):
        rows = []
        for r in BASE_WEIGHTS:
            ew, acc = eff_weight(r)
            rs = st.session_state.rule_stats.get(r, {"wins": 0, "trials": 0})
            rows.append({
                "रूल": r,
                "बेस वेट": BASE_WEIGHTS[r],
                "लाइव सटीकता": f"{acc*100:.0f}%",
                "प्रयोग": rs["trials"],
                "जीत": rs["wins"],
                "प्रभावी वेट": round(ew, 1),
            })
        lb = pd.DataFrame(rows).sort_values("प्रभावी वेट", ascending=False)
        st.dataframe(lb, use_container_width=True, hide_index=True)

# ---------------- RIGHT: INPUT & STATS ----------------
with col_right:
    st.markdown("### 📥 बल्क डेटा लोड")
    batch = st.text_area("नंबर कॉमा से डालें (जैसे: 5,8,7,2,0,9):", height=70)
    if st.button("🚀 डेटा प्रोसेस करें", use_container_width=True):
        try:
            raw = [int(x.strip()) for x in batch.split(",")
                   if x.strip().isdigit() and 0 <= int(x.strip()) <= 9]
            if len(raw) >= 2:
                st.session_state.history = [
                    {"number": n, "size": num_size(n),
                     "color": num_color(n), "ts": datetime.now().isoformat(timespec="seconds")}
                    for n in raw[-80:]
                ]
                st.session_state.alert = f"✅ {len(raw)} नंबर लोड हो गए।"
                rerun()
            else:
                st.error("कम से कम 2 वैध नंबर चाहिए।")
        except Exception:
            st.error("❌ गलत फॉर्मेट।")

    st.markdown("---")
    st.markdown("### 🔄 वास्तविक रिजल्ट दर्ज करें")

    if st.session_state.alert:
        st.success(st.session_state.alert)
        st.session_state.alert = ""

    quick = st.columns(10)
    for i in range(10):
        if quick[i].button(str(i), key=f"q{i}", use_container_width=True):
            st.session_state["pending_num"] = i

    live_num = st.number_input(
        "आया हुआ नया नंबर (0-9)",
        min_value=0, max_value=9,
        value=st.session_state.get("pending_num", 0),
        key="live_num_input"
    )

    if st.button("✨ नंबर सबमिट करें", type="primary", use_container_width=True):
        act_size, act_color = num_size(live_num), num_color(live_num)
        bet = current_bet()
        pred = st.session_state.last_pred

        if pred is not None and st.session_state.last_fired:
            st.session_state.total += 1
            update_learning(st.session_state.last_fired, act_size)

            if act_size == pred["size"]:
                st.session_state.correct += 1
                st.session_state.total_pnl += bet * 0.95
                st.session_state.level = 1
                st.session_state.commentary = (
                    f"🎯 शानदार! एन्सेम्बल सही रहा। जीत ₹{bet * 0.95:.2f} — लेवल 1 पर रीसेट।"
                )
            else:
                st.session_state.total_pnl -= bet
                st.session_state.level = st.session_state.level % 8 + 1
                st.session_state.commentary = (
                    f"📉 गलत अनुमान। ₹{bet} गए। अब लेवल {st.session_state.level} — "
                    f"गलत रूल्स की सटीकता गिराई गई है।"
                )
        else:
            st.session_state.commentary = "पहला परिणाम दर्ज हुआ। अगली चाल से एन्सेम्बल सक्रिय होगा।"

        st.session_state.history.append({
            "number": live_num, "size": act_size,
            "color": act_color, "ts": datetime.now().isoformat(timespec="seconds")
        })
        if len(st.session_state.history) > 80:
            st.session_state.history.pop(0)

        st.session_state.pnl_curve.append(round(st.session_state.total_pnl, 2))
        st.session_state["pending_num"] = 0
        st.session_state.alert = f"✅ दर्ज: #{live_num} ({act_size} / {act_color})"
        rerun()

    # ------- Performance -------
    st.markdown("### 📊 परफॉरमेंस ट्रैकर")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Net P/L", f"₹ {st.session_state.total_pnl:.2f}")
    m2.metric("लेवल", f"L-{st.session_state.level}/8")
    acc = (st.session_state.correct / st.session_state.total * 100
           if st.session_state.total else 0)
    m3.metric("सटीकता", f"{acc:.1f}%")
    m4.metric("कुल प्रेडिक्शन", st.session_state.total)

    if st.session_state.pnl_curve:
        st.line_chart(pd.DataFrame(
            {"P/L": st.session_state.pnl_curve},
            index=range(1, len(st.session_state.pnl_curve) + 1)
        ))

    # ------- History -------
    if st.session_state.history:
        st.markdown("### 📜 हाल का इतिहास")
        hist_df = pd.DataFrame(st.session_state.history[-25:][::-1])
        hist_df.index = range(1, len(hist_df) + 1)
        st.dataframe(hist_df[["number", "size", "color"]],
                     use_container_width=True, height=220)

        with st.expander("📈 साइज डिस्ट्रिब्यूशन (पूरा सेशन)"):
            dist = Counter(h["size"] for h in st.session_state.history)
            st.bar_chart(pd.DataFrame(
                {"गिनती": [dist.get("Big", 0), dist.get("Small", 0)]},
                index=["Big", "Small"]
            ))

    if st.button("🔄 इंजन रीसेट करें", use_container_width=True):
        for k in ["history", "rule_stats", "total_pnl", "pnl_curve", "correct",
                  "total", "last_pred", "last_fired"]:
            st.session_state.pop(k, None)
        st.session_state.level = 1
        st.session_state.alert = "इंजन रीसेट हो गया।"
        init_state()
        rerun()
