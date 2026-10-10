#!/usr/bin/env python3
"""
Ember and Tide  -  Python (tkinter) edition
-------------------------------------------
Easy (Scout) and Medium (Explorer) modes only.
The window is fully resizable: every page stretches to the full window width,
text re-wraps, fonts scale with the window, and long pages scroll.

Run:   python ember_and_tide.py
Keys:  1-4 answer multiple choice, Enter = continue, F11 = fullscreen, Esc = leave fullscreen
Needs: Python 3.8+ with tkinter (ships with the python.org installers).
"""
import json
import math
import os
import random
import re
import time
import tkinter as tk
import tkinter.font as tkfont

# --------------------------------------------------------------------------- data
QUESTIONS = json.loads(r'''[{"z":1,"k":"MCQ","mode":"c","d":1,"q":"Which approach to AI builds systems that do the right thing given what they know, judged by expected outcome rather than by resemblance to people?","o":["Thinking humanly","Acting humanly","Thinking rationally","Acting rationally"],"a":3,"h":"The modern textbook view centres on the rational agent.","w":"Acting rationally (the rational-agent approach) aims at the best expected outcome. Acting humanly is the Turing Test approach."},{"z":1,"k":"MCQ","mode":"c","d":1,"q":"In the Turing Test, the interrogator's job is to decide…","o":["whether the machine can solve NP-hard problems","whether the unseen respondent is a human or a machine","whether the machine is conscious","whether the machine can beat a human at chess"],"a":1,"h":"It is a text conversation through a screen.","w":"The interrogator chats with two hidden parties and tries to tell which one is the machine. If they cannot, the machine passes."},{"z":1,"k":"True / False","mode":"c","d":2,"q":"A machine that passes the basic (text-only) Turing Test must also be able to see objects and move them around.","o":["True","False"],"a":1,"h":"Which version of the test adds vision and robotics?","w":"False. Seeing and manipulating objects belongs to the Total Turing Test. The basic test is text only.","o_fixed":"TF"},{"z":1,"k":"MCQ","mode":"c","d":2,"q":"Which capability is NOT needed to pass the basic, text-only Turing Test?","o":["Natural language processing","Knowledge representation","Computer vision","Machine learning"],"a":2,"h":"The conversation happens through typed text.","w":"Vision is needed only for the Total Turing Test. The basic test needs language, stored knowledge, reasoning and learning."},{"z":1,"k":"Scenario","mode":"c","d":1,"tags":["real"],"q":"A hospital deploys a system that scans chest X-rays and highlights suspicious regions for the radiologist. Which AI area does this mainly use?","o":["Computer vision","Speech recognition","Game playing","Robot motion planning"],"a":0,"h":"The input is an image.","w":"Interpreting images is the job of computer vision, usually with learned models."},{"z":1,"k":"Match the Following","mode":"m","d":1,"tags":["real","search"],"q":"Match each everyday product to the AI area behind it.","m":[["Phone face unlock","Computer vision"],["Voice assistant answering a question","Speech and language"],["Maps choosing a route","Search algorithms"],["Shopping site suggestions","Machine learning"]],"h":"Think about what the input is in each case.","w":"Face unlock reads images, assistants process speech and language, route finders run graph search, and recommendations are learned from past behaviour."},{"z":1,"k":"Fill in the Blank","mode":"f","d":2,"q":"A version of the Turing Test that also requires computer vision and robotics is called the ______ Turing Test.","a":["total"],"h":"It tests the whole body, not just the conversation.","w":"The Total Turing Test adds a video channel and physical objects to pass through a hatch."},{"z":1,"k":"Assertion–Reason","mode":"c","d":3,"q":"A: Passing the Turing Test proves that a machine truly understands language.\nR: The test only checks whether the machine's behaviour is indistinguishable from a human's.","o":["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, but R is false","A is false, but R is true"],"a":3,"h":"Remember Searle's Chinese Room argument.","w":"A is false: behaving convincingly is not proof of understanding. R is true, and it is exactly why A fails.","o_fixed":"AR"},{"z":1,"k":"Scenario","mode":"c","d":2,"q":"ELIZA fooled some users by turning their sentences into questions using simple pattern rules. What does this show about the Turing Test?","o":["Pattern tricks can imitate conversation without real understanding","ELIZA understood human emotions","The Turing Test can never be passed","The test needs speech, not text"],"a":0,"h":"Was there any reasoning inside ELIZA?","w":"ELIZA used keyword rules. It shows that convincing talk can come from shallow tricks, which is a known weakness of the test."},{"z":1,"k":"MCQ","mode":"c","d":2,"tags":["real","search"],"q":"IBM's Deep Blue beat the world chess champion mainly by…","o":["searching deep game trees and scoring positions with an evaluation function","learning from millions of self-play games with a neural network","asking human grandmasters for each move","memorising every possible chess game"],"a":0,"h":"Think search plus a scoring function.","w":"Deep Blue combined very fast game-tree search with a hand-tuned evaluation function. Chess has far too many games to memorise."},{"z":2,"k":"MCQ","mode":"c","d":1,"q":"An agent perceives its environment through ______ and acts on it through ______.","o":["sensors, actuators","actuators, sensors","goals, plans","rules, facts"],"a":0,"h":"Eyes and hands are the human version.","w":"Sensors deliver percepts and actuators carry out actions. Together they form the agent's link with the world."},{"z":2,"k":"MCQ","mode":"c","d":1,"q":"The mapping from every possible percept sequence to an action is called the agent's…","o":["agent program","agent function","performance measure","environment"],"a":1,"h":"One is the abstract mapping, the other is the code that implements it.","w":"The agent function is the abstract mapping. The agent program is the concrete code that runs on the machine."},{"z":2,"k":"True / False","mode":"c","d":2,"q":"A rational agent must be omniscient, meaning it knows the actual outcome of every action in advance.","o":["True","False"],"a":1,"h":"Rational is not the same as perfect.","w":"False. Rationality maximises expected performance given the percepts so far. Omniscience is impossible in practice.","o_fixed":"TF"},{"z":2,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"You are designing a robot vacuum. Which performance measure encourages better behaviour?","o":["Amount of dirt collected in 8 hours","Number of clean squares at each time step, minus a penalty for energy and noise","Number of times the suction motor is switched on","Minutes spent moving"],"a":1,"h":"A measure on dirt collected can be gamed by dumping the dirt and collecting it again.","w":"Reward the state of the environment you actually want (clean floor), not the agent's activity. Otherwise the robot can cheat the measure."},{"z":2,"k":"MCQ","mode":"c","d":1,"q":"PEAS is the framework used to specify a task environment. What does it stand for?","o":["Performance, Environment, Actuators, Sensors","Planning, Execution, Action, Search","Percept, Event, Action, State","Problem, Evaluation, Algorithm, Solution"],"a":0,"h":"Four letters, four things to write down before building an agent.","w":"PEAS = Performance measure, Environment, Actuators, Sensors."},{"z":2,"k":"Match the Following","mode":"m","d":2,"tags":["real"],"q":"Match each PEAS element to an example for a self-driving taxi.","m":[["Performance measure","Safe, legal, fast, comfortable trip"],["Environment","Roads, traffic, pedestrians"],["Actuators","Steering, accelerator, brake"],["Sensors","Cameras, GPS, speedometer"]],"h":"Sensors feed in, actuators act out.","w":"The performance measure says what is good, the environment is the world, actuators are outputs and sensors are inputs."},{"z":2,"k":"MCQ","mode":"c","d":2,"tags":["real"],"q":"Which description fits the task environment of a self-driving taxi?","o":["Fully observable and deterministic","Partially observable, stochastic, dynamic and continuous","Fully observable, static and discrete","Episodic and single-agent"],"a":1,"h":"Other cars, weather, and pedestrians are unpredictable.","w":"The taxi cannot see everything, outcomes are uncertain, the world changes while it thinks, and positions and speeds are continuous."},{"z":2,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"An agent classifies each X-ray independently, and the label for one image never affects the next. This is a(n) ______ environment.","o":["sequential","episodic","dynamic","continuous"],"a":1,"h":"Each decision is a separate, self-contained episode.","w":"In an episodic environment the current decision does not depend on earlier ones. Chess and taxi driving are sequential."},{"z":2,"k":"Fill in the Blank","mode":"f","d":1,"q":"A simple reflex agent chooses its action using only the ______ percept.","a":["current","present","latest"],"h":"No memory of the past is used.","w":"Simple reflex agents apply condition–action rules to the current percept alone."},{"z":2,"k":"MCQ","mode":"c","d":2,"q":"Which kind of agent keeps an internal model of the world so it can cope with partial observability?","o":["Simple reflex agent","Model-based reflex agent","Random agent","Table-lookup agent with one entry"],"a":1,"h":"It tracks what it cannot currently see.","w":"A model-based reflex agent maintains internal state, updated from percepts and knowledge of how the world evolves."},{"z":2,"k":"Scenario","mode":"c","d":1,"tags":["real"],"q":"A thermostat switches the heater on when the room is below 20°C and off otherwise. What type of agent is it?","o":["Simple reflex agent","Goal-based agent","Utility-based agent","Learning agent"],"a":0,"h":"One rule: IF too cold THEN heat.","w":"It maps the current percept straight to an action with a condition–action rule."},{"z":2,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"A navigation app picks a route by weighing travel time, tolls and road safety, then chooses the best trade-off. Which agent type is this?","o":["Simple reflex","Model-based reflex","Utility-based","Table-driven"],"a":2,"h":"There is a score for how happy each outcome would make the user.","w":"A utility-based agent compares states by a utility function, which lets it trade conflicting goals against each other."},{"z":2,"k":"Assertion–Reason","mode":"c","d":2,"q":"A: A learning agent can improve its performance over time in an unknown environment.\nR: It has a learning element that uses feedback from a critic to modify the performance element.","o":["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, but R is false","A is false, but R is true"],"a":0,"h":"Learning element, critic, performance element, problem generator.","w":"Both are true and R is the mechanism that explains A.","o_fixed":"AR"},{"z":2,"k":"True / False","mode":"c","d":2,"q":"In a fully observable environment, an agent does not need to keep internal state to track the world.","o":["True","False"],"a":0,"h":"If the sensors show everything, what is left to remember?","w":"True. Full observability means the percept already contains the complete relevant state.","o_fixed":"TF"},{"z":2,"k":"MCQ","mode":"c","d":1,"q":"Which of these is a single-agent environment?","o":["Chess","Poker","Solving a crossword puzzle","Driving in city traffic"],"a":2,"h":"No opponent or other decision maker is acting.","w":"A crossword involves one agent only. Chess and poker are competitive multi-agent, and taxi driving is multi-agent."},{"z":3,"k":"MCQ","mode":"c","d":1,"q":"Which component of a formal problem tells the agent which state results from doing action a in state s?","o":["Initial state","Goal test","Transition model (successor function)","Path cost"],"a":2,"h":"It answers: if I do this here, where do I end up?","w":"The transition model maps (state, action) to the next state. The goal test only says whether a state is a goal."},{"z":3,"k":"Fill in the Blank","mode":"f","d":1,"q":"The set of all states reachable from the initial state by any sequence of actions is called the ______ space.","a":["state","state space"],"h":"Two words in the topic name: state ___ search.","w":"The state space is a graph whose nodes are states and whose edges are actions."},{"z":3,"k":"Problem Solving","mode":"c","d":3,"tags":["search"],"q":"WATER JUGS. You have a 4 L jug and a 3 L jug with no markings. Both start empty. You may fill a jug, empty a jug, or pour one into the other until the source is empty or the target is full. What is the minimum number of actions needed to leave exactly 2 L in the 4 L jug?","o":["4","5","6","7"],"a":2,"h":"Write states as (4L jug, 3L jug) and run BFS from (0,0). The 3 L jug can hold 2 L after 4 actions, but that is not what is asked.","w":"BFS over states (4L, 3L) reaches (4,2) at depth 4 and (0,2) at depth 5, but the first states with 2 in the 4 L jug appear at depth 6. One route: fill 3L, pour into 4L, fill 3L, pour into 4L, empty 4L, pour 3L into 4L, which gives (2,0). So the minimum is 6."},{"z":3,"k":"MCQ","mode":"c","d":2,"q":"A production system is made of…","o":["rules, a global database (working memory) and a control strategy","a compiler, a linker and a loader","a neural network and a loss function","sensors, actuators and an environment"],"a":0,"h":"IF–THEN rules need data to match against and a way to pick one.","w":"Rules (knowledge), a global database of current facts, and a control strategy that decides which matching rule fires."},{"z":3,"k":"Fill in the Blank","mode":"f","d":2,"q":"When several rules match at the same time in a production system, picking one of them is called ______ resolution.","a":["conflict"],"h":"The rules conflict over who gets to fire.","w":"Conflict resolution strategies include rule order, recency, and specificity."},{"z":3,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"A garage's diagnostic tool stores rules like “IF engine cranks AND does not start THEN check the fuel pump”. It reads symptoms from the mechanic and applies matching rules. Which AI structure is this?","o":["Production system","Minimax tree","Genetic algorithm","Convolutional network"],"a":0,"h":"Look at the IF–THEN shape and the facts being matched.","w":"Condition–action rules acting on a working memory of symptoms is a production system, the base of classic expert systems."},{"z":3,"k":"MCQ","mode":"c","d":2,"q":"In the problem characteristics of Rich and Knight, chess moves are best described as…","o":["ignorable","recoverable","irrecoverable","decomposable"],"a":2,"h":"Can you take a move back?","w":"A chess move cannot be undone, so mistakes cannot be recovered by backtracking over real moves. The 8-puzzle is recoverable, and theorem proving is ignorable."},{"z":3,"k":"Match the Following","mode":"m","d":2,"tags":["search"],"q":"Match each problem to the characteristic that describes it best.","m":[["Proving a theorem","Ignorable steps"],["Solving the 8-puzzle","Recoverable steps"],["Playing chess","Irrecoverable steps"],["Travelling salesman","Needs the best path, not any path"]],"h":"Ask: can I undo a step, and do I need the best solution or just any?","w":"Theorem steps can be ignored if unhelpful, puzzle moves can be reversed, chess moves are permanent, and the TSP asks for the shortest tour."},{"z":3,"k":"True / False","mode":"c","d":1,"q":"In the travelling salesman problem, any route that visits every city once is an acceptable solution.","o":["True","False"],"a":1,"h":"The word “salesman” hints at cost.","w":"False. A solution must be the shortest tour. This is a best-path problem, unlike a puzzle where any solution will do.","o_fixed":"TF"},{"z":3,"k":"Scenario","mode":"c","d":3,"q":"A planner has one clearly stated goal state but a huge number of possible starting situations, and from the goal only a few actions lead back. Which direction of search is likely to be cheaper?","o":["Forward from the start","Backward from the goal","Neither, they are always equal","Random jumps between states"],"a":1,"h":"Choose the direction with the smaller branching factor.","w":"Direction of search is a design issue. Prefer the direction with fewer branches, and backward search suits an explicit goal with few predecessors."},{"z":3,"k":"Scenario","mode":"c","d":2,"tags":["real","search"],"q":"A Rubik's Cube has about 43 quintillion states. What is the main problem for a blind search solver?","o":["The goal is unknown","The state space is so large that blind search is hopeless, so heuristics are needed","The cube has no legal moves","The path cost is negative"],"a":1,"h":"Count states, not moves.","w":"Combinatorial explosion makes uninformed search impractical. Heuristics and pruning shrink the effective search."},{"z":3,"k":"Problem Solving","mode":"c","d":2,"tags":["search"],"q":"8-PUZZLE. Start:\n1 2 3\n4 _ 6\n7 5 8\nGoal:\n1 2 3\n4 5 6\n7 8 _\nWhat is the minimum number of tile moves?","o":["1","2","3","4"],"a":1,"h":"Misplaced tiles are 5 and 8, each only one step from its place.","w":"Slide 5 up into the blank, then slide 8 left. The Manhattan distance heuristic is 1+1 = 2, so 2 moves is optimal."},{"z":3,"k":"Assertion–Reason","mode":"c","d":2,"tags":["search"],"q":"A: State-space search can be viewed as finding a path in a graph.\nR: States are nodes and actions are edges between them.","o":["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, but R is false","A is false, but R is true"],"a":0,"h":"Draw the state space as dots and arrows.","w":"Both true and R is the exact mapping that makes A possible.","o_fixed":"AR"},{"z":4,"k":"Problem Solving","mode":"g","d":2,"tags":["search"],"q":"TAP THE ORDER. Breadth-First Search starts at A and always visits children left to right. Tap the nodes in the order BFS visits them.","g":{"n":{"A":[200,30],"B":[110,100],"C":[290,100],"D":[60,175],"E":[160,175],"F":[250,175],"G":[340,175],"H":[60,245]},"e":[["A","B"],["A","C"],["B","D"],["B","E"],["C","F"],["C","G"],["D","H"]]},"a":["A","B","C","D","E","F","G","H"],"h":"Finish a whole level before going deeper.","w":"BFS uses a queue and explores level by level: A, then B C, then D E F G, then H."},{"z":4,"k":"Problem Solving","mode":"g","d":2,"tags":["search"],"q":"TAP THE ORDER. Depth-First Search starts at A and tries the left child first. Tap the nodes in the order DFS visits them.","g":{"n":{"A":[200,30],"B":[110,100],"C":[290,100],"D":[60,175],"E":[160,175],"F":[250,175],"G":[340,175],"H":[60,245]},"e":[["A","B"],["A","C"],["B","D"],["B","E"],["C","F"],["C","G"],["D","H"]]},"a":["A","B","D","H","E","C","F","G"],"h":"Go as deep as possible, then backtrack.","w":"DFS uses a stack: A, B, D, H (dead end), back to E, back up to C, then F, G."},{"z":4,"k":"MCQ","mode":"c","d":1,"q":"If you replace the FIFO queue in breadth-first search with a LIFO stack, you get…","o":["Depth-first search","Uniform-cost search","Hill climbing","Iterative deepening"],"a":0,"h":"Last in, first out means the newest node is expanded first.","w":"A stack always expands the most recently generated node, which dives deep first."},{"z":4,"k":"MCQ","mode":"c","d":2,"tags":["search"],"q":"BFS is guaranteed to return an optimal (shortest) solution when…","o":["all step costs are equal","the graph is infinite","the branching factor is 1","the goal is at depth 0 only"],"a":0,"h":"It finds the shallowest goal first.","w":"BFS finds the shallowest goal, which is cheapest only if each step costs the same."},{"z":4,"k":"True / False","mode":"c","d":2,"q":"Depth-first search is complete even in a search tree with infinite depth.","o":["True","False"],"a":1,"h":"It might follow one endless branch forever.","w":"False. DFS can descend an infinite branch and never return. It is complete only in finite spaces with repeated-state checking.","o_fixed":"TF"},{"z":4,"k":"Scenario","mode":"c","d":3,"tags":["real","search"],"q":"A rescue robot has only 64 MB of memory. It explores a huge maze with branching factor 10, and nobody knows how deep the exit is. Which strategy is most suitable?","o":["Plain BFS","Plain DFS","Iterative deepening DFS","Random walk"],"a":2,"h":"Which one gets BFS's completeness and DFS's tiny memory?","w":"Iterative deepening uses O(bd) memory like DFS and is complete and optimal for unit costs like BFS."},{"z":4,"k":"Fill in the Blank","mode":"f","d":2,"tags":["search"],"q":"Iterative deepening search runs depth-limited searches with limit 0, 1, 2… and has time complexity O(b^__), where the blank is the depth of the shallowest goal. Fill in the letter.","a":["d"],"h":"Same order as BFS in the worst case.","w":"The repeated work at shallow levels is small, so total time is still O(b^d)."},{"z":4,"k":"Problem Solving","mode":"c","d":2,"tags":["search"],"q":"A complete binary tree has depth 3 (the root is at depth 0). Just before BFS expands any depth-3 node, how many nodes does its frontier hold?","o":["4","7","8","15"],"a":2,"h":"Every depth-2 node has two children.","w":"There are 2³ = 8 nodes at depth 3, and all of them are waiting in the frontier. This is why BFS memory grows as b^d."},{"z":4,"k":"Assertion–Reason","mode":"c","d":3,"tags":["search"],"q":"A: Depth-limited search can fail to find a solution even though one exists.\nR: If the depth limit l is smaller than the depth d of the shallowest goal, the goal lies beyond the cutoff.","o":["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, but R is false","A is false, but R is true"],"a":0,"h":"What happens when the limit is too small?","w":"Both true, and R is exactly why the cutoff causes failure.","o_fixed":"AR"},{"z":4,"k":"Scenario","mode":"c","d":2,"tags":["real","search"],"q":"A web crawler must collect all pages within 2 clicks of the home page before moving on to deeper pages. Which strategy matches?","o":["Breadth-first search","Depth-first search","Hill climbing","Means-end analysis"],"a":0,"h":"Level by level.","w":"Visiting by distance from the start is exactly BFS."},{"z":4,"k":"Match the Following","mode":"m","d":2,"tags":["search"],"q":"Match each uninformed search to its best-known property.","m":[["BFS","Complete and optimal for unit step cost"],["DFS","Memory only O(b·m)"],["Iterative deepening","Complete with linear memory"],["Depth-limited search","Needs a cutoff, may miss deeper goals"]],"h":"Think about time, memory, and completeness.","w":"These are the standard comparison points of the blind search family."},{"z":5,"k":"MCQ","mode":"c","d":1,"q":"Hill climbing is best described as…","o":["a greedy local search that moves to the best neighbour and never backtracks","a complete search that stores the whole tree","a search that always finds the global optimum","a blind search with a queue"],"a":0,"h":"It only looks at its immediate neighbours.","w":"Hill climbing keeps one current state and repeatedly moves uphill. It can get stuck, and it uses very little memory."},{"z":5,"k":"Match the Following","mode":"m","d":2,"tags":["search"],"q":"Match each hill-climbing trap to its description.","m":[["Local maximum","Higher than all neighbours but lower than the best peak"],["Plateau","Flat region where all neighbours score the same"],["Ridge","Sequence of local maxima that single moves cannot climb"],["Global maximum","The best state in the whole landscape"]],"h":"Picture a landscape of hills.","w":"These are the standard failure modes that variants such as random restart and sideways moves try to fix."},{"z":5,"k":"MCQ","mode":"c","d":2,"q":"Which hill-climbing variant is the best choice when each state has thousands of successors?","o":["Steepest-ascent","First-choice","Breadth-first search","Exhaustive enumeration"],"a":1,"h":"You do not want to score every neighbour.","w":"First-choice generates successors randomly and takes the first one better than the current state, which avoids evaluating all neighbours."},{"z":5,"k":"MCQ","mode":"c","d":2,"q":"Which variant picks randomly among the uphill moves, with higher probability for steeper moves?","o":["Steepest-ascent","Stochastic hill climbing","Random-restart hill climbing","Simulated annealing"],"a":1,"h":"The name tells you chance is involved in the choice of uphill move.","w":"Stochastic hill climbing chooses among uphill moves at random, weighted by steepness."},{"z":5,"k":"Scenario","mode":"c","d":3,"tags":["search"],"q":"A hill climber on 8-queens stops at a state where h = 1 (one pair attacking) and every neighbour has h ≥ 1. Which fix works best?","o":["Run it again from many random initial states and keep the best result","Reduce the board size","Switch to breadth-first search on the same state","Add more queens"],"a":0,"h":"If one start gets stuck, try another.","w":"Random-restart hill climbing is complete with probability approaching 1, because some restart will land near the global optimum."},{"z":5,"k":"True / False","mode":"c","d":1,"q":"Steepest-ascent hill climbing is guaranteed to find the global maximum.","o":["True","False"],"a":1,"h":"What about local maxima?","w":"False. It can stop at a local maximum, a plateau or a ridge.","o_fixed":"TF"},{"z":5,"k":"MCQ","mode":"c","d":2,"tags":["search"],"q":"Which heuristic for the 8-puzzle is admissible, meaning it never overestimates the true cost?","o":["Sum of Manhattan distances of the tiles (not the blank)","Twice the sum of Manhattan distances","Number of moves already made","A random number from 0 to 30"],"a":0,"h":"Each move shifts one tile by one square.","w":"A tile needs at least its Manhattan distance in moves, so the sum is a lower bound. Doubling it can overestimate."},{"z":5,"k":"Problem Solving","mode":"g","d":3,"tags":["search"],"q":"GREEDY BEST-FIRST. The number under each node is its heuristic h. Greedy best-first always expands the frontier node with the smallest h. Tap the nodes in the order they are expanded, from S until G.","g":{"n":{"S":[200,30],"A":[100,100],"B":[300,100],"C":[60,175],"D":[220,175],"G":[140,245]},"e":[["S","A"],["S","B"],["A","C"],["A","D"],["B","D"],["C","G"],["D","G"]],"h":{"S":7,"A":4,"B":6,"C":2,"D":3,"G":0}},"a":["S","A","C","G"],"h":"After S, compare A(4) with B(6). Then add A's children to the frontier.","w":"Expand S, giving A(4), B(6) so A goes next. Expanding A adds C(2) and D(3), so C is next. C leads to G(0), which is expanded and passes the goal test."},{"z":5,"k":"MCQ","mode":"c","d":2,"q":"The evaluation function of A* is f(n) = g(n) + h(n). Greedy best-first search uses…","o":["f(n) = g(n)","f(n) = h(n)","f(n) = g(n) − h(n)","f(n) = 1"],"a":1,"h":"Greedy ignores the cost already paid.","w":"Greedy best-first uses only the heuristic estimate h(n), so it is fast but neither optimal nor always complete."},{"z":5,"k":"Scenario","mode":"c","d":1,"tags":["real","search"],"q":"A map app uses the straight-line distance to the destination to decide which road to try first. This straight-line estimate is an example of…","o":["a heuristic function","a constraint","a percept","an actuator"],"a":0,"h":"It estimates the remaining cost.","w":"A heuristic estimates the cost to the goal. Straight-line distance never exceeds road distance, so it is admissible."},{"z":5,"k":"True / False","mode":"c","d":2,"q":"Greedy best-first search always returns the cheapest path.","o":["True","False"],"a":1,"h":"It ignores the cost so far.","w":"False. It follows the most promising-looking node and can end up on an expensive route.","o_fixed":"TF"},{"z":5,"k":"Problem Solving","mode":"c","d":2,"tags":["search"],"q":"In A*, node P has g = 5 and h = 3. Node Q has g = 2 and h = 7. Which node is expanded first?","o":["P, because f = 8 is less than Q's f = 9","Q, because its g is smaller","Q, because its h is larger","They tie"],"a":0,"h":"Compute f = g + h for both.","w":"f(P) = 5 + 3 = 8 and f(Q) = 2 + 7 = 9. A* expands the node with the smaller f."},{"z":6,"k":"MCQ","mode":"c","d":1,"q":"A constraint satisfaction problem (CSP) is defined by…","o":["variables, domains and constraints","states, actions and rewards","nodes, queues and stacks","percepts, sensors and actuators"],"a":0,"h":"Think of map colouring: regions, colours, and rules.","w":"A CSP has variables, a domain of values for each, and constraints that restrict the allowed combinations."},{"z":6,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"A college schedules exams so that no student has two exams at the same time. If exams that share students cannot take the same slot, what are the variables of this CSP?","o":["The time slots","The exams","The students","The rooms"],"a":1,"h":"Variables are the things that need a value assigned.","w":"Each exam is a variable whose domain is the set of time slots. The clash rule is a binary constraint between exams."},{"z":6,"k":"MCQ","mode":"c","d":2,"q":"In map colouring, the constraint “WA ≠ NT” involves two variables. It is a ______ constraint.","o":["unary","binary","global","soft"],"a":1,"h":"Count the variables in the constraint.","w":"A constraint on exactly two variables is binary."},{"z":6,"k":"Problem Solving","mode":"c","d":3,"tags":["search"],"q":"X, Y and Z each take a value from {1, 2, 3}. Constraints: X < Y and Y < Z. How many complete assignments satisfy all constraints?","o":["0","1","3","6"],"a":1,"h":"Y must have something smaller and something larger.","w":"Y has to be strictly between X and Z, so Y = 2, X = 1, Z = 3. Exactly one solution."},{"z":6,"k":"MCQ","mode":"c","d":2,"tags":["search"],"q":"After assigning a value to a variable, forward checking…","o":["removes inconsistent values from the domains of its unassigned neighbours","undoes the assignment","assigns all other variables at once","sorts the variables alphabetically"],"a":0,"h":"It looks one step ahead for dead ends.","w":"Forward checking prunes neighbour domains and backtracks as soon as some domain becomes empty."},{"z":6,"k":"Scenario","mode":"c","d":2,"tags":["real"],"q":"While solving a Sudoku, cell A has 2 candidate digits and cell B has 5. The minimum remaining values (MRV) heuristic picks…","o":["cell A, the most constrained cell","cell B, the least constrained cell","whichever is nearer the top left","a random cell, ignoring the counts"],"a":0,"h":"Fail early.","w":"MRV picks the variable with the fewest legal values. It exposes dead ends sooner and keeps the tree small."},{"z":6,"k":"Fill in the Blank","mode":"f","d":2,"q":"In n-queens as a CSP, “no two queens attack each other” is a constraint between pairs of queens, so it is a ______ constraint.","a":["binary"],"h":"How many variables does each constraint touch?","w":"Each attack check involves two queens, which is binary."},{"z":6,"k":"MCQ","mode":"c","d":2,"q":"Means-end analysis solves a problem by…","o":["finding the difference between the current state and the goal and applying an operator that reduces it","expanding every node level by level","always moving to the neighbour with the highest value","assigning values to variables in alphabetical order"],"a":0,"h":"Compare, then act.","w":"Means-end analysis picks the largest difference and an operator that reduces it. If the operator cannot be applied yet, it creates a sub-goal."},{"z":6,"k":"Scenario","mode":"c","d":3,"tags":["real"],"q":"A robot must bring a book from a locked room. The difference is “book not in hand”. The operator PICK-UP needs the robot to be at the book, and being in the room needs the door unlocked. Which is the means-end approach?","o":["Make sub-goals: unlock the door, enter the room, then pick up the book","Try random actions until the book appears","Pick the book up from where it is now","Start BFS from the book"],"a":0,"h":"Preconditions become new goals.","w":"When an operator's preconditions are not met, means-end analysis sets them as sub-goals and works recursively."},{"z":6,"k":"True / False","mode":"c","d":2,"q":"Means-end analysis was a central technique in Newell and Simon's General Problem Solver (GPS).","o":["True","False"],"a":0,"h":"Think of the 1950s and early AI.","w":"True. GPS used difference reduction, which is means-end analysis.","o_fixed":"TF"},{"z":6,"k":"Assertion–Reason","mode":"c","d":3,"tags":["search"],"q":"A: Arc consistency can detect failure earlier than plain backtracking.\nR: It removes values from a variable's domain that have no supporting value in a neighbouring variable's domain.","o":["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, but R is false","A is false, but R is true"],"a":0,"h":"What does pruning domains do to dead ends?","w":"Both true. Emptying a domain during propagation shows that no solution exists on this path before more assignments are made.","o_fixed":"AR"}]''')

