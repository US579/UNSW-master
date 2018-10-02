
run:-
style_check(-singleton).
style_check(-discontiguous).
set_prolog_flag(prompt_alternatives_on, groundness).
[gridworld].
[land1].
[agent].
init_world.
incorporate_goals([goal(1,2),goal(5,2),goal(1,4)], intents([[goal(4,4),[]]],[[goal(2,2),[]]]), Intentions).
