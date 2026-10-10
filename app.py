<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ember and Tide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bungee&family=Chakra+Petch:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
:root {
  box-sizing: border-box;
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
  --ink: #12101c;
  --stone: #1c1930;
  --stone-2: #28234a;
  --line: #3b3562;
  --text: #f0ecff;
  --mute: #a7a1c9;
  --ember: #ff7a3d;
  --ember-deep: #a8431a;
  --tide: #35c6d9;
  --tide-deep: #1b7f8c;
  --gold: #f4c95d;
  --ok: #6ee7a0;
  --bad: #ff5d6c;
  --font-display: "Bungee", "Arial Black", Impact, sans-serif;
  --font-body: "Chakra Petch", "Trebuchet MS", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  color-scheme: dark;
}
html { scroll-padding-top: env(safe-area-inset-top, 0px); }
* { box-sizing: border-box; }
html, body { min-height: 100%; }
body {
  margin: 0;
  background-color: var(--ink);
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,.045) 1px, transparent 0);
  background-size: 22px 22px;
  color: var(--text);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.5;
  padding-inline: 16px;
  padding-block: 16px 48px;
}
[hidden] { display: none !important; }
.wrap { max-width: 900px; margin-inline: auto; display: flex; flex-direction: column; gap: 16px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 400; line-height: 1.1; margin: 0; text-wrap: balance; letter-spacing: .01em; }
p { margin: 0; }
.mute { color: var(--mute); }
.mono { font-family: var(--font-mono); }
.label { font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); font-weight: 600; }

/* HUD */
.hud { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 20px; }
.brand { font-family: var(--font-display); font-size: 20px; display: flex; gap: 8px; align-items: baseline; }
.brand b { color: var(--ember); font-weight: 400; }
.brand i { color: var(--tide); font-style: normal; }
.brand span { color: var(--mute); font-size: 14px; }
.stats { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }
.stat { display: flex; flex-direction: column; min-width: 56px; }
.stat b { font-family: var(--font-display); font-weight: 400; font-size: 20px; font-variant-numeric: tabular-nums; }
.lives { display: flex; gap: 4px; }
.lives svg { width: 20px; height: 20px; }