C = dict(
    ink="#12101c", stone="#1c1930", stone2="#28234a", line="#3b3562", text="#f0ecff",
    mute="#a7a1c9", ember="#ff7a3d", ember_deep="#a8431a", tide="#35c6d9", tide_deep="#1b7f8c",
    gold="#f4c95d", ok="#6ee7a0", bad="#ff5d6c", ok_bg="#153227", bad_bg="#3a1620",
    fb_ok="#12291f", fb_no="#2e121a", tip_bg="#2c2610", tip_line="#6b5a22",
)
LETTERS = "ABCDEFGH"
DLABEL = ["", "Easy", "Medium", "Hard"]

ZONES = [None,
    dict(n="Gate of Minds", t="Foundations and the Turing Test",
         tip="AI can be judged by how it thinks or how it acts, and by whether it copies people or is rational. Modern AI aims at acting rationally."),
    dict(n="Hall of Agents", t="Rational agents and environments",
         tip="An agent maps percepts to actions. Judge it with a performance measure, and describe its task with PEAS and the properties of its environment."),
    dict(n="Maze of Problems", t="State spaces and production systems",
         tip="A problem has an initial state, actions, a transition model, a goal test and a path cost. Search is then a walk through the state-space graph."),
    dict(n="Blind Bridge", t="BFS, DFS and iterative deepening",
         tip="Blind search has no idea how close a state is to the goal. BFS goes shallow first, DFS goes deep first, and iterative deepening mixes both."),
    dict(n="Heuristic Peak", t="Hill climbing, heuristics and best-first search",
         tip="A heuristic estimates the distance to the goal. Hill climbing climbs greedily and can get stuck. Best-first and A* keep a frontier."),
    dict(n="Vault of Constraints", t="CSP and means-end analysis",
         tip="A CSP has variables, domains and constraints. Means-end analysis shrinks the gap between state and goal by picking operators and sub-goals."),
]

