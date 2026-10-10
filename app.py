"""Ember and Tide: an AI quiz game for Units I and II of Artificial Intelligence.

Two heroes cross six chambers. Every question is a pit. A correct answer carries the
heroes across, a wrong answer costs a life. Run with:  streamlit run app.py
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

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
h1, h2, h3 { font-family: 'Bungee', 'Arial Black', sans-serif !important; font-weight: 400 !important; letter-spacing: .01em; }
.tide-title b { color: #ff7a3d; font-weight: 400; } .tide-title i { color: #35c6d9; font-style: normal; }
.qtext { font-size: 1.15rem; white-space: pre-wrap; margin: .25rem 0 .75rem 0; }
.chip { display:inline-block; font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; font-weight:700;
        padding:2px 9px; border:2px solid #3b3562; border-radius:3px; margin-right:6px; color:#a7a1c9; }
.chip.fmt { color:#f4c95d; border-color:#6b5a22; }
.chip.ember { color:#ff7a3d; border-color:#a8431a; } .chip.tide { color:#35c6d9; border-color:#1b7f8c; }
.fb-ok { border:2px solid #6ee7a0; background:#12291f; padding:12px 14px; border-radius:6px; }
.fb-no { border:2px solid #ff5d6c; background:#2e121a; padding:12px 14px; border-radius:6px; }
.tip { border:2px dashed #6b5a22; background:#2c2610; color:#f4c95d; padding:10px 12px; border-radius:6px; }

/* ---- single-screen layout: no header, no sidebar, tight spacing ---- */
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display:none !important; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
.block-container { padding:1.2rem 1.6rem .5rem !important; max-width:1240px !important; }
[data-testid="stVerticalBlock"] { gap:.7rem !important; }
h1 { font-size:1.9rem !important; line-height:1.2 !important; padding:0 !important; margin:0 0 .4rem 0 !important; }
h2, h3 { font-size:1.1rem !important; line-height:1.3 !important; padding:0 !important; margin:0 0 .35rem 0 !important; }
.stButton > button { min-height:2.1rem; padding:.15rem .8rem; }
[data-testid="stRadio"] [role="radiogroup"] { gap:.1rem; }
[data-testid="stRadio"] label { padding:.1rem 0; }
[data-testid="stSelectbox"] label p, [data-testid="stTextInput"] label p { font-size:.85rem; }
[data-testid="stCaptionContainer"] { margin:0; }
.qtext { font-size:1.08rem; margin:.1rem 0 .3rem 0; }
.hud { display:flex; gap:18px; align-items:center; background:#1b1736; border:2px solid #3b3562; border-radius:6px; padding:6px 14px; }
.hud .lbl { font-size:.68rem; letter-spacing:.1em; text-transform:uppercase; color:#a7a1c9; display:block; }
.hud .val { font-size:1.25rem; font-weight:700; color:#f0ecff; }
.hud .hearts { color:#ff5d6c; letter-spacing:.1em; }
.hud .grow { flex:1; }
.panel { border:2px solid #3b3562; border-radius:6px; padding:10px 14px; background:#1b1736; }
.fb-ok, .fb-no { font-size:.95rem; }
@keyframes ebFade { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
[class*="st-key-scr-"] { animation: ebFade .4s ease-out both; }
[data-stale="true"] { opacity:1 !important; transition:none !important; }
@media (prefers-reduced-motion: reduce) { [class*="st-key-scr-"] { animation:none; } }
.mini { font-size:.7rem; letter-spacing:.1em; text-transform:uppercase; color:#a7a1c9; line-height:1.1; }
.mv { font-size:1.25rem; font-weight:700; color:#f0ecff; line-height:1.3; }
.big { font-family:'Bungee','Arial Black',sans-serif; font-size:3rem; line-height:1; color:#f4c95d; }
</style>
"""

def show_html(content, height):
    """Embed an HTML string. st.iframe is the current API; older Streamlit versions use components.html."""
    if hasattr(st, "iframe"):
        st.iframe(content, height=height)
    else:
        components.html(content, height=height)


# ----------------------------------------------------------------------------
# Scene: two heroes crossing one pit per question (drawn as SVG)
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


