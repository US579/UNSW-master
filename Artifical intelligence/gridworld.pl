% gridworld.pl
% Simulates a single agent in the Gridworld where stones appear on
% each cycle at randomly determined locations in the 10x10 grid with probability 0.1

% run a trial of 100 cycles of the BDI interpreter starting with the agent at (0,0)

run :-
    consult(land),
    consult(agent),
    init_world,
    initial_intentions(Intentions),
    write('Initial Goals: '), writeln(Intentions),
    agent_steps(0, 100, Intentions).

% initial state of the world

init_world :-
    assert(stone_at(0,0)),
    retractall(stone_at(_,_)),
    assert(picked(0,0)),
    retractall(picked(_,_)),
    assert(dropped(0,0)),
    retractall(dropped(_,_)),
    retractall(agent_at(_,_)),
    assert(agent_at(1,1)),
    retractall(agent_stones(_)),
    assert(agent_stones(0)).

% run trials up to N

% end the trial if the monster has been killed
agent_steps( _, _, _ ) :-
    monster(X,Y),
    dropped(X,Y),
    writeln('Monster successfully slain'), ! .

% end the trial if the maximum number of steps has been reached
agent_steps(N, N, _ ) :-
    writeln('Maximum number of steps exceeded.'), ! .

% otherwise, continue running agent cycles
agent_steps(N1, N, Intentions) :-
    N1 < N,
    agent_cycle(N1, Intentions, Intentions1),
    N2 is N1 + 1,
    agent_steps(N2, N, Intentions1).

% the BDI interpretation cycle used by the agent

agent_cycle(N, Intentions, Intentions3) :-
    write('Cycle '), write(N), writeln(':'),
    new_events(2),
    agent_at(X,Y),
    write('  Agent at: ('), write((X,Y)), writeln(')'),
    world(World),
    write('  World: '), writeln(World),
    percepts(World, Percepts),
    write('  Percepts: '), writeln(Percepts),
    trigger(Percepts, Goals),
    write('  Goals: '), writeln(Goals),
    incorporate_goals(Goals, Intentions, Intentions1),
    write('  Intentions: '), writeln(Intentions1),
    get_action(Intentions1, Intentions2, Action),
    write('  New Intentions: '), writeln(Intentions2),
    write('  Action: '), writeln(Action), !,
    execute(Action),
    world(World1),
    write('  Updated World: '), writeln(World1),
    observe(Action, Observation),
    write('  Observation: '), writeln(Observation),
    update_intentions(Observation, Intentions2, Intentions3),
    write('  Updated Intentions: '), writeln(Intentions3).

% list of stones in the world

world(World) :-
    findall(stone_at(X,Y), stone_at(X,Y), World), ! .

world([]).

%  each with probability 0.1, a new stone appears in at most M random locations on the 10x10 grid

new_events(0).

new_events(M) :-
    Prob is random(10),
    Prob = 0,
    X is round(random(10)),
    Y is round(random(10)),
    land(X,Y),
    not(stone_at(X,Y)),
    not(agent_at(X,Y)), !,
    write('  Event: stone appears at '), write('('), write(X), write(','), write(Y), writeln(')'),
    assert(stone_at(X,Y)),
    M1 is M - 1,
    new_events(M1).

new_events(M) :-
    M1 is M - 1,
    new_events(M1).

% new percepts are stones within a viewing range of 10 of the agent

percepts([], []).

percepts([stone_at(X,Y)|World], [stone(X,Y)|Percepts]) :-
    agent_at(X1,Y1),
    distance((X,Y), (X1,Y1), D),
    D < 10, !,
    percepts(World, Percepts).

percepts([stone_at(_,_)|World], Percepts) :-
    percepts(World, Percepts).

% applicable actions in a state

applicable(move(X,Y)) :-
    agent_at(X,Y).

applicable(move(X,Y)) :-
    agent_at(X0,Y0),
    distance((X0,Y0), (X,Y), 1),
    land_or_dropped(X,Y).

applicable(pick(X,Y)) :-
    stone_at(X,Y),
    agent_stones(0),
    agent_at(X0,Y0),
    distance((X0,Y0), (X,Y), 1).

applicable(drop(X,Y)) :-
    agent_stones(1),
    agent_at(X0,Y0),
    distance((X0,Y0), (X,Y), 1),
    not(land(X,Y)),
    not(dropped(X,Y)).

% execute action in the Gridworld -- always successfully!

execute(pick(X,Y)) :-
    retract(stone_at(X,Y)),
    retract(agent_stones(0)),
    assert(agent_stones(1)),
    assert(picked(X,Y)).

execute(drop(X,Y)) :-
    retract(agent_stones(1)),
    assert(agent_stones(0)),
    assert(dropped(X,Y)).

execute(move(X,Y)) :-
    agent_at(X,Y), ! .

execute(move(X,Y)) :-
    retract(agent_at(X0,Y0)),
    distance((X0,Y0), (X,Y), 1),
    land_or_dropped(X,Y),
    assert(agent_at(X,Y)).

land_or_dropped(X,Y) :-
    land(X,Y).

land_or_dropped(X,Y) :-
    dropped(X,Y).

% Manhattan distance between two squares

distance((X,Y), (X1,Y1), D) :-
    dif(X, X1, Dx),
    dif(Y, Y1, Dy),
    D is Dx + Dy.

% D is |A - B|
dif(A, B, D) :-
    D is A - B, D >= 0, !.

dif(A, B, D) :-
    D is B - A.

% observe result of action

observe(move(_,_), at(X,Y)) :-
    agent_at(X,Y).

observe(pick(X,Y), picked(X,Y)) :-
    retract(picked(X,Y)).

observe(drop(X,Y), dropped(X,Y)).