# Only the two modes you asked for: Easy and Medium.
DIFFS = {
    "scout":    dict(name="Easy",   per=3, hearts=6, time=45, maxd=2,
                     blurb="3 per chamber, easier picks, 6 lives, 45 s"),
    "explorer": dict(name="Medium", per=5, hearts=5, time=30, maxd=None,
                     blurb="5 per chamber, 5 lives, 30 s"),
}

LB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ember_tide_leaderboard.json")


def normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def options_of(q):
    return q["o"]


def ans_text(q):
    m = q["mode"]
    if m == "c":
        return q["o"][q["a"]]
    if m == "f":
        return "  /  ".join(q["a"])
    if m == "m":
        return "\n".join(p[0] + "  ->  " + p[1] for p in q["m"])
    if m == "g":
        return "  ->  ".join(q["a"])
    return ""


# --------------------------------------------------------------------------- widgets
class Btn(tk.Label):
    """Flat label-based button: looks identical on Windows, macOS and Linux."""
    KINDS = {
        "ember": (C["ember"], "#1d0b02", "#4a2c1c", C["ember"]),
        "tide":  (C["tide"], "#03242a", "#1c4a52", C["tide"]),
        "plain": (C["stone2"], C["text"], C["stone2"], C["line"]),
        "ghost": (C["stone"], C["text"], C["stone"], C["line"]),
        "opt":   (C["stone2"], C["text"], C["stone2"], C["line"]),
    }

    def __init__(self, parent, text, command, font, kind="plain", anchor="center", wrap=False, padx=18, pady=9):
        bg, fg, dbg, border = self.KINDS[kind]
        super().__init__(parent, text=text, font=font, bg=bg, fg=fg, anchor=anchor,
                         justify="left" if anchor in ("w", "nw") else "center", padx=padx, pady=pady,
                         cursor="hand2", highlightthickness=2, highlightbackground=border,
                         highlightcolor=C["gold"], takefocus=1)
        self.cmd, self.enabled = command, True
        self.kind, self.fg0, self.bg0, self.dbg, self.border0 = kind, fg, bg, dbg, border
        self.bind("<Button-1>", self._click)
        self.bind("<Return>", self._click)
        self.bind("<space>", self._click)
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        if wrap:
            self.bind("<Configure>", lambda e: self.config(wraplength=max(60, e.width - 2 * padx - 6)))

    def _click(self, _e=None):
        if self.enabled and self.cmd:
            self.cmd()
        return "break"

    def _enter(self, _e):
        if self.enabled and self.kind in ("opt", "plain", "ghost"):
            self.config(highlightbackground=C["mute"])

    def _leave(self, _e):
        if self.enabled:
            self.config(highlightbackground=self.border0)

    def set_enabled(self, on):
        self.enabled = on
        if on:
            self.config(fg=self.fg0, bg=self.bg0, cursor="hand2")
        else:
            self.config(fg=C["mute"], bg=self.dbg, cursor="arrow")

    def paint(self, bg=None, border=None, fg=None):
        if bg:
            self.bg0 = bg
            self.config(bg=bg)
        if border:
            self.border0 = border
            self.config(highlightbackground=border)
        if fg:
            self.fg0 = fg
            self.config(fg=fg)