def scene_html(zone, n, stone, door_open, splash_pit, remaining=None, from_stone=None):
    """SVG scene. stone = stone the heroes stand on, splash_pit = pit with bubbles (wrong answer)."""
    W, H, gy = 800, 170, 108
    sp = 660 / n
    sw = min(72, sp * 0.58)
    xs = [70 + i * sp for i in range(n + 1)]
    scale = max(0.52, min(1, sp / 110))
    off = min(15, sw * 0.24)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">',
         f'<rect width="{W}" height="{H}" fill="#161330"/>']
    for r in range(4):
        s.append(f'<rect x="0" y="{r * 34 + 8}" width="{W}" height="1" fill="#2a2548"/>')
    s.append(f'<text x="16" y="28" font-family="Arial Black, sans-serif" font-size="15" fill="#a7a1c9">'
             f'CHAMBER {zone}  ·  {ZONES[zone][0].upper()}</text>')
    for i in range(n):
        x1, x2 = xs[i] + sw / 2, xs[i + 1] - sw / 2
        lava = i % 2 == 1                       # pit i is the nemesis of the hero who answers question i
        s.append(f'<rect x="{x1}" y="{gy + 10}" width="{x2 - x1}" height="{H - gy - 10}" fill="{EMBER if lava else TIDE}" opacity=".85"/>')
        s.append(f'<rect x="{x1}" y="{gy + 10}" width="{x2 - x1}" height="3" fill="#fff" opacity=".35"/>')
        cx = (x1 + x2) / 2
        if i == splash_pit:
            s.append(f'<circle cx="{cx - 3}" cy="{gy + 2}" r="3.2" fill="#fff"/><circle cx="{cx + 5}" cy="{gy - 8}" r="2.6" fill="#fff"/>'
                     f'<circle cx="{cx}" cy="{gy - 18}" r="2" fill="#fff"/>')
        if i >= stone:                           # gem still waiting
            s.append(f'<polygon points="{cx},{gy - 62} {cx + 8},{gy - 52} {cx},{gy - 42} {cx - 8},{gy - 52}" fill="{GOLD}" stroke="#8a6d1e" stroke-width="2"/>')
    for i in range(n + 1):
        s.append(f'<rect x="{xs[i] - sw / 2}" y="{gy}" width="{sw}" height="{H - gy}" fill="#2c2750" stroke="#3b3562" stroke-width="2"/>'
                 f'<rect x="{xs[i] - sw / 2}" y="{gy}" width="{sw}" height="5" fill="#4a4380"/>')
    dx = xs[n]
    door_w = 5 if door_open else 36
    s.append(f'<rect x="{dx - 22}" y="{gy - 70}" width="44" height="70" rx="4" fill="#12101c" stroke="{GOLD}" stroke-width="3"/>')
    s.append(f'<rect x="{dx + 18 - door_w}" y="{gy - 66}" width="{door_w}" height="66" fill="{GOLD}" opacity=".92"/>')
    for kind, sign in (("ember", -1), ("tide", 1)):
        x_to = xs[stone] + sign * off
        anim = ""
        if from_stone is not None and from_stone != stone:
            x_from = xs[from_stone] + sign * off
            anim = (f'<animateTransform attributeName="transform" type="translate" from="{x_from} {gy}" to="{x_to} {gy}" '
                    'dur="0.6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>')
        s.append(f'<g transform="translate({x_to},{gy})">{anim}<g transform="scale({scale})">{hero_svg(kind)}</g></g>')
    s.append("</svg>")
    return "<body style='margin:0;background:transparent'>" + "".join(s) + "</body>"


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


def lb_show(height=300):
    board = lb_load()
    if not board:
        st.caption("No runs yet. Finish a run to take first place.")
        return
    rows = [{"#": i + 1, "Hero": e["name"], "Level": e["level"], "Accuracy": f'{e["acc"]}%', "Score": e["score"]}
            for i, e in enumerate(board[:8])]
    try:
        st.dataframe(rows, hide_index=True, width="stretch", height=height)
    except TypeError:                      # older Streamlit
        st.dataframe(rows, hide_index=True, use_container_width=True, height=height)


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
    z = run["deck"][i][0]
    idxs = [j for j, (zz, _) in enumerate(run["deck"]) if zz == z]
    return z, len(idxs), i - idxs[0]


