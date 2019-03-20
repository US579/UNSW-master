%% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Assignment for COMP9414 Semester 1, 2018
%
% Group: Wanze LIU, z5137189
        Zhou JIANG, z5146092
%        
%
% Group Number: 462
%
% Assignment name: Assignment 3, Option 2: Prolog (BDI Agent)
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [PART 1] initial_intentions
% This part is to search the shortest path from the begining to the
% monster, then choose the points which are not on 'land' to form the
% list of intentions.

% Function s is the cost-1000 solve algorithm, making this funtion
% dynamic as we will retract it to avoid errors. Otherwise, it will let
% agent pass through the river.

:- dynamic s/3.

% This function is to get the coordinates of monster, used by several
% functions

monster_position(X,Y):-
   monster(X,Y).

% This function is to get the coordinates of agent, which can be
% dynamic, used by several functions

agent_position(X,Y):-
   agent_at(X,Y).

% This function is to establish the original path from agent position to
% monster, we first assert the position then use ucsdijkstra algorithm
% to solve, then retract it to avoid errors for other functions

path_searching(Path):-
  agent_position(Xa,Ya),
  monster_position(Xm,Ym),
  assert(goal(goal(Xa,Ya))),
  solve(goal(Xm,Ym),Path,_,_),
  retract(goal(goal(Xa,Ya))),
  retractall(s(_,_,1000)).

% This function is to filter actual initial goals from original path, if
% goal coordinates are 'on land' , we dismiss them. Otherwise we keep
% them to form initial intentions.

filter_goal([],[]).

filter_goal([goal(X,Y)|RestGoal],[[goal(X,Y),[]]|RestInitGoal]):-
   not(land(X,Y)),
   filter_goal(RestGoal,RestInitGoal).

filter_goal([goal(X,Y)|RestGoal],InitGoal):-
   land(X,Y),
   filter_goal(RestGoal,InitGoal).

% This function calls path searching, then calls filter goal to form and
% filter the initial intentions.

initial_intentions(intents(L,[])):-
  path_searching(Path),
  filter_goal(Path,L).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [PART 2]
% A predicate that takes a list of events , each of the form stone(X,Y), and
% computes the corresponding list of goals for the agent, each of the
% form goal(X,Y).
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

trigger([], []).
trigger([stone(X, Y)|Percepts], [goal(X, Y)|Goals]) :-
    trigger(Percepts, Goals).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [PART 3]
% incorporate_goals
% This functions is to filter available goals from percepts, then sort
% them by the distance cost from current position to goals.
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% Base case : In case there are no new goals,intentions do not change anything.

incorporate_goals([],Intentions,Intentions).

% Recursively insert the new goals. we should retract the cost-1000
% algorithm as it will cause errors to let agent pass through the river.

incorporate_goals([Goal|Goals],Intentions,Intentions1):-
   retractall(s(_,_,1000)),
   agent_position(A,B),
   assert(goal(goal(A,B))),
   insert(Goal,Intentions,IntA),
   retract(goal(goal(A,B))),
   incorporate_goals(Goals,IntA,Intentions1),!.

% In case that can not find a path ,do not change anything.

insert(Goal,intents(I_drop,I_pick),intents(I_drop,I_pick)):-
   not(solve(Goal,_,_,_)),!.

% If it finds a path ,compare its length and insert it into the list recursively.

insert(Goal,intents(I_drop,I_pick),intents(I_drop,I_pick1)):-
   solve(Goal,_,G,_),
   insert_ass(Goal,G,I_pick,I_pick1),!.


% If we found that the length of path is no path longer than that ,we insert it at the end of list.

insert_ass(Goal, _, [],[[Goal,[]]]).

% If find the same goals ,do not change anything.

insert_ass(Goal, _,[[Goal,Plan]|Rt],[[Goal,Plan]|Rt]).

% If the length of path that we found is shorter or equal to the length of G path,keep recursiving.

insert_ass(Goal, G,[[NGoal,NP]|Rt],[[NGoal,NP]|Rt1]):-
   solve(NGoal, _,NG, _),
   G >= NG,
   insert_ass(Goal,G,Rt,Rt1).

