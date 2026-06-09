import streamlit as st
import math

st.title("Correct Score Helper")
st.caption("For education only. Bet responsibly.")

h1 = st.number_input("Home scored avg", 0.0, 5.0, 1.8, 0.1)
h2 = st.number_input("Home conceded avg", 0.0, 5.0, 1.0, 0.1)
a1 = st.number_input("Away scored avg", 0.0, 5.0, 1.5, 0.1)
a2 = st.number_input("Away conceded avg", 0.0, 5.0, 1.2, 0.1)

odds_input = st.text_input("Odds like 1-0:8.5,2-1:9.0,1-1:7.5")

def calc(avg_h, avg_a):
    out = {}
    for h in range(3):
        for a in range(3):
            ph = (math.exp(-avg_h) * avg_h**h) / math.factorial(h)
            pa = (math.exp(-avg_a) * avg_a**a) / math.factorial(a)
            out[f"{h}-{a}"] = ph * pa
    return out

if st.button("Run"):
    avg_h = (h1 + a2) / 2
    avg_a = (a1 + h2) / 2
    st.write(f"**Expected Goals:** Home {avg_h:.2f} - Away {avg_a:.2f}")

    probs = calc(avg_h, avg_a)

    odds = {}
    for pair in odds_input.split(","):
        if ":" in pair:
            k, v = pair.split(":")
            odds[k.strip()] = float(v.strip())

    st.subheader("Top Value Bets")
    for score, p in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5]:
        if score in odds:
            model_odds = 1 / p if p > 0 else 999
            value = ((odds[score] / model_odds) - 1) * 100
            if value > 0:
                st.write(f"{score}: {round(p*100,1)}% | Odds {odds[score]} | Value {round(value,1)}%")

    if not any(score in odds for score in probs.keys()):
        st.info("Enter odds to see value bets")