def hearts_text(run):
    return "".join("♥" if k < run["hearts"] else "♡" for k in range(run["max_hearts"]))


def rank_title(acc, status):
    if status == "fallen":
        return "Fallen Hero"
    return "Archmage of Search" if acc >= 90 else "Temple Warden" if acc >= 75 else "Path Finder" if acc >= 55 else "Apprentice"


# ----------------------------------------------------------------------------
# Run control
# ----------------------------------------------------------------------------
def start_run():
    S = st.session_state
    cfg = LEVELS[S.level]
    deck, spare = build_deck(S.level, S.zone)
    S.run = dict(level=S.level, zone=S.zone, deck=deck, spare=spare, i=0, hearts=cfg["hearts"], max_hearts=cfg["hearts"],
                 score=0, streak=0, best=0, log=[], life=dict(hint=3, cull=2, freeze=2, swap=1),
                 phase="intro", cur=None, t0=time.time(), leave=False, nonce=0)
    S.screen = "run"
    S.run["phase"] = "intro"


def init_question(run):
    z, n, k = zone_info(run, run["i"])
    q = QUESTIONS[run["deck"][run["i"]][1]]
    run["nonce"] += 1
    limit = LEVELS[run["level"]]["time"] + (20 if q["mode"] in ("g", "m") else 0)
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
    gained, parts = 0, []
    if ok:
        run["streak"] += 1
        run["best"] = max(run["best"], run["streak"])
        left = max(0, cur["limit"] - (time.time() - cur["start"]))
        base = 60 + 20 * q["d"] - (20 if cur["hint"] else 0)
        speed = round(40 * left / cur["limit"])
        streak_bonus = min(run["streak"], 5) * 10
        gained = base + speed + streak_bonus
        run["score"] += gained
        parts = [f"base {base}", f"speed +{speed}", f"streak +{streak_bonus}"]
        if run["streak"] % 5 == 0 and run["hearts"] < run["max_hearts"]:
            run["hearts"] += 1
            parts.append("a life restored")
    else:
        run["streak"] = 0
        run["hearts"] -= 1
    run["log"].append(dict(z=z, qid=q["id"], ok=ok, given=given, gained=gained))
    cur["result"] = dict(ok=ok, gained=gained, parts=parts, reason=reason, given=given)
    run["phase"] = "fb"


def finish(status):
    S = st.session_state
    run = S.run
    total = len(run["log"])
    right = sum(1 for l in run["log"] if l["ok"])
    acc = round(right / total * 100) if total else 0
    label = run["level"] + (f' · C{run["zone"]}' if run["zone"] else "")
    lb_add(dict(name=S.get("name") or "Hero", score=run["score"], level=label, acc=acc))
    run["status"], run["acc"], run["secs"] = status, acc, round(time.time() - run["t0"])
    S.screen = "result"


# ----------------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------------
def render_title():
    S = st.session_state
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("<h1 class='tide-title'><b>Ember</b> and <i>Tide</i></h1>", unsafe_allow_html=True)
    st.write("Two heroes, six chambers, one temple of AI concepts. Each question is a pit: answer right and your heroes "
             "cross, answer wrong and one takes a swim in the wrong liquid.")
    left, right = st.columns([3, 2], gap="large")
    with left:
        show_html(scene_html(1, 6, 0, False, None), height=165)
        a, b = st.columns(2)
        S.name = a.text_input("Hero name for the leaderboard", value=S.get("name", ""), max_chars=18)
        names = {0: "All chambers", **{z: f"{z}. {ZONES[z][0]}" for z in ZONES}}
        S.zone = b.selectbox("Pick where to play", list(names), format_func=lambda z: names[z], index=S.get("zone", 0))
        S.level = st.radio("Pick a level", list(LEVELS), index=list(LEVELS).index(S.get("level", "Medium")),
                           format_func=lambda k: f"{k} ({run_size(k, S.zone)})", horizontal=True)
        st.caption(LEVELS[S.level]["text"])
        if st.button("Enter the temple", type="primary"):
            start_run()
            st.rerun()
    with right:
        with st.container(border=True):
            st.subheader("Leaderboard")
            lb_show(height=200)
        with st.container(border=True):
            st.subheader("How to play")
            st.markdown(
                "- Ember cannot touch water, Tide cannot touch lava.\n"
                "- A wrong answer costs a life, a right one earns points for accuracy, speed and streak.\n"
                "- **Hint**, **Cull** (drop wrong options), **Freeze** (+15 s) and **Swap** (new question) help you out.\n"
                f"- {len(QUESTIONS)} questions in 7 formats across 6 chambers.")