% In case that find  a path that longer than the  length of G ,stop recursive.

insert_ass(Goal, G,[[NGoal,NP]|Rt],[[Goal,[]],[NGoal,NP]|Rt]):-
   solve(NGoal, _,NG, _),
   G < NG,!.


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [Part 4] get_action function
% The get_action function firstly checks if the agent holds a stone.

% If agent hold a stone, the drop intents should be added or modified
% through the drop action, the pick intents should not be changed.

get_action(intents(IntentDrop,IntentPick),intents(NewIntentDrop,IntentPick),Action):-
   agent_stones(1),
   agent_position(X,Y),
   assert(goal(goal(X,Y))),
   drop_action(IntentDrop,NewIntentDrop,Action),
   retract(goal(goal(X,Y))),
   !.

% If agent does not hold a stone, the pick intents should be added or
% modified through the pick action, the drop intents should not be
% changed.

get_action(intents(IntentDrop,IntentPick),intents(IntentDrop,NewIntentPick),Action):-
   agent_stones(0),
   agent_position(X,Y),
   assert(goal(goal(X,Y))),
   pick_action(IntentPick,NewIntentPick,Action),
   retract(goal(goal(X,Y))),
   !.

% This function is to convert goal(X,Y) to move(X,Y), used by several
% functions

convert_goal_to_move([],[]).

convert_goal_to_move([goal(G1,G2)|RestGoal],[move(G1,G2)|RestMove]):-
   convert_goal_to_move(RestGoal,RestMove).

% Base case, when drop list contains no goal, agent will stay at its
% position.

drop_action([],[],move(X,Y)):-
   agent_position(X,Y).

% When first plan of drop is applicable, choose it as the action, then
% delete the plan from the drop list.

drop_action([[goal(X,Y),[FirstPlan|RestPlan]]|IntentPick],[[goal(X,Y),RestPlan]|IntentPick],FirstPlan):-
   applicable(FirstPlan).

% When list contains goals but no related intents, append related drop
% intents after the goals, firstly add 'move' then add 'drop'

drop_action([[goal(X,Y),[]]|IntentPick],[[goal(X,Y),NewPlan]|IntentPick],Action):-
   solve(goal(X,Y),Path,_,_),
   append([_|RestPath],[_],Path),
   convert_goal_to_move(RestPath,PosNewPlan),
   append(PosNewPlan,[drop(X,Y)],[Action|NewPlan]).

% When list contains goals but first plan is not applicable, create a
% new intent after the goals, firstly add 'move' then add 'drop'

drop_action([[goal(X,Y),[FirstPlan|_]]|IntentPick],[[goal(X,Y),NewPlan]|IntentPick],Action):-
   not(applicable(FirstPlan)),
   solve(goal(X,Y),Path,_,_),
   append([_|RestPath],[_],Path),
   convert_goal_to_move(RestPath,PosNewPlan),
   append(PosNewPlan,[drop(X,Y)],[Action|NewPlan]).

% Base case, when pick list contains no goal, agent will stay at its
% position.

pick_action([],[],move(X,Y)):-
   agent_position(X,Y).

% When first plan of pick is applicable, choose it as the action, then
% delete the plan from the pick list.

pick_action([[goal(X, Y),[FirstPlan|RestPlan]]|IntentPick],[[goal(X,Y),RestPlan]|IntentPick],FirstPlan):-
   applicable(FirstPlan).

% When list contains goals but no related intents, append related pick
% intents after the goals, firstly add 'move' then add 'pick'

pick_action([[goal(X,Y),[]]|IntentPick],[[goal(X,Y),NewPlan]|IntentPick],Action):-
   solve(goal(X,Y),Path,_,_),
   append([_|RestPath],[_],Path),
   convert_goal_to_move(RestPath,PosNewPlan),
   append(PosNewPlan,[pick(X,Y)],[Action|NewPlan]).

% When list contains goals but first plan is not applicable, create a
% new intent after the goals, firstly add 'move' then add 'pick'