/* Panels */
.panel { background: var(--stone); border: 2px solid var(--line); border-radius: 6px; padding: 18px; }
.panel.tight { padding: 12px 14px; }
.stack { display: flex; flex-direction: column; gap: 14px; }
.row { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.grow { flex: 1 1 0; min-width: 0; }

/* Buttons */
.btn {
  font: 700 14px var(--font-body); letter-spacing: .08em; text-transform: uppercase;
  padding: 11px 18px; border: 0; border-radius: 4px; cursor: pointer;
  background: var(--stone-2); color: var(--text); box-shadow: 0 4px 0 #0c0a18;
  transition: transform .06s, box-shadow .06s, filter .15s;
}
.btn:hover { filter: brightness(1.12); }
.btn:active { transform: translateY(3px); box-shadow: 0 1px 0 #0c0a18; }
.btn:focus-visible, .opt:focus-visible, .node:focus-visible, input:focus-visible, select:focus-visible, summary:focus-visible { outline: 3px solid var(--gold); outline-offset: 2px; }
.btn.ember { background: var(--ember); color: #1d0b02; box-shadow: 0 4px 0 var(--ember-deep); }
.btn.ember:active { box-shadow: 0 1px 0 var(--ember-deep); }
.btn.tide { background: var(--tide); color: #03242a; box-shadow: 0 4px 0 var(--tide-deep); }
.btn.tide:active { box-shadow: 0 1px 0 var(--tide-deep); }
.btn.ghost { background: transparent; border: 2px solid var(--line); box-shadow: none; }
.btn.ghost:active { transform: none; }
.btn[disabled] { opacity: .35; cursor: not-allowed; filter: none; transform: none; }
.btn.small { padding: 7px 12px; font-size: 12px; box-shadow: 0 3px 0 #0c0a18; }

/* Title screen */
.hero { display: grid; grid-template-columns: 1fr; gap: 16px; align-items: center; }
.hero h1 { font-size: clamp(34px, 8vw, 64px); }
.hero h1 b { color: var(--ember); font-weight: 400; }
.hero h1 i { color: var(--tide); font-style: normal; }
.hero .sub { color: var(--mute); max-width: 56ch; }
.diffs { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
.diff { text-align: left; background: var(--stone); border: 2px solid var(--line); border-radius: 6px; padding: 12px 14px; color: var(--text); cursor: pointer; font-family: var(--font-body); display: flex; flex-direction: column; gap: 2px; }
.diff b { font-family: var(--font-display); font-weight: 400; font-size: 18px; }
.diff span { font-size: 13px; color: var(--mute); }
.diff[aria-pressed="true"] { border-color: var(--gold); background: var(--stone-2); }
input[type=text] { font: 600 16px var(--font-body); background: var(--ink); color: var(--text); border: 2px solid var(--line); border-radius: 4px; padding: 10px 12px; width: 100%; }
.board { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.board td, .board th { padding: 6px 8px; text-align: left; border-bottom: 1px solid var(--line); font-size: 14px; }
.board th { font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); }
.board td.n { text-align: right; font-family: var(--font-mono); }
.scroll-x { overflow-x: auto; }

/* Scene */
.scene { padding: 0; overflow: hidden; }
.scene svg { display: block; width: 100%; height: auto; }
.hero-g { transition: transform .7s cubic-bezier(.3,.7,.3,1); }
.hop { animation: hop .7s ease-out; }
@keyframes hop { 0%{translate:0 0} 40%{translate:0 -34px} 100%{translate:0 0} }
.hurt { animation: hurt .6s ease-in-out; }
@keyframes hurt { 0%,100%{translate:0 0} 20%{translate:-6px 6px} 40%{translate:6px 10px} 60%{translate:-5px 8px} 80%{translate:4px 4px} }
.door-shut { transition: transform .8s ease; transform-box: fill-box; transform-origin: right center; }
.door-open { transform: scaleX(.12); }
.gem-got { opacity: 0; transition: opacity .4s; }
.bubble { animation: bub 1.4s ease-in infinite; }
@keyframes bub { 0%{translate:0 0;opacity:.9} 100%{translate:0 -20px;opacity:0} }

/* Question */
.qhead { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; justify-content: space-between; }
.chip { font-size: 12px; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; padding: 3px 9px; border-radius: 3px; border: 2px solid var(--line); color: var(--mute); }
.chip.fmt { color: var(--gold); border-color: #6b5a22; }
.chip.who-ember { color: var(--ember); border-color: var(--ember-deep); }
.chip.who-tide { color: var(--tide); border-color: var(--tide-deep); }
.timer { height: 8px; background: var(--ink); border-radius: 4px; overflow: hidden; border: 1px solid var(--line); }
.timer > div { height: 100%; background: var(--tide); transition: width 1s linear, background .3s; }
.timer.low > div { background: var(--bad); }
.qtext { font-size: 18px; font-weight: 500; white-space: pre-wrap; text-wrap: pretty; max-width: 68ch; }
.opts { display: flex; flex-direction: column; gap: 10px; }
.opt { display: flex; gap: 12px; align-items: flex-start; text-align: left; width: 100%; font: 500 16px var(--font-body); color: var(--text); background: var(--stone-2); border: 2px solid var(--line); border-radius: 6px; padding: 12px 14px; cursor: pointer; }
.opt:hover:not([disabled]) { border-color: var(--mute); }
.opt .key { flex: none; width: 26px; height: 26px; display: grid; place-items: center; font: 700 13px var(--font-mono); background: var(--ink); border-radius: 3px; }
.opt .txt { min-width: 0; padding-top: 1px; overflow-wrap: anywhere; }
.opt.right { border-color: var(--ok); background: #153227; }
.opt.wrong { border-color: var(--bad); background: #3a1620; }
.opt.gone { opacity: .25; text-decoration: line-through; }
.opt[disabled] { cursor: default; }
.fillrow { display: flex; flex-wrap: wrap; gap: 10px; }
.fillrow input { flex: 1 1 200px; min-width: 0; font-family: var(--font-mono); }
.fb { border-radius: 6px; padding: 14px; display: flex; flex-direction: column; gap: 6px; border: 2px solid; }
.fb.ok { border-color: var(--ok); background: #12291f; }
.fb.no { border-color: var(--bad); background: #2e121a; }
.fb h3 { font-size: 18px; }
.fb.ok h3 { color: var(--ok); }
.fb.no h3 { color: var(--bad); }
.fb .why { white-space: pre-wrap; max-width: 68ch; }
.lifes { display: flex; flex-wrap: wrap; gap: 8px; }
.tip { background: #2c2610; border: 2px dashed #6b5a22; color: var(--gold); border-radius: 6px; padding: 10px 12px; font-size: 15px; }

/* Match */
.mgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; }
.mcell { display: flex; gap: 8px; align-items: center; text-align: left; font: 500 15px var(--font-body); color: var(--text); background: var(--stone-2); border: 2px solid var(--line); border-radius: 6px; padding: 10px 12px; cursor: pointer; min-width: 0; overflow-wrap: anywhere; }
.mcell.cur { border-color: var(--gold); }
.mcell .pair { flex: none; width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font: 700 12px var(--font-mono); background: var(--ink); color: var(--gold); }
.mcell.good { border-color: var(--ok); }
.mcell.bad { border-color: var(--bad); }
.mcell[disabled] { cursor: default; }
@media (max-width: 520px) { .mgrid { grid-template-columns: 1fr; } }

/* Graph */
.gwrap { background: var(--ink); border: 2px solid var(--line); border-radius: 6px; padding: 6px; max-width: 460px; }
.gwrap svg { display: block; width: 100%; height: auto; }
.node { cursor: pointer; }
.node circle { fill: var(--stone-2); stroke: var(--line); stroke-width: 3; transition: fill .15s, stroke .15s; }
.node:hover circle { stroke: var(--mute); }
.node.picked circle { fill: #3b3010; stroke: var(--gold); }
.node.right circle { fill: #153227; stroke: var(--ok); }
.node.wrong circle { fill: #3a1620; stroke: var(--bad); }
.node text { fill: var(--text); font: 700 16px var(--font-mono); text-anchor: middle; pointer-events: none; }
.node .ord { fill: var(--gold); font-size: 12px; }
.hval { fill: var(--mute); font: 500 12px var(--font-mono); text-anchor: middle; }
.seq { font-family: var(--font-mono); min-height: 1.6em; color: var(--gold); }

/* Progress */
.prog { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }
.prog div { height: 8px; background: var(--ink); border: 1px solid var(--line); border-radius: 2px; overflow: hidden; }
.prog div i { display: block; height: 100%; background: var(--gold); width: 0; transition: width .4s; }
.prog-cap { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; font-size: 13px; color: var(--mute); }

/* Interstitial / results */
.banner { display: flex; flex-direction: column; gap: 10px; align-items: flex-start; }
.banner h2 { font-size: clamp(26px, 6vw, 40px); }
.big { font-family: var(--font-display); font-size: clamp(44px, 12vw, 84px); line-height: 1; color: var(--gold); font-variant-numeric: tabular-nums; }
.bars { display: flex; flex-direction: column; gap: 8px; }
.bar { display: grid; grid-template-columns: minmax(110px, 190px) 1fr 48px; gap: 10px; align-items: center; font-size: 14px; }
.bar .track { height: 12px; background: var(--ink); border: 1px solid var(--line); border-radius: 2px; overflow: hidden; }
.bar .track i { display: block; height: 100%; background: var(--tide); }
.bar b { font-family: var(--font-mono); text-align: right; font-weight: 500; }
.tag { font-size: 10px; letter-spacing: .1em; text-transform: uppercase; padding: 1px 6px; border: 1px solid var(--line); border-radius: 3px; color: var(--mute); }
@media (prefers-reduced-motion: reduce) {
  .hero-g, .door-open, .timer > div { transition: none; }
  .hop, .hurt, .bubble { animation: none; }
}
.tgl { display: flex; gap: 8px; flex-wrap: wrap; }
.art { display: block; width: 100%; max-width: 360px; height: auto; }
.btn.ghost[aria-pressed="true"] { border-color: var(--gold); color: var(--gold); }

/* ===================== single-screen layout (no page scroll) ===================== */
html, body { height: 100%; overflow: hidden; }
body { padding: 10px 22px; }
.wrap { max-width: 1400px; width: 100%; height: 100%; gap: 10px; }
.hud { flex: none; }
.brand { font-size: clamp(17px, 2.8vh, 22px); }
.screen { flex: 1 1 0; min-height: 0; display: grid; gap: 12px; }
.screen > * { min-height: 0; }
.panel { padding: clamp(10px, 1.8vh, 18px) clamp(12px, 1.4vw, 20px); }
.stack { gap: clamp(8px, 1.4vh, 14px); }
.col { display: flex; flex-direction: column; gap: 12px; min-height: 0; }

/* title screen */
.g-title { grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr); grid-template-rows: minmax(0, 1fr); }
.g-title .hero { gap: 6px; }
.g-title .hero h1 { font-size: clamp(34px, 7.5vh, 64px); }
.g-title .sub { font-size: clamp(13px, 2vh, 16px); max-width: 78ch; }
.g-title .panel.form { flex: 1 1 auto; justify-content: space-between; }
.diffs { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.diff { padding: clamp(10px, 2vh, 18px) 16px; gap: 4px; min-height: clamp(86px, 13vh, 120px); }
.diff b { font-size: clamp(17px, 2.8vh, 24px); }
.diff span { font-size: clamp(12px, 1.8vh, 14px); }
.g-title .art { max-height: 20vh; width: auto; max-width: 100%; margin-inline: auto; }
.g-title .board td, .g-title .board th { padding: 5px 8px; }
.title-right { overflow: hidden; }

/* run screen */
.g-run { grid-template-rows: auto minmax(0, 1fr); }
.scene svg { max-height: 27vh; margin-inline: auto; }
.progwrap { margin-top: 8px; }
.g-run .prog-cap { font-size: 12px; margin-top: 4px; }
#qpanel { display: flex; flex-direction: column; gap: clamp(8px, 1.4vh, 12px); overflow: auto; }
.qgrid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 22px; flex: 1 1 auto; min-height: 0; }
.qleft, .qright { display: flex; flex-direction: column; gap: clamp(8px, 1.4vh, 12px); min-height: 0; }
.qtext { font-size: clamp(16px, 2.6vh, 21px); max-width: none; }
.opts { gap: clamp(6px, 1vh, 10px); }
.opt { padding: clamp(8px, 1.4vh, 13px) 14px; font-size: clamp(14px, 2.1vh, 16px); }
.lifes { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.lifes .btn { width: 100%; }
.gwrap { max-width: none; }
.gwrap svg { width: 100%; height: clamp(150px, 31vh, 300px); }
.mgrid .mcell { padding: clamp(7px, 1.2vh, 10px) 12px; }
#qpanel .banner { height: 100%; justify-content: center; }

/* result screen */
.g-result { grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr); grid-template-rows: minmax(0, 1fr); }
.g-result .big { font-size: clamp(44px, 12vh, 96px); }
.tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.tabpane { flex: 1 1 auto; min-height: 0; overflow: auto; }
.rv .opts-list { white-space: pre-wrap; color: var(--mute); margin: 10px 0; }
.rv .ans { color: var(--ok); font-weight: 600; margin: 8px 0; white-space: pre-wrap; }
.rv .ex { color: var(--mute); white-space: pre-wrap; }

/* short or narrow windows: let the page scroll instead of squeezing things */
@media (max-width: 900px), (max-height: 540px) {
  html, body { height: auto; overflow: auto; }
  .wrap { height: auto; }
  .screen { display: flex; flex-direction: column; }
  .diffs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .qgrid { grid-template-columns: 1fr; }
  .scene svg { max-height: none; }
  .gwrap svg { height: auto; }
}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
/* Question bank. Fields: z=chamber, k=format label, mode=c(choice)|f(fill)|m(match)|g(graph order),
   d=difficulty 1-3, q=prompt, o=options, a=answer, h=hint, w=why, tags=['real','search'] */
const QB = [];
const TF = ["True", "False"];
const AR = [
  "Both A and R are true, and R is the correct explanation of A",
  "Both A and R are true, but R is not the correct explanation of A",
  "A is true, but R is false",
  "A is false, but R is true"
];

/* ---------- CHAMBER 1: Foundations, Applications, Turing Test ---------- */
QB.push(
{ z:1, k:"MCQ", mode:"c", d:1,
  q:"Which approach to AI builds systems that do the right thing given what they know, judged by expected outcome rather than by resemblance to people?",
  o:["Thinking humanly","Acting humanly","Thinking rationally","Acting rationally"], a:3,
  h:"The modern textbook view centres on the rational agent.",
  w:"Acting rationally (the rational-agent approach) aims at the best expected outcome. Acting humanly is the Turing Test approach." },

{ z:1, k:"MCQ", mode:"c", d:1,
  q:"In the Turing Test, the interrogator's job is to decide…",
  o:["whether the machine can solve NP-hard problems","whether the unseen respondent is a human or a machine","whether the machine is conscious","whether the machine can beat a human at chess"], a:1,
  h:"It is a text conversation through a screen.",
  w:"The interrogator chats with two hidden parties and tries to tell which one is the machine. If they cannot, the machine passes." },

{ z:1, k:"True / False", mode:"c", d:2,
  q:"A machine that passes the basic (text-only) Turing Test must also be able to see objects and move them around.",
  o:TF, a:1,
  h:"Which version of the test adds vision and robotics?",
  w:"False. Seeing and manipulating objects belongs to the Total Turing Test. The basic test is text only." },

{ z:1, k:"MCQ", mode:"c", d:2,
  q:"Which capability is NOT needed to pass the basic, text-only Turing Test?",
  o:["Natural language processing","Knowledge representation","Computer vision","Machine learning"], a:2,
  h:"The conversation happens through typed text.",
  w:"Vision is needed only for the Total Turing Test. The basic test needs language, stored knowledge, reasoning and learning." },

{ z:1, k:"Scenario", mode:"c", d:1, tags:["real"],
  q:"A hospital deploys a system that scans chest X-rays and highlights suspicious regions for the radiologist. Which AI area does this mainly use?",
  o:["Computer vision","Speech recognition","Game playing","Robot motion planning"], a:0,
  h:"The input is an image.",
  w:"Interpreting images is the job of computer vision, usually with learned models." },

{ z:1, k:"Match the Following", mode:"m", d:1, tags:["real","search"],
  q:"Match each everyday product to the AI area behind it.",
  m:[["Phone face unlock","Computer vision"],["Voice assistant answering a question","Speech and language"],["Maps choosing a route","Search algorithms"],["Shopping site suggestions","Machine learning"]],
  h:"Think about what the input is in each case.",
  w:"Face unlock reads images, assistants process speech and language, route finders run graph search, and recommendations are learned from past behaviour." },

{ z:1, k:"Fill in the Blank", mode:"f", d:2,
  q:"A version of the Turing Test that also requires computer vision and robotics is called the ______ Turing Test.",
  a:["total"],
  h:"It tests the whole body, not just the conversation.",
  w:"The Total Turing Test adds a video channel and physical objects to pass through a hatch." },

{ z:1, k:"Assertion–Reason", mode:"c", d:3,
  q:"A: Passing the Turing Test proves that a machine truly understands language.\nR: The test only checks whether the machine's behaviour is indistinguishable from a human's.",
  o:AR, a:3,
  h:"Remember Searle's Chinese Room argument.",
  w:"A is false: behaving convincingly is not proof of understanding. R is true, and it is exactly why A fails." },

{ z:1, k:"Scenario", mode:"c", d:2,
  q:"ELIZA fooled some users by turning their sentences into questions using simple pattern rules. What does this show about the Turing Test?",
  o:["Pattern tricks can imitate conversation without real understanding","ELIZA understood human emotions","The Turing Test can never be passed","The test needs speech, not text"], a:0,
  h:"Was there any reasoning inside ELIZA?",
  w:"ELIZA used keyword rules. It shows that convincing talk can come from shallow tricks, which is a known weakness of the test." },

{ z:1, k:"MCQ", mode:"c", d:2, tags:["real","search"],
  q:"IBM's Deep Blue beat the world chess champion mainly by…",
  o:["searching deep game trees and scoring positions with an evaluation function","learning from millions of self-play games with a neural network","asking human grandmasters for each move","memorising every possible chess game"], a:0,
  h:"Think search plus a scoring function.",
  w:"Deep Blue combined very fast game-tree search with a hand-tuned evaluation function. Chess has far too many games to memorise." }
);

/* ---------- CHAMBER 2: Agents, Environments, Good Behaviour ---------- */
QB.push(
{ z:2, k:"MCQ", mode:"c", d:1,
  q:"An agent perceives its environment through ______ and acts on it through ______.",
  o:["sensors, actuators","actuators, sensors","goals, plans","rules, facts"], a:0,
  h:"Eyes and hands are the human version.",
  w:"Sensors deliver percepts and actuators carry out actions. Together they form the agent's link with the world." },

{ z:2, k:"MCQ", mode:"c", d:1,
  q:"The mapping from every possible percept sequence to an action is called the agent's…",
  o:["agent program","agent function","performance measure","environment"], a:1,
  h:"One is the abstract mapping, the other is the code that implements it.",
  w:"The agent function is the abstract mapping. The agent program is the concrete code that runs on the machine." },

{ z:2, k:"True / False", mode:"c", d:2,
  q:"A rational agent must be omniscient, meaning it knows the actual outcome of every action in advance.",
  o:TF, a:1,
  h:"Rational is not the same as perfect.",
  w:"False. Rationality maximises expected performance given the percepts so far. Omniscience is impossible in practice." },

{ z:2, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"You are designing a robot vacuum. Which performance measure encourages better behaviour?",
  o:["Amount of dirt collected in 8 hours","Number of clean squares at each time step, minus a penalty for energy and noise","Number of times the suction motor is switched on","Minutes spent moving"], a:1,
  h:"A measure on dirt collected can be gamed by dumping the dirt and collecting it again.",
  w:"Reward the state of the environment you actually want (clean floor), not the agent's activity. Otherwise the robot can cheat the measure." },

{ z:2, k:"MCQ", mode:"c", d:1,
  q:"PEAS is the framework used to specify a task environment. What does it stand for?",
  o:["Performance, Environment, Actuators, Sensors","Planning, Execution, Action, Search","Percept, Event, Action, State","Problem, Evaluation, Algorithm, Solution"], a:0,
  h:"Four letters, four things to write down before building an agent.",
  w:"PEAS = Performance measure, Environment, Actuators, Sensors." },

{ z:2, k:"Match the Following", mode:"m", d:2, tags:["real"],
  q:"Match each PEAS element to an example for a self-driving taxi.",
  m:[["Performance measure","Safe, legal, fast, comfortable trip"],["Environment","Roads, traffic, pedestrians"],["Actuators","Steering, accelerator, brake"],["Sensors","Cameras, GPS, speedometer"]],
  h:"Sensors feed in, actuators act out.",
  w:"The performance measure says what is good, the environment is the world, actuators are outputs and sensors are inputs." },

{ z:2, k:"MCQ", mode:"c", d:2, tags:["real"],
  q:"Which description fits the task environment of a self-driving taxi?",
  o:["Fully observable and deterministic","Partially observable, stochastic, dynamic and continuous","Fully observable, static and discrete","Episodic and single-agent"], a:1,
  h:"Other cars, weather, and pedestrians are unpredictable.",
  w:"The taxi cannot see everything, outcomes are uncertain, the world changes while it thinks, and positions and speeds are continuous." },

{ z:2, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"An agent classifies each X-ray independently, and the label for one image never affects the next. This is a(n) ______ environment.",
  o:["sequential","episodic","dynamic","continuous"], a:1,
  h:"Each decision is a separate, self-contained episode.",
  w:"In an episodic environment the current decision does not depend on earlier ones. Chess and taxi driving are sequential." },

{ z:2, k:"Fill in the Blank", mode:"f", d:1,
  q:"A simple reflex agent chooses its action using only the ______ percept.",
  a:["current","present","latest"],
  h:"No memory of the past is used.",
  w:"Simple reflex agents apply condition–action rules to the current percept alone." },

{ z:2, k:"MCQ", mode:"c", d:2,
  q:"Which kind of agent keeps an internal model of the world so it can cope with partial observability?",
  o:["Simple reflex agent","Model-based reflex agent","Random agent","Table-lookup agent with one entry"], a:1,
  h:"It tracks what it cannot currently see.",
  w:"A model-based reflex agent maintains internal state, updated from percepts and knowledge of how the world evolves." },

{ z:2, k:"Scenario", mode:"c", d:1, tags:["real"],
  q:"A thermostat switches the heater on when the room is below 20°C and off otherwise. What type of agent is it?",
  o:["Simple reflex agent","Goal-based agent","Utility-based agent","Learning agent"], a:0,
  h:"One rule: IF too cold THEN heat.",
  w:"It maps the current percept straight to an action with a condition–action rule." },

{ z:2, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"A navigation app picks a route by weighing travel time, tolls and road safety, then chooses the best trade-off. Which agent type is this?",
  o:["Simple reflex","Model-based reflex","Utility-based","Table-driven"], a:2,
  h:"There is a score for how happy each outcome would make the user.",
  w:"A utility-based agent compares states by a utility function, which lets it trade conflicting goals against each other." },

{ z:2, k:"Assertion–Reason", mode:"c", d:2,
  q:"A: A learning agent can improve its performance over time in an unknown environment.\nR: It has a learning element that uses feedback from a critic to modify the performance element.",
  o:AR, a:0,
  h:"Learning element, critic, performance element, problem generator.",
  w:"Both are true and R is the mechanism that explains A." },

{ z:2, k:"True / False", mode:"c", d:2,
  q:"In a fully observable environment, an agent does not need to keep internal state to track the world.",
  o:TF, a:0,
  h:"If the sensors show everything, what is left to remember?",
  w:"True. Full observability means the percept already contains the complete relevant state." },

{ z:2, k:"MCQ", mode:"c", d:1,
  q:"Which of these is a single-agent environment?",
  o:["Chess","Poker","Solving a crossword puzzle","Driving in city traffic"], a:2,
  h:"No opponent or other decision maker is acting.",
  w:"A crossword involves one agent only. Chess and poker are competitive multi-agent, and taxi driving is multi-agent." }
);

/* ---------- CHAMBER 3: Problems, State Space, Production Systems ---------- */
QB.push(
{ z:3, k:"MCQ", mode:"c", d:1,
  q:"Which component of a formal problem tells the agent which state results from doing action a in state s?",
  o:["Initial state","Goal test","Transition model (successor function)","Path cost"], a:2,
  h:"It answers: if I do this here, where do I end up?",
  w:"The transition model maps (state, action) to the next state. The goal test only says whether a state is a goal." },

{ z:3, k:"Fill in the Blank", mode:"f", d:1,
  q:"The set of all states reachable from the initial state by any sequence of actions is called the ______ space.",
  a:["state","state space"],
  h:"Two words in the topic name: state ___ search.",
  w:"The state space is a graph whose nodes are states and whose edges are actions." },

{ z:3, k:"Problem Solving", mode:"c", d:3, tags:["search"],
  q:"WATER JUGS. You have a 4 L jug and a 3 L jug with no markings. Both start empty. You may fill a jug, empty a jug, or pour one into the other until the source is empty or the target is full. What is the minimum number of actions needed to leave exactly 2 L in the 4 L jug?",
  o:["4","5","6","7"], a:2,
  h:"Write states as (4L jug, 3L jug) and run BFS from (0,0). The 3 L jug can hold 2 L after 4 actions, but that is not what is asked.",
  w:"BFS over states (4L, 3L) reaches (4,2) at depth 4 and (0,2) at depth 5, but the first states with 2 in the 4 L jug appear at depth 6. One route: fill 3L, pour into 4L, fill 3L, pour into 4L, empty 4L, pour 3L into 4L, which gives (2,0). So the minimum is 6." },

{ z:3, k:"MCQ", mode:"c", d:2,
  q:"A production system is made of…",
  o:["rules, a global database (working memory) and a control strategy","a compiler, a linker and a loader","a neural network and a loss function","sensors, actuators and an environment"], a:0,
  h:"IF–THEN rules need data to match against and a way to pick one.",
  w:"Rules (knowledge), a global database of current facts, and a control strategy that decides which matching rule fires." },

{ z:3, k:"Fill in the Blank", mode:"f", d:2,
  q:"When several rules match at the same time in a production system, picking one of them is called ______ resolution.",
  a:["conflict"],
  h:"The rules conflict over who gets to fire.",
  w:"Conflict resolution strategies include rule order, recency, and specificity." },

{ z:3, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"A garage's diagnostic tool stores rules like “IF engine cranks AND does not start THEN check the fuel pump”. It reads symptoms from the mechanic and applies matching rules. Which AI structure is this?",
  o:["Production system","Minimax tree","Genetic algorithm","Convolutional network"], a:0,
  h:"Look at the IF–THEN shape and the facts being matched.",
  w:"Condition–action rules acting on a working memory of symptoms is a production system, the base of classic expert systems." },

{ z:3, k:"MCQ", mode:"c", d:2,
  q:"In the problem characteristics of Rich and Knight, chess moves are best described as…",
  o:["ignorable","recoverable","irrecoverable","decomposable"], a:2,
  h:"Can you take a move back?",
  w:"A chess move cannot be undone, so mistakes cannot be recovered by backtracking over real moves. The 8-puzzle is recoverable, and theorem proving is ignorable." },

{ z:3, k:"Match the Following", mode:"m", d:2, tags:["search"],
  q:"Match each problem to the characteristic that describes it best.",
  m:[["Proving a theorem","Ignorable steps"],["Solving the 8-puzzle","Recoverable steps"],["Playing chess","Irrecoverable steps"],["Travelling salesman","Needs the best path, not any path"]],
  h:"Ask: can I undo a step, and do I need the best solution or just any?",
  w:"Theorem steps can be ignored if unhelpful, puzzle moves can be reversed, chess moves are permanent, and the TSP asks for the shortest tour." },

{ z:3, k:"True / False", mode:"c", d:1,
  q:"In the travelling salesman problem, any route that visits every city once is an acceptable solution.",
  o:TF, a:1,
  h:"The word “salesman” hints at cost.",
  w:"False. A solution must be the shortest tour. This is a best-path problem, unlike a puzzle where any solution will do." },

{ z:3, k:"Scenario", mode:"c", d:3,
  q:"A planner has one clearly stated goal state but a huge number of possible starting situations, and from the goal only a few actions lead back. Which direction of search is likely to be cheaper?",
  o:["Forward from the start","Backward from the goal","Neither, they are always equal","Random jumps between states"], a:1,
  h:"Choose the direction with the smaller branching factor.",
  w:"Direction of search is a design issue. Prefer the direction with fewer branches, and backward search suits an explicit goal with few predecessors." },

{ z:3, k:"Scenario", mode:"c", d:2, tags:["real","search"],
  q:"A Rubik's Cube has about 43 quintillion states. What is the main problem for a blind search solver?",
  o:["The goal is unknown","The state space is so large that blind search is hopeless, so heuristics are needed","The cube has no legal moves","The path cost is negative"], a:1,
  h:"Count states, not moves.",
  w:"Combinatorial explosion makes uninformed search impractical. Heuristics and pruning shrink the effective search." },

{ z:3, k:"Problem Solving", mode:"c", d:2, tags:["search"],
  q:"8-PUZZLE. Start:\n1 2 3\n4 _ 6\n7 5 8\nGoal:\n1 2 3\n4 5 6\n7 8 _\nWhat is the minimum number of tile moves?",
  o:["1","2","3","4"], a:1,
  h:"Misplaced tiles are 5 and 8, each only one step from its place.",
  w:"Slide 5 up into the blank, then slide 8 left. The Manhattan distance heuristic is 1+1 = 2, so 2 moves is optimal." },

{ z:3, k:"Assertion–Reason", mode:"c", d:2, tags:["search"],
  q:"A: State-space search can be viewed as finding a path in a graph.\nR: States are nodes and actions are edges between them.",
  o:AR, a:0,
  h:"Draw the state space as dots and arrows.",
  w:"Both true and R is the exact mapping that makes A possible." }
);

/* ---------- CHAMBER 4: BFS, DFS, Iterative Deepening ---------- */
const TREE = {
  n:{A:[200,30],B:[110,100],C:[290,100],D:[60,175],E:[160,175],F:[250,175],G:[340,175],H:[60,245]},
  e:[["A","B"],["A","C"],["B","D"],["B","E"],["C","F"],["C","G"],["D","H"]]
};
QB.push(
{ z:4, k:"Problem Solving", mode:"g", d:2, tags:["search"],
  q:"TAP THE ORDER. Breadth-First Search starts at A and always visits children left to right. Tap the nodes in the order BFS visits them.",
  g:TREE, a:["A","B","C","D","E","F","G","H"],
  h:"Finish a whole level before going deeper.",
  w:"BFS uses a queue and explores level by level: A, then B C, then D E F G, then H." },

{ z:4, k:"Problem Solving", mode:"g", d:2, tags:["search"],
  q:"TAP THE ORDER. Depth-First Search starts at A and tries the left child first. Tap the nodes in the order DFS visits them.",
  g:TREE, a:["A","B","D","H","E","C","F","G"],
  h:"Go as deep as possible, then backtrack.",
  w:"DFS uses a stack: A, B, D, H (dead end), back to E, back up to C, then F, G." },

{ z:4, k:"MCQ", mode:"c", d:1,
  q:"If you replace the FIFO queue in breadth-first search with a LIFO stack, you get…",
  o:["Depth-first search","Uniform-cost search","Hill climbing","Iterative deepening"], a:0,
  h:"Last in, first out means the newest node is expanded first.",
  w:"A stack always expands the most recently generated node, which dives deep first." },

{ z:4, k:"MCQ", mode:"c", d:2, tags:["search"],
  q:"BFS is guaranteed to return an optimal (shortest) solution when…",
  o:["all step costs are equal","the graph is infinite","the branching factor is 1","the goal is at depth 0 only"], a:0,
  h:"It finds the shallowest goal first.",
  w:"BFS finds the shallowest goal, which is cheapest only if each step costs the same." },

{ z:4, k:"True / False", mode:"c", d:2,
  q:"Depth-first search is complete even in a search tree with infinite depth.",
  o:TF, a:1,
  h:"It might follow one endless branch forever.",
  w:"False. DFS can descend an infinite branch and never return. It is complete only in finite spaces with repeated-state checking." },

{ z:4, k:"Scenario", mode:"c", d:3, tags:["real","search"],
  q:"A rescue robot has only 64 MB of memory. It explores a huge maze with branching factor 10, and nobody knows how deep the exit is. Which strategy is most suitable?",
  o:["Plain BFS","Plain DFS","Iterative deepening DFS","Random walk"], a:2,
  h:"Which one gets BFS's completeness and DFS's tiny memory?",
  w:"Iterative deepening uses O(bd) memory like DFS and is complete and optimal for unit costs like BFS." },

{ z:4, k:"Fill in the Blank", mode:"f", d:2, tags:["search"],
  q:"Iterative deepening search runs depth-limited searches with limit 0, 1, 2… and has time complexity O(b^__), where the blank is the depth of the shallowest goal. Fill in the letter.",
  a:["d"],
  h:"Same order as BFS in the worst case.",
  w:"The repeated work at shallow levels is small, so total time is still O(b^d)." },

{ z:4, k:"Problem Solving", mode:"c", d:2, tags:["search"],
  q:"A complete binary tree has depth 3 (the root is at depth 0). Just before BFS expands any depth-3 node, how many nodes does its frontier hold?",
  o:["4","7","8","15"], a:2,
  h:"Every depth-2 node has two children.",
  w:"There are 2³ = 8 nodes at depth 3, and all of them are waiting in the frontier. This is why BFS memory grows as b^d." },

{ z:4, k:"Assertion–Reason", mode:"c", d:3, tags:["search"],
  q:"A: Depth-limited search can fail to find a solution even though one exists.\nR: If the depth limit l is smaller than the depth d of the shallowest goal, the goal lies beyond the cutoff.",
  o:AR, a:0,
  h:"What happens when the limit is too small?",
  w:"Both true, and R is exactly why the cutoff causes failure." },

{ z:4, k:"Scenario", mode:"c", d:2, tags:["real","search"],
  q:"A web crawler must collect all pages within 2 clicks of the home page before moving on to deeper pages. Which strategy matches?",
  o:["Breadth-first search","Depth-first search","Hill climbing","Means-end analysis"], a:0,
  h:"Level by level.",
  w:"Visiting by distance from the start is exactly BFS." },

{ z:4, k:"Match the Following", mode:"m", d:2, tags:["search"],
  q:"Match each uninformed search to its best-known property.",
  m:[["BFS","Complete and optimal for unit step cost"],["DFS","Memory only O(b·m)"],["Iterative deepening","Complete with linear memory"],["Depth-limited search","Needs a cutoff, may miss deeper goals"]],
  h:"Think about time, memory, and completeness.",
  w:"These are the standard comparison points of the blind search family." }
);

/* ---------- CHAMBER 5: Hill Climbing, Heuristics, Best-First ---------- */
const HGRAPH = {
  n:{S:[200,30],A:[100,100],B:[300,100],C:[60,175],D:[220,175],G:[140,245]},
  e:[["S","A"],["S","B"],["A","C"],["A","D"],["B","D"],["C","G"],["D","G"]],
  h:{S:7,A:4,B:6,C:2,D:3,G:0}
};
QB.push(
{ z:5, k:"MCQ", mode:"c", d:1,
  q:"Hill climbing is best described as…",
  o:["a greedy local search that moves to the best neighbour and never backtracks","a complete search that stores the whole tree","a search that always finds the global optimum","a blind search with a queue"], a:0,
  h:"It only looks at its immediate neighbours.",
  w:"Hill climbing keeps one current state and repeatedly moves uphill. It can get stuck, and it uses very little memory." },

{ z:5, k:"Match the Following", mode:"m", d:2, tags:["search"],
  q:"Match each hill-climbing trap to its description.",
  m:[["Local maximum","Higher than all neighbours but lower than the best peak"],["Plateau","Flat region where all neighbours score the same"],["Ridge","Sequence of local maxima that single moves cannot climb"],["Global maximum","The best state in the whole landscape"]],
  h:"Picture a landscape of hills.",
  w:"These are the standard failure modes that variants such as random restart and sideways moves try to fix." },

{ z:5, k:"MCQ", mode:"c", d:2,
  q:"Which hill-climbing variant is the best choice when each state has thousands of successors?",
  o:["Steepest-ascent","First-choice","Breadth-first search","Exhaustive enumeration"], a:1,
  h:"You do not want to score every neighbour.",
  w:"First-choice generates successors randomly and takes the first one better than the current state, which avoids evaluating all neighbours." },

{ z:5, k:"MCQ", mode:"c", d:2,
  q:"Which variant picks randomly among the uphill moves, with higher probability for steeper moves?",
  o:["Steepest-ascent","Stochastic hill climbing","Random-restart hill climbing","Simulated annealing"], a:1,
  h:"The name tells you chance is involved in the choice of uphill move.",
  w:"Stochastic hill climbing chooses among uphill moves at random, weighted by steepness." },

{ z:5, k:"Scenario", mode:"c", d:3, tags:["search"],
  q:"A hill climber on 8-queens stops at a state where h = 1 (one pair attacking) and every neighbour has h ≥ 1. Which fix works best?",
  o:["Run it again from many random initial states and keep the best result","Reduce the board size","Switch to breadth-first search on the same state","Add more queens"], a:0,
  h:"If one start gets stuck, try another.",
  w:"Random-restart hill climbing is complete with probability approaching 1, because some restart will land near the global optimum." },

{ z:5, k:"True / False", mode:"c", d:1,
  q:"Steepest-ascent hill climbing is guaranteed to find the global maximum.",
  o:TF, a:1,
  h:"What about local maxima?",
  w:"False. It can stop at a local maximum, a plateau or a ridge." },

{ z:5, k:"MCQ", mode:"c", d:2, tags:["search"],
  q:"Which heuristic for the 8-puzzle is admissible, meaning it never overestimates the true cost?",
  o:["Sum of Manhattan distances of the tiles (not the blank)","Twice the sum of Manhattan distances","Number of moves already made","A random number from 0 to 30"], a:0,
  h:"Each move shifts one tile by one square.",
  w:"A tile needs at least its Manhattan distance in moves, so the sum is a lower bound. Doubling it can overestimate." },

{ z:5, k:"Problem Solving", mode:"g", d:3, tags:["search"],
  q:"GREEDY BEST-FIRST. The number under each node is its heuristic h. Greedy best-first always expands the frontier node with the smallest h. Tap the nodes in the order they are expanded, from S until G.",
  g:HGRAPH, a:["S","A","C","G"],
  h:"After S, compare A(4) with B(6). Then add A's children to the frontier.",
  w:"Expand S, giving A(4), B(6) so A goes next. Expanding A adds C(2) and D(3), so C is next. C leads to G(0), which is expanded and passes the goal test." },

{ z:5, k:"MCQ", mode:"c", d:2,
  q:"The evaluation function of A* is f(n) = g(n) + h(n). Greedy best-first search uses…",
  o:["f(n) = g(n)","f(n) = h(n)","f(n) = g(n) − h(n)","f(n) = 1"], a:1,
  h:"Greedy ignores the cost already paid.",
  w:"Greedy best-first uses only the heuristic estimate h(n), so it is fast but neither optimal nor always complete." },

{ z:5, k:"Scenario", mode:"c", d:1, tags:["real","search"],
  q:"A map app uses the straight-line distance to the destination to decide which road to try first. This straight-line estimate is an example of…",
  o:["a heuristic function","a constraint","a percept","an actuator"], a:0,
  h:"It estimates the remaining cost.",
  w:"A heuristic estimates the cost to the goal. Straight-line distance never exceeds road distance, so it is admissible." },

{ z:5, k:"True / False", mode:"c", d:2,
  q:"Greedy best-first search always returns the cheapest path.",
  o:TF, a:1,
  h:"It ignores the cost so far.",
  w:"False. It follows the most promising-looking node and can end up on an expensive route." },

{ z:5, k:"Problem Solving", mode:"c", d:2, tags:["search"],
  q:"In A*, node P has g = 5 and h = 3. Node Q has g = 2 and h = 7. Which node is expanded first?",
  o:["P, because f = 8 is less than Q's f = 9","Q, because its g is smaller","Q, because its h is larger","They tie"], a:0,
  h:"Compute f = g + h for both.",
  w:"f(P) = 5 + 3 = 8 and f(Q) = 2 + 7 = 9. A* expands the node with the smaller f." }
);

/* ---------- CHAMBER 6: Constraint Satisfaction and Means-End Analysis ---------- */
QB.push(
{ z:6, k:"MCQ", mode:"c", d:1,
  q:"A constraint satisfaction problem (CSP) is defined by…",
  o:["variables, domains and constraints","states, actions and rewards","nodes, queues and stacks","percepts, sensors and actuators"], a:0,
  h:"Think of map colouring: regions, colours, and rules.",
  w:"A CSP has variables, a domain of values for each, and constraints that restrict the allowed combinations." },

{ z:6, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"A college schedules exams so that no student has two exams at the same time. If exams that share students cannot take the same slot, what are the variables of this CSP?",
  o:["The time slots","The exams","The students","The rooms"], a:1,
  h:"Variables are the things that need a value assigned.",
  w:"Each exam is a variable whose domain is the set of time slots. The clash rule is a binary constraint between exams." },

{ z:6, k:"MCQ", mode:"c", d:2,
  q:"In map colouring, the constraint “WA ≠ NT” involves two variables. It is a ______ constraint.",
  o:["unary","binary","global","soft"], a:1,
  h:"Count the variables in the constraint.",
  w:"A constraint on exactly two variables is binary." },

{ z:6, k:"Problem Solving", mode:"c", d:3, tags:["search"],
  q:"X, Y and Z each take a value from {1, 2, 3}. Constraints: X < Y and Y < Z. How many complete assignments satisfy all constraints?",
  o:["0","1","3","6"], a:1,
  h:"Y must have something smaller and something larger.",
  w:"Y has to be strictly between X and Z, so Y = 2, X = 1, Z = 3. Exactly one solution." },

{ z:6, k:"MCQ", mode:"c", d:2, tags:["search"],
  q:"After assigning a value to a variable, forward checking…",
  o:["removes inconsistent values from the domains of its unassigned neighbours","undoes the assignment","assigns all other variables at once","sorts the variables alphabetically"], a:0,
  h:"It looks one step ahead for dead ends.",
  w:"Forward checking prunes neighbour domains and backtracks as soon as some domain becomes empty." },

{ z:6, k:"Scenario", mode:"c", d:2, tags:["real"],
  q:"While solving a Sudoku, cell A has 2 candidate digits and cell B has 5. The minimum remaining values (MRV) heuristic picks…",
  o:["cell A, the most constrained cell","cell B, the least constrained cell","whichever is nearer the top left","a random cell, ignoring the counts"], a:0,
  h:"Fail early.",
  w:"MRV picks the variable with the fewest legal values. It exposes dead ends sooner and keeps the tree small." },

{ z:6, k:"Fill in the Blank", mode:"f", d:2,
  q:"In n-queens as a CSP, “no two queens attack each other” is a constraint between pairs of queens, so it is a ______ constraint.",
  a:["binary"],
  h:"How many variables does each constraint touch?",
  w:"Each attack check involves two queens, which is binary." },

{ z:6, k:"MCQ", mode:"c", d:2,
  q:"Means-end analysis solves a problem by…",
  o:["finding the difference between the current state and the goal and applying an operator that reduces it","expanding every node level by level","always moving to the neighbour with the highest value","assigning values to variables in alphabetical order"], a:0,
  h:"Compare, then act.",
  w:"Means-end analysis picks the largest difference and an operator that reduces it. If the operator cannot be applied yet, it creates a sub-goal." },

{ z:6, k:"Scenario", mode:"c", d:3, tags:["real"],
  q:"A robot must bring a book from a locked room. The difference is “book not in hand”. The operator PICK-UP needs the robot to be at the book, and being in the room needs the door unlocked. Which is the means-end approach?",
  o:["Make sub-goals: unlock the door, enter the room, then pick up the book","Try random actions until the book appears","Pick the book up from where it is now","Start BFS from the book"], a:0,
  h:"Preconditions become new goals.",
  w:"When an operator's preconditions are not met, means-end analysis sets them as sub-goals and works recursively." },

{ z:6, k:"True / False", mode:"c", d:2,
  q:"Means-end analysis was a central technique in Newell and Simon's General Problem Solver (GPS).",
  o:TF, a:0,
  h:"Think of the 1950s and early AI.",
  w:"True. GPS used difference reduction, which is means-end analysis." },

{ z:6, k:"Assertion–Reason", mode:"c", d:3, tags:["search"],
  q:"A: Arc consistency can detect failure earlier than plain backtracking.\nR: It removes values from a variable's domain that have no supporting value in a neighbouring variable's domain.",
  o:AR, a:0,
  h:"What does pruning domains do to dead ends?",
  w:"Both true. Emptying a domain during propagation shows that no solution exists on this path before more assignments are made." }
);

/* ===================== game engine ===================== */
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const APP = document.getElementById("app");

const ZONES = [null,
  { n: "Gate of Minds", t: "Foundations and the Turing Test", tip: "AI can be judged by how it thinks or how it acts, and by whether it copies people or is rational. Modern AI aims at acting rationally." },
  { n: "Hall of Agents", t: "Rational agents and environments", tip: "An agent maps percepts to actions. Judge it with a performance measure, and describe its task with PEAS and the properties of its environment." },
  { n: "Maze of Problems", t: "State spaces and production systems", tip: "A problem has an initial state, actions, a transition model, a goal test and a path cost. Search is then a walk through the state-space graph." },
  { n: "Blind Bridge", t: "BFS, DFS and iterative deepening", tip: "Blind search has no idea how close a state is to the goal. BFS goes shallow first, DFS goes deep first, and iterative deepening mixes both." },
  { n: "Heuristic Peak", t: "Hill climbing, heuristics and best-first search", tip: "A heuristic estimates the distance to the goal. Hill climbing climbs greedily and can get stuck. Best-first and A* keep a frontier." },
  { n: "Vault of Constraints", t: "CSP and means-end analysis", tip: "A CSP has variables, domains and constraints. Means-end analysis shrinks the gap between state and goal by picking operators and sub-goals." }
];
const DIFFS = {
  easy:   { name: "Easy",        per: 3,  hearts: 6, time: 45, target: 1, blurb: "gentle questions, 6 lives, 45 s" },
  medium: { name: "Medium",      per: 5,  hearts: 5, time: 30, target: 2, blurb: "balanced questions, 5 lives, 30 s" },
  hard:   { name: "Hard",        per: 5,  hearts: 4, time: 25, target: 3, blurb: "toughest questions, 4 lives, 25 s" },
  full:   { name: "Full Temple", per: 99, hearts: 5, time: 30, target: 2, blurb: "every question, 5 lives, 30 s" }
};
function runSize(k, zone) {
  const zs = zone ? [zone] : [1, 2, 3, 4, 5, 6];
  return zs.reduce((n, z) => n + Math.min(DIFFS[k].per, QB.filter(q => q.z === z).length), 0);
}
const DLABEL = ["", "Easy", "Medium", "Hard"];
const LETTERS = "ABCDEFGH";

const S = { name: "", diff: "medium", zone: 0 };
let R = null;      // current run
let SC = null;     // current scene geometry
let memLB = [];
try { memLB = JSON.parse(localStorage.getItem("et-lb") || "[]"); } catch (e) { memLB = []; }

function lbAdd(entry) {
  memLB.push(entry);
  memLB.sort((a, b) => b.score - a.score);
  memLB = memLB.slice(0, 30);
  try { localStorage.setItem("et-lb", JSON.stringify(memLB)); } catch (e) { /* storage unavailable */ }
}

function ansText(q) {
  if (q.mode === "c") return q.o[q.a];
  if (q.mode === "f") return q.a.join("  /  ");
  if (q.mode === "m") return q.m.map(p => p[0] + "  →  " + p[1]).join("\n");
  if (q.mode === "g") return q.a.join("  →  ");
  return "";
}

/* ---------- small SVG pieces ---------- */
function heartSVG(full) {
  return `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z" fill="${full ? "var(--bad)" : "none"}" stroke="var(--bad)" stroke-width="2"/></svg>`;
}
function heroG(kind) {
  const col = kind === "ember" ? "#ff7a3d" : "#35c6d9";
  const head = kind === "ember"
    ? `<path d="M-10 -30 C-14 -46 -3 -50 0 -64 C6 -52 14 -46 10 -30 Z" fill="#f4c95d"/><path d="M-6 -30 C-8 -40 -1 -44 0 -52 C4 -44 8 -40 6 -30 Z" fill="#ff7a3d"/>`
    : `<path d="M0 -66 C10 -52 13 -43 10 -30 L-10 -30 C-13 -43 -10 -52 0 -66 Z" fill="#8be3ee"/>`;
  return `${head}<rect x="-12" y="-32" width="24" height="32" rx="5" fill="${col}"/><circle cx="-4" cy="-20" r="3.4" fill="#fff"/><circle cx="4" cy="-20" r="3.4" fill="#fff"/><circle cx="-3.2" cy="-19.6" r="1.6" fill="#12101c"/><circle cx="4.8" cy="-19.6" r="1.6" fill="#12101c"/><rect x="-9" y="-3" width="7" height="7" rx="2" fill="#12101c"/><rect x="2" y="-3" width="7" height="7" rx="2" fill="#12101c"/>`;
}
function titleArt() {
  return `<svg class="art" viewBox="0 0 360 170" role="img" aria-label="Ember and Tide standing at the edge of a pit">
    <rect width="360" height="170" rx="6" fill="#161330"/>
    <rect x="0" y="118" width="110" height="52" fill="#2c2750"/><rect x="250" y="118" width="110" height="52" fill="#2c2750"/>
    <rect x="110" y="128" width="70" height="42" fill="#35c6d9" opacity=".85"/><rect x="180" y="128" width="70" height="42" fill="#ff7a3d" opacity=".85"/>
    <g transform="translate(60 118) scale(1.2)">${heroG("ember")}</g>
    <g transform="translate(300 118) scale(1.2)">${heroG("tide")}</g>
    <polygon points="180,60 190,74 180,88 170,74" fill="#f4c95d"/>
    <text x="180" y="30" text-anchor="middle" font-family="Bungee, Arial Black, sans-serif" font-size="13" fill="#a7a1c9">ONE PIT EACH. ANSWER TO CROSS.</text>
  </svg>`;
}

/* ---------- screens: shell ---------- */
function hudHTML(inRun) {
  const stats = inRun ? `
    <div class="stats" aria-live="polite">
      <div class="stat"><span class="label">Lives</span><div class="lives" id="h-lives"></div></div>
      <div class="stat"><span class="label">Score</span><b id="h-score">0</b></div>
      <div class="stat"><span class="label">Streak</span><b id="h-streak">0</b></div>
      <div id="h-quit"><button class="btn small ghost" data-act="quit">Menu</button></div>
    </div>` : "";
  return `<header class="hud"><div class="brand"><b>Ember</b><span>&amp;</span><i>Tide</i></div>${stats}</header>`;
}
function bankCounts() {
  const fmts = new Set(QB.map(q => q.k));
  return {
    total: QB.length, fmts: fmts.size,
    real: QB.filter(q => (q.tags || []).includes("real")).length,
    search: QB.filter(q => (q.tags || []).includes("search")).length
  };
}

function lbTable(highlight, max = 8) {
  if (!memLB.length) return `<p class="mute">No runs yet. Finish a run to claim the first place.</p>`;
  const rows = memLB.slice(0, max).map((e, i) =>
    `<tr${highlight && e.id === highlight ? ' style="color:var(--gold)"' : ""}><td class="n">${i + 1}</td><td>${esc(e.name)}</td><td>${esc(e.diff)}</td><td class="n">${e.acc}%</td><td class="n">${e.score}</td></tr>`).join("");
  return `<div class="scroll-x"><table class="board"><thead><tr><th>#</th><th>Hero</th><th>Mode</th><th>Acc</th><th>Score</th></tr></thead><tbody>${rows}</tbody></table></div>
    <p class="mute" style="font-size:13px;margin-top:8px">Scores are kept in this browser only.</p>`;
}

function showTitle() {
  stopTimer();
  const bc = bankCounts();
  const dbtn = Object.entries(DIFFS).map(([k, d]) =>
    `<button class="diff" data-act="diff" data-k="${k}" aria-pressed="${S.diff === k}"><b>${d.name}</b><span class="mono" data-size="${k}">${runSize(k, S.zone)} questions</span><span>${d.blurb}</span></button>`).join("");
  const zbtn = [`<button class="btn small ghost" data-act="zone" data-z="0" aria-pressed="${S.zone === 0}">All chambers</button>`]
    .concat([1, 2, 3, 4, 5, 6].map(z => `<button class="btn small ghost" data-act="zone" data-z="${z}" aria-pressed="${S.zone === z}">${z}. ${esc(ZONES[z].n)}</button>`)).join("");
  APP.innerHTML = `${hudHTML(false)}
  <main class="screen g-title">
    <div class="col">
      <div class="hero">
        <h1><b>Ember</b> and <i>Tide</i></h1>
        <p class="sub">Two heroes, six chambers, one temple of AI concepts. Ember cannot touch water and Tide cannot touch lava. Each question is a pit. Answer right and your heroes cross. Answer wrong and one of them takes a swim in the wrong liquid.</p>
      </div>
      <div class="panel stack form">
        <div class="stack" style="gap:6px">
          <label class="label" for="name">Hero name for the leaderboard</label>
          <input id="name" type="text" maxlength="18" autocomplete="off" placeholder="Your name" value="${esc(S.name)}">
        </div>
        <div class="stack" style="gap:6px">
          <span class="label">Pick a level</span>
          <div class="diffs">${dbtn}</div>
        </div>
        <div class="stack" style="gap:6px">
          <span class="label">Pick where to play</span>
          <div class="tgl">${zbtn}</div>
        </div>
        <div class="row"><button class="btn ember" data-act="start">Enter the temple</button></div>
      </div>
    </div>
    <div class="col title-right">
      ${titleArt()}
      <div class="panel stack"><h3 style="font-size:19px">Leaderboard</h3>${lbTable(null, 5)}</div>
      <div class="panel stack">
        <h3 style="font-size:19px">How it plays</h3>
        <p class="mute" style="font-size:14px">Beat the timer, keep your lives, build streaks. Five correct in a row restores a life. Four lifelines per run: Hint, Cull (removes two wrong options), Freeze (+15 s) and Swap (new question).</p>
        <p class="mute" style="font-size:14px"><span class="mono" style="color:var(--gold)">${bc.total}</span> questions · <span class="mono" style="color:var(--gold)">${bc.fmts}</span> formats · <span class="mono" style="color:var(--gold)">${bc.real}</span> real-world · <span class="mono" style="color:var(--gold)">${bc.search}</span> search problems</p>
      </div>
    </div>
  </main>`;
}

/* ---------- scene: two heroes crossing one pit per question ---------- */
function buildScene(z, n) {
  const W = 1200, H = 170, gy = 108;
  const sp = 1060 / n, sw = Math.min(72, sp * 0.58);
  const xs = Array.from({ length: n + 1 }, (_, i) => 70 + i * sp);
  SC = { n, xs, gy, scale: Math.max(0.52, Math.min(1, sp / 110)), off: Math.min(15, sw * 0.24) };
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Chamber ${z}: two heroes crossing ${n} pits toward the chamber door">`;
  s += `<rect width="${W}" height="${H}" fill="#161330"/>`;
  for (let r = 0; r < 4; r++) s += `<rect x="0" y="${r * 34 + 8}" width="${W}" height="1" fill="#2a2548"/>`;
  s += `<text x="16" y="28" font-family="Bungee, Arial Black, sans-serif" font-size="15" fill="#a7a1c9">CHAMBER ${z}  ·  ${ZONES[z].n.toUpperCase()}</text>`;
  for (let i = 0; i < n; i++) {
    const x1 = xs[i] + sw / 2, x2 = xs[i + 1] - sw / 2, lava = i % 2 === 1;
    s += `<rect x="${x1}" y="${gy + 10}" width="${x2 - x1}" height="${H - gy - 10}" fill="${lava ? "#ff7a3d" : "#35c6d9"}" opacity=".85"/>`;
    s += `<rect x="${x1}" y="${gy + 10}" width="${x2 - x1}" height="3" fill="#ffffff" opacity=".35"/>`;
    const cx = (x1 + x2) / 2;
    s += `<g id="bub-${i}" visibility="hidden"><circle class="bubble" cx="${cx - 3}" cy="${gy + 6}" r="3" fill="#fff"/><circle class="bubble" style="animation-delay:.4s" cx="${cx + 4}" cy="${gy + 2}" r="2.4" fill="#fff"/></g>`;
    s += `<polygon id="gem-${i}" points="${cx},${gy - 62} ${cx + 8},${gy - 52} ${cx},${gy - 42} ${cx - 8},${gy - 52}" fill="#f4c95d" stroke="#8a6d1e" stroke-width="2"/>`;
  }
  for (let i = 0; i <= n; i++) {
    s += `<rect x="${xs[i] - sw / 2}" y="${gy}" width="${sw}" height="${H - gy}" fill="#2c2750" stroke="#3b3562" stroke-width="2"/><rect x="${xs[i] - sw / 2}" y="${gy}" width="${sw}" height="5" fill="#4a4380"/>`;
  }
  const dx = xs[n];
  s += `<rect x="${dx - 22}" y="${gy - 70}" width="44" height="70" rx="4" fill="#12101c" stroke="#f4c95d" stroke-width="3"/>`;
  s += `<rect id="door" class="door-shut" x="${dx - 18}" y="${gy - 66}" width="36" height="66" fill="#f4c95d" opacity=".92"/>`;
  s += `<g id="hE" class="hero-g" style="transform:translate(${xs[0] - SC.off}px,${gy}px) scale(${SC.scale})"><g id="hEi">${heroG("ember")}<polygon id="aE" points="-7,-84 7,-84 0,-74" fill="#ff7a3d"/></g></g>`;
  s += `<g id="hT" class="hero-g" style="transform:translate(${xs[0] + SC.off}px,${gy}px) scale(${SC.scale})"><g id="hTi">${heroG("tide")}<polygon id="aT" points="-7,-84 7,-84 0,-74" fill="#35c6d9" visibility="hidden"/></g></g>`;
  s += `</svg>`;
  $("#scenebox").innerHTML = s;
}
function setActive(k) {
  const e = $("#aE"), t = $("#aT");
  if (e) e.setAttribute("visibility", k % 2 === 0 ? "visible" : "hidden");
  if (t) t.setAttribute("visibility", k % 2 === 1 ? "visible" : "hidden");
}
function moveTo(i) {
  const h1 = $("#hE"), h2 = $("#hT");
  if (!h1 || !SC) return;
  h1.style.transform = `translate(${SC.xs[i] - SC.off}px,${SC.gy}px) scale(${SC.scale})`;
  h2.style.transform = `translate(${SC.xs[i] + SC.off}px,${SC.gy}px) scale(${SC.scale})`;
}
function pulse(id, cls, ms) {
  const el = $(id); if (!el) return;
  el.classList.remove(cls); void el.getBoundingClientRect(); el.classList.add(cls);
  setTimeout(() => el.classList.remove(cls), ms);
}
function sceneAdvance(k) {
  pulse(k % 2 === 0 ? "#hEi" : "#hTi", "hop", 800);
  moveTo(k + 1);
  const g = $("#gem-" + k); if (g) g.classList.add("gem-got");
  if (k + 1 === SC.n) $("#door").classList.add("door-open");
}
function sceneHurt(k) {
  pulse(k % 2 === 0 ? "#hEi" : "#hTi", "hurt", 700);
  const b = $("#bub-" + k);
  if (b) { b.setAttribute("visibility", "visible"); setTimeout(() => b.setAttribute("visibility", "hidden"), 1600); }
}

/* ---------- run setup ---------- */
function buildDeck(key) {
  const D = DIFFS[key], deck = [], spare = {};
  const zs = S.zone ? [S.zone] : [1, 2, 3, 4, 5, 6];
  zs.forEach(z => {
    const pool = shuffle(QB.filter(q => q.z === z));
    let pick = pool;
    if (D.per < pool.length) {
      pool.sort((a, b) => Math.abs(a.d - D.target) - Math.abs(b.d - D.target));
      pick = pool.slice(0, D.per);
      spare[z] = pool.slice(D.per);
    } else spare[z] = [];
    pick.sort((a, b) => (a.d + Math.random() * 0.9) - (b.d + Math.random() * 0.9));
    pick.forEach(q => deck.push({ q, z }));
  });
  return { deck, spare };
}
function startRun() {
  const D = DIFFS[S.diff], built = buildDeck(S.diff);
  R = { D, deck: built.deck, spare: built.spare, i: -1, hearts: D.hearts, score: 0, streak: 0, best: 0, log: [],
        life: { hint: 3, cull: 2, freeze: 2, swap: 1 }, t0: Date.now(), cur: null, tick: null };
  APP.innerHTML = `${hudHTML(true)}
    <main class="screen g-run">
      <div><div class="panel scene" id="scenebox"></div>
      <div class="progwrap"><div class="prog" id="prog">${[1,2,3,4,5,6].map(() => "<div><i></i></div>").join("")}</div>
      <div class="prog-cap"><span id="pcap1"></span><span id="pcap2"></span></div></div></div>
      <div class="panel" id="qpanel"></div>
    </main>`;
  nextQuestion();
}
function zoneInfo(i) {
  const z = R.deck[i].z, first = R.deck.findIndex(d => d.z === z), n = R.deck.filter(d => d.z === z).length;
  return { z, first, n, k: i - first };
}
function nextQuestion() {
  R.i++;
  if (R.i >= R.deck.length) return finish("cleared");
  const info = zoneInfo(R.i);
  updateHUD(); updateProg();
  if (info.k === 0) {
    buildScene(info.z, info.n); setActive(0);
    const Z = ZONES[info.z];
    $("#qpanel").innerHTML = `<div class="banner"><span class="label">Chamber ${info.z} of 6 · ${info.n} pit${info.n > 1 ? "s" : ""}</span>
      <h2>${esc(Z.n)}</h2><p class="mute">${esc(Z.t)}</p>
      <div class="tip">${esc(Z.tip)}</div>
      <button class="btn ember" id="go" data-act="enter">Enter chamber</button></div>`;
    const go = $("#go"); if (go) go.focus();
  } else showQuestion();
}

/* ---------- HUD ---------- */
function updateHUD() {
  const L = $("#h-lives"); if (!L) return;
  let h = ""; for (let i = 0; i < R.D.hearts; i++) h += heartSVG(i < R.hearts);
  L.innerHTML = h;
  $("#h-score").textContent = R.score;
  $("#h-streak").textContent = R.streak;
}
function updateProg() {
  const bars = document.querySelectorAll("#prog i");
  for (let z = 1; z <= 6; z++) {
    const total = R.deck.filter(d => d.z === z).length;
    const done = R.log.filter(l => l.z === z).length;
    bars[z - 1].style.width = total ? (done / total * 100) + "%" : "0";
  }
  const c1 = $("#pcap1"), c2 = $("#pcap2");
  if (c1) c1.textContent = `Question ${Math.min(R.i + 1, R.deck.length)} of ${R.deck.length}`;
  if (c2) c2.textContent = `Chamber ${R.deck[Math.min(R.i, R.deck.length - 1)].z} of 6`;
}

/* ---------- question view ---------- */
function prepView(q) {
  const v = {};
  if (q.mode === "c") {
    const n = q.o.length, fixed = q.o === AR || q.o === TF;
    v.order = fixed ? [...Array(n).keys()] : shuffle([...Array(n).keys()]);
    v.correct = v.order.indexOf(q.a);
    v.gone = new Set();
  } else if (q.mode === "m") {
    v.right = shuffle([...Array(q.m.length).keys()]);
    v.map = Array(q.m.length).fill(null);
    v.left = null;
  } else if (q.mode === "g") v.seq = [];
  return v;
}
function lifeHTML() {
  const c = R.cur, q = c.q, L = R.life;
  const canCull = q.mode === "c" && q.o.length > 2 && !c.view.culled;
  const canSwap = L.swap > 0 && (R.spare[c.info.z] || []).length > 0;
  return `<button class="btn small" data-act="hint" ${L.hint > 0 && !c.hint ? "" : "disabled"}>Hint (${L.hint})</button>
    <button class="btn small" data-act="cull" ${L.cull > 0 && canCull ? "" : "disabled"}>Cull (${L.cull})</button>
    <button class="btn small" data-act="freeze" ${L.freeze > 0 ? "" : "disabled"}>Freeze +15s (${L.freeze})</button>
    <button class="btn small" data-act="swap" ${canSwap ? "" : "disabled"}>Swap (${L.swap})</button>`;
}
function graphSVG(q, v) {
  const g = q.g;
  let s = `<svg viewBox="0 0 400 ${q.g.h ? 285 : 275}" role="group" aria-label="Search graph">`;
  g.e.forEach(([a, b]) => {
    s += `<line x1="${g.n[a][0]}" y1="${g.n[a][1]}" x2="${g.n[b][0]}" y2="${g.n[b][1]}" stroke="#3b3562" stroke-width="3"/>`;
  });
  Object.entries(g.n).forEach(([id, [x, y]]) => {
    s += `<g class="node" data-act="node" data-id="${id}" tabindex="0" role="button" aria-label="Node ${id}"><circle cx="${x}" cy="${y}" r="21"/><text x="${x}" y="${y + 5}">${id}</text><text class="ord" id="ord-${id}" x="${x + 22}" y="${y - 16}"></text></g>`;
    if (g.h) s += `<text class="hval" x="${x}" y="${y + 38}">h=${g.h[id]}</text>`;
  });
  return s + `</svg>`;
}
function showQuestion() {
  const item = R.deck[R.i], q = item.q, info = zoneInfo(R.i);
  const tMax = R.D.time + (q.mode === "g" || q.mode === "m" ? 20 : 0);
  R.cur = { q, info, view: prepView(q), hint: false, done: false, advanced: false, tMax, tLeft: tMax };
  const c = R.cur, hero = info.k % 2 === 0 ? "ember" : "tide";
  setActive(info.k);
  let body = "", gbox = "";
  if (q.mode === "c") {
    body = `<div class="opts" id="opts">${c.view.order.map((oi, si) =>
      `<button class="opt" data-act="opt" data-i="${si}"><span class="key">${LETTERS[si]}</span><span class="txt">${esc(q.o[oi])}</span></button>`).join("")}</div>`;
  } else if (q.mode === "f") {
    body = `<div class="fillrow"><input id="fillin" type="text" autocomplete="off" spellcheck="false" aria-label="Your answer" placeholder="Type your answer"><button class="btn ember" id="go" data-act="fill">Check</button></div>`;
  } else if (q.mode === "m") {
    let cells = "";
    q.m.forEach((p, r) => {
      cells += `<button class="mcell" data-act="ml" data-i="${r}" id="ml-${r}"><span class="pair" id="mlp-${r}"></span><span>${esc(p[0])}</span></button>`;
      const ri = c.view.right[r];
      cells += `<button class="mcell" data-act="mr" data-i="${ri}" id="mr-${ri}"><span class="pair" id="mrp-${ri}"></span><span>${esc(q.m[ri][1])}</span></button>`;
    });
    body = `<p class="mute" style="font-size:14px">Tap an item on the left, then its partner on the right. Tap a paired item to undo it.</p><div class="mgrid">${cells}</div>
      <div class="row"><button class="btn ember" id="go" data-act="lock" disabled>Lock in pairs</button></div>`;
  } else if (q.mode === "g") {
    gbox = `<div class="gwrap">${graphSVG(q, c.view)}</div>`;
    body = `<div class="seq" id="seq" aria-live="polite">Your order: </div>
      <div class="row"><button class="btn small" data-act="undo">Undo</button><button class="btn small" data-act="reset">Reset</button><button class="btn ember" id="go" data-act="lockg" disabled>Lock in order</button></div>`;
  }
  $("#qpanel").innerHTML = `
    <div class="qhead"><div class="row"><span class="chip fmt">${esc(q.k)}</span><span class="chip">${DLABEL[q.d]}</span><span class="chip who-${hero}">${hero === "ember" ? "Ember" : "Tide"}'s turn</span></div>
      <div class="mono" style="font-size:14px"><span id="tnum">${tMax}</span>s</div></div>
    <div class="timer" id="timer"><div style="width:100%"></div></div>
    <div class="qgrid">
      <div class="qleft"><div class="qtext">${esc(q.q)}</div>${body}</div>
      <div class="qright">${gbox}<div id="tipbox"></div><div class="lifes" id="lifes">${lifeHTML()}</div><div id="fbox" class="stack"></div></div>
    </div>`;
  startTimer();
  const f = $("#fillin"); if (f) f.focus();
}

/* ---------- timer ---------- */
function stopTimer() { if (R && R.tick) { clearInterval(R.tick); R.tick = null; } }
function updateTimer() {
  const c = R.cur; if (!c) return;
  const t = $("#timer"), n = $("#tnum"); if (!t) return;
  n.textContent = Math.max(0, c.tLeft);
  t.firstElementChild.style.width = Math.max(0, c.tLeft / c.tMax * 100) + "%";
  t.classList.toggle("low", c.tLeft <= 8);
}
function startTimer() {
  stopTimer();
  R.tick = setInterval(() => {
    const c = R.cur;
    if (!c || c.done) return stopTimer();
    c.tLeft--; updateTimer();
    if (c.tLeft <= 0) timedOut();
  }, 1000);
}
function timedOut() {
  const c = R.cur, q = c.q;
  if (q.mode === "c") markChoice(-1);
  else if (q.mode === "m") markMatch();
  else if (q.mode === "g") markGraph();
  resolve(false, "(ran out of time)", "time");
}

/* ---------- answer marking ---------- */
function markChoice(picked) {
  const c = R.cur;
  document.querySelectorAll("#opts .opt").forEach((b, si) => {
    b.disabled = true;
    if (si === c.view.correct) b.classList.add("right");
    else if (si === picked) b.classList.add("wrong");
  });
}
function markMatch() {
  const c = R.cur, q = c.q;
  q.m.forEach((p, r) => {
    const ok = c.view.map[r] === r;
    [ $("#ml-" + r), c.view.map[r] != null ? $("#mr-" + c.view.map[r]) : null ].forEach(el => { if (el) el.classList.add(ok ? "good" : "bad"); });
  });
  document.querySelectorAll(".mcell").forEach(b => b.disabled = true);
}
function markGraph() {
  const c = R.cur, q = c.q;
  c.view.seq.forEach((id, p) => { const el = document.querySelector(`.node[data-id="${id}"]`); if (el) el.classList.add(q.a[p] === id ? "right" : "wrong"); });
  document.querySelectorAll(".node").forEach(n => n.removeAttribute("tabindex"));
}

function normalize(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim(); }

function resolve(ok, given, reason) {
  const c = R.cur; if (c.done) return;
  c.done = true; stopTimer();
  const q = c.q, k = c.info.k, hero = k % 2 === 0 ? "Ember" : "Tide";
  let gained = 0, parts = [];
  if (ok) {
    R.streak++; R.best = Math.max(R.best, R.streak);
    const base = 60 + 20 * q.d - (c.hint ? 20 : 0), tb = Math.round(40 * c.tLeft / c.tMax), sb = Math.min(R.streak, 5) * 10;
    gained = base + tb + sb; R.score += gained;
    parts.push(`base ${base}`, `speed +${tb}`, `streak +${sb}`);
    if (R.streak % 5 === 0 && R.hearts < R.D.hearts) { R.hearts++; parts.push("a life restored"); }
    sceneAdvance(k); c.advanced = true;
  } else {
    R.streak = 0; R.hearts--;
    sceneHurt(k);
  }
  R.log.push({ q, z: c.info.z, ok, given, gained, hint: c.hint });
  updateHUD(); updateProg();
  const verdict = ok ? "Path clear" : reason === "time" ? "Time is up" : (k % 2 === 0 ? "Hiss! Ember hit water" : "Sizzle! Tide hit lava");
  const last = R.hearts <= 0;
  $("#lifes").innerHTML = "";
  $("#tipbox").innerHTML = "";
  $("#fbox").innerHTML = `<div class="fb ${ok ? "ok" : "no"}"><h3>${verdict}</h3>
    ${ok ? `<div class="mono" style="font-size:14px">+${gained} points (${parts.join(", ")})</div>` : `<div><span class="label">Correct answer</span><div style="white-space:pre-wrap;font-weight:600">${esc(ansText(q))}</div></div>`}
    <div class="why">${esc(q.w)}</div></div>
    <div class="row"><button class="btn ${ok ? "ember" : "tide"}" id="go" data-act="next">${last ? "See result" : "Continue"}</button><span class="mute" style="font-size:13px">${hero} ${ok ? "crosses" : "wades in"}${last ? ". No lives left." : ""}</span></div>`;
  const go = $("#go"); if (go) go.focus();
}

/* ---------- actions ---------- */
function onAct(act, el) {
  const c = R && R.cur, q = c && c.q;
  switch (act) {
    case "diff": S.diff = el.dataset.k; document.querySelectorAll(".diff").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.k === S.diff))); break;
    case "zone":
      S.zone = +el.dataset.z;
      document.querySelectorAll('[data-act="zone"]').forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.z === S.zone)));
      document.querySelectorAll("[data-size]").forEach(s => { s.textContent = runSize(s.dataset.size, S.zone) + " questions"; });
      break;
    case "quit": {
      if (R) stopTimer();
      const h = $("#h-quit");
      if (h) h.innerHTML = '<div class="row"><button class="btn small tide" data-act="quitNo">Keep playing</button><button class="btn small ghost" data-act="quitYes">Leave run</button></div>';
      break;
    }
    case "quitNo": {
      const h = $("#h-quit");
      if (h) h.innerHTML = '<button class="btn small ghost" data-act="quit">Menu</button>';
      if (R && R.cur && !R.cur.done) startTimer();
      break;
    }
    case "quitYes": stopTimer(); R = null; showTitle(); break;
    case "start": { const n = $("#name"); S.name = (n && n.value.trim()) || S.name || "Hero"; startRun(); break; }
    case "title": showTitle(); break;
    case "tab": RTAB = el.dataset.t; renderResult(); break;
    case "rv": RIDX = Math.max(0, Math.min(RES.missed.length - 1, RIDX + (+el.dataset.d))); renderResult(); break;
    case "enter": showQuestion(); break;
    case "opt": {
      if (c.done) return;
      const si = +el.dataset.i; markChoice(si);
      resolve(si === c.view.correct, q.o[c.view.order[si]]); break;
    }
    case "fill": {
      if (c.done) return;
      const inp = $("#fillin"), val = inp.value; if (!val.trim()) { inp.focus(); return; }
      inp.disabled = true; el.disabled = true;
      resolve(q.a.map(normalize).includes(normalize(val)), val); break;
    }
    case "ml": {
      if (c.done) return; const r = +el.dataset.i;
      if (c.view.map[r] != null) { c.view.map[r] = null; refreshMatch(); return; }
      c.view.left = r; refreshMatch(); break;
    }
    case "mr": {
      if (c.done) return; const ri = +el.dataset.i;
      const owner = c.view.map.indexOf(ri);
      if (owner >= 0) { c.view.map[owner] = null; refreshMatch(); return; }
      if (c.view.left == null) return;
      c.view.map[c.view.left] = ri; c.view.left = null; refreshMatch(); break;
    }
    case "lock": {
      if (c.done) return; markMatch();
      const ok = c.view.map.every((m, r) => m === r);
      resolve(ok, c.view.map.map((m, r) => q.m[r][0] + " → " + (m == null ? "?" : q.m[m][1])).join("; ")); break;
    }
    case "node": {
      if (c.done) return; const id = el.dataset.id, s = c.view.seq;
      if (s.includes(id)) return; s.push(id); refreshGraph(); break;
    }
    case "undo": if (!c.done) { c.view.seq.pop(); refreshGraph(); } break;
    case "reset": if (!c.done) { c.view.seq.length = 0; refreshGraph(); } break;
    case "lockg": {
      if (c.done) return; markGraph();
      const ok = c.view.seq.length === q.a.length && q.a.every((x, p) => x === c.view.seq[p]);
      resolve(ok, c.view.seq.join(" → ")); break;
    }
    case "hint":
      if (c.done || c.hint || R.life.hint < 1) return;
      R.life.hint--; c.hint = true;
      $("#tipbox").innerHTML = `<div class="tip">Hint: ${esc(q.h)} (worth 20 fewer points)</div>`;
      $("#lifes").innerHTML = lifeHTML(); break;
    case "cull": {
      if (c.done || R.life.cull < 1 || q.mode !== "c" || c.view.culled) return;
      const wrong = shuffle([...Array(q.o.length).keys()].filter(si => si !== c.view.correct));
      wrong.slice(0, Math.max(1, Math.min(2, q.o.length - 2))).forEach(si => { const b = document.querySelector(`#opts .opt[data-i="${si}"]`); b.classList.add("gone"); b.disabled = true; });
      c.view.culled = true; R.life.cull--; $("#lifes").innerHTML = lifeHTML(); break;
    }
    case "freeze":
      if (c.done || R.life.freeze < 1) return;
      R.life.freeze--; c.tLeft += 15; c.tMax = Math.max(c.tMax, c.tLeft); updateTimer(); $("#lifes").innerHTML = lifeHTML(); break;
    case "swap": {
      const pool = R.spare[c.info.z] || [];
      if (c.done || R.life.swap < 1 || !pool.length) return;
      stopTimer(); R.life.swap--; R.deck[R.i].q = pool.pop(); showQuestion(); break;
    }
    case "next":
      if (!c.advanced) { sceneAdvance(c.info.k); c.advanced = true; }
      if (R.hearts <= 0) return finish("fallen");
      nextQuestion(); break;
  }
}
function refreshMatch() {
  const c = R.cur, q = c.q;
  q.m.forEach((p, r) => {
    const L = $("#ml-" + r), P = $("#mlp-" + r);
    const paired = c.view.map[r] != null;
    L.classList.toggle("cur", c.view.left === r);
    P.textContent = paired ? r + 1 : "";
    const ri = c.view.map[r];
    if (paired) $("#mrp-" + ri).textContent = r + 1;
  });
  q.m.forEach((p, ri) => { if (c.view.map.indexOf(ri) < 0) $("#mrp-" + ri).textContent = ""; });
  $("#go").disabled = c.view.map.some(m => m == null);
}
function refreshGraph() {
  const c = R.cur, q = c.q;
  document.querySelectorAll(".node").forEach(n => { n.classList.remove("picked"); });
  Object.keys(q.g.n).forEach(id => { const o = $("#ord-" + id); if (o) o.textContent = ""; });
  c.view.seq.forEach((id, p) => {
    document.querySelector(`.node[data-id="${id}"]`).classList.add("picked");
    $("#ord-" + id).textContent = p + 1;
  });
  $("#seq").textContent = "Your order: " + c.view.seq.join(" → ");
  $("#go").disabled = c.view.seq.length < 2;
}

/* ---------- results ---------- */
function finish(status) {
  stopTimer();
  const total = R.log.length, right = R.log.filter(l => l.ok).length;
  const acc = total ? Math.round(right / total * 100) : 0;
  const secs = Math.round((Date.now() - R.t0) / 1000);
  const id = Date.now() + "-" + Math.random().toString(36).slice(2, 6);
  lbAdd({ id, name: S.name || "Hero", score: R.score, diff: R.D.name + (S.zone ? " · C" + S.zone : ""), acc });
  const rank = status === "fallen" ? "Fallen Hero" : acc >= 90 ? "Archmage of Search" : acc >= 75 ? "Temple Warden" : acc >= 55 ? "Path Finder" : "Apprentice";
  const bars = [1, 2, 3, 4, 5, 6].map(z => {
    const L = R.log.filter(l => l.z === z); if (!L.length) return "";
    const r = L.filter(l => l.ok).length, p = Math.round(r / L.length * 100);
    return `<div class="bar"><span>${esc(ZONES[z].n)}</span><div class="track"><i style="width:${p}%"></i></div><b>${r}/${L.length}</b></div>`;
  }).join("");
  const missed = R.log.filter(l => !l.ok);
  RES = { status, right, total, acc, secs, rank, id, bars, missed };
  RTAB = "chap"; RIDX = 0;
  renderResult();
  R.cur = null;
}

let RES = null, RTAB = "chap", RIDX = 0;
function reviewCard(q) {
  const tags = (q.tags || []).map(t => `<span class="tag">${t === "real" ? "real-world" : "search"}</span>`).join(" ");
  return `<div class="rv stack"><div class="row"><span class="chip fmt">${esc(q.k)}</span>${tags}</div>
    <div class="qtext">${esc(q.q)}</div>
    ${q.mode === "c" ? `<div class="opts-list">${q.o.map((o, j) => LETTERS[j] + ". " + esc(o)).join("\n")}</div>` : ""}
    <div class="ans">Answer: ${esc(ansText(q))}</div>
    <div class="ex">${esc(q.w)}</div></div>`;
}
function renderResult() {
  const r = RES, m = r.missed;
  let pane;
  if (RTAB === "chap") pane = `<div class="bars">${r.bars}</div>`;
  else if (RTAB === "lb") pane = lbTable(r.id, 8);
  else if (!m.length) pane = `<p>Flawless. Nothing to review.</p>`;
  else pane = `<div class="row" style="justify-content:space-between"><span class="label">Missed question ${RIDX + 1} of ${m.length}</span>
      <span class="row"><button class="btn small ghost" data-act="rv" data-d="-1" ${RIDX === 0 ? "disabled" : ""}>Previous</button><button class="btn small ghost" data-act="rv" data-d="1" ${RIDX >= m.length - 1 ? "disabled" : ""}>Next</button></span></div>
      ${reviewCard(m[RIDX].q)}`;
  const tab = (t, label) => `<button class="btn small ghost" data-act="tab" data-t="${t}" aria-pressed="${RTAB === t}">${label}</button>`;
  APP.innerHTML = `${hudHTML(false)}
  <main class="screen g-result">
    <div class="panel banner" style="justify-content:center">
      <span class="label">${r.status === "fallen" ? "No lives left" : S.zone ? "Chamber " + S.zone + " cleared" : "All six chambers cleared"} · ${esc(R.D.name)}</span>
      <h2>${esc(r.rank)}</h2>
      <div class="big">${R.score}</div>
      <div class="stack mono" style="font-size:14px;gap:4px">
        <span>${r.right}/${r.total} correct (${r.acc}%)</span><span>best streak ${R.best}</span><span>${Math.max(0, R.hearts)} lives left</span><span>${Math.floor(r.secs / 60)}m ${r.secs % 60}s</span>
      </div>
      <div class="row"><button class="btn ember" data-act="start">Play again</button><button class="btn ghost" data-act="title">Change level</button></div>
    </div>
    <div class="panel stack" style="display:flex;flex-direction:column">
      <div class="tabs">${tab("chap", "By chamber")}${tab("lb", "Leaderboard")}${tab("rev", "Review missed (" + m.length + ")")}</div>
      <div class="tabpane">${pane}</div>
    </div>
  </main>`;
}

/* ---------- wiring ---------- */
APP.addEventListener("click", e => {
  const b = e.target.closest("[data-act]");
  if (!b || b.disabled) return;
  onAct(b.dataset.act, b);
});
APP.addEventListener("keydown", e => {
  const t = e.target;
  if ((e.key === "Enter" || e.key === " ") && t.matches && t.matches('.node[data-act]')) { e.preventDefault(); t.dispatchEvent(new MouseEvent("click", { bubbles: true })); return; }
  if (e.key === "Enter" && t.id === "fillin") { e.preventDefault(); const g = $("#go"); if (g && !g.disabled) g.click(); return; }
  if (e.key === "Enter" && t.id === "name") { e.preventDefault(); onAct("start", t); return; }
});
document.addEventListener("keydown", e => {
  if (!R || !R.cur || R.cur.done || R.cur.q.mode !== "c") return;
  if (document.activeElement && document.activeElement.tagName === "INPUT") return;
  const si = "1234".indexOf(e.key);
  if (si >= 0) { const b = document.querySelector(`#opts .opt[data-i="${si}"]`); if (b && !b.disabled) b.click(); }
});
showTitle();
</script>
</body>
</html>