def top_hud(run, z):
    """Top bar built from native Streamlit containers and columns, so it never overlaps the scene."""
    if run["leave"]:
        with st.container(border=True):
            c = st.columns([5, 1, 1], vertical_alignment="center")
            c[0].write("Leave this run? Your progress will be lost.")
            if c[1].button("Leave", use_container_width=True):
                st.session_state.screen = "title"
                st.session_state.pop("run", None)
                st.rerun()
            if c[2].button("Stay", use_container_width=True):
                run["leave"] = False
                st.rerun()
        return
    total = len(run["deck"])
    answered = len(run["log"])
    with st.container(border=True):
        c = st.columns([2.4, 1.5, 1, 1, 3.4, 1], vertical_alignment="center")
        c[0].markdown(f"<div class='mini'>Chamber {z} of 6</div><div class='mv'>{ZONES[z][0]}</div>", unsafe_allow_html=True)
        c[1].markdown(f"<div class='mini'>Lives</div><div class='mv' style='color:#ff5d6c'>{hearts_text(run)}</div>", unsafe_allow_html=True)
        c[2].markdown(f"<div class='mini'>Score</div><div class='mv'>{run['score']}</div>", unsafe_allow_html=True)
        c[3].markdown(f"<div class='mini'>Streak</div><div class='mv'>{run['streak']}</div>", unsafe_allow_html=True)
        c[4].progress(answered / total if total else 0, text=f"Question {min(answered + 1, total)} of {total}")
        if c[5].button("Menu", use_container_width=True):
            run["leave"] = True
            st.rerun()