class Scroll(tk.Frame):
    """Vertical scroll area whose content always matches the window width."""
    def __init__(self, parent):
        super().__init__(parent, bg=C["ink"])
        self.cv = tk.Canvas(self, bg=C["ink"], highlightthickness=0)
        self.sb = tk.Scrollbar(self, orient="vertical", command=self.cv.yview)
        self.cv.configure(yscrollcommand=self.sb.set)
        self.sb.pack(side="right", fill="y")
        self.cv.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.cv, bg=C["ink"])
        self.win = self.cv.create_window(0, 0, window=self.inner, anchor="nw")
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfigure(self.win, width=e.width))
        self.inner.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))

    def wheel(self, units):
        if self.inner.winfo_reqheight() > self.cv.winfo_height():
            self.cv.yview_scroll(units, "units")

    def to_top(self):
        self.cv.yview_moveto(0)


# --------------------------------------------------------------------------- hero art
def draw_hero(cv, x, y, k, kind, tag, active=False):
    col = C["ember"] if kind == "ember" else C["tide"]

    def pts(*p):
        out = []
        for px, py in p:
            out += [x + px * k, y + py * k]
        return out

    if kind == "ember":
        cv.create_polygon(pts((-10, -30), (-13, -42), (-5, -52), (0, -64), (5, -52), (13, -42), (10, -30)),
                          fill=C["gold"], outline="", tags=tag)
        cv.create_polygon(pts((-6, -30), (-7, -40), (0, -52), (7, -40), (6, -30)),
                          fill=C["ember"], outline="", tags=tag)
    else:
        cv.create_polygon(pts((0, -66), (8, -54), (12, -43), (10, -30), (-10, -30), (-12, -43), (-8, -54)),
                          fill="#8be3ee", outline="", tags=tag)
    cv.create_rectangle(x - 12 * k, y - 32 * k, x + 12 * k, y, fill=col, outline="", tags=tag)
    for ex in (-4, 4):
        cv.create_oval(x + (ex - 3.4) * k, y - 23.4 * k, x + (ex + 3.4) * k, y - 16.6 * k, fill="#fff", outline="", tags=tag)
        cv.create_oval(x + (ex + 0.8 - 1.6) * k, y - 21.2 * k, x + (ex + 0.8 + 1.6) * k, y - 18 * k, fill=C["ink"], outline="", tags=tag)
    cv.create_rectangle(x - 9 * k, y - 3 * k, x - 2 * k, y + 4 * k, fill=C["ink"], outline="", tags=tag)
    cv.create_rectangle(x + 2 * k, y - 3 * k, x + 9 * k, y + 4 * k, fill=C["ink"], outline="", tags=tag)
    if active:
        cv.create_polygon(pts((-7, -84), (7, -84), (0, -74)), fill=col, outline="", tags=tag)