pick_action([[goal(X,Y),[FirstPlan|_]]|IntentPick],[[goal(X,Y),NewPlan]|IntentPick],Action):-
   not(applicable(FirstPlan)),
   solve(goal(X,Y),Path,_,_),
   append([_|RestPath],[_],Path),
   convert_goal_to_move(RestPath,PosNewPlan),
   append(PosNewPlan,[pick(X,Y)],[Action|NewPlan]).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [Part 5] update_intentions function

% This function firstly checks the observation
% If the observation is 'at' means it will not update intentions,
% agent is moving or stay at position.

update_intentions(at(_,_),Intentions, Intentions).

% If the observation is 'pick' means agent will pick up a stone, then it
% will delete the first element of pick list to update.

update_intentions(picked(_,_),intents(Drop,[_|RestPick]), intents(Drop,RestPick)).

% If the observation is 'drop' means agent will drop a stone, then it
% will delete the first element of drop list to update.

update_intentions(dropped(_,_),intents([_|RestDrop],Pick), intents(RestDrop,Pick)).


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% THIS PART IS COPIED FROM SOME CODE OF Assignment2, WITH SOME
% MODIFICATIONS

s(goal(X1,Y1),goal(X2,Y2), 1) :-
    land_or_dropped(X2,Y2),
    distance((X1,Y1),(X2,Y2),1).

s(goal(X1,Y1),goal(X2,Y2), 1000) :-
    Ylm1 is Y1 + 1, Ylm2 is Y1 - 1, between(Ylm2,Ylm1,Y2),
    Xlm1 is X1 + 1, Xlm2 is X1 - 1, between(Xlm2,Xlm1,X2),
    distance((X1,Y1),(X2,Y2),1).

solve(goal(X1,Y1),Solution,G,N):-
   goal(goal(X1,Y1)),
   Xlm1 is X1 + 1, Xlm2 is X1 - 1,
   Ylm1 is Y1 + 1, Ylm2 is Y1 - 1,
   between(Ylm2,Ylm1,Y2),
   between(Xlm2,Xlm1,X2),
   land_or_dropped(X2,Y2),
   distance((X1,Y1),(X2,Y2),1),
   Solution = [goal(X2,Y2),goal(X1,Y1)],
   G = 2,
   N = 1.

solve(Start, Solution, G, N)  :-
    ucsdijkstra([[Start,Start,0]], [], Solution, G, 1, N).

ucsdijkstra([[Node,Pred,G]|_Generated], Expanded, Path, G, N, N)  :-
    goal(Node),
    build_path([[Node,Pred]|Expanded], Path).

ucsdijkstra([[Node,Pred,G]| Generated], Expanded, Solution, G1, L, N) :-
    extend(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    ucsdijkstra(Generated1, [[Node,Pred]|Expanded], Solution, G1, M, N).

extend(Node, G, Expanded, NewLegs) :-
    findall([NewNode, Node, G1], (s(Node, NewNode, C)
    , not(head_member(NewNode, Expanded))
    , G1 is G + C
    ), NewLegs).

insert_one_leg([], Leg, [Leg]).

insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated]) :-
    Leg  = [Node,_Pred, G ],
    Leg1 = [Node,_Pred1,G1],
    G >= G1, ! .

insert_one_leg([Leg1|Generated], Leg, [Leg,Leg1|Generated]) :-
    Leg  = [_Node, _Pred, G ],
    Leg1 = [_Node1,_Pred1,G1],
    G < G1, ! .

insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated1]) :-
    insert_one_leg(Generated, Leg, Generated1).

insert_legs(Generated, [], Generated).

insert_legs(Generated, [Leg|Legs], Generated2) :-
   insert_one_leg(Generated, Leg, Generated1),
   insert_legs(Generated1, Legs, Generated2).

head_member(Node,[[Node,_]|_]).

head_member(Node,[_|Tail]) :-
  head_member(Node,Tail).

build_path([[Next,Start],[Start,Start]], [Next,Start]).

build_path([[C,B],[B,A]|Expanded],[C,B,A|Path]) :-
   build_path([[B,A]|Expanded],[B,A|Path]), ! .

build_path([Leg,_SkipLeg|Expanded],Path) :-
   build_path([Leg|Expanded],Path).