def render_run():
    S = st.session_state
    run = S.run
    st.markdown(CSS, unsafe_allow_html=True)
    z, n, k = zone_info(run, run["i"])
    cur = run["cur"]
    stone, door_open, splash, from_stone = k, False, None, None
    if run["phase"] == "fb" and cur and cur["result"]:
        if cur["result"]["ok"]:
            stone = k + 1
            from_stone = k
            door_open = stone == n
        else:
            splash = k
    top_hud(run, z)

    if run["phase"] == "intro":
        name, topic, tip = ZONES[z]
        show_html(scene_html(z, n, stone, door_open, splash), height=250)
        c1, c2 = st.columns([3, 1], gap="large", vertical_alignment="center")
        with c1:
            st.caption(f"CHAMBER {z} OF 6 · {n} PIT{'S' if n > 1 else ''}")
            st.subheader(name)
            st.write(topic)
            st.markdown(f"<div class='tip'>{tip}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("Enter chamber", type="primary", use_container_width=True):
                init_question(run)
                st.rerun()
        return

    left, right = st.columns([3, 2], gap="medium")
    with left:
        show_html(scene_html(z, n, stone, door_open, splash, from_stone=from_stone), height=160)

    q = QUESTIONS[cur["qid"]]
    hero = "Ember" if k % 2 == 0 else "Tide"
    with left:
        st.markdown(f"<span class='chip fmt'>{q['k']}</span><span class='chip'>{DIFF_LABEL[q['d']]}</span>"
                    f"<span class='chip {hero.lower()}'>{hero}'s turn</span>", unsafe_allow_html=True)
        if run["phase"] == "ask":
            remaining = cur["limit"] - (time.time() - cur["start"])
            show_html(countdown_html(max(0, remaining)), height=30)
        st.markdown(f"<div class='qtext'>{html.escape(q['q'])}</div>", unsafe_allow_html=True)
        if run["phase"] == "ask":
            ask(run, q, cur, k)
    with right:
        if run["phase"] == "ask":
            if q["mode"] == "g":
                show_html(graph_html(q), height=252)
            if cur["hint"]:
                st.markdown(f"<div class='tip'>Hint: {html.escape(q['h'])} (worth 20 fewer points)</div>", unsafe_allow_html=True)
            st.caption("Lifelines")
            lifelines(run, q, cur)
        else:
            feedback(run, q, cur, n)


def lifelines(run, q, cur):
    L = run["life"]
    can_cull = q["mode"] == "c" and len(q["o"]) > 2 and not cur["culled"]
    can_swap = L["swap"] > 0 and run["spare"].get(zone_info(run, run["i"])[0])
    r1 = st.columns(2)
    r2 = st.columns(2)
    if r1[0].button(f"Hint ({L['hint']})", disabled=L["hint"] < 1 or cur["hint"], key=f"hint{run['nonce']}", use_container_width=True):
        L["hint"] -= 1
        cur["hint"] = True
        st.rerun()
    if r1[1].button(f"Cull ({L['cull']})", disabled=L["cull"] < 1 or not can_cull, key=f"cull{run['nonce']}", use_container_width=True):
        L["cull"] -= 1
        cur["culled"] = True
        wrong = [o for o in cur["order"] if o != q["a"]]
        random.shuffle(wrong)
        drop = set(wrong[:max(1, min(2, len(q["o"]) - 2))])
        cur["order"] = [o for o in cur["order"] if o not in drop]
        st.rerun()
    if r2[0].button(f"Freeze +15s ({L['freeze']})", disabled=L["freeze"] < 1, key=f"fr{run['nonce']}", use_container_width=True):
        L["freeze"] -= 1
        cur["limit"] += 15
        st.rerun()
    if r2[1].button(f"Swap ({L['swap']})", disabled=not can_swap, key=f"sw{run['nonce']}", use_container_width=True):
        L["swap"] -= 1
        z = zone_info(run, run["i"])[0]
        new_id = run["spare"][z].pop()
        run["deck"][run["i"]] = (z, new_id)
        init_question(run)
        st.rerun()


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
        st.caption("Pick the partner for each item on the left.")
        rights = [q["m"][r][1] for r in cur["right"]]
        picks = []
        mc = st.columns(2)
        for i, (left, _) in enumerate(q["m"]):
            picks.append(mc[i % 2].selectbox(left, rights, index=None, placeholder="Choose a partner", key=f"m{nonce}_{i}"))
        if st.button("Lock in pairs", type="primary", disabled=any(p is None for p in picks), key=f"go{nonce}"):
            answered = True
            ok = all(picks[i] == q["m"][i][1] for i in range(len(picks)))
            given = "; ".join(f"{q['m'][i][0]} → {picks[i]}" for i in range(len(picks)))
    else:
        st.caption(f"Choose the nodes in the order the algorithm visits them ({len(q['a'])} steps).")
        nodes = sorted(q["g"]["n"])
        cols = st.columns(4)
        seq = []
        for s in range(len(q["a"])):
            seq.append(cols[s % 4].selectbox(f"Step {s + 1}", nodes, index=None, placeholder="Node", key=f"g{nonce}_{s}"))
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
    s = ['<body style="margin:0;background:transparent"><svg viewBox="0 0 400 290" width="100%" style="max-width:330px;background:#12101c;border:2px solid #3b3562;border-radius:6px">']
    for a, b in g["e"]:
        (x1, y1), (x2, y2) = g["n"][a], g["n"][b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3b3562" stroke-width="3"/>')
    for nid, (x, y) in g["n"].items():
        s.append(f'<circle cx="{x}" cy="{y}" r="21" fill="#28234a" stroke="#3b3562" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="monospace" font-weight="700" font-size="16" fill="#f0ecff">{nid}</text>')
        if "h" in g:
            s.append(f'<text x="{x}" y="{y + 38}" text-anchor="middle" font-family="monospace" font-size="12" fill="#a7a1c9">h={g["h"][nid]}</text>')
    s.append("</svg></body>")
    return "".join(s)


def feedback(run, q, cur, n):
    res = cur["result"]
    last = run["hearts"] <= 0
    z, _, k = zone_info(run, run["i"])
    if res["ok"]:
        st.markdown(f"<div class='fb-ok'><b>Path clear</b><br>+{res['gained']} points ({', '.join(res['parts'])})<br>{html.escape(q['w'])}</div>",
                    unsafe_allow_html=True)
    else:
        verdict = "Time is up" if res["reason"] == "time" else ("Hiss! Ember hit water" if k % 2 == 0 else "Sizzle! Tide hit lava")
        correct = html.escape(answer_text(q)).replace("\n", "<br>")
        st.markdown(f"<div class='fb-no'><b>{verdict}</b><br><br><b>Correct answer</b><br>{correct}<br>{html.escape(q['w'])}</div>",
                    unsafe_allow_html=True)
    label = "See result" if last else "Continue"
    if st.button(label, type="primary", key=f"next{run['nonce']}"):
        if last:
            finish("fallen")
        else:
            run["i"] += 1
            if run["i"] >= len(run["deck"]):
                finish("cleared")
            else:
                nz, _, nk = zone_info(run, run["i"])
                if nk == 0:
                    run["phase"], run["cur"] = "intro", None
                else:
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
    missed = [l for l in run["log"] if not l["ok"]]
    secs = run["secs"]
    left, rightc = st.columns([2, 3], gap="large")
    with left:
        st.caption(f"{'No lives left' if status == 'fallen' else where} · {run['level']}")
        st.markdown(f"<h1>{rank_title(run['acc'], status)}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='big'>{run['score']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='panel'><b>{right}/{total}</b> correct ({run['acc']}%)<br>"
                    f"Best streak <b>{run['best']}</b> · Lives left <b>{max(0, run['hearts'])}</b><br>"
                    f"Time <b>{secs // 60}m {secs % 60}s</b></div>", unsafe_allow_html=True)
        a, b = st.columns(2)
        if a.button("Play again", type="primary", use_container_width=True):
            start_run()
            st.rerun()
        if b.button("Change level", use_container_width=True):
            S.screen = "title"
            st.rerun()
    with rightc:
        t1, t2, t3 = st.tabs(["By chamber", "Leaderboard", f"Review missed ({len(missed)})"])
        with t1:
            for z in ZONES:
                rows = [l for l in run["log"] if l["z"] == z]
                if rows:
                    good = sum(1 for l in rows if l["ok"])
                    st.progress(good / len(rows), text=f"{ZONES[z][0]}: {good}/{len(rows)}")
        with t2:
            lb_show(height=250)
        with t3:
            if not missed:
                st.success("Flawless. Nothing to review.")
            else:
                labels = {f"{i + 1}. {QUESTIONS[l['qid']]['k']}: {QUESTIONS[l['qid']]['q'][:70]}": l["qid"] for i, l in enumerate(missed)}
                pick = st.selectbox("Pick a question to review", list(labels), label_visibility="collapsed")
                q = QUESTIONS[labels[pick]]
                st.markdown(f"<div class='qtext'>{html.escape(q['q'])}</div>", unsafe_allow_html=True)
                if q["mode"] == "c":
                    st.write("  \n".join(f"{LETTERS[i]}. {o}" for i, o in enumerate(q["o"])))
                st.success("Answer: " + answer_text(q))
                st.caption(q["w"])


# ----------------------------------------------------------------------------
def screen_key(S):
    if S.screen == "run" and "run" in S:
        r = S.run
        return f"scr-run-{r['i']}-{r['nonce']}-{r['phase']}"
    return f"scr-{S.screen}"


def main():
    S = st.session_state
    S.setdefault("screen", "title")
    if S.screen in ("run", "result") and "run" not in S:
        S.screen = "title"
    with st.container(key=screen_key(S)):
        if S.screen == "title":
            render_title()
        elif S.screen == "run":
            render_run()
        elif S.screen == "result":
            render_result()


main()
