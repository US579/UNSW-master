%Name:  Wanze Liu
%Student number:  z5137189
%assignment name:   Prolog Programming

% Program:  comp9414 assignment1.pl
% Source:   Prolog
%
% Purpose:  This is a answer to the comp9414.pl assignment task 
%
% History:  Original code by Wanze Liu


% question1:
% input
sumsq_neg(List,Sum):-
  tosetHelper(List,0,Sum).
% base case
tosetHelper([],Acc,Acc).

% Judge if H < 0 ,H*H sum up
tosetHelper([H|T],Acc,Sum):-
  H<0,
  NewAcc is (H**2 + Acc),
  tosetHelper(T,NewAcc,Sum).

% judge if H > 0 do nothing 
tosetHelper([H|T],Acc,Sum):-
  H >= 0,
tosetHelper(T,Acc,Sum).

% question2:
likes(mary, apple).
likes(mary, pear).
likes(mary, grapes).
likes(tim, mango).
likes(tim, apple).
likes(jane, apple).
likes(jane, mango).

% base case
all_like(_,[]).

% compare fact
all_like(H,[P|W]):-
  likes(H,P),
  all_like(H,W).

% base case
all_like_all([],_).
all_like_all(_,[]).

% input
% extract the Head and Tail from the both Lists 
all_like_all([H|T],[F|S]):-
  all_like(H,[F|S]),
  all_like_all(T,[F|S]).

% question3:
% input
% This query would find the "boundary cases"
sqrt_table(N, M, Result):-
  N > 0,
  M > 0,
  N >= M,
  sqrt_table1(N,M,[],Result).

% base case
sqrt_table1(N,M,Acc,Acc):-
  N < M.

%  Num and sqrt are bound to the number of elements in List.
sqrt_table1(N,M,Acc,Result):-
  N >= M,
  H is M,
  T is sqrt(N),
  Num = M + 1 ,
  sqrt_table1(N,Num,[[H|[T]]|Acc],Result).

% question4:
% input
% base case
chop_up([],[]).
chop_up([X],[X]).

chop_up([Firstnum,Secondnum|A],[Firstnum|B]):-    
  Firstnum+1=\=Secondnum,                   
chop_up([Secondnum|A],B).          

% recursive and cut the number in the middle of sequence
chop_up(List,[[Firstnum,Secondnum]|B]):-
  append([Firstnum|_],[Secondnum,Thirdnum|A],List),
  Secondnum+1=\=Thirdnum,
  chop_up([Thirdnum|A],B).
chop_up([First|X],[[First,B]]):-
  append(_,[B],X).


%question5:
% input
tree_eval(_Input, tree(empty,Z,empty), Eval) :- 
    number(Z),
    Eval is Z.

% change the variable z into the value Z 
tree_eval(Input, tree(empty,Z,empty), Eval) :- 
   Z=z, 
   Eval is Input. 

% recursive branches of tree
tree_eval(Value, tree(tree(LL,LOp,LR),Op,tree(RL,ROp,RR)), Eval) :-
   tree_eval(Value, tree(LL,LOp,LR), L),
   tree_eval(Value, tree(RL,ROp,RR), R),
   Result=..[Op,L,R],
   Eval is Result.


