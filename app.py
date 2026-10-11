"""Ember and Tide: an AI quiz game for Units I and II of Artificial Intelligence.

Two heroes cross six chambers. Every question is a pit. A correct answer carries the
heroes across. A wrong answer costs a life and the heroes stay where they are: the same pit
comes back with a new question. Each chamber has its own look and its own rule.
Run with:  streamlit run app.py

Layout notes
- Every screen is built to fit one viewport (no page scroll). Chrome is hidden, the HUD is a
  single top strip, and question screens use two columns: question on the left, answers on the right.
- Each screen change swaps a keyed container, which replays a short fade/slide-in.
- The heroes hop across the pit when an answer is correct.
"""
import html
import json
import random
import re
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from questions import QUESTIONS

st.set_page_config(page_title="Ember and Tide", layout="wide", initial_sidebar_state="collapsed")

# ----------------------------------------------------------------------------
# Game data
# ----------------------------------------------------------------------------
for _i, _q in enumerate(QUESTIONS):
    _q["id"] = _i

ZONES = {
    1: ("Gate of Minds", "Foundations and the Turing Test",
        "AI can be judged by how it thinks or how it acts, and by whether it copies people or is rational. Modern AI aims at acting rationally."),
    2: ("Hall of Agents", "Rational agents and environments",
        "An agent maps percepts to actions. Judge it with a performance measure, and describe its task with PEAS and the properties of its environment."),
    3: ("Maze of Problems", "State spaces and production systems",
        "A problem has an initial state, actions, a transition model, a goal test and a path cost. Search is then a walk through the state-space graph."),
    4: ("Blind Bridge", "BFS, DFS and iterative deepening",
        "Blind search has no idea how close a state is to the goal. BFS goes shallow first, DFS goes deep first, and iterative deepening mixes both."),
    5: ("Heuristic Peak", "Hill climbing, heuristics and best-first search",
        "A heuristic estimates the distance to the goal. Hill climbing climbs greedily and can get stuck. Best-first and A* keep a frontier."),
    6: ("Vault of Constraints", "CSP and means-end analysis",
        "A CSP has variables, domains and constraints. Means-end analysis shrinks the gap between state and goal by picking operators and sub-goals."),
}

# Each chamber has its own look (THEMES, drawn in scene_html) and its own rule (RULES, applied in
# init_question, resolve and lifelines).
THEMES = {
    1: dict(bg="#161330", wall="#2a2548", stone="#2c2750", top="#4a4380", accent="#a78bfa", gem="#f4c95d", motif="gate"),
    2: dict(bg="#0f2230", wall="#1f4156", stone="#1f3a4a", top="#3f7390", accent="#5ad1c3", gem="#7ef0d0", motif="eyes"),
    3: dict(bg="#1d1a12", wall="#3f3722", stone="#3a3322", top="#6b5d36", accent="#d9a441", gem="#f4c95d", motif="maze"),
    4: dict(bg="#1a2230", wall="#2c3a4c", stone="#3b3f4a", top="#8a7a5a", accent="#9bb4d6", gem="#e9eefc", motif="fog"),
    5: dict(bg="#2a1722", wall="#4a2a3c", stone="#47303f", top="#c9a6b8", accent="#ff8fab", gem="#ffd6e0", motif="peaks"),
    6: dict(bg="#0e1a14", wall="#1d3a2a", stone="#1f3a2c", top="#4f8f6a", accent="#6ee7a0", gem="#b9f5d2", motif="vault"),
}
RULES = {
    1: ("Warm-up", "Your first wrong answer in this chamber costs no life."),
    2: ("Torchlight", "The streak bonus is doubled."),
    3: ("Open maps", "Hints are free and do not use up a charge."),
    4: ("Fog", "10 seconds less on every question, and +25 points for each correct answer."),
    5: ("Summit wind", "Every correct answer scores x1.25."),
    6: ("Sealed vault", "All lifelines are locked. Every correct answer scores x1.5."),
}

# per = questions per chamber, target = difficulty the picker aims for
LEVELS = {
    "Easy": dict(per=3, hearts=6, time=45, target=1, text="gentle questions, 6 lives, 45 s each"),
    "Medium": dict(per=5, hearts=5, time=30, target=2, text="balanced questions, 5 lives, 30 s each"),
    "Hard": dict(per=5, hearts=4, time=25, target=3, text="toughest questions, 4 lives, 25 s each"),
    "Full Temple": dict(per=99, hearts=5, time=30, target=2, text="every question, 5 lives, 30 s each"),
}
DIFF_LABEL = {1: "Easy", 2: "Medium", 3: "Hard"}
LETTERS = "ABCDEFGH"
FIXED_ORDER_FORMATS = ("True / False", "Assertion–Reason")
LB_FILE = Path(__file__).with_name("leaderboard.json")

EMBER, TIDE, GOLD = "#ff7a3d", "#35c6d9", "#f4c95d"
SCENE_H = 142      # px height of the pit scene
GRAPH_H = 178      # px height of the graph picture

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');

/* ---- one-screen shell: no page scroll, no Streamlit chrome ------------------ */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  height: 100vh; overflow: hidden !important; }
[data-testid="stMain"] { overflow-y: auto !important; }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"],
[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"], footer, #MainMenu { display: none !important; }
[data-testid="stMainBlockContainer"], .block-container {
  padding: clamp(14px, 3vh, 28px) 2.4rem clamp(18px, 4vh, 36px) !important; max-width: 1240px !important;
  height: auto; min-height: 100vh; box-sizing: border-box; overflow: visible; }
[data-testid="stVerticalBlock"] { gap: clamp(10px, 1.7vh, 18px) !important; }
[data-stale="true"] { opacity: 1 !important; }                 /* no grey flash while a rerun is in flight */
[data-testid="stMarkdownContainer"], [data-testid="stMarkdown"] { margin: 0 !important; }
.stMarkdown p { margin: 0 0 .25rem 0; }
.hud, .tip { margin: 0; }
.scn, .gph { margin: 0 0 clamp(14px, 2.6vh, 28px) 0; }
@media (max-width: 760px), (max-height: 560px) {                /* phones and tiny windows: allow scrolling */
  html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] { overflow: auto !important; height: auto; }
  [data-testid="stMainBlockContainer"], .block-container { height: auto; overflow: visible; }
}

