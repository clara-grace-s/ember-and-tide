"""Question bank for Ember and Tide (AI Units I and II).

Each question is a dictionary:
  z     chamber number 1-6
  k     format label shown to the player
  mode  c = choice, f = fill in the blank, m = match, g = tap the order on a graph
  d     difficulty 1 easy, 2 medium, 3 hard
  q     question text
  o     options (choice questions)
  m     pairs to match (match questions)
  g     graph nodes, edges and heuristic values (graph questions)
  a     correct answer: option index, list of accepted words, or node order
  h     hint,  w  reason shown after answering
  tags  real = real-world application, search = search / state-space problem
"""

QUESTIONS = [
 {
  "z": 1,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "Which approach to AI builds systems that do the right thing given what they know, judged by expected outcome rather than by resemblance to people?",
  "o": [
   "Thinking humanly",
   "Acting humanly",
   "Thinking rationally",
   "Acting rationally"
  ],
  "a": 3,
  "h": "The modern textbook view centres on the rational agent.",
  "w": "Acting rationally (the rational-agent approach) aims at the best expected outcome. Acting humanly is the Turing Test approach.",
  "tags": []
 },
 {
  "z": 1,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "In the Turing Test, the interrogator's job is to decide…",
  "o": [
   "whether the machine can solve NP-hard problems",
   "whether the unseen respondent is a human or a machine",
   "whether the machine is conscious",
   "whether the machine can beat a human at chess"
  ],
  "a": 1,
  "h": "It is a text conversation through a screen.",
  "w": "The interrogator chats with two hidden parties and tries to tell which one is the machine. If they cannot, the machine passes.",
  "tags": []
 },
 {
  "z": 1,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "A machine that passes the basic (text-only) Turing Test must also be able to see objects and move them around.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "Which version of the test adds vision and robotics?",
  "w": "False. Seeing and manipulating objects belongs to the Total Turing Test. The basic test is text only.",
  "tags": []
 },
 {
  "z": 1,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which capability is NOT needed to pass the basic, text-only Turing Test?",
  "o": [
   "Natural language processing",
   "Knowledge representation",
   "Computer vision",
   "Machine learning"
  ],
  "a": 2,
  "h": "The conversation happens through typed text.",
  "w": "Vision is needed only for the Total Turing Test. The basic test needs language, stored knowledge, reasoning and learning.",
  "tags": []
 },
 {
  "z": 1,
  "k": "Scenario",
  "mode": "c",
  "d": 1,
  "q": "A hospital deploys a system that scans chest X-rays and highlights suspicious regions for the radiologist. Which AI area does this mainly use?",
  "o": [
   "Computer vision",
   "Speech recognition",
   "Game playing",
   "Robot motion planning"
  ],
  "a": 0,
  "h": "The input is an image.",
  "w": "Interpreting images is the job of computer vision, usually with learned models.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 1,
  "k": "Match the Following",
  "mode": "m",
  "d": 1,
  "q": "Match each everyday product to the AI area behind it.",
  "m": [
   [
    "Phone face unlock",
    "Computer vision"
   ],
   [
    "Voice assistant answering a question",
    "Speech and language"
   ],
   [
    "Maps choosing a route",
    "Search algorithms"
   ],
   [
    "Shopping site suggestions",
    "Machine learning"
   ]
  ],
  "h": "Think about what the input is in each case.",
  "w": "Face unlock reads images, assistants process speech and language, route finders run graph search, and recommendations are learned from past behaviour.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 1,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 2,
  "q": "A version of the Turing Test that also requires computer vision and robotics is called the ______ Turing Test.",
  "a": [
   "total"
  ],
  "h": "It tests the whole body, not just the conversation.",
  "w": "The Total Turing Test adds a video channel and physical objects to pass through a hatch.",
  "tags": []
 },
 {
  "z": 1,
  "k": "Assertion–Reason",
  "mode": "c",
  "d": 3,
  "q": "A: Passing the Turing Test proves that a machine truly understands language.\nR: The test only checks whether the machine's behaviour is indistinguishable from a human's.",
  "o": [
   "Both A and R are true, and R is the correct explanation of A",
   "Both A and R are true, but R is not the correct explanation of A",
   "A is true, but R is false",
   "A is false, but R is true"
  ],
  "a": 3,
  "h": "Remember Searle's Chinese Room argument.",
  "w": "A is false: behaving convincingly is not proof of understanding. R is true, and it is exactly why A fails.",
  "tags": []
 },
 {
  "z": 1,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "ELIZA fooled some users by turning their sentences into questions using simple pattern rules. What does this show about the Turing Test?",
  "o": [
   "Pattern tricks can imitate conversation without real understanding",
   "ELIZA understood human emotions",
   "The Turing Test can never be passed",
   "The test needs speech, not text"
  ],
  "a": 0,
  "h": "Was there any reasoning inside ELIZA?",
  "w": "ELIZA used keyword rules. It shows that convincing talk can come from shallow tricks, which is a known weakness of the test.",
  "tags": []
 },
 {
  "z": 1,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "IBM's Deep Blue beat the world chess champion mainly by…",
  "o": [
   "searching deep game trees and scoring positions with an evaluation function",
   "learning from millions of self-play games with a neural network",
   "asking human grandmasters for each move",
   "memorising every possible chess game"
  ],
  "a": 0,
  "h": "Think search plus a scoring function.",
  "w": "Deep Blue combined very fast game-tree search with a hand-tuned evaluation function. Chess has far too many games to memorise.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "An agent perceives its environment through ______ and acts on it through ______.",
  "o": [
   "sensors, actuators",
   "actuators, sensors",
   "goals, plans",
   "rules, facts"
  ],
  "a": 0,
  "h": "Eyes and hands are the human version.",
  "w": "Sensors deliver percepts and actuators carry out actions. Together they form the agent's link with the world.",
  "tags": []
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "The mapping from every possible percept sequence to an action is called the agent's…",
  "o": [
   "agent program",
   "agent function",
   "performance measure",
   "environment"
  ],
  "a": 1,
  "h": "One is the abstract mapping, the other is the code that implements it.",
  "w": "The agent function is the abstract mapping. The agent program is the concrete code that runs on the machine.",
  "tags": []
 },
 {
  "z": 2,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "A rational agent must be omniscient, meaning it knows the actual outcome of every action in advance.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "Rational is not the same as perfect.",
  "w": "False. Rationality maximises expected performance given the percepts so far. Omniscience is impossible in practice.",
  "tags": []
 },
 {
  "z": 2,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "You are designing a robot vacuum. Which performance measure encourages better behaviour?",
  "o": [
   "Amount of dirt collected in 8 hours",
   "Number of clean squares at each time step, minus a penalty for energy and noise",
   "Number of times the suction motor is switched on",
   "Minutes spent moving"
  ],
  "a": 1,
  "h": "A measure on dirt collected can be gamed by dumping the dirt and collecting it again.",
  "w": "Reward the state of the environment you actually want (clean floor), not the agent's activity. Otherwise the robot can cheat the measure.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "PEAS is the framework used to specify a task environment. What does it stand for?",
  "o": [
   "Performance, Environment, Actuators, Sensors",
   "Planning, Execution, Action, Search",
   "Percept, Event, Action, State",
   "Problem, Evaluation, Algorithm, Solution"
  ],
  "a": 0,
  "h": "Four letters, four things to write down before building an agent.",
  "w": "PEAS = Performance measure, Environment, Actuators, Sensors.",
  "tags": []
 },
 {
  "z": 2,
  "k": "Match the Following",
  "mode": "m",
  "d": 2,
  "q": "Match each PEAS element to an example for a self-driving taxi.",
  "m": [
   [
    "Performance measure",
    "Safe, legal, fast, comfortable trip"
   ],
   [
    "Environment",
    "Roads, traffic, pedestrians"
   ],
   [
    "Actuators",
    "Steering, accelerator, brake"
   ],
   [
    "Sensors",
    "Cameras, GPS, speedometer"
   ]
  ],
  "h": "Sensors feed in, actuators act out.",
  "w": "The performance measure says what is good, the environment is the world, actuators are outputs and sensors are inputs.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which description fits the task environment of a self-driving taxi?",
  "o": [
   "Fully observable and deterministic",
   "Partially observable, stochastic, dynamic and continuous",
   "Fully observable, static and discrete",
   "Episodic and single-agent"
  ],
  "a": 1,
  "h": "Other cars, weather, and pedestrians are unpredictable.",
  "w": "The taxi cannot see everything, outcomes are uncertain, the world changes while it thinks, and positions and speeds are continuous.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "An agent classifies each X-ray independently, and the label for one image never affects the next. This is a(n) ______ environment.",
  "o": [
   "sequential",
   "episodic",
   "dynamic",
   "continuous"
  ],
  "a": 1,
  "h": "Each decision is a separate, self-contained episode.",
  "w": "In an episodic environment the current decision does not depend on earlier ones. Chess and taxi driving are sequential.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 1,
  "q": "A simple reflex agent chooses its action using only the ______ percept.",
  "a": [
   "current",
   "present",
   "latest"
  ],
  "h": "No memory of the past is used.",
  "w": "Simple reflex agents apply condition–action rules to the current percept alone.",
  "tags": []
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which kind of agent keeps an internal model of the world so it can cope with partial observability?",
  "o": [
   "Simple reflex agent",
   "Model-based reflex agent",
   "Random agent",
   "Table-lookup agent with one entry"
  ],
  "a": 1,
  "h": "It tracks what it cannot currently see.",
  "w": "A model-based reflex agent maintains internal state, updated from percepts and knowledge of how the world evolves.",
  "tags": []
 },
 {
  "z": 2,
  "k": "Scenario",
  "mode": "c",
  "d": 1,
  "q": "A thermostat switches the heater on when the room is below 20°C and off otherwise. What type of agent is it?",
  "o": [
   "Simple reflex agent",
   "Goal-based agent",
   "Utility-based agent",
   "Learning agent"
  ],
  "a": 0,
  "h": "One rule: IF too cold THEN heat.",
  "w": "It maps the current percept straight to an action with a condition–action rule.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "A navigation app picks a route by weighing travel time, tolls and road safety, then chooses the best trade-off. Which agent type is this?",
  "o": [
   "Simple reflex",
   "Model-based reflex",
   "Utility-based",
   "Table-driven"
  ],
  "a": 2,
  "h": "There is a score for how happy each outcome would make the user.",
  "w": "A utility-based agent compares states by a utility function, which lets it trade conflicting goals against each other.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 2,
  "k": "Assertion–Reason",
  "mode": "c",
  "d": 2,
  "q": "A: A learning agent can improve its performance over time in an unknown environment.\nR: It has a learning element that uses feedback from a critic to modify the performance element.",
  "o": [
   "Both A and R are true, and R is the correct explanation of A",
   "Both A and R are true, but R is not the correct explanation of A",
   "A is true, but R is false",
   "A is false, but R is true"
  ],
  "a": 0,
  "h": "Learning element, critic, performance element, problem generator.",
  "w": "Both are true and R is the mechanism that explains A.",
  "tags": []
 },
 {
  "z": 2,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "In a fully observable environment, an agent does not need to keep internal state to track the world.",
  "o": [
   "True",
   "False"
  ],
  "a": 0,
  "h": "If the sensors show everything, what is left to remember?",
  "w": "True. Full observability means the percept already contains the complete relevant state.",
  "tags": []
 },
 {
  "z": 2,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "Which of these is a single-agent environment?",
  "o": [
   "Chess",
   "Poker",
   "Solving a crossword puzzle",
   "Driving in city traffic"
  ],
  "a": 2,
  "h": "No opponent or other decision maker is acting.",
  "w": "A crossword involves one agent only. Chess and poker are competitive multi-agent, and taxi driving is multi-agent.",
  "tags": []
 },
 {
  "z": 3,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "Which component of a formal problem tells the agent which state results from doing action a in state s?",
  "o": [
   "Initial state",
   "Goal test",
   "Transition model (successor function)",
   "Path cost"
  ],
  "a": 2,
  "h": "It answers: if I do this here, where do I end up?",
  "w": "The transition model maps (state, action) to the next state. The goal test only says whether a state is a goal.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 1,
  "q": "The set of all states reachable from the initial state by any sequence of actions is called the ______ space.",
  "a": [
   "state",
   "state space"
  ],
  "h": "Two words in the topic name: state ___ search.",
  "w": "The state space is a graph whose nodes are states and whose edges are actions.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Problem Solving",
  "mode": "c",
  "d": 3,
  "q": "WATER JUGS. You have a 4 L jug and a 3 L jug with no markings. Both start empty. You may fill a jug, empty a jug, or pour one into the other until the source is empty or the target is full. What is the minimum number of actions needed to leave exactly 2 L in the 4 L jug?",
  "o": [
   "4",
   "5",
   "6",
   "7"
  ],
  "a": 2,
  "h": "Write states as (4L jug, 3L jug) and run BFS from (0,0). The 3 L jug can hold 2 L after 4 actions, but that is not what is asked.",
  "w": "BFS over states (4L, 3L) reaches (4,2) at depth 4 and (0,2) at depth 5, but the first states with 2 in the 4 L jug appear at depth 6. One route: fill 3L, pour into 4L, fill 3L, pour into 4L, empty 4L, pour 3L into 4L, which gives (2,0). So the minimum is 6.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 3,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "A production system is made of…",
  "o": [
   "rules, a global database (working memory) and a control strategy",
   "a compiler, a linker and a loader",
   "a neural network and a loss function",
   "sensors, actuators and an environment"
  ],
  "a": 0,
  "h": "IF–THEN rules need data to match against and a way to pick one.",
  "w": "Rules (knowledge), a global database of current facts, and a control strategy that decides which matching rule fires.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 2,
  "q": "When several rules match at the same time in a production system, picking one of them is called ______ resolution.",
  "a": [
   "conflict"
  ],
  "h": "The rules conflict over who gets to fire.",
  "w": "Conflict resolution strategies include rule order, recency, and specificity.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "A garage's diagnostic tool stores rules like “IF engine cranks AND does not start THEN check the fuel pump”. It reads symptoms from the mechanic and applies matching rules. Which AI structure is this?",
  "o": [
   "Production system",
   "Minimax tree",
   "Genetic algorithm",
   "Convolutional network"
  ],
  "a": 0,
  "h": "Look at the IF–THEN shape and the facts being matched.",
  "w": "Condition–action rules acting on a working memory of symptoms is a production system, the base of classic expert systems.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 3,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "In the problem characteristics of Rich and Knight, chess moves are best described as…",
  "o": [
   "ignorable",
   "recoverable",
   "irrecoverable",
   "decomposable"
  ],
  "a": 2,
  "h": "Can you take a move back?",
  "w": "A chess move cannot be undone, so mistakes cannot be recovered by backtracking over real moves. The 8-puzzle is recoverable, and theorem proving is ignorable.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Match the Following",
  "mode": "m",
  "d": 2,
  "q": "Match each problem to the characteristic that describes it best.",
  "m": [
   [
    "Proving a theorem",
    "Ignorable steps"
   ],
   [
    "Solving the 8-puzzle",
    "Recoverable steps"
   ],
   [
    "Playing chess",
    "Irrecoverable steps"
   ],
   [
    "Travelling salesman",
    "Needs the best path, not any path"
   ]
  ],
  "h": "Ask: can I undo a step, and do I need the best solution or just any?",
  "w": "Theorem steps can be ignored if unhelpful, puzzle moves can be reversed, chess moves are permanent, and the TSP asks for the shortest tour.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 3,
  "k": "True / False",
  "mode": "c",
  "d": 1,
  "q": "In the travelling salesman problem, any route that visits every city once is an acceptable solution.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "The word “salesman” hints at cost.",
  "w": "False. A solution must be the shortest tour. This is a best-path problem, unlike a puzzle where any solution will do.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Scenario",
  "mode": "c",
  "d": 3,
  "q": "A planner has one clearly stated goal state but a huge number of possible starting situations, and from the goal only a few actions lead back. Which direction of search is likely to be cheaper?",
  "o": [
   "Forward from the start",
   "Backward from the goal",
   "Neither, they are always equal",
   "Random jumps between states"
  ],
  "a": 1,
  "h": "Choose the direction with the smaller branching factor.",
  "w": "Direction of search is a design issue. Prefer the direction with fewer branches, and backward search suits an explicit goal with few predecessors.",
  "tags": []
 },
 {
  "z": 3,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "A Rubik's Cube has about 43 quintillion states. What is the main problem for a blind search solver?",
  "o": [
   "The goal is unknown",
   "The state space is so large that blind search is hopeless, so heuristics are needed",
   "The cube has no legal moves",
   "The path cost is negative"
  ],
  "a": 1,
  "h": "Count states, not moves.",
  "w": "Combinatorial explosion makes uninformed search impractical. Heuristics and pruning shrink the effective search.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 3,
  "k": "Problem Solving",
  "mode": "c",
  "d": 2,
  "q": "8-PUZZLE. Start:\n1 2 3\n4 _ 6\n7 5 8\nGoal:\n1 2 3\n4 5 6\n7 8 _\nWhat is the minimum number of tile moves?",
  "o": [
   "1",
   "2",
   "3",
   "4"
  ],
  "a": 1,
  "h": "Misplaced tiles are 5 and 8, each only one step from its place.",
  "w": "Slide 5 up into the blank, then slide 8 left. The Manhattan distance heuristic is 1+1 = 2, so 2 moves is optimal.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 3,
  "k": "Assertion–Reason",
  "mode": "c",
  "d": 2,
  "q": "A: State-space search can be viewed as finding a path in a graph.\nR: States are nodes and actions are edges between them.",
  "o": [
   "Both A and R are true, and R is the correct explanation of A",
   "Both A and R are true, but R is not the correct explanation of A",
   "A is true, but R is false",
   "A is false, but R is true"
  ],
  "a": 0,
  "h": "Draw the state space as dots and arrows.",
  "w": "Both true and R is the exact mapping that makes A possible.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Problem Solving",
  "mode": "g",
  "d": 2,
  "q": "PICK THE ORDER. Breadth-First Search starts at A and always visits children left to right. Pick the nodes in the order BFS visits them.",
  "g": {
   "n": {
    "A": [
     200,
     30
    ],
    "B": [
     110,
     100
    ],
    "C": [
     290,
     100
    ],
    "D": [
     60,
     175
    ],
    "E": [
     160,
     175
    ],
    "F": [
     250,
     175
    ],
    "G": [
     340,
     175
    ],
    "H": [
     60,
     245
    ]
   },
   "e": [
    [
     "A",
     "B"
    ],
    [
     "A",
     "C"
    ],
    [
     "B",
     "D"
    ],
    [
     "B",
     "E"
    ],
    [
     "C",
     "F"
    ],
    [
     "C",
     "G"
    ],
    [
     "D",
     "H"
    ]
   ]
  },
  "a": [
   "A",
   "B",
   "C",
   "D",
   "E",
   "F",
   "G",
   "H"
  ],
  "h": "Finish a whole level before going deeper.",
  "w": "BFS uses a queue and explores level by level: A, then B C, then D E F G, then H.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Problem Solving",
  "mode": "g",
  "d": 2,
  "q": "PICK THE ORDER. Depth-First Search starts at A and tries the left child first. Pick the nodes in the order DFS visits them.",
  "g": {
   "n": {
    "A": [
     200,
     30
    ],
    "B": [
     110,
     100
    ],
    "C": [
     290,
     100
    ],
    "D": [
     60,
     175
    ],
    "E": [
     160,
     175
    ],
    "F": [
     250,
     175
    ],
    "G": [
     340,
     175
    ],
    "H": [
     60,
     245
    ]
   },
   "e": [
    [
     "A",
     "B"
    ],
    [
     "A",
     "C"
    ],
    [
     "B",
     "D"
    ],
    [
     "B",
     "E"
    ],
    [
     "C",
     "F"
    ],
    [
     "C",
     "G"
    ],
    [
     "D",
     "H"
    ]
   ]
  },
  "a": [
   "A",
   "B",
   "D",
   "H",
   "E",
   "C",
   "F",
   "G"
  ],
  "h": "Go as deep as possible, then backtrack.",
  "w": "DFS uses a stack: A, B, D, H (dead end), back to E, back up to C, then F, G.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "If you replace the FIFO queue in breadth-first search with a LIFO stack, you get…",
  "o": [
   "Depth-first search",
   "Uniform-cost search",
   "Hill climbing",
   "Iterative deepening"
  ],
  "a": 0,
  "h": "Last in, first out means the newest node is expanded first.",
  "w": "A stack always expands the most recently generated node, which dives deep first.",
  "tags": []
 },
 {
  "z": 4,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "BFS is guaranteed to return an optimal (shortest) solution when…",
  "o": [
   "all step costs are equal",
   "the graph is infinite",
   "the branching factor is 1",
   "the goal is at depth 0 only"
  ],
  "a": 0,
  "h": "It finds the shallowest goal first.",
  "w": "BFS finds the shallowest goal, which is cheapest only if each step costs the same.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "Depth-first search is complete even in a search tree with infinite depth.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "It might follow one endless branch forever.",
  "w": "False. DFS can descend an infinite branch and never return. It is complete only in finite spaces with repeated-state checking.",
  "tags": []
 },
 {
  "z": 4,
  "k": "Scenario",
  "mode": "c",
  "d": 3,
  "q": "A rescue robot has only 64 MB of memory. It explores a huge maze with branching factor 10, and nobody knows how deep the exit is. Which strategy is most suitable?",
  "o": [
   "Plain BFS",
   "Plain DFS",
   "Iterative deepening DFS",
   "Random walk"
  ],
  "a": 2,
  "h": "Which one gets BFS's completeness and DFS's tiny memory?",
  "w": "Iterative deepening uses O(bd) memory like DFS and is complete and optimal for unit costs like BFS.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 2,
  "q": "Iterative deepening search runs depth-limited searches with limit 0, 1, 2… and has time complexity O(b^__), where the blank is the depth of the shallowest goal. Fill in the letter.",
  "a": [
   "d"
  ],
  "h": "Same order as BFS in the worst case.",
  "w": "The repeated work at shallow levels is small, so total time is still O(b^d).",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Problem Solving",
  "mode": "c",
  "d": 2,
  "q": "A complete binary tree has depth 3 (the root is at depth 0). Just before BFS expands any depth-3 node, how many nodes does its frontier hold?",
  "o": [
   "4",
   "7",
   "8",
   "15"
  ],
  "a": 2,
  "h": "Every depth-2 node has two children.",
  "w": "There are 2³ = 8 nodes at depth 3, and all of them are waiting in the frontier. This is why BFS memory grows as b^d.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Assertion–Reason",
  "mode": "c",
  "d": 3,
  "q": "A: Depth-limited search can fail to find a solution even though one exists.\nR: If the depth limit l is smaller than the depth d of the shallowest goal, the goal lies beyond the cutoff.",
  "o": [
   "Both A and R are true, and R is the correct explanation of A",
   "Both A and R are true, but R is not the correct explanation of A",
   "A is true, but R is false",
   "A is false, but R is true"
  ],
  "a": 0,
  "h": "What happens when the limit is too small?",
  "w": "Both true, and R is exactly why the cutoff causes failure.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "A web crawler must collect all pages within 2 clicks of the home page before moving on to deeper pages. Which strategy matches?",
  "o": [
   "Breadth-first search",
   "Depth-first search",
   "Hill climbing",
   "Means-end analysis"
  ],
  "a": 0,
  "h": "Level by level.",
  "w": "Visiting by distance from the start is exactly BFS.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 4,
  "k": "Match the Following",
  "mode": "m",
  "d": 2,
  "q": "Match each uninformed search to its best-known property.",
  "m": [
   [
    "BFS",
    "Complete and optimal for unit step cost"
   ],
   [
    "DFS",
    "Memory only O(b·m)"
   ],
   [
    "Iterative deepening",
    "Complete with linear memory"
   ],
   [
    "Depth-limited search",
    "Needs a cutoff, may miss deeper goals"
   ]
  ],
  "h": "Think about time, memory, and completeness.",
  "w": "These are the standard comparison points of the blind search family.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 5,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "Hill climbing is best described as…",
  "o": [
   "a greedy local search that moves to the best neighbour and never backtracks",
   "a complete search that stores the whole tree",
   "a search that always finds the global optimum",
   "a blind search with a queue"
  ],
  "a": 0,
  "h": "It only looks at its immediate neighbours.",
  "w": "Hill climbing keeps one current state and repeatedly moves uphill. It can get stuck, and it uses very little memory.",
  "tags": []
 },
 {
  "z": 5,
  "k": "Match the Following",
  "mode": "m",
  "d": 2,
  "q": "Match each hill-climbing trap to its description.",
  "m": [
   [
    "Local maximum",
    "Higher than all neighbours but lower than the best peak"
   ],
   [
    "Plateau",
    "Flat region where all neighbours score the same"
   ],
   [
    "Ridge",
    "Sequence of local maxima that single moves cannot climb"
   ],
   [
    "Global maximum",
    "The best state in the whole landscape"
   ]
  ],
  "h": "Picture a landscape of hills.",
  "w": "These are the standard failure modes that variants such as random restart and sideways moves try to fix.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 5,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which hill-climbing variant is the best choice when each state has thousands of successors?",
  "o": [
   "Steepest-ascent",
   "First-choice",
   "Breadth-first search",
   "Exhaustive enumeration"
  ],
  "a": 1,
  "h": "You do not want to score every neighbour.",
  "w": "First-choice generates successors randomly and takes the first one better than the current state, which avoids evaluating all neighbours.",
  "tags": []
 },
 {
  "z": 5,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which variant picks randomly among the uphill moves, with higher probability for steeper moves?",
  "o": [
   "Steepest-ascent",
   "Stochastic hill climbing",
   "Random-restart hill climbing",
   "Simulated annealing"
  ],
  "a": 1,
  "h": "The name tells you chance is involved in the choice of uphill move.",
  "w": "Stochastic hill climbing chooses among uphill moves at random, weighted by steepness.",
  "tags": []
 },
 {
  "z": 5,
  "k": "Scenario",
  "mode": "c",
  "d": 3,
  "q": "A hill climber on 8-queens stops at a state where h = 1 (one pair attacking) and every neighbour has h ≥ 1. Which fix works best?",
  "o": [
   "Run it again from many random initial states and keep the best result",
   "Reduce the board size",
   "Switch to breadth-first search on the same state",
   "Add more queens"
  ],
  "a": 0,
  "h": "If one start gets stuck, try another.",
  "w": "Random-restart hill climbing is complete with probability approaching 1, because some restart will land near the global optimum.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 5,
  "k": "True / False",
  "mode": "c",
  "d": 1,
  "q": "Steepest-ascent hill climbing is guaranteed to find the global maximum.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "What about local maxima?",
  "w": "False. It can stop at a local maximum, a plateau or a ridge.",
  "tags": []
 },
 {
  "z": 5,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Which heuristic for the 8-puzzle is admissible, meaning it never overestimates the true cost?",
  "o": [
   "Sum of Manhattan distances of the tiles (not the blank)",
   "Twice the sum of Manhattan distances",
   "Number of moves already made",
   "A random number from 0 to 30"
  ],
  "a": 0,
  "h": "Each move shifts one tile by one square.",
  "w": "A tile needs at least its Manhattan distance in moves, so the sum is a lower bound. Doubling it can overestimate.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 5,
  "k": "Problem Solving",
  "mode": "g",
  "d": 3,
  "q": "GREEDY BEST-FIRST. The number under each node is its heuristic h. Greedy best-first always expands the frontier node with the smallest h. Pick the nodes in the order they are expanded, from S until G.",
  "g": {
   "n": {
    "S": [
     200,
     30
    ],
    "A": [
     100,
     100
    ],
    "B": [
     300,
     100
    ],
    "C": [
     60,
     175
    ],
    "D": [
     220,
     175
    ],
    "G": [
     140,
     245
    ]
   },
   "e": [
    [
     "S",
     "A"
    ],
    [
     "S",
     "B"
    ],
    [
     "A",
     "C"
    ],
    [
     "A",
     "D"
    ],
    [
     "B",
     "D"
    ],
    [
     "C",
     "G"
    ],
    [
     "D",
     "G"
    ]
   ],
   "h": {
    "S": 7,
    "A": 4,
    "B": 6,
    "C": 2,
    "D": 3,
    "G": 0
   }
  },
  "a": [
   "S",
   "A",
   "C",
   "G"
  ],
  "h": "After S, compare A(4) with B(6). Then add A's children to the frontier.",
  "w": "Expand S, giving A(4), B(6) so A goes next. Expanding A adds C(2) and D(3), so C is next. C leads to G(0), which is expanded and passes the goal test.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 5,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "The evaluation function of A* is f(n) = g(n) + h(n). Greedy best-first search uses…",
  "o": [
   "f(n) = g(n)",
   "f(n) = h(n)",
   "f(n) = g(n) − h(n)",
   "f(n) = 1"
  ],
  "a": 1,
  "h": "Greedy ignores the cost already paid.",
  "w": "Greedy best-first uses only the heuristic estimate h(n), so it is fast but neither optimal nor always complete.",
  "tags": []
 },
 {
  "z": 5,
  "k": "Scenario",
  "mode": "c",
  "d": 1,
  "q": "A map app uses the straight-line distance to the destination to decide which road to try first. This straight-line estimate is an example of…",
  "o": [
   "a heuristic function",
   "a constraint",
   "a percept",
   "an actuator"
  ],
  "a": 0,
  "h": "It estimates the remaining cost.",
  "w": "A heuristic estimates the cost to the goal. Straight-line distance never exceeds road distance, so it is admissible.",
  "tags": [
   "real",
   "search"
  ]
 },
 {
  "z": 5,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "Greedy best-first search always returns the cheapest path.",
  "o": [
   "True",
   "False"
  ],
  "a": 1,
  "h": "It ignores the cost so far.",
  "w": "False. It follows the most promising-looking node and can end up on an expensive route.",
  "tags": []
 },
 {
  "z": 5,
  "k": "Problem Solving",
  "mode": "c",
  "d": 2,
  "q": "In A*, node P has g = 5 and h = 3. Node Q has g = 2 and h = 7. Which node is expanded first?",
  "o": [
   "P, because f = 8 is less than Q's f = 9",
   "Q, because its g is smaller",
   "Q, because its h is larger",
   "They tie"
  ],
  "a": 0,
  "h": "Compute f = g + h for both.",
  "w": "f(P) = 5 + 3 = 8 and f(Q) = 2 + 7 = 9. A* expands the node with the smaller f.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 6,
  "k": "MCQ",
  "mode": "c",
  "d": 1,
  "q": "A constraint satisfaction problem (CSP) is defined by…",
  "o": [
   "variables, domains and constraints",
   "states, actions and rewards",
   "nodes, queues and stacks",
   "percepts, sensors and actuators"
  ],
  "a": 0,
  "h": "Think of map colouring: regions, colours, and rules.",
  "w": "A CSP has variables, a domain of values for each, and constraints that restrict the allowed combinations.",
  "tags": []
 },
 {
  "z": 6,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "A college schedules exams so that no student has two exams at the same time. If exams that share students cannot take the same slot, what are the variables of this CSP?",
  "o": [
   "The time slots",
   "The exams",
   "The students",
   "The rooms"
  ],
  "a": 1,
  "h": "Variables are the things that need a value assigned.",
  "w": "Each exam is a variable whose domain is the set of time slots. The clash rule is a binary constraint between exams.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 6,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "In map colouring, the constraint “WA ≠ NT” involves two variables. It is a ______ constraint.",
  "o": [
   "unary",
   "binary",
   "global",
   "soft"
  ],
  "a": 1,
  "h": "Count the variables in the constraint.",
  "w": "A constraint on exactly two variables is binary.",
  "tags": []
 },
 {
  "z": 6,
  "k": "Problem Solving",
  "mode": "c",
  "d": 3,
  "q": "X, Y and Z each take a value from {1, 2, 3}. Constraints: X < Y and Y < Z. How many complete assignments satisfy all constraints?",
  "o": [
   "0",
   "1",
   "3",
   "6"
  ],
  "a": 1,
  "h": "Y must have something smaller and something larger.",
  "w": "Y has to be strictly between X and Z, so Y = 2, X = 1, Z = 3. Exactly one solution.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 6,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "After assigning a value to a variable, forward checking…",
  "o": [
   "removes inconsistent values from the domains of its unassigned neighbours",
   "undoes the assignment",
   "assigns all other variables at once",
   "sorts the variables alphabetically"
  ],
  "a": 0,
  "h": "It looks one step ahead for dead ends.",
  "w": "Forward checking prunes neighbour domains and backtracks as soon as some domain becomes empty.",
  "tags": [
   "search"
  ]
 },
 {
  "z": 6,
  "k": "Scenario",
  "mode": "c",
  "d": 2,
  "q": "While solving a Sudoku, cell A has 2 candidate digits and cell B has 5. The minimum remaining values (MRV) heuristic picks…",
  "o": [
   "cell A, the most constrained cell",
   "cell B, the least constrained cell",
   "whichever is nearer the top left",
   "a random cell, ignoring the counts"
  ],
  "a": 0,
  "h": "Fail early.",
  "w": "MRV picks the variable with the fewest legal values. It exposes dead ends sooner and keeps the tree small.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 6,
  "k": "Fill in the Blank",
  "mode": "f",
  "d": 2,
  "q": "In n-queens as a CSP, “no two queens attack each other” is a constraint between pairs of queens, so it is a ______ constraint.",
  "a": [
   "binary"
  ],
  "h": "How many variables does each constraint touch?",
  "w": "Each attack check involves two queens, which is binary.",
  "tags": []
 },
 {
  "z": 6,
  "k": "MCQ",
  "mode": "c",
  "d": 2,
  "q": "Means-end analysis solves a problem by…",
  "o": [
   "finding the difference between the current state and the goal and applying an operator that reduces it",
   "expanding every node level by level",
   "always moving to the neighbour with the highest value",
   "assigning values to variables in alphabetical order"
  ],
  "a": 0,
  "h": "Compare, then act.",
  "w": "Means-end analysis picks the largest difference and an operator that reduces it. If the operator cannot be applied yet, it creates a sub-goal.",
  "tags": []
 },
 {
  "z": 6,
  "k": "Scenario",
  "mode": "c",
  "d": 3,
  "q": "A robot must bring a book from a locked room. The difference is “book not in hand”. The operator PICK-UP needs the robot to be at the book, and being in the room needs the door unlocked. Which is the means-end approach?",
  "o": [
   "Make sub-goals: unlock the door, enter the room, then pick up the book",
   "Try random actions until the book appears",
   "Pick the book up from where it is now",
   "Start BFS from the book"
  ],
  "a": 0,
  "h": "Preconditions become new goals.",
  "w": "When an operator's preconditions are not met, means-end analysis sets them as sub-goals and works recursively.",
  "tags": [
   "real"
  ]
 },
 {
  "z": 6,
  "k": "True / False",
  "mode": "c",
  "d": 2,
  "q": "Means-end analysis was a central technique in Newell and Simon's General Problem Solver (GPS).",
  "o": [
   "True",
   "False"
  ],
  "a": 0,
  "h": "Think of the 1950s and early AI.",
  "w": "True. GPS used difference reduction, which is means-end analysis.",
  "tags": []
 },
 {
  "z": 6,
  "k": "Assertion–Reason",
  "mode": "c",
  "d": 3,
  "q": "A: Arc consistency can detect failure earlier than plain backtracking.\nR: It removes values from a variable's domain that have no supporting value in a neighbouring variable's domain.",
  "o": [
   "Both A and R are true, and R is the correct explanation of A",
   "Both A and R are true, but R is not the correct explanation of A",
   "A is true, but R is false",
   "A is false, but R is true"
  ],
  "a": 0,
  "h": "What does pruning domains do to dead ends?",
  "w": "Both true. Emptying a domain during propagation shows that no solution exists on this path before more assignments are made.",
  "tags": [
   "search"
  ]
 }
]