# --------------------------------------------------------------------------- app
class App:
    def __init__(self, root):
        self.root = root
        root.title("Ember and Tide")
        root.configure(bg=C["ink"])
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        w, h = int(sw * 0.94), int(sh * 0.90)
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{max(0, (sh - h) // 4)}")
        root.minsize(720, 520)

        fam, mono = "Helvetica", "Consolas"
        specs = dict(
            body=(fam, 12, "normal"), bold=(fam, 12, "bold"), small=(fam, 10, "normal"), label=(fam, 9, "bold"),
            mono=(mono, 11, "normal"), monob=(mono, 12, "bold"), h1=("Arial Black", 36, "normal"),
            h2=("Arial Black", 24, "normal"), h3=("Arial Black", 15, "normal"), big=("Arial Black", 54, "normal"),
            btn=(fam, 11, "bold"), q=(fam, 16, "normal"), brand=("Arial Black", 20, "normal"), opt=(fam, 13, "normal"),
        )
        self.base = {k: v[1] for k, v in specs.items()}
        self.f = {k: tkfont.Font(family=v[0], size=v[1], weight=v[2]) for k, v in specs.items()}
        self.scale = 1.0

        self.S = dict(name="", diff="explorer")
        self.R = None
        self.page = None
        self.sc = None
        self.sc_cv = None
        self.tick_job = None
        self.enter_cmd = None
        self.fullscreen = False
        self.h_lives = self.h_score = self.h_streak = None
        self.lb = self.lb_load()

        root.bind("<Configure>", self.on_cfg)
        root.bind("<MouseWheel>", lambda e: self.wheel(-1 if e.delta > 0 else 1))
        root.bind("<Button-4>", lambda e: self.wheel(-1))
        root.bind("<Button-5>", lambda e: self.wheel(1))
        root.bind("<Return>", self.on_return)
        root.bind("<Key>", self.on_key)
        root.bind("<F11>", self.toggle_fs)
        root.bind("<Escape>", self.leave_fs)
        self.show_title()
        self.on_cfg()

    # ---- window plumbing ------------------------------------------------------
    def on_cfg(self, e=None):
        if e is not None and e.widget is not self.root:
            return
        w = self.root.winfo_width()
        s = max(0.85, min(1.8, w / 1100))
        if abs(s - self.scale) > 0.04:
            self.scale = s
            for k, f in self.f.items():
                f.configure(size=max(7, round(self.base[k] * s)))

    def toggle_fs(self, _e=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def leave_fs(self, _e=None):
        if self.fullscreen:
            self.toggle_fs()

    def wheel(self, units):
        if self.page is not None:
            self.page.wheel(units * 3)

    def on_return(self, _e=None):
        f = self.root.focus_get()
        if isinstance(f, tk.Entry) and str(f.cget("state")) == "normal":
            return
        if self.enter_cmd:
            self.enter_cmd()

    def on_key(self, e):
        R = self.R
        if not R or not R.get("cur") or R["cur"]["done"] or R["cur"]["q"]["mode"] != "c":
            return
        if isinstance(self.root.focus_get(), tk.Entry):
            return
        if e.char in ("1", "2", "3", "4"):
            si = int(e.char) - 1
            if si < len(self.opt_btns):
                self.pick(si)

    # ---- small helpers --------------------------------------------------------
    def L(self, parent, text="", font="body", fg=None, wrap=True, **kw):
        bg = kw.pop("bg", None) or parent.cget("bg")
        lb = tk.Label(parent, text=text, font=self.f[font], fg=fg or C["text"], bg=bg,
                      justify="left", anchor="w", **kw)
        if wrap:
            lb.bind("<Configure>", lambda e, lb=lb: lb.config(wraplength=max(60, e.width - 2)))
        return lb

    def B(self, parent, text, cmd, kind="plain", **kw):
        return Btn(parent, text, cmd, self.f["btn"], kind, **kw)

    def panel(self, parent, **kw):
        return tk.Frame(parent, bg=C["stone"], highlightbackground=C["line"], highlightthickness=2,
                        padx=kw.get("padx", 20), pady=kw.get("pady", 16))

    def new_page(self):
        self.stop_timer()
        self.enter_cmd = None
        self.sc = None
        self.sc_cv = None
        if self.page is not None:
            self.page.destroy()
        self.page = Scroll(self.root)
        self.page.pack(fill="both", expand=True)
        body = tk.Frame(self.page.inner, bg=C["ink"])
        body.pack(fill="both", expand=True, padx=24, pady=(18, 40))
        return body

    def hud(self, parent, in_run):
        h = tk.Frame(parent, bg=C["ink"])
        h.pack(fill="x", pady=(0, 14))
        br = tk.Frame(h, bg=C["ink"])
        br.pack(side="left")
        tk.Label(br, text="Ember", font=self.f["brand"], fg=C["ember"], bg=C["ink"]).pack(side="left")
        tk.Label(br, text=" & ", font=self.f["body"], fg=C["mute"], bg=C["ink"]).pack(side="left")
        tk.Label(br, text="Tide", font=self.f["brand"], fg=C["tide"], bg=C["ink"]).pack(side="left")
        self.h_lives = self.h_score = self.h_streak = None
        if in_run:
            st = tk.Frame(h, bg=C["ink"])
            st.pack(side="right")
            cells = []
            for name in ("Lives", "Score", "Streak"):
                cell = tk.Frame(st, bg=C["ink"])
                cell.pack(side="left", padx=(24, 0))
                tk.Label(cell, text=name.upper(), font=self.f["label"], fg=C["mute"], bg=C["ink"]).pack(anchor="w")
                v = tk.Label(cell, text="0", font=self.f["h3"], fg=C["bad"] if name == "Lives" else C["text"], bg=C["ink"])
                v.pack(anchor="w")
                cells.append(v)
            self.h_lives, self.h_score, self.h_streak = cells

    def two_col(self, parent, w1=3, w2=2):
        cols = tk.Frame(parent, bg=C["ink"])
        left, right = tk.Frame(cols, bg=C["ink"]), tk.Frame(cols, bg=C["ink"])
        state = {"wide": None}

        def lay(_e=None):
            wide = cols.winfo_width() >= 900
            if wide == state["wide"]:
                return
            state["wide"] = wide
            left.grid_forget()
            right.grid_forget()
            if wide:
                cols.columnconfigure(0, weight=w1, uniform="c")
                cols.columnconfigure(1, weight=w2, uniform="c")
                left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
                right.grid(row=0, column=1, sticky="nsew")
            else:
                cols.columnconfigure(0, weight=1, uniform="")
                cols.columnconfigure(1, weight=0, uniform="")
                left.grid(row=0, column=0, sticky="ew")
                right.grid(row=1, column=0, sticky="ew", pady=(16, 0))

        cols.bind("<Configure>", lay)
        return cols, left, right

    # ---- leaderboard ----------------------------------------------------------
    def lb_load(self):
        try:
            with open(LB_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def lb_add(self, entry):
        self.lb.append(entry)
        self.lb.sort(key=lambda e: -e["score"])
        self.lb = self.lb[:30]
        try:
            with open(LB_FILE, "w", encoding="utf-8") as fh:
                json.dump(self.lb, fh)
        except Exception:
            pass

    def lb_table(self, parent, highlight=None):
        if not self.lb:
            self.L(parent, "No runs yet. Finish a run to claim the first place.", fg=C["mute"]).pack(fill="x")
            return
        t = tk.Frame(parent, bg=C["stone"])
        t.pack(fill="x")
        heads = ["#", "Hero", "Mode", "Acc", "Score"]
        t.columnconfigure(1, weight=1)
        for c, h in enumerate(heads):
            tk.Label(t, text=h.upper(), font=self.f["label"], fg=C["mute"], bg=C["stone"], anchor="w").grid(row=0, column=c, sticky="w", padx=6, pady=3)
        for r, e in enumerate(self.lb[:8], start=1):
            col = C["gold"] if highlight and e.get("id") == highlight else C["text"]
            vals = [str(r), e["name"], e["diff"], f"{e['acc']}%", str(e["score"])]
            for c, v in enumerate(vals):
                tk.Label(t, text=v, font=self.f["mono"] if c in (0, 3, 4) else self.f["body"], fg=col,
                         bg=C["stone"], anchor="w").grid(row=r, column=c, sticky="w", padx=6, pady=3)
        self.L(parent, "Scores are saved next to this script (ember_tide_leaderboard.json).", font="small", fg=C["mute"]).pack(fill="x", pady=(8, 0))

    # ---- collapsible question card -------------------------------------------
    def qblock(self, parent, q, i=None):
        box = tk.Frame(parent, bg=C["stone"], highlightbackground=C["line"], highlightthickness=2)
        box.pack(fill="x", pady=4)
        tags = " ".join(("[real-world]" if t == "real" else "[search]") for t in q.get("tags", []))
        title = (f"{i}. " if i else "") + f"[{q['k']}] {tags}\n{q['q']}"
        body = tk.Frame(box, bg=C["stone"])
        state = {"open": False}
        head = Btn(box, "\u25B8  " + title, None, self.f["body"], "ghost", anchor="w", wrap=True, padx=14, pady=10)
        head.pack(fill="x")

        def toggle():
            state["open"] = not state["open"]
            head.config(text=("\u25BE  " if state["open"] else "\u25B8  ") + title)
            if state["open"]:
                body.pack(fill="x", padx=14, pady=(0, 12))
            else:
                body.pack_forget()

        head.cmd = toggle
        if q["mode"] == "c":
            self.L(body, "\n".join(f"{LETTERS[j]}. {o}" for j, o in enumerate(q["o"])), fg=C["mute"]).pack(fill="x", pady=(0, 6))
        self.L(body, "Answer: " + ans_text(q), font="bold", fg=C["ok"]).pack(fill="x")
        self.L(body, q["w"], fg=C["mute"]).pack(fill="x", pady=(6, 0))

    # ======================================================================= title
    def show_title(self):
        self.R = None
        b = self.new_page()
        self.hud(b, False)
        cols, left, right = self.two_col(b)
        cols.pack(fill="both", expand=True)

        tk.Label(left, text="Ember and Tide", font=self.f["h1"], fg=C["ember"], bg=C["ink"], anchor="w").pack(fill="x")
        self.L(left, "Two heroes, six chambers, one temple of AI concepts. Ember cannot touch water and Tide cannot touch lava. "
                     "Each question is a pit. Answer right and your heroes cross. Answer wrong and one of them takes a swim "
                     "in the wrong liquid.", fg=C["mute"], font="opt").pack(fill="x", pady=(6, 12))

        art = tk.Canvas(left, height=190, bg="#161330", highlightthickness=0)
        art.pack(fill="x", pady=(0, 14))
        art.bind("<Configure>", lambda e: self.draw_title_art(art))

        p = self.panel(left)
        p.pack(fill="x")
        self.L(p, "HERO NAME FOR THE LEADERBOARD", font="label", fg=C["mute"]).pack(fill="x")
        self.name_var = tk.StringVar(value=self.S["name"])
        ent = tk.Entry(p, textvariable=self.name_var, font=self.f["bold"], bg=C["ink"], fg=C["text"],
                       insertbackground=C["text"], relief="flat", highlightthickness=2,
                       highlightbackground=C["line"], highlightcolor=C["gold"])
        ent.pack(fill="x", pady=(4, 12), ipady=6)
        ent.bind("<Return>", lambda e: self.start_clicked())
        self.L(p, "PICK A MODE", font="label", fg=C["mute"]).pack(fill="x")
        mrow = tk.Frame(p, bg=C["stone"])
        mrow.pack(fill="x", pady=(4, 12))
        mrow.columnconfigure(0, weight=1, uniform="m")
        mrow.columnconfigure(1, weight=1, uniform="m")
        self.mode_btns = {}
        for c, (key, d) in enumerate(DIFFS.items()):
            n = d["per"] * 6
            txt = f"{d['name']}\n{n} questions\n{d['blurb']}"
            btn = Btn(mrow, txt, lambda k=key: self.set_diff(k), self.f["body"], "opt", anchor="nw", wrap=True, padx=14, pady=10)
            btn.grid(row=0, column=c, sticky="nsew", padx=(0 if c == 0 else 6, 6 if c == 0 else 0))
            self.mode_btns[key] = btn
        self.set_diff(self.S["diff"])
        row = tk.Frame(p, bg=C["stone"])
        row.pack(fill="x")
        self.B(row, "Enter the temple", self.start_clicked, "ember").pack(side="left", padx=(0, 10))
        self.B(row, "Viva drill", self.show_viva, "ghost").pack(side="left", padx=(0, 10))
        self.B(row, "Question bank", self.show_bank, "ghost").pack(side="left")

        lbp = self.panel(right)
        lbp.pack(fill="x")
        tk.Label(lbp, text="Leaderboard", font=self.f["h3"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(0, 8))
        self.lb_table(lbp)

        hp = self.panel(right)
        hp.pack(fill="x", pady=(16, 0))
        tk.Label(hp, text="How it plays", font=self.f["h3"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(0, 8))
        self.L(hp, "Beat the timer, keep your lives, build streaks. Five correct in a row restores a life. You get four "
                   "lifelines per run: Hint, Cull (removes two wrong options), Freeze (+15 s) and Swap (new question).",
               fg=C["mute"]).pack(fill="x")
        fm = len({q["k"] for q in QUESTIONS})
        real = sum(1 for q in QUESTIONS if "real" in q.get("tags", []))
        srch = sum(1 for q in QUESTIONS if "search" in q.get("tags", []))
        self.L(hp, f"{len(QUESTIONS)} questions  |  {fm} formats  |  {real} real-world  |  {srch} search problems",
               font="mono", fg=C["gold"]).pack(fill="x", pady=(8, 0))
        ent.focus_set()

    def draw_title_art(self, cv):
        cv.delete("all")
        w, h = max(cv.winfo_width(), 300), 190
        k = h / 170
        cv.create_rectangle(0, 118 * k, w * 0.30, h, fill="#2c2750", outline="")
        cv.create_rectangle(w * 0.70, 118 * k, w, h, fill="#2c2750", outline="")
        cv.create_rectangle(w * 0.30, 128 * k, w * 0.50, h, fill=C["tide"], outline="")
        cv.create_rectangle(w * 0.50, 128 * k, w * 0.70, h, fill=C["ember"], outline="")
        draw_hero(cv, w * 0.17, 118 * k, 1.2 * k, "ember", "a")
        draw_hero(cv, w * 0.83, 118 * k, 1.2 * k, "tide", "b")
        cx = w / 2
        cv.create_polygon(cx, 60 * k, cx + 10 * k, 74 * k, cx, 88 * k, cx - 10 * k, 74 * k, fill=C["gold"], outline="")
        cv.create_text(cx, 30 * k, text="ONE PIT EACH. ANSWER TO CROSS.", fill=C["mute"], font=("Arial Black", max(9, int(13 * k))))

    def set_diff(self, key):
        self.S["diff"] = key
        for k, b in self.mode_btns.items():
            b.paint(border=C["gold"] if k == key else C["line"], bg=C["stone2"])

    def start_clicked(self):
        n = self.name_var.get().strip() if hasattr(self, "name_var") else ""
        self.S["name"] = n or self.S["name"] or "Hero"
        self.start_run()

    # ======================================================================= viva / bank
    def show_viva(self):
        b = self.new_page()
        self.hud(b, False)
        p = self.panel(b)
        p.pack(fill="x")
        tk.Label(p, text="Viva drill", font=self.f["h2"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x")
        self.L(p, "Ten random questions from the bank, the way your teacher may ask them. Say your answer out loud first, "
                  "then open the card to check it and read the reasoning.", fg=C["mute"]).pack(fill="x", pady=8)
        row = tk.Frame(p, bg=C["stone"])
        row.pack(fill="x")
        self.B(row, "Draw ten new", self.show_viva, "ember").pack(side="left", padx=(0, 10))
        self.B(row, "Back", self.show_title, "ghost").pack(side="left")
        wrap = tk.Frame(b, bg=C["ink"])
        wrap.pack(fill="x", pady=(14, 0))
        for i, q in enumerate(random.sample(QUESTIONS, 10), 1):
            self.qblock(wrap, q, i)

    def show_bank(self):
        b = self.new_page()
        self.hud(b, False)
        p = self.panel(b)
        p.pack(fill="x")
        tk.Label(p, text="Question bank", font=self.f["h2"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x")
        self.L(p, f"{len(QUESTIONS)} questions. Open any card for the correct answer and the reasoning.", fg=C["mute"]).pack(fill="x", pady=8)
        self.B(p, "Back", self.show_title, "ghost").pack(anchor="w")
        n = 0
        for z in range(1, 7):
            items = [q for q in QUESTIONS if q["z"] == z]
            tk.Label(b, text=f"Chamber {z}: {ZONES[z]['n']}", font=self.f["h3"], fg=C["text"], bg=C["ink"], anchor="w").pack(fill="x", pady=(16, 0))
            self.L(b, f"{ZONES[z]['t']} ({len(items)} questions)", fg=C["mute"]).pack(fill="x", pady=(0, 4))
            for q in items:
                n += 1
                self.qblock(b, q, n)

    # ======================================================================= run
    def build_deck(self, key):
        D = DIFFS[key]
        deck, spare = [], {}
        for z in range(1, 7):
            pool = [q for q in QUESTIONS if q["z"] == z]
            random.shuffle(pool)
            pick = pool
            if D["per"] < len(pool):
                if D["maxd"]:
                    pool.sort(key=lambda q: 1 if q["d"] > D["maxd"] else 0)
                pick = pool[:D["per"]]
                spare[z] = pool[D["per"]:]
            else:
                spare[z] = []
            pick = sorted(pick, key=lambda q: q["d"] + random.random() * 0.9)
            deck += [dict(q=q, z=z) for q in pick]
        return deck, spare

    def start_run(self):
        D = DIFFS[self.S["diff"]]
        deck, spare = self.build_deck(self.S["diff"])
        self.R = dict(D=D, deck=deck, spare=spare, i=-1, hearts=D["hearts"], score=0, streak=0, best=0, log=[],
                      life=dict(hint=3, cull=2, freeze=2, swap=1), t0=time.time(), cur=None)
        b = self.new_page()
        self.hud(b, True)
        self.scene_frame = tk.Frame(b, bg=C["stone"], highlightbackground=C["line"], highlightthickness=2)
        self.scene_frame.pack(fill="x")
        self.sc_cv = None
        pg = tk.Frame(b, bg=C["ink"])
        pg.pack(fill="x", pady=(12, 0))
        self.prog_cv = tk.Canvas(pg, height=10, bg=C["ink"], highlightthickness=0)
        self.prog_cv.pack(fill="x")
        self.prog_cv.bind("<Configure>", lambda e: self.draw_prog())
        cap = tk.Frame(pg, bg=C["ink"])
        cap.pack(fill="x", pady=(4, 0))
        self.cap1 = tk.Label(cap, text="", font=self.f["small"], fg=C["mute"], bg=C["ink"])
        self.cap1.pack(side="left")
        self.cap2 = tk.Label(cap, text="", font=self.f["small"], fg=C["mute"], bg=C["ink"])
        self.cap2.pack(side="right")
        self.qpanel = self.panel(b)
        self.qpanel.pack(fill="x", pady=(12, 0))
        self.next_question()

    def zone_info(self, i):
        R = self.R
        z = R["deck"][i]["z"]
        first = next(j for j, d in enumerate(R["deck"]) if d["z"] == z)
        n = sum(1 for d in R["deck"] if d["z"] == z)
        return dict(z=z, first=first, n=n, k=i - first)

    def clear_q(self):
        for w in self.qpanel.winfo_children():
            w.destroy()
        self.enter_cmd = None
        self.opt_btns = []
        return self.qpanel

    def next_question(self):
        R = self.R
        R["i"] += 1
        if R["i"] >= len(R["deck"]):
            return self.finish("cleared")
        info = self.zone_info(R["i"])
        self.update_hud()
        self.update_prog()
        if info["k"] == 0:
            R["cur"] = None
            self.build_scene(info["z"], info["n"])
            self.scene_set_active(0)
            Z = ZONES[info["z"]]
            p = self.clear_q()
            plural = "s" if info["n"] > 1 else ""
            self.L(p, f"CHAMBER {info['z']} OF 6  |  {info['n']} PIT{plural.upper()}", font="label", fg=C["mute"]).pack(fill="x")
            tk.Label(p, text=Z["n"], font=self.f["h2"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(6, 2))
            self.L(p, Z["t"], fg=C["mute"]).pack(fill="x")
            tip = tk.Frame(p, bg=C["tip_bg"], highlightbackground=C["tip_line"], highlightthickness=2, padx=12, pady=10)
            tip.pack(fill="x", pady=12)
            self.L(tip, Z["tip"], fg=C["gold"], font="opt").pack(fill="x")
            self.B(p, "Enter chamber", self.show_question, "ember").pack(anchor="w")
            self.enter_cmd = self.show_question
        else:
            self.show_question()

    def update_hud(self):
        R = self.R
        if not R or not self.h_lives or not self.h_lives.winfo_exists():
            return
        full = max(0, R["hearts"])
        self.h_lives.config(text="\u2665" * full + "\u2661" * (R["D"]["hearts"] - full))
        self.h_score.config(text=str(R["score"]))
        self.h_streak.config(text=str(R["streak"]))

    def draw_prog(self):
        cv = self.prog_cv
        if not cv.winfo_exists():
            return
        cv.delete("all")
        w = max(cv.winfo_width(), 60)
        gap = 6
        sw = (w - gap * 5) / 6
        R = self.R
        for z in range(1, 7):
            x0 = (z - 1) * (sw + gap)
            cv.create_rectangle(x0, 1, x0 + sw, 9, fill=C["ink"], outline=C["line"])
            if R:
                total = sum(1 for d in R["deck"] if d["z"] == z)
                done = sum(1 for l in R["log"] if l["z"] == z)
                if total and done:
                    cv.create_rectangle(x0, 1, x0 + sw * done / total, 9, fill=C["gold"], outline="")

    def update_prog(self):
        R = self.R
        self.draw_prog()
        self.cap1.config(text=f"Question {min(R['i'] + 1, len(R['deck']))} of {len(R['deck'])}")
        self.cap2.config(text=f"Chamber {R['deck'][min(R['i'], len(R['deck']) - 1)]['z']} of 6")

    # ======================================================================= scene
    def build_scene(self, z, n):
        for w in self.scene_frame.winfo_children():
            w.destroy()
        cv = tk.Canvas(self.scene_frame, bg="#161330", highlightthickness=0, height=200)
        cv.pack(fill="x")
        W, gy = 800, 130
        sp = 660 / n
        sw = min(72, sp * 0.58)
        xs = [70 + i * sp for i in range(n + 1)]
        self.sc = dict(z=z, n=n, xs=xs, gy=gy, sw=sw, scale=max(0.52, min(1, sp / 110)), off=min(15, sw * 0.24),
                       hx=xs[0], active=0, gems=set(), door=0.0, bub=set(), dy=[0, 0], shake=[0, 0])
        self.sc_cv = cv

        def on_cfg(e):
            nh = int(min(max(e.width, 300) / 800 * 200, max(150, self.root.winfo_height() * 0.30)))
            if abs(cv.winfo_height() - nh) > 1:
                cv.config(height=nh)
            self.scene_draw()
        cv.bind("<Configure>", on_cfg)

    def scene_draw(self):
        cv, s = self.sc_cv, self.sc
        if cv is None or s is None or not cv.winfo_exists():
            return
        w = max(cv.winfo_width(), 300)
        h = max(cv.winfo_height(), 120)
        kx, ky = w / 800, h / 200          # stretch to the full box, whatever its shape
        ks = min(kx, ky)                   # heroes / text keep their proportions
        H, gy, n, xs, sw = 200, s["gy"], s["n"], s["xs"], s["sw"]
        X = lambda v: v * kx
        Y = lambda v: v * ky
        cv.delete("all")
        cv.create_rectangle(0, 0, w, h, fill="#161330", outline="")
        for r in range(4):
            cv.create_rectangle(0, Y(r * 34 + 8), w, Y(r * 34 + 8) + 1, fill="#2a2548", outline="")
        cv.create_text(X(16), Y(28), anchor="w", fill=C["mute"], font=("Arial Black", max(8, int(14 * ks))),
                       text=f"CHAMBER {s['z']}  \u00B7  {ZONES[s['z']]['n'].upper()}")
        for i in range(n):
            x1, x2 = xs[i] + sw / 2, xs[i + 1] - sw / 2
            lava = i % 2 == 1
            cv.create_rectangle(X(x1), Y(gy + 10), X(x2), h, fill=C["ember"] if lava else C["tide"], outline="")
            cv.create_rectangle(X(x1), Y(gy + 10), X(x2), Y(gy + 13), fill="#ffffff", outline="", stipple="gray50")
            cx = (x1 + x2) / 2
            if i in s["bub"]:
                cv.create_oval(X(cx - 6), Y(gy + 3), X(cx), Y(gy + 9), fill="#fff", outline="")
                cv.create_oval(X(cx + 2), Y(gy - 3), X(cx + 7), Y(gy + 2), fill="#fff", outline="")
            if i not in s["gems"]:
                cv.create_polygon(X(cx), Y(gy - 62), X(cx + 8), Y(gy - 52), X(cx), Y(gy - 42),
                                  X(cx - 8), Y(gy - 52), fill=C["gold"], outline="#8a6d1e", width=2)
        for i in range(n + 1):
            cv.create_rectangle(X(xs[i] - sw / 2), Y(gy), X(xs[i] + sw / 2), h, fill="#2c2750", outline=C["line"], width=2)
            cv.create_rectangle(X(xs[i] - sw / 2), Y(gy), X(xs[i] + sw / 2), Y(gy + 5), fill="#4a4380", outline="")
        dx = xs[n]
        cv.create_rectangle(X(dx - 22), Y(gy - 70), X(dx + 22), Y(gy), fill=C["ink"], outline=C["gold"], width=3)
        left = dx + 18 - 36 * (1 - 0.88 * s["door"])
        cv.create_rectangle(X(left), Y(gy - 66), X(dx + 18), Y(gy), fill=C["gold"], outline="")
        hs = ks * s["scale"]
        for idx, kind in enumerate(("ember", "tide")):
            off = -s["off"] if idx == 0 else s["off"]
            x = X(s["hx"] + off + s["shake"][idx])
            y = Y(gy + s["dy"][idx])
            draw_hero(cv, x, y, hs, kind, kind, active=(s["active"] % 2 == idx))

    def scene_set_active(self, k):
        if self.sc:
            self.sc["active"] = k
            self.scene_draw()

    def anim(self, n, step, done=None, i=0, sc=None):
        sc = sc or self.sc
        if sc is None or self.sc is not sc or self.sc_cv is None or not self.sc_cv.winfo_exists():
            return
        step(i / n)
        self.scene_draw()
        if i < n:
            self.root.after(28, lambda: self.anim(n, step, done, i + 1, sc))
        elif done:
            done()

    def scene_advance(self, k):
        s = self.sc
        if not s:
            return
        a, b, idx = s["hx"], s["xs"][k + 1], k % 2
        s["gems"].add(k)

        def step(t):
            e = t * t * (3 - 2 * t)
            s["hx"] = a + (b - a) * e
            s["dy"][idx] = -34 * 4 * t * (1 - t)

        def done():
            s["dy"][idx] = 0
            if k + 1 == s["n"]:
                self.anim(12, lambda t: s.__setitem__("door", t), None, 0, s)
        self.anim(22, step, done)

    def scene_hurt(self, k):
        s = self.sc
        if not s:
            return
        idx = k % 2
        s["bub"].add(k)

        def step(t):
            s["shake"][idx] = math.sin(t * math.pi * 5) * 6 * (1 - t)
            s["dy"][idx] = abs(math.sin(t * math.pi * 3)) * 6 * (1 - t)

        def done():
            s["shake"][idx] = 0
            s["dy"][idx] = 0

        def clear():
            s["bub"].discard(k)
            if self.sc is s:
                self.scene_draw()
        self.anim(16, step, done)
        self.root.after(1600, clear)

    # ======================================================================= question
    def prep_view(self, q):
        v = {}
        if q["mode"] == "c":
            n = len(q["o"])
            order = list(range(n))
            if not q.get("o_fixed"):
                random.shuffle(order)
            v.update(order=order, correct=order.index(q["a"]), culled=False)
        elif q["mode"] == "m":
            right = list(range(len(q["m"])))
            random.shuffle(right)
            v.update(right=right, map=[None] * len(q["m"]), left=None)
        elif q["mode"] == "g":
            v.update(seq=[])
        return v

    def show_question(self):
        R = self.R
        item = R["deck"][R["i"]]
        q = item["q"]
        info = self.zone_info(R["i"])
        tmax = R["D"]["time"] + (20 if q["mode"] in ("g", "m") else 0)
        c = dict(q=q, info=info, view=self.prep_view(q), hint=False, done=False, advanced=False, tMax=tmax, tLeft=tmax)
        R["cur"] = c
        hero = "ember" if info["k"] % 2 == 0 else "tide"
        self.scene_set_active(info["k"])
        p = self.clear_q()

        head = tk.Frame(p, bg=C["stone"])
        head.pack(fill="x")
        chips = tk.Frame(head, bg=C["stone"])
        chips.pack(side="left")
        for txt, fg, bd in ((q["k"], C["gold"], C["tip_line"]), (DLABEL[q["d"]], C["mute"], C["line"]),
                            (("Ember" if hero == "ember" else "Tide") + "'s turn",
                             C["ember"] if hero == "ember" else C["tide"],
                             C["ember_deep"] if hero == "ember" else C["tide_deep"])):
            tk.Label(chips, text=txt.upper(), font=self.f["label"], fg=fg, bg=C["stone"], padx=8, pady=2,
                     highlightthickness=2, highlightbackground=bd).pack(side="left", padx=(0, 8))
        self.tnum = tk.Label(head, text=f"{tmax}s", font=self.f["monob"], fg=C["text"], bg=C["stone"])
        self.tnum.pack(side="right")
        self.timer_cv = tk.Canvas(p, height=10, bg=C["ink"], highlightthickness=1, highlightbackground=C["line"])
        self.timer_cv.pack(fill="x", pady=(10, 12))
        self.timer_cv.bind("<Configure>", lambda e: self.update_timer())
        self.L(p, q["q"], font="q").pack(fill="x", pady=(0, 12))
        self.tipbox = tk.Frame(p, bg=C["stone"])
        self.tipbox.pack(fill="x")

        body = tk.Frame(p, bg=C["stone"])
        body.pack(fill="x")
        mode = q["mode"]
        if mode == "c":
            self.build_choice(body, q, c)
        elif mode == "f":
            self.build_fill(body, q, c)
        elif mode == "m":
            self.build_match(body, q, c)
        elif mode == "g":
            self.build_graph(body, q, c)

        self.lifes = tk.Frame(p, bg=C["stone"])
        self.lifes.pack(fill="x", pady=(14, 0))
        self.draw_lifes()
        self.fbox = tk.Frame(p, bg=C["stone"])
        self.fbox.pack(fill="x")
        self.start_timer()

    # ---- builders
    def build_choice(self, body, q, c):
        for si, oi in enumerate(c["view"]["order"]):
            b = Btn(body, f"{LETTERS[si]}    {q['o'][oi]}", (lambda si=si: self.pick(si)), self.f["opt"], "opt",
                    anchor="nw", wrap=True, padx=16, pady=11)
            b.pack(fill="x", pady=5)
            self.opt_btns.append(b)

    def pick(self, si):
        c = self.R["cur"]
        if c["done"] or not self.opt_btns[si].enabled:
            return
        q = c["q"]
        self.mark_choice(si)
        self.resolve(si == c["view"]["correct"], q["o"][c["view"]["order"][si]])

    def mark_choice(self, picked):
        c = self.R["cur"]
        for si, b in enumerate(self.opt_btns):
            b.enabled = False
            b.config(cursor="arrow", fg=C["text"])
            if si == c["view"]["correct"]:
                b.paint(bg=C["ok_bg"], border=C["ok"])
            elif si == picked:
                b.paint(bg=C["bad_bg"], border=C["bad"])

    def build_fill(self, body, q, c):
        row = tk.Frame(body, bg=C["stone"])
        row.pack(fill="x")
        self.fill_var = tk.StringVar()
        self.fill_ent = tk.Entry(row, textvariable=self.fill_var, font=self.f["monob"], bg=C["ink"], fg=C["text"],
                                 insertbackground=C["text"], relief="flat", highlightthickness=2,
                                 highlightbackground=C["line"], highlightcolor=C["gold"])
        self.fill_ent.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.fill_ent.bind("<Return>", lambda e: self.do_fill())
        self.fill_btn = self.B(row, "Check", self.do_fill, "ember")
        self.fill_btn.pack(side="left")
        self.fill_ent.focus_set()

    def do_fill(self):
        c = self.R["cur"]
        if c["done"]:
            return
        val = self.fill_var.get()
        if not val.strip():
            self.fill_ent.focus_set()
            return
        self.fill_ent.config(state="disabled")
        self.fill_btn.set_enabled(False)
        q = c["q"]
        self.resolve(normalize(val) in [normalize(a) for a in q["a"]], val)

    def build_match(self, body, q, c):
        self.L(body, "Click an item on the left, then its partner on the right. Click a paired item to undo it.",
               font="small", fg=C["mute"]).pack(fill="x", pady=(0, 8))
        grid = tk.Frame(body, bg=C["stone"])
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1, uniform="g")
        grid.columnconfigure(1, weight=1, uniform="g")
        self.mL, self.mR = {}, {}
        for r, p in enumerate(q["m"]):
            lb = Btn(grid, p[0], (lambda r=r: self.match_left(r)), self.f["opt"], "opt", anchor="nw", wrap=True, padx=12, pady=9)
            lb.grid(row=r, column=0, sticky="nsew", padx=(0, 7), pady=5)
            ri = c["view"]["right"][r]
            rb = Btn(grid, q["m"][ri][1], (lambda ri=ri: self.match_right(ri)), self.f["opt"], "opt", anchor="nw", wrap=True, padx=12, pady=9)
            rb.grid(row=r, column=1, sticky="nsew", padx=(7, 0), pady=5)
            self.mL[r], self.mR[ri] = lb, rb
        row = tk.Frame(body, bg=C["stone"])
        row.pack(fill="x", pady=(10, 0))
        self.lock_btn = self.B(row, "Lock in pairs", self.lock_match, "ember")
        self.lock_btn.pack(side="left")
        self.lock_btn.set_enabled(False)

    def match_left(self, r):
        c = self.R["cur"]
        if c["done"]:
            return
        if c["view"]["map"][r] is not None:
            c["view"]["map"][r] = None
        else:
            c["view"]["left"] = r
        self.refresh_match()

    def match_right(self, ri):
        c = self.R["cur"]
        if c["done"]:
            return
        m = c["view"]["map"]
        if ri in m:
            m[m.index(ri)] = None
        elif c["view"]["left"] is not None:
            m[c["view"]["left"]] = ri
            c["view"]["left"] = None
        self.refresh_match()

    def refresh_match(self):
        c = self.R["cur"]
        q, v = c["q"], c["view"]
        for r, p in enumerate(q["m"]):
            paired = v["map"][r] is not None
            self.mL[r].config(text=(f"({r + 1})  " if paired else "") + p[0])
            self.mL[r].paint(border=C["gold"] if v["left"] == r else (C["mute"] if paired else C["line"]))
        for ri in range(len(q["m"])):
            owner = v["map"].index(ri) if ri in v["map"] else None
            self.mR[ri].config(text=(f"({owner + 1})  " if owner is not None else "") + q["m"][ri][1])
            self.mR[ri].paint(border=C["mute"] if owner is not None else C["line"])
        self.lock_btn.set_enabled(all(m is not None for m in v["map"]))

    def mark_match(self):
        c = self.R["cur"]
        q, v = c["q"], c["view"]
        for r in range(len(q["m"])):
            ok = v["map"][r] == r
            col, bg = (C["ok"], C["ok_bg"]) if ok else (C["bad"], C["bad_bg"])
            self.mL[r].paint(bg=bg, border=col)
            if v["map"][r] is not None:
                self.mR[v["map"][r]].paint(bg=bg, border=col)
        for b in list(self.mL.values()) + list(self.mR.values()):
            b.enabled = False
            b.config(cursor="arrow")
        self.lock_btn.set_enabled(False)

    def lock_match(self):
        c = self.R["cur"]
        if c["done"]:
            return
        self.mark_match()
        q, v = c["q"], c["view"]
        ok = all(m == r for r, m in enumerate(v["map"]))
        given = "; ".join(q["m"][r][0] + " -> " + ("?" if m is None else q["m"][m][1]) for r, m in enumerate(v["map"]))
        self.resolve(ok, given)

    def build_graph(self, body, q, c):
        host = tk.Frame(body, bg=C["stone"])
        host.pack(fill="x")
        gh = q["g"].get("h")
        base_h = 285 if gh else 275
        cv = tk.Canvas(host, bg=C["ink"], highlightthickness=2, highlightbackground=C["line"])
        cv.pack(anchor="w")
        self.g_cv = cv
        self.g_state = {}      # node id -> "right" / "wrong"

        def redraw(_e=None):
            w = max(260, min(host.winfo_width(), 620))
            k = w / 400
            cv.config(width=w, height=int(base_h * k))
            self.draw_graph(q, c, k)
        host.bind("<Configure>", redraw)
        self.seq_lbl = self.L(body, "Your order: ", font="mono", fg=C["gold"])
        self.seq_lbl.pack(fill="x", pady=8)
        row = tk.Frame(body, bg=C["stone"])
        row.pack(fill="x")
        self.B(row, "Undo", self.g_undo, "plain", padx=12, pady=6).pack(side="left", padx=(0, 8))
        self.B(row, "Reset", self.g_reset, "plain", padx=12, pady=6).pack(side="left", padx=(0, 8))
        self.lock_btn = self.B(row, "Lock in order", self.lock_graph, "ember")
        self.lock_btn.pack(side="left")
        self.lock_btn.set_enabled(False)

    def draw_graph(self, q, c, k):
        cv, g = self.g_cv, q["g"]
        if not cv.winfo_exists():
            return
        cv.delete("all")
        seq = c["view"]["seq"]
        for a, b in g["e"]:
            cv.create_line(g["n"][a][0] * k, g["n"][a][1] * k, g["n"][b][0] * k, g["n"][b][1] * k, fill=C["line"], width=max(2, 3 * k))
        for nid, (x, y) in g["n"].items():
            st = self.g_state.get(nid)
            fill, out = C["stone2"], C["line"]
            if st == "right":
                fill, out = C["ok_bg"], C["ok"]
            elif st == "wrong":
                fill, out = C["bad_bg"], C["bad"]
            elif nid in seq:
                fill, out = "#3b3010", C["gold"]
            r = 21 * k
            tag = "n_" + nid
            cv.create_oval((x * k) - r, (y * k) - r, (x * k) + r, (y * k) + r, fill=fill, outline=out, width=3, tags=tag)
            cv.create_text(x * k, y * k, text=nid, fill=C["text"], font=("Consolas", max(10, int(15 * k)), "bold"), tags=tag)
            if nid in seq:
                cv.create_text(x * k + 24 * k, y * k - 16 * k, text=str(seq.index(nid) + 1), fill=C["gold"],
                               font=("Consolas", max(8, int(12 * k)), "bold"))
            if g.get("h"):
                cv.create_text(x * k, y * k + 38 * k, text=f"h={g['h'][nid]}", fill=C["mute"], font=("Consolas", max(8, int(11 * k))))
            cv.tag_bind(tag, "<Button-1>", lambda e, nid=nid: self.g_click(nid))
            cv.tag_bind(tag, "<Enter>", lambda e: cv.config(cursor="hand2"))
            cv.tag_bind(tag, "<Leave>", lambda e: cv.config(cursor=""))

    def g_redraw(self):
        c = self.R["cur"]
        w = int(self.g_cv.cget("width"))
        self.draw_graph(c["q"], c, w / 400)
        self.seq_lbl.config(text="Your order: " + "  ->  ".join(c["view"]["seq"]))
        self.lock_btn.set_enabled(len(c["view"]["seq"]) >= 2)

    def g_click(self, nid):
        c = self.R["cur"]
        if c["done"] or nid in c["view"]["seq"]:
            return
        c["view"]["seq"].append(nid)
        self.g_redraw()

    def g_undo(self):
        c = self.R["cur"]
        if not c["done"] and c["view"]["seq"]:
            c["view"]["seq"].pop()
            self.g_redraw()

    def g_reset(self):
        c = self.R["cur"]
        if not c["done"]:
            c["view"]["seq"].clear()
            self.g_redraw()

    def mark_graph(self):
        c = self.R["cur"]
        q, seq = c["q"], c["view"]["seq"]
        for p, nid in enumerate(seq):
            self.g_state[nid] = "right" if p < len(q["a"]) and q["a"][p] == nid else "wrong"
        self.g_redraw()
        self.lock_btn.set_enabled(False)

    def lock_graph(self):
        c = self.R["cur"]
        if c["done"]:
            return
        q, seq = c["q"], c["view"]["seq"]
        ok = seq == q["a"]
        self.mark_graph()
        self.resolve(ok, " -> ".join(seq))

    # ---- lifelines
    def draw_lifes(self):
        for w in self.lifes.winfo_children():
            w.destroy()
        R = self.R
        c = R["cur"]
        q, L = c["q"], R["life"]
        can_cull = q["mode"] == "c" and len(q["o"]) > 2 and not c["view"]["culled"]
        can_swap = L["swap"] > 0 and len(R["spare"].get(c["info"]["z"], [])) > 0
        for txt, cmd, on in ((f"Hint ({L['hint']})", self.life_hint, L["hint"] > 0 and not c["hint"]),
                             (f"Cull ({L['cull']})", self.life_cull, L["cull"] > 0 and can_cull),
                             (f"Freeze +15s ({L['freeze']})", self.life_freeze, L["freeze"] > 0),
                             (f"Swap ({L['swap']})", self.life_swap, can_swap)):
            b = self.B(self.lifes, txt, cmd, "plain", padx=12, pady=6)
            b.pack(side="left", padx=(0, 8))
            b.set_enabled(bool(on))

    def life_hint(self):
        R, c = self.R, self.R["cur"]
        if c["done"] or c["hint"] or R["life"]["hint"] < 1:
            return
        R["life"]["hint"] -= 1
        c["hint"] = True
        tip = tk.Frame(self.tipbox, bg=C["tip_bg"], highlightbackground=C["tip_line"], highlightthickness=2, padx=12, pady=8)
        tip.pack(fill="x", pady=(0, 10))
        self.L(tip, "Hint: " + c["q"]["h"] + "  (worth 20 fewer points)", fg=C["gold"]).pack(fill="x")
        self.draw_lifes()

    def life_cull(self):
        R, c = self.R, self.R["cur"]
        q = c["q"]
        if c["done"] or R["life"]["cull"] < 1 or q["mode"] != "c" or c["view"]["culled"]:
            return
        wrong = [si for si in range(len(q["o"])) if si != c["view"]["correct"]]
        random.shuffle(wrong)
        for si in wrong[:max(1, min(2, len(q["o"]) - 2))]:
            b = self.opt_btns[si]
            b.enabled = False
            b.config(fg=C["line"], cursor="arrow", text="\u2717  " + b.cget("text").split("    ", 1)[-1])
        c["view"]["culled"] = True
        R["life"]["cull"] -= 1
        self.draw_lifes()

    def life_freeze(self):
        R, c = self.R, self.R["cur"]
        if c["done"] or R["life"]["freeze"] < 1:
            return
        R["life"]["freeze"] -= 1
        c["tLeft"] += 15
        c["tMax"] = max(c["tMax"], c["tLeft"])
        self.update_timer()
        self.draw_lifes()

    def life_swap(self):
        R, c = self.R, self.R["cur"]
        pool = R["spare"].get(c["info"]["z"], [])
        if c["done"] or R["life"]["swap"] < 1 or not pool:
            return
        self.stop_timer()
        R["life"]["swap"] -= 1
        R["deck"][R["i"]]["q"] = pool.pop()
        self.show_question()

    # ---- timer
    def stop_timer(self):
        if self.tick_job is not None:
            try:
                self.root.after_cancel(self.tick_job)
            except Exception:
                pass
            self.tick_job = None

    def start_timer(self):
        self.stop_timer()
        self.tick_job = self.root.after(1000, self.tick)

    def tick(self):
        self.tick_job = None
        c = self.R and self.R.get("cur")
        if not c or c["done"]:
            return
        c["tLeft"] -= 1
        self.update_timer()
        if c["tLeft"] <= 0:
            return self.timed_out()
        self.tick_job = self.root.after(1000, self.tick)

    def update_timer(self):
        c = self.R and self.R.get("cur")
        if not c:
            return
        try:
            if not self.timer_cv.winfo_exists():
                return
        except Exception:
            return
        left = max(0, c["tLeft"])
        self.tnum.config(text=f"{left}s")
        cv = self.timer_cv
        cv.delete("all")
        w, h = max(cv.winfo_width(), 50), max(cv.winfo_height(), 8)
        cv.create_rectangle(0, 0, w * left / c["tMax"], h, fill=C["bad"] if left <= 8 else C["tide"], outline="")

    def timed_out(self):
        c = self.R["cur"]
        m = c["q"]["mode"]
        if m == "c":
            self.mark_choice(-1)
        elif m == "m":
            self.mark_match()
        elif m == "g":
            self.mark_graph()
        elif m == "f":
            self.fill_ent.config(state="disabled")
            self.fill_btn.set_enabled(False)
        self.resolve(False, "(ran out of time)", "time")

    # ---- resolve
    def resolve(self, ok, given, reason=None):
        R = self.R
        c = R["cur"]
        if c["done"]:
            return
        c["done"] = True
        self.stop_timer()
        q, k = c["q"], c["info"]["k"]
        hero = "Ember" if k % 2 == 0 else "Tide"
        gained, parts = 0, []
        if ok:
            R["streak"] += 1
            R["best"] = max(R["best"], R["streak"])
            base = 60 + 20 * q["d"] - (20 if c["hint"] else 0)
            tb = round(40 * c["tLeft"] / c["tMax"])
            sb = min(R["streak"], 5) * 10
            gained = base + tb + sb
            R["score"] += gained
            parts += [f"base {base}", f"speed +{tb}", f"streak +{sb}"]
            if R["streak"] % 5 == 0 and R["hearts"] < R["D"]["hearts"]:
                R["hearts"] += 1
                parts.append("a life restored")
            self.scene_advance(k)
            c["advanced"] = True
        else:
            R["streak"] = 0
            R["hearts"] -= 1
            self.scene_hurt(k)
        R["log"].append(dict(q=q, z=c["info"]["z"], ok=ok, given=given, gained=gained, hint=c["hint"]))
        self.update_hud()
        self.update_prog()
        verdict = ("Path clear" if ok else "Time is up" if reason == "time"
                   else "Hiss! Ember hit water" if k % 2 == 0 else "Sizzle! Tide hit lava")
        last = R["hearts"] <= 0
        for w in self.lifes.winfo_children():
            w.destroy()
        for w in self.tipbox.winfo_children():
            w.destroy()
        for w in self.fbox.winfo_children():
            w.destroy()
        good = ok
        fb = tk.Frame(self.fbox, bg=C["fb_ok"] if good else C["fb_no"], highlightthickness=2,
                      highlightbackground=C["ok"] if good else C["bad"], padx=16, pady=14)
        fb.pack(fill="x", pady=(14, 10))
        bg = fb.cget("bg")
        tk.Label(fb, text=verdict, font=self.f["h3"], fg=C["ok"] if good else C["bad"], bg=bg, anchor="w").pack(fill="x")
        if ok:
            self.L(fb, f"+{gained} points ({', '.join(parts)})", font="mono", bg=bg).pack(fill="x", pady=(4, 0))
        else:
            self.L(fb, "CORRECT ANSWER", font="label", fg=C["mute"], bg=bg).pack(fill="x", pady=(6, 0))
            self.L(fb, ans_text(q), font="bold", bg=bg).pack(fill="x")
        self.L(fb, q["w"], bg=bg).pack(fill="x", pady=(8, 0))
        row = tk.Frame(self.fbox, bg=C["stone"])
        row.pack(fill="x")
        self.B(row, "See result" if last else "Continue", self.go_next, "ember" if ok else "tide").pack(side="left", padx=(0, 12))
        tk.Label(row, text=f"{hero} {'crosses' if ok else 'wades in'}{'. No lives left.' if last else ''}",
                 font=self.f["small"], fg=C["mute"], bg=C["stone"]).pack(side="left")
        self.enter_cmd = self.go_next

    def go_next(self):
        R = self.R
        c = R["cur"]
        if not c or not c["done"]:
            return
        self.enter_cmd = None
        if not c["advanced"]:
            self.scene_advance(c["info"]["k"])
            c["advanced"] = True
        if R["hearts"] <= 0:
            return self.finish("fallen")
        self.next_question()

    # ======================================================================= results
    def finish(self, status):
        R = self.R
        self.stop_timer()
        total = len(R["log"])
        right = sum(1 for l in R["log"] if l["ok"])
        acc = round(right / total * 100) if total else 0
        secs = round(time.time() - R["t0"])
        rid = f"{int(time.time() * 1000)}-{random.randint(0, 9999)}"
        self.lb_add(dict(id=rid, name=self.S["name"] or "Hero", score=R["score"], diff=R["D"]["name"], acc=acc))
        rank = ("Fallen Hero" if status == "fallen" else "Archmage of Search" if acc >= 90 else
                "Temple Warden" if acc >= 75 else "Path Finder" if acc >= 55 else "Apprentice")
        b = self.new_page()
        self.R = R
        self.hud(b, False)
        p = self.panel(b)
        p.pack(fill="x")
        self.L(p, ("NO LIVES LEFT" if status == "fallen" else "ALL SIX CHAMBERS CLEARED") + "  |  " + R["D"]["name"].upper(),
               font="label", fg=C["mute"]).pack(fill="x")
        tk.Label(p, text=rank, font=self.f["h2"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(6, 0))
        tk.Label(p, text=str(R["score"]), font=self.f["big"], fg=C["gold"], bg=C["stone"], anchor="w").pack(fill="x")
        self.L(p, f"{right}/{total} correct ({acc}%)   |   best streak {R['best']}   |   {max(0, R['hearts'])} lives left   |   {secs // 60}m {secs % 60}s",
               font="monob").pack(fill="x", pady=(0, 12))
        row = tk.Frame(p, bg=C["stone"])
        row.pack(fill="x")
        self.B(row, "Play again", self.start_run, "ember").pack(side="left", padx=(0, 10))
        self.B(row, "Change mode", self.show_title, "ghost").pack(side="left", padx=(0, 10))
        self.B(row, "Viva drill", self.show_viva, "ghost").pack(side="left")

        cols, left, right_col = self.two_col(b, 1, 1)
        cols.pack(fill="x", pady=(16, 0))
        bp = self.panel(left)
        bp.pack(fill="x")
        tk.Label(bp, text="By chamber", font=self.f["h3"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(0, 8))
        for z in range(1, 7):
            logs = [l for l in R["log"] if l["z"] == z]
            if not logs:
                continue
            r = sum(1 for l in logs if l["ok"])
            line = tk.Frame(bp, bg=C["stone"])
            line.pack(fill="x", pady=4)
            line.columnconfigure(1, weight=1)
            tk.Label(line, text=ZONES[z]["n"], font=self.f["body"], fg=C["text"], bg=C["stone"], anchor="w", width=20).grid(row=0, column=0, sticky="w")
            bar = tk.Canvas(line, height=12, bg=C["ink"], highlightthickness=1, highlightbackground=C["line"])
            bar.grid(row=0, column=1, sticky="ew", padx=10)
            frac = r / len(logs)
            bar.bind("<Configure>", lambda e, bar=bar, frac=frac: (bar.delete("all"),
                     bar.create_rectangle(0, 0, e.width * frac, 12, fill=C["tide"], outline="")))
            tk.Label(line, text=f"{r}/{len(logs)}", font=self.f["mono"], fg=C["text"], bg=C["stone"]).grid(row=0, column=2)
        lp = self.panel(right_col)
        lp.pack(fill="x")
        tk.Label(lp, text="Leaderboard", font=self.f["h3"], fg=C["text"], bg=C["stone"], anchor="w").pack(fill="x", pady=(0, 8))
        self.lb_table(lp, rid)

        tk.Label(b, text="Review the ones you missed", font=self.f["h3"], fg=C["text"], bg=C["ink"], anchor="w").pack(fill="x", pady=(20, 6))
        missed = [l for l in R["log"] if not l["ok"]]
        if missed:
            for i, l in enumerate(missed, 1):
                self.qblock(b, l["q"], i)
        else:
            pp = self.panel(b)
            pp.pack(fill="x")
            self.L(pp, "Flawless. Nothing to review.").pack(fill="x")
        self.page.to_top()
        R["cur"] = None; R["finished"] = True


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