/* ---- screen transition: the page container is re-keyed on every screen change -- */
@keyframes pagein_a { from { opacity: 0; transform: translateY(16px) scale(.985); } to { opacity: 1; transform: none; } }
@keyframes pagein_b { from { opacity: 0; transform: translateY(16px) scale(.985); } to { opacity: 1; transform: none; } }
[class*="st-key-page_a_"] { animation: pagein_a .45s cubic-bezier(.2,.7,.2,1) both; }
[class*="st-key-page_b_"] { animation: pagein_b .45s cubic-bezier(.2,.7,.2,1) both; }
@media (prefers-reduced-motion: reduce) { [class*="st-key-page_"] { animation: none !important; } }

/* ---- type ---------------------------------------------------------------- */
h1, h2, h3 { font-family: 'Bungee', 'Arial Black', sans-serif !important; font-weight: 400 !important;
             letter-spacing: .01em; padding: 0 !important; margin: .6vh 0 1.2vh 0 !important; line-height: 1.2 !important; }
[data-testid="stHeading"] { margin-bottom: 1vh; }
.tide-title { margin: 1vh 0 .4vh 0 !important; }
h1 { font-size: clamp(1.8rem, 5vh, 2.8rem) !important; } h2 { font-size: clamp(1.4rem, 4vh, 2.2rem) !important; } h3 { font-size: clamp(1.1rem, 2.8vh, 1.6rem) !important; }
.tide-title b { color: #ff7a3d; font-weight: 400; } .tide-title i { color: #35c6d9; font-style: normal; }
.qtext { font-size: clamp(1.05rem, 3.1vh, 1.7rem); line-height: 1.35; white-space: pre-wrap; margin: .4vh 0 .6vh 0;
         max-height: 26vh; overflow-y: auto; scrollbar-width: thin; }
.chip { display:inline-block; font-size:.7rem; letter-spacing:.08em; text-transform:uppercase; font-weight:700;
        padding:2px 9px; border:2px solid #3b3562; border-radius:3px; margin-right:6px; color:#a7a1c9; }
.chip.fmt { color:#f4c95d; border-color:#6b5a22; }
.chip.ember { color:#ff7a3d; border-color:#a8431a; } .chip.tide { color:#35c6d9; border-color:#1b7f8c; }
.fb-ok { border:2px solid #6ee7a0; background:#12291f; padding:12px 14px; border-radius:6px; animation: pop .35s ease both; }
.fb-no { border:2px solid #ff5d6c; background:#2e121a; padding:12px 14px; border-radius:6px; animation: pop .35s ease both; }
.fb-ok, .fb-no { max-height: 34vh; overflow-y: auto; scrollbar-width: thin; font-size: clamp(.95rem, 2.2vh, 1.2rem); padding: 1.6vh 1.2rem; }
@keyframes pop { from { opacity: 0; transform: scale(.96); } to { opacity: 1; transform: none; } }
.tip { border:2px dashed #6b5a22; background:#2c2610; color:#f4c95d; padding:1.4vh 1rem; border-radius:6px; font-size:clamp(.92rem, 2.1vh, 1.15rem); line-height:1.45; }

/* ---- HUD ------------------------------------------------------------------ */
.hud { display:flex; align-items:center; gap:22px; flex-wrap:wrap; font-size:clamp(.9rem, 2.3vh, 1.2rem); color:#a7a1c9; }
.hud b { color:#f0ecff; }
.hud .brand { font-family:'Bungee','Arial Black',sans-serif; font-size:clamp(1.1rem, 3vh, 1.6rem); color:#f0ecff; }
.hud .brand i { color:#35c6d9; font-style:normal; } .hud .brand em { color:#ff7a3d; font-style:normal; }
.hud .hearts { color:#ff5d6c; font-size:1.15rem; letter-spacing:.05em; }
.pbar { height:.9vh; min-height:5px; background:#12101c; border:1px solid #3b3562; border-radius:3px; overflow:hidden; margin-top:2px; }
.pbar > div { height:100%; background:linear-gradient(90deg,#ff7a3d,#f4c95d); transition: width .8s cubic-bezier(.3,.7,.2,1); }
.cb { display:flex; align-items:center; gap:10px; font-size:.9rem; margin-bottom:.35rem; }
.cb span:first-child { flex:0 0 11rem; } .cb .pbar { flex:1; height:9px; } .cb span:last-child { flex:0 0 3rem; text-align:right; color:#a7a1c9; }
.mrow { font-size:.92rem; padding-top:.45rem; }

/* ---- compact controls ----------------------------------------------------- */
.stButton > button { width: 100%; padding: .3rem .6rem; min-height: clamp(2.3rem, 5.4vh, 3.3rem); font-size: clamp(.9rem, 2.1vh, 1.1rem); transition: transform .12s ease, filter .12s ease; }
.stButton > button:not(:disabled):hover { transform: translateY(-1px); }
[class*="st-key-ans"] [role="radiogroup"] { gap: clamp(8px, 1.4vh, 14px); width: 100%; }
[class*="st-key-ans"] label[data-baseweb="radio"] { width: 100%; box-sizing: border-box; border: 1px solid #3b3562; border-radius: 8px;
  padding: clamp(8px, 1.5vh, 16px) 1rem; margin: 0; background: #1b1838; transition: background .15s ease, border-color .15s ease; }
[class*="st-key-ans"] label[data-baseweb="radio"] p, [class*="st-key-ans"] label[data-baseweb="radio"] div { font-size: clamp(.95rem, 2.3vh, 1.3rem) !important; }
[class*="st-key-ans"] label[data-baseweb="radio"]:hover { background: #1d1a3a; border-color: #6b5a22; }
[class*="st-key-ans"] label[data-baseweb="radio"]:has(input:checked) { background: #2a2350; border-color: #f4c95d; }
[data-testid="stTextInput"] input, [data-baseweb="select"] > div { min-height: clamp(2.3rem, 5.4vh, 3.2rem); font-size: clamp(.95rem, 2.2vh, 1.2rem); }

/* ---- fill the window: everything is sized from the viewport height ---------- */
.scn { width:100%; aspect-ratio:1000/167; max-height:26vh; min-height:110px; background:#161330; border-radius:8px; overflow:hidden; }
.scn svg { display:block; width:100%; height:100%; }
[class*="st-key-scene_title"] .scn { max-height:20vh; }
.gph { width:100%; height:26vh; min-height:140px; }
.gph svg { display:block; width:100%; height:100%; background:#12101c; border:2px solid #3b3562; border-radius:8px; box-sizing:border-box; }

[class*="st-key-panel"] { --ph: 45vh; min-height: var(--ph) !important; box-sizing: border-box; margin-top: clamp(16px, 3vh, 32px) !important;
  border: 1px solid #3b3562 !important; border-radius: 10px; background: #161330; padding: clamp(14px, 2.6vh, 26px) 1.8rem !important; gap: clamp(10px, 1.7vh, 18px);
  display: flex !important; flex-direction: column; }
[class*="st-key-panel_t_"] { --ph: 38vh; }
[class*="st-key-panel_xl"] { --ph: 78vh; }
[data-testid="stHorizontalBlock"] { align-items: stretch !important; }
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] { height: 100%; }
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > div:has(> [class*="st-key-panel"]) { flex: 1; display: flex; flex-direction: column; }
[data-testid="stColumn"] [class*="st-key-panel"] { flex: 1; }
[class*="st-key-panel_l"] { justify-content: space-between; }
[class*="st-key-panel_r"], [class*="st-key-panel_c"] { justify-content: center; }
[class*="st-key-panel"] .stMarkdown p { font-size: clamp(1rem, 2.4vh, 1.3rem); }
[class*="st-key-panel"] [data-testid="stCaptionContainer"] { margin-bottom: .6vh; }
.tide-title { font-size: clamp(2.2rem, 6.4vh, 3.6rem) !important; }

/* ---- scene animation (inline SVG, so the page CSS drives it) ------------------ */
.scn .hop { animation: hop .9s ease-in-out .15s; }
@keyframes hop { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-24px); } }
.scn .bub { animation: rise 1.1s ease-out infinite; }
.scn .bub:nth-of-type(2n) { animation-delay: .35s; }
@keyframes rise { from { transform: translateY(8px); opacity: 1; } to { transform: translateY(-16px); opacity: 0; } }
.scn .door { transform-box: fill-box; transform-origin: 100% 50%; }
.scn .door.open { transform: scaleX(.14); animation: dopen .7s ease .7s both; }
@keyframes dopen { from { transform: scaleX(1); } to { transform: scaleX(.14); } }
.scn .gem { animation: glint 2.4s ease-in-out infinite; }
@keyframes glint { 50% { opacity: .6; } }
.rule { border:2px solid #3b3562; border-left-width:6px; background:#12101c; padding:1.2vh 1rem; border-radius:6px;
        font-size:clamp(.92rem, 2.1vh, 1.15rem); line-height:1.45; }
.rule b { color:#f0ecff; }
@media (prefers-reduced-motion: reduce) { .scn * { animation: none !important; } }
</style>
"""


def show_html(content, height):
    """Embed an HTML string. st.iframe is the current API; older Streamlit versions use components.html."""
    if hasattr(st, "iframe"):
        st.iframe(content, height=height)
    else:
        components.html(content, height=height)


def page(key):
    """Keyed container. A new key means a new DOM node, which replays the fade/slide-in transition.
    The a/b suffix alternates so the CSS animation name changes even if the browser reuses the node."""
    S = st.session_state
    if S.get("_pk") != key:
        S["_pk"] = key
        S["_pn"] = S.get("_pn", 0) + 1
    safe = re.sub(r"[^A-Za-z0-9_]", "_", key)
    return st.container(key=f"page_{'a' if S['_pn'] % 2 else 'b'}_{safe}")


# ----------------------------------------------------------------------------
# Scene: two heroes crossing one pit per question (drawn as SVG, animated with CSS)
# ----------------------------------------------------------------------------
def hero_svg(kind):
    col = EMBER if kind == "ember" else TIDE
    if kind == "ember":
        head = ('<path d="M-10 -30 C-14 -46 -3 -50 0 -64 C6 -52 14 -46 10 -30 Z" fill="#f4c95d"/>'
                '<path d="M-6 -30 C-8 -40 -1 -44 0 -52 C4 -44 8 -40 6 -30 Z" fill="#ff7a3d"/>')
    else:
        head = '<path d="M0 -66 C10 -52 13 -43 10 -30 L-10 -30 C-13 -43 -10 -52 0 -66 Z" fill="#8be3ee"/>'
    return (head + f'<rect x="-12" y="-32" width="24" height="32" rx="5" fill="{col}"/>'
            '<circle cx="-4" cy="-20" r="3.4" fill="#fff"/><circle cx="4" cy="-20" r="3.4" fill="#fff"/>'
            '<circle cx="-3.2" cy="-19.6" r="1.6" fill="#12101c"/><circle cx="4.8" cy="-19.6" r="1.6" fill="#12101c"/>'
            '<rect x="-9" y="-3" width="7" height="7" rx="2" fill="#12101c"/><rect x="2" y="-3" width="7" height="7" rx="2" fill="#12101c"/>')





def decor(motif, gy, wall, accent):
    """Background decoration that gives each chamber its own look."""
    d = []
    if motif == "gate":                     # arched gates joined by a thought line
        for x in (120, 340, 560, 780):
            d.append(f'<path d="M{x} {gy} V82 A34 34 0 0 1 {x + 68} 82 V{gy}" fill="none" stroke="{wall}" stroke-width="5"/>')
            d.append(f'<circle cx="{x + 34}" cy="70" r="5" fill="{accent}" opacity=".5"/>')
        d.append(f'<path d="M154 70 L374 70 L594 70 L814 70" stroke="{accent}" stroke-width="1.5" opacity=".35" fill="none" stroke-dasharray="4 6"/>')
    elif motif == "eyes":                   # sensors watching the hall
        for i, x in enumerate(range(110, 960, 130)):
            y = 78 + (i % 2) * 18
            d.append(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="13" fill="none" stroke="{wall}" stroke-width="4"/>')
            d.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{accent}" opacity=".55"/>')
            d.append(f'<line x1="{x}" y1="{y + 13}" x2="{x}" y2="{gy}" stroke="{wall}" stroke-width="2" stroke-dasharray="3 5"/>')
    elif motif == "maze":                   # maze walls
        d.append(f'<path d="M0 100 H90 V60 H170 V100 H250 V50 H340 V95 H420 V60 H520 V105 H600 V55 H690 V100 H770 V60 H860 V95 H1000" fill="none" stroke="{wall}" stroke-width="5"/>')
        d.append(f'<path d="M0 118 H60 V80 H140 V118 H220 V70 H300 V110 H380 V76 H470 V118 H560 V72 H650 V112 H730 V78 H820 V118 H920 V84 H1000" fill="none" stroke="{accent}" stroke-width="2" opacity=".3"/>')
    elif motif == "fog":                    # fog banks and a rope line
        for x, y, rx in ((140, 70, 120), (420, 92, 150), (700, 66, 130), (930, 96, 110)):
            d.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="22" fill="#ffffff" opacity=".07"/>')
        d.append(f'<path d="M0 {gy - 14} Q250 {gy - 30} 500 {gy - 14} T1000 {gy - 14}" fill="none" stroke="{accent}" stroke-width="2" opacity=".4" stroke-dasharray="2 5"/>')
    elif motif == "peaks":                  # snowy mountains
        for x, h, w in ((80, 60, 110), (260, 70, 140), (470, 55, 100), (660, 80, 150), (880, 65, 120)):
            top = gy - h
            d.append(f'<polygon points="{x - w},{gy} {x},{top} {x + w},{gy}" fill="{wall}"/>')
            d.append(f'<polygon points="{x - w * 0.28:.0f},{top + h * 0.28:.0f} {x},{top} {x + w * 0.28:.0f},{top + h * 0.28:.0f}" fill="#ffffff" opacity=".55"/>')
    elif motif == "vault":                  # riveted vault panels
        for i in range(7):
            x = 70 + i * 120
            d.append(f'<rect x="{x}" y="52" width="86" height="58" rx="4" fill="none" stroke="{wall}" stroke-width="3"/>')
            for dx, dy in ((12, 12), (74, 12), (12, 46), (74, 46)):
                d.append(f'<circle cx="{x + dx}" cy="{52 + dy}" r="3" fill="{accent}" opacity=".45"/>')
    return "".join(d)


def scene_html(zone, n, stone, door_open, splash_pit, from_stone=None):
    """SVG scene in the chamber's own theme. stone = stone the heroes stand on.
    splash_pit = pit the active hero just fell into (wrong answer): that hero sinks and stays on this stone.
    from_stone = where the heroes start when they hop to `stone` (correct answer)."""
    T = THEMES[zone]
    W, H, gy = 1000, 175, 125
    sp = 860 / n
    sw = min(72, sp * 0.58)
    xs = [70 + i * sp for i in range(n + 1)]
    scale = max(0.52, min(1, sp / 110))
    off = min(15, sw * 0.24)
    s = [f'<div class="scn"><svg viewBox="0 8 {W} {H - 8}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">',
         f'<rect y="0" width="{W}" height="{H}" fill="{T["bg"]}"/>']
    for r in range(5):
        s.append(f'<rect x="0" y="{r * 30 + 22}" width="{W}" height="1" fill="{T["wall"]}"/>')
    s.append(decor(T["motif"], gy, T["wall"], T["accent"]))
    s.append(f'<text x="18" y="38" font-family="Arial Black, sans-serif" font-size="16" fill="{T["accent"]}">'
             f'{html.escape(ZONES[zone][0].upper())}</text>')
    for i in range(n):
        x1, x2 = xs[i] + sw / 2, xs[i + 1] - sw / 2
        lava = i % 2 == 1                       # pit i is the nemesis of the hero who answers question i
        s.append(f'<rect x="{x1}" y="{gy + 10}" width="{x2 - x1}" height="{H - gy - 10}" fill="{EMBER if lava else TIDE}" opacity=".85"/>')
        s.append(f'<rect x="{x1}" y="{gy + 10}" width="{x2 - x1}" height="3" fill="#fff" opacity=".35"/>')
        cx = (x1 + x2) / 2
        if i == splash_pit:
            s.append(f'<circle class="bub" cx="{cx - 3}" cy="{gy + 2}" r="3.2" fill="#fff"/>'
                     f'<circle class="bub" cx="{cx + 5}" cy="{gy - 8}" r="2.6" fill="#fff"/>'
                     f'<circle class="bub" cx="{cx}" cy="{gy - 18}" r="2" fill="#fff"/>')
        if i >= stone:                           # gem still waiting
            s.append(f'<polygon class="gem" points="{cx},{gy - 62} {cx + 8},{gy - 52} {cx},{gy - 42} {cx - 8},{gy - 52}" fill="{T["gem"]}" stroke="{T["accent"]}" stroke-width="2"/>')
    for i in range(n + 1):
        s.append(f'<rect x="{xs[i] - sw / 2}" y="{gy}" width="{sw}" height="{H - gy}" fill="{T["stone"]}" stroke="{T["wall"]}" stroke-width="2"/>'
                 f'<rect x="{xs[i] - sw / 2}" y="{gy}" width="{sw}" height="5" fill="{T["top"]}"/>')
    dx = xs[n]
    s.append(f'<rect x="{dx - 22}" y="{gy - 70}" width="44" height="70" rx="4" fill="#12101c" stroke="{T["accent"]}" stroke-width="3"/>')
    s.append(f'<rect class="door{" open" if door_open else ""}" x="{dx - 18}" y="{gy - 66}" width="36" height="66" fill="{T["gem"]}" opacity=".92"/>')
    faller = ("ember", "tide")[splash_pit % 2] if splash_pit is not None else None
    # The hop and the fall are keyframes written with plain numbers. Streamlit's markdown sanitiser removes CSS
    # custom properties (--x) from inline styles, so keyframes that read var(--x) would leave the heroes invisible.
    uid = f"{zone}_{n}_{stone}_{from_stone}_{splash_pit}"
    kf = []
    for kind, sign in (("ember", -1), ("tide", 1)):
        tx = xs[stone] + sign * off
        here = f"transform:translate({tx}px,{gy}px) scale({scale})"
        if kind == faller:                       # wrong answer: the active hero sinks into the pit it tried to cross
            px = (xs[splash_pit] + xs[splash_pit + 1]) / 2
            name = f"fall_{kind}_{uid}"
            kf.append(f"@keyframes {name}{{0%{{transform:translate({tx}px,{gy}px) scale({scale});opacity:1}}"
                      f"45%{{transform:translate({(tx + px) / 2}px,{gy - 34}px) scale({scale});opacity:1}}"
                      f"100%{{transform:translate({px}px,{gy + 34}px) scale({scale});opacity:.35}}}}")
            s.append(f'<g class="hero" style="transform:translate({px}px,{gy + 34}px) scale({scale});opacity:.35;'
                     f'animation:{name} .9s cubic-bezier(.4,0,.6,1) .1s both"><g>{hero_svg(kind)}</g></g>')
            continue
        anim = ""
        if from_stone is not None:               # correct answer: hop from the previous stone
            fx = xs[from_stone] + sign * off
            name = f"mv_{kind}_{uid}"
            kf.append(f"@keyframes {name}{{from{{transform:translate({fx}px,{gy}px) scale({scale})}}"
                      f"to{{transform:translate({tx}px,{gy}px) scale({scale})}}}}")
            anim = f";animation:{name} .9s cubic-bezier(.5,0,.2,1) .15s both"
        s.append(f'<g class="hero" style="{here}{anim}"><g class="{"hop" if from_stone is not None else ""}">{hero_svg(kind)}</g></g>')
    s.append("</svg></div>")
    return (f"<style>{''.join(kf)}</style>" if kf else "") + "".join(s)


def countdown_html(remaining):
    """Display-only countdown. The server checks the real time when the answer is submitted."""
    return f"""
    <body style="margin:0;font-family:Arial,sans-serif;color:#f0ecff;background:transparent">
    <div style="display:flex;align-items:center;gap:10px">
      <div style="flex:1;height:10px;background:#12101c;border:1px solid #3b3562;border-radius:4px;overflow:hidden">
        <div id="bar" style="height:100%;width:100%;background:#35c6d9"></div></div>
      <div id="t" style="font-family:monospace;font-size:15px;min-width:42px;text-align:right"></div></div>
    <script>
      const total = {max(remaining, 1):.1f};
      let left = {remaining:.1f};
      function draw() {{
        const v = Math.max(0, Math.ceil(left));
        document.getElementById('t').textContent = v + ' s';
        const b = document.getElementById('bar');
        b.style.width = Math.max(0, left / total * 100) + '%';
        b.style.background = left <= 8 ? '#ff5d6c' : '#35c6d9';
      }}
      draw();
      setInterval(() => {{ left -= 0.25; draw(); }}, 250);
    </script></body>"""


# ----------------------------------------------------------------------------
# Leaderboard (a JSON file on the server, shared by everyone who plays)
# ----------------------------------------------------------------------------
def lb_load():
    try:
        return json.loads(LB_FILE.read_text())
    except Exception:
        return st.session_state.get("lb_mem", [])


def lb_add(entry):
    board = lb_load()
    board.append(entry)
    board.sort(key=lambda e: e["score"], reverse=True)
    board = board[:30]
    st.session_state["lb_mem"] = board
    try:
        LB_FILE.write_text(json.dumps(board))
    except Exception:
        pass


def lb_show(limit=6):
    board = lb_load()
    if not board:
        st.caption("No runs yet. Finish a run to take first place.")
        return
    rows = [{"#": i + 1, "Hero": e["name"], "Level": e["level"], "Accuracy": f'{e["acc"]}%', "Score": e["score"]}
            for i, e in enumerate(board[:limit])]
    h = 35 * (len(rows) + 1) + 3
    try:
        st.dataframe(rows, hide_index=True, width="stretch", height=h)
    except TypeError:                      # older Streamlit
        st.dataframe(rows, hide_index=True, use_container_width=True, height=h)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def answer_text(q):
    if q["mode"] == "c":
        return q["o"][q["a"]]
    if q["mode"] == "f":
        return " / ".join(q["a"])
    if q["mode"] == "m":
        return "\n".join(f"{l}  →  {r}" for l, r in q["m"])
    return "  →  ".join(q["a"])


def run_size(level, zone):
    zones = [zone] if zone else range(1, 7)
    return sum(min(LEVELS[level]["per"], len([q for q in QUESTIONS if q["z"] == z])) for z in zones)


def build_deck(level, zone):
    cfg = LEVELS[level]
    deck, spare = [], {}
    for z in ([zone] if zone else range(1, 7)):
        pool = [q["id"] for q in QUESTIONS if q["z"] == z]
        random.shuffle(pool)
        if cfg["per"] < len(pool):
            pool.sort(key=lambda i: abs(QUESTIONS[i]["d"] - cfg["target"]))   # stable: ties stay shuffled
            pick, spare[z] = pool[:cfg["per"]], pool[cfg["per"]:]
        else:
            pick, spare[z] = pool, []
        pick.sort(key=lambda i: QUESTIONS[i]["d"] + random.random() * 0.9)   # easy to hard inside a chamber
        deck += [(z, i) for i in pick]
    return deck, spare


def zone_info(run, i):
    """(chamber, number of pits in it, pits already crossed in it). A wrong answer does not change k."""
    z = run["deck"][i][0]
    return z, run["pits"][z], run["k"]


def queue_retry(run, q):
    """A wrong answer does not move the heroes. The same pit comes back with a fresh question from the
    chamber's reserve, or, when there is none left (Full Temple), with the missed question one step later."""
    i = run["i"]
    z = run["deck"][i][0]
    reserve = run["spare"].get(z, [])
    if reserve:
        entry, pos = (z, reserve.pop(0)), i + 1
    else:
        same_next = i + 1 < len(run["deck"]) and run["deck"][i + 1][0] == z
        entry, pos = (z, q["id"]), (i + 2 if same_next else i + 1)
    run["deck"].insert(pos, entry)
    run["i"] = i + 1


def hearts_text(run):
    return "".join("♥" if k < run["hearts"] else "♡" for k in range(run["max_hearts"]))


def rank_title(acc, status):
    if status == "fallen":
        return "Fallen Hero"
    return "Archmage of Search" if acc >= 90 else "Temple Warden" if acc >= 75 else "Path Finder" if acc >= 55 else "Apprentice"


# ----------------------------------------------------------------------------
# Run control
# ----------------------------------------------------------------------------
def clean_name(raw):
    """Hero name: any text (a single character is fine), trimmed with inner spaces collapsed. Empty means not entered."""
    return re.sub(r"\s+", " ", (raw or "")).strip()[:18]


def start_run():
    S = st.session_state
    cfg = LEVELS[S.level]
    deck, spare = build_deck(S.level, S.zone)
    pits = {}
    for z, _ in deck:
        pits[z] = pits.get(z, 0) + 1                  # one pit per planned question
    S.run = dict(level=S.level, zone=S.zone, deck=deck, spare=spare, i=0, hearts=cfg["hearts"], max_hearts=cfg["hearts"],
                 score=0, streak=0, best=0, log=[], life=dict(hint=3, cull=2, freeze=2, swap=1),
                 phase="intro", cur=None, t0=time.time(), nonce=0,
                 pits=pits, total_pits=len(deck), k=0, crossed=0, free_used=False)
    S.screen = "run"


def init_question(run):
    z, n, k = zone_info(run, run["i"])
    q = QUESTIONS[run["deck"][run["i"]][1]]
    run["nonce"] += 1
    limit = LEVELS[run["level"]]["time"] + (20 if q["mode"] in ("g", "m") else 0)
    if z == 4:                                        # Fog: less time
        limit = max(10, limit - 10)
    cur = dict(qid=q["id"], start=time.time(), limit=limit, hint=False, culled=False, result=None)
    if q["mode"] == "c":
        order = list(range(len(q["o"])))
        if q["k"] not in FIXED_ORDER_FORMATS:
            random.shuffle(order)
        cur["order"] = order
    elif q["mode"] == "m":
        cur["right"] = random.sample(range(len(q["m"])), len(q["m"]))
    run["cur"] = cur
    run["phase"] = "ask"


def resolve(run, q, ok, given, reason=""):
    cur = run["cur"]
    z, n, k = zone_info(run, run["i"])
    gained, parts, free = 0, [], False
    if ok:
        run["streak"] += 1
        run["best"] = max(run["best"], run["streak"])
        left = max(0, cur["limit"] - (time.time() - cur["start"]))
        base = 60 + 20 * q["d"] - (20 if cur["hint"] else 0)
        speed = round(40 * left / cur["limit"])
        streak_bonus = min(run["streak"], 5) * 10 * (2 if z == 2 else 1)      # Torchlight
        flat = 25 if z == 4 else 0                                             # Fog
        mult = {5: 1.25, 6: 1.5}.get(z, 1)                                     # Summit wind, Sealed vault
        gained = round((base + speed + streak_bonus + flat) * mult)
        run["score"] += gained
        parts = [f"base {base}", f"speed +{speed}", f"streak +{streak_bonus}"]
        if flat:
            parts.append(f"fog +{flat}")
        if mult != 1:
            parts.append(f"chamber x{mult:g}")
        if run["streak"] % 5 == 0 and run["hearts"] < run["max_hearts"]:
            run["hearts"] += 1
            parts.append("a life restored")
    else:
        run["streak"] = 0
        if z == 1 and not run["free_used"]:                                    # Warm-up: first miss is free
            run["free_used"] = True
            free = True
        else:
            run["hearts"] -= 1
    run["log"].append(dict(z=z, qid=q["id"], ok=ok, given=given, gained=gained))
    cur["result"] = dict(ok=ok, gained=gained, parts=parts, reason=reason, given=given, free=free)
    run["phase"] = "fb"


def finish(status):
    S = st.session_state
    run = S.run
    total = len(run["log"])
    right = sum(1 for l in run["log"] if l["ok"])
    acc = round(right / total * 100) if total else 0
    label = run["level"] + (f' · C{run["zone"]}' if run["zone"] else "")
    lb_add(dict(name=clean_name(S.get("name")) or "Hero", score=run["score"], level=label, acc=acc))
    run["status"], run["acc"], run["secs"] = status, acc, round(time.time() - run["t0"])
    S["rev"] = 0
    S["res_view"] = "By chamber"
    S.screen = "result"


# ----------------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------------
def render_title():
    S = st.session_state
    st.markdown(CSS, unsafe_allow_html=True)
    with page("title"):
        with st.container(key="scene_title"):
            st.markdown(scene_html(1, 6, 0, False, None), unsafe_allow_html=True)
        st.markdown("<h1 class='tide-title'><b>Ember</b> and <i>Tide</i></h1>", unsafe_allow_html=True)
        st.write("Two heroes, six chambers, one temple of AI concepts. Ember cannot touch water and Tide cannot touch lava. "
                 "Each question is a pit: answer right and your heroes cross. Answer wrong and one falls in, loses a life, and must try the same pit again. "
                 "Every chamber has its own look and its own rule.")
        left, right = st.columns([3, 2], gap="medium")
        with left:
            with st.container(key="panel_t_l"):
                c1, c2 = st.columns(2, gap="medium")
                S.name = c1.text_input("Hero name for the leaderboard", value=S.get("name", ""), max_chars=18, placeholder="Name or character")
                names = {0: "All chambers", **{z: f"{z}. {ZONES[z][0]}" for z in ZONES}}
                S.zone = c2.selectbox("Pick where to play", list(names), format_func=lambda z: names[z], index=S.get("zone", 0))
                S.level = st.radio("Pick a level", list(LEVELS), index=list(LEVELS).index(S.get("level", "Medium")),
                                   format_func=lambda k: f"{k} ({run_size(k, S.zone)})", horizontal=True)
                st.caption(f"{LEVELS[S.level]['text']}  ·  {run_size(S.level, S.zone)} questions")
                valid = bool(clean_name(S.name))
                if not valid:
                    st.caption("Enter a name or a character to start.")
                if st.button("Enter the temple", type="primary", disabled=not valid):
                    if clean_name(S.name):                  # re-check on the server, the disabled state is only cosmetic
                        S.name = clean_name(S.name)
                        start_run()
                        st.rerun()
        with right:
            with st.container(key="panel_t_r"):
                st.subheader("Leaderboard")
                lb_show()
                st.caption(f"{len(QUESTIONS)} questions · 7 formats · lifelines: Hint, Cull, Freeze, Swap")


def hud(run):
    total = run["total_pits"]
    z = zone_info(run, run["i"])[0]
    pct = run["crossed"] / total * 100 if total else 0
    a, b = st.columns([9, 1], vertical_alignment="center")
    a.markdown(
        "<div class='hud'><span class='brand'><em>Ember</em> <i>Tide</i></span>"
        f"<span>Chamber <b>{z}/6</b></span><span>Rule <b>{RULES[z][0]}</b></span>"
        f"<span class='hearts'>{hearts_text(run)}</span>"
        f"<span>Score <b>{run['score']}</b></span><span>Streak <b>{run['streak']}</b></span>"
        f"<span>{run['level']} · Pits <b>{run['crossed']}/{total}</b></span></div>"
        f"<div class='pbar'><div style='width:{pct:.1f}%'></div></div>", unsafe_allow_html=True)
    with b.popover("Menu"):
        st.caption("Leave this run? Your progress is lost.")
        if st.button("Leave run", key="leave"):
            st.session_state.screen = "title"
            st.session_state.pop("run", None)
            st.rerun()


def render_run():
    S = st.session_state
    run = S.run
    st.markdown(CSS, unsafe_allow_html=True)
    hud(run)
    z, n, k = zone_info(run, run["i"])
    T = THEMES[z]
    st.markdown(f"<style>[class*='st-key-panel'] {{ border-color: {T['accent']}88 !important; }}"
                f"[class*='st-key-panel'] h3 {{ color: {T['accent']} !important; }}"
                f".rule {{ border-left-color: {T['accent']}; }}"
                f".pbar > div {{ background: linear-gradient(90deg,{T['accent']},{T['gem']}) !important; }}</style>",
                unsafe_allow_html=True)
    cur = run["cur"]
    stone, door_open, splash, frm = k, False, None, None
    if run["phase"] == "fb" and cur and cur["result"]:
        if cur["result"]["ok"]:
            stone, frm = k + 1, k
            door_open = stone == n
        else:
            splash = k

    with page(f"run_{run['phase']}_{run['i']}_{run['nonce']}"):
        with st.container(key="scene"):
            st.markdown(scene_html(z, n, stone, door_open, splash, frm), unsafe_allow_html=True)

        if run["phase"] == "intro":
            name, topic, tip = ZONES[z]
            with st.container(key="panel_c"):
                st.caption(f"CHAMBER {z} OF 6 · {n} PIT{'S' if n > 1 else ''}")
                st.subheader(name)
                st.write(topic)
                st.markdown(f"<div class='tip'>{tip}</div>", unsafe_allow_html=True)
                rname, rtext = RULES[z]
                st.markdown(f"<div class='rule'><b>Chamber rule: {rname}.</b> {rtext}</div>", unsafe_allow_html=True)
                if st.button("Enter chamber", type="primary"):
                    init_question(run)
                    st.rerun()
            return

        q = QUESTIONS[cur["qid"]]
        hero = "Ember" if k % 2 == 0 else "Tide"
        left, right = st.columns([5, 6], gap="medium")
        with left:
            with st.container(key="panel_l"):
                with st.container():
                    st.markdown(f"<span class='chip fmt'>{q['k']}</span><span class='chip'>{DIFF_LABEL[q['d']]}</span>"
                                f"<span class='chip {hero.lower()}'>{hero}'s turn</span>", unsafe_allow_html=True)
                    if run["phase"] == "ask":
                        remaining = cur["limit"] - (time.time() - cur["start"])
                        show_html(countdown_html(max(0, remaining)), height=30)
                    st.markdown(f"<div class='qtext'>{html.escape(q['q'])}</div>", unsafe_allow_html=True)
                    if run["phase"] == "ask" and cur["hint"]:
                        st.markdown(f"<div class='tip'>Hint: {html.escape(q['h'])} (20 fewer points)</div>", unsafe_allow_html=True)
                if run["phase"] == "ask":
                    lifelines(run, q, cur)
        with right:
            with st.container(key="panel_r"):
                if run["phase"] == "ask":
                    ask(run, q, cur, k)
                else:
                    feedback(run, q, cur, n)


def lifelines(run, q, cur):
    L = run["life"]
    z = zone_info(run, run["i"])[0]
    locked = z == 6                                   # Sealed vault: no lifelines
    free_hint = z == 3                                # Open maps: hints cost no charge
    can_cull = q["mode"] == "c" and len(q["o"]) > 2 and not cur["culled"]
    can_swap = L["swap"] > 0 and run["spare"].get(z)
    c1, c2, c3, c4 = st.columns(4, gap="small")
    if c1.button("Hint free" if free_hint else f"Hint {L['hint']}", key=f"hint{run['nonce']}",
                 disabled=locked or cur["hint"] or (L["hint"] < 1 and not free_hint),
                 help="Show a hint (worth 20 fewer points)"):
        if not free_hint:
            L["hint"] -= 1
        cur["hint"] = True
        st.rerun()
    if c2.button(f"Cull {L['cull']}", disabled=locked or L["cull"] < 1 or not can_cull, key=f"cull{run['nonce']}",
                 help="Remove wrong options"):
        L["cull"] -= 1
        cur["culled"] = True
        wrong = [o for o in cur["order"] if o != q["a"]]
        random.shuffle(wrong)
        drop = set(wrong[:max(1, min(2, len(q["o"]) - 2))])
        cur["order"] = [o for o in cur["order"] if o not in drop]
        st.rerun()
    if c3.button(f"Freeze {L['freeze']}", disabled=locked or L["freeze"] < 1, key=f"fr{run['nonce']}", help="Add 15 seconds"):
        L["freeze"] -= 1
        cur["limit"] += 15
        st.rerun()
    if c4.button(f"Swap {L['swap']}", disabled=locked or not can_swap, key=f"sw{run['nonce']}", help="Swap for another question"):
        L["swap"] -= 1
        new_id = run["spare"][z].pop()
        run["deck"][run["i"]] = (z, new_id)
        init_question(run)
        st.rerun()
    if locked:
        st.caption("The sealed vault locks every lifeline.")


def ask(run, q, cur, k):
    nonce = run["nonce"]
    answered, ok, given = False, False, ""

    if q["mode"] == "c":
        labels = {f"{LETTERS[p]}. {q['o'][oi]}": oi for p, oi in enumerate(cur["order"])}
        choice = st.radio("Choose one", list(labels), index=None, key=f"ans{nonce}", label_visibility="collapsed")
        if st.button("Lock in answer", type="primary", disabled=choice is None, key=f"go{nonce}"):
            answered, ok, given = True, labels[choice] == q["a"], q["o"][labels[choice]]
    elif q["mode"] == "f":
        text = st.text_input("Your answer", key=f"ans{nonce}", placeholder="Type your answer")
        if st.button("Check", type="primary", disabled=not text.strip(), key=f"go{nonce}"):
            answered, ok, given = True, normalize(text) in [normalize(a) for a in q["a"]], text
    elif q["mode"] == "m":
        st.caption("Pick the partner for each item.")
        rights = [q["m"][r][1] for r in cur["right"]]
        picks = []
        for i, (lt, _) in enumerate(q["m"]):
            a, b = st.columns([1, 1.3], gap="small")
            a.markdown(f"<div class='mrow'>{html.escape(lt)}</div>", unsafe_allow_html=True)
            picks.append(b.selectbox(lt, rights, index=None, placeholder="Choose a partner",
                                     key=f"m{nonce}_{i}", label_visibility="collapsed"))
        if st.button("Lock in pairs", type="primary", disabled=any(p is None for p in picks), key=f"go{nonce}"):
            answered = True
            ok = all(picks[i] == q["m"][i][1] for i in range(len(picks)))
            given = "; ".join(f"{q['m'][i][0]} → {picks[i]}" for i in range(len(picks)))
    else:
        with st.container(key="graphbox"):
            st.markdown(graph_html(q), unsafe_allow_html=True)
        st.caption(f"Pick the nodes in the order they are visited ({len(q['a'])} steps).")
        nodes = sorted(q["g"]["n"])
        cols = st.columns(4, gap="small")
        seq = []
        for s in range(len(q["a"])):
            seq.append(cols[s % 4].selectbox(f"Step {s + 1}", nodes, index=None, placeholder=f"Step {s + 1}",
                                             key=f"g{nonce}_{s}", label_visibility="collapsed"))
        if st.button("Lock in order", type="primary", disabled=any(x is None for x in seq), key=f"go{nonce}"):
            answered, ok, given = True, seq == q["a"], " → ".join(seq)

    if answered:
        elapsed = time.time() - cur["start"]
        if elapsed > cur["limit"] + 2:           # 2 s grace for the network round trip
            resolve(run, q, False, "(ran out of time)", "time")
        else:
            resolve(run, q, ok, given)
        st.rerun()


def graph_html(q):
    g = q["g"]
    s = ['<div class="gph"><svg viewBox="0 0 400 290" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">']
    for a, b in g["e"]:
        (x1, y1), (x2, y2) = g["n"][a], g["n"][b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3b3562" stroke-width="3"/>')
    for nid, (x, y) in g["n"].items():
        s.append(f'<circle cx="{x}" cy="{y}" r="21" fill="#28234a" stroke="#3b3562" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="monospace" font-weight="700" font-size="16" fill="#f0ecff">{nid}</text>')
        if "h" in g:
            s.append(f'<text x="{x}" y="{y + 38}" text-anchor="middle" font-family="monospace" font-size="12" fill="#a7a1c9">h={g["h"][nid]}</text>')
    s.append("</svg></div>")
    return "".join(s)


def feedback(run, q, cur, n):
    res = cur["result"]
    last = run["hearts"] <= 0
    z, _, k = zone_info(run, run["i"])
    if res["ok"]:
        st.markdown(f"<div class='fb-ok'><b>Path clear</b><br>+{res['gained']} points ({', '.join(res['parts'])})<br><br>{html.escape(q['w'])}</div>",
                    unsafe_allow_html=True)
    else:
        hero = "Ember" if k % 2 == 0 else "Tide"
        verdict = "Time is up" if res["reason"] == "time" else ("Hiss! Ember hit water" if k % 2 == 0 else "Sizzle! Tide hit lava")
        if last:
            note = "No lives left."
        elif res.get("free"):
            note = f"Warm-up: no life lost. {hero} climbs out and tries this pit again with a new question."
        else:
            note = f"{hero} climbs out and stays on this stone. Try this pit again with a new question."
        correct = html.escape(answer_text(q)).replace("\n", "<br>")
        st.markdown(f"<div class='fb-no'><b>{verdict}</b><br>{note}<br><br><b>Correct answer</b><br>{correct}<br><br>{html.escape(q['w'])}</div>",
                    unsafe_allow_html=True)
    label = "See result" if last else ("Continue" if res["ok"] else "Try this pit again")
    if st.button(label, type="primary", key=f"next{run['nonce']}"):
        if last:
            finish("fallen")
        elif res["ok"]:
            run["k"] += 1
            run["crossed"] += 1
            run["i"] += 1
            if run["crossed"] >= run["total_pits"]:
                finish("cleared")
            elif run["k"] >= n:                      # last pit of this chamber crossed
                run["k"] = 0
                run["phase"], run["cur"] = "intro", None
            else:
                init_question(run)
        else:                                        # wrong: the heroes do not move
            queue_retry(run, q)
            init_question(run)
        st.rerun()


def render_result():
    S = st.session_state
    run = S.run
    st.markdown(CSS, unsafe_allow_html=True)
    total = len(run["log"])
    right = sum(1 for l in run["log"] if l["ok"])
    status = run["status"]
    where = f"Chamber {run['zone']} cleared" if run["zone"] else "All six chambers cleared"
    missed, seen = [], set()
    for l in run["log"]:                             # a question missed twice is reviewed once
        if not l["ok"] and l["qid"] not in seen:
            seen.add(l["qid"])
            missed.append(l)
    secs = run["secs"]

    with page("result"):
        left, rightc = st.columns([2, 3], gap="medium")
        with left, st.container(key="panel_xl_l"):
            st.caption(f"{'No lives left' if status == 'fallen' else where} · {run['level']}")
            st.markdown(f"<h1>{rank_title(run['acc'], status)}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:#f4c95d;font-size:3.2rem !important'>{run['score']}</h1>", unsafe_allow_html=True)
            st.write(f"{right}/{total} correct ({run['acc']}%)  \nBest streak {run['best']} · {max(0, run['hearts'])} lives left · {secs // 60}m {secs % 60}s")
            a, b = st.columns(2, gap="small")
            if a.button("Play again", type="primary"):
                start_run()
                st.rerun()
            if b.button("Change level"):
                S.screen = "title"
                st.rerun()
        with rightc, st.container(key="panel_xl_r"):
            views = ["By chamber", "Leaderboard", f"Review ({len(missed)})"]
            # the review label carries a count, so key the choice on its prefix
            view = st.radio("View", views, horizontal=True, label_visibility="collapsed", key="res_view_ui",
                            index=views.index(next((v for v in views if v.split(" (")[0] == S.get("res_view", "By chamber").split(" (")[0]), views[0])))
            S["res_view"] = view
            if view == "By chamber":
                for z in ZONES:
                    rows = [l for l in run["log"] if l["z"] == z]
                    if rows:
                        good = sum(1 for l in rows if l["ok"])
                        st.markdown(f"<div class='cb'><span>{ZONES[z][0]}</span><div class='pbar'><div style='width:{good / len(rows) * 100:.0f}%'></div></div>"
                                    f"<span>{good}/{len(rows)}</span></div>", unsafe_allow_html=True)
            elif view == "Leaderboard":
                lb_show(7)
            else:
                if not missed:
                    st.success("Flawless. Nothing to review.")
                else:
                    S["rev"] = max(0, min(S.get("rev", 0), len(missed) - 1))
                    q = QUESTIONS[missed[S["rev"]]["qid"]]
                    st.caption(f"Missed {S['rev'] + 1} of {len(missed)} · {q['k']}")
                    st.markdown(f"<div class='qtext' style='max-height:20vh'>{html.escape(q['q'])}</div>", unsafe_allow_html=True)
                    if q["mode"] == "c":
                        st.caption("  ·  ".join(f"{LETTERS[i]}. {o}" for i, o in enumerate(q["o"])))
                    st.success("Answer: " + answer_text(q))
                    st.caption(q["w"])
                    p, nx = st.columns(2, gap="small")
                    if p.button("Previous", disabled=S["rev"] == 0):
                        S["rev"] -= 1
                        st.rerun()
                    if nx.button("Next", disabled=S["rev"] >= len(missed) - 1):
                        S["rev"] += 1
                        st.rerun()


# ----------------------------------------------------------------------------
def main():
    S = st.session_state
    S.setdefault("screen", "title")
    if S.screen == "title":
        render_title()
    elif S.screen == "run" and "run" in S:
        render_run()
    elif S.screen == "result" and "run" in S:
        render_result()
    else:
        S.screen = "title"
        render_title()


main()
