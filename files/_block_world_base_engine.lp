object(table,white,100).


% goal predicate which holds when the goal conditions have be reached
goal :- time(T), goal(T).
:- not goal. 

% goal(T) holds for all subsequent situations 
% This is used for blocking all operators after the goal has been reached
goal(T2) :- nextstate(T2,T1), goal(T1).
%goal(T):- time(T), on(a,c,T).
%goal(T) :- time(T), 
%   on(e,table,T), 
%   on(b,e,T), 
%   on(c,b,T), 
%   on(d,table,T), 
%   on(a,d,T), 
%   on(f,table,T).

% Stop applying operators when the goal has been reached
% operator preconditions
{moveop(X,Y,T)}:- 
	time(T),
	block(X,CX,LX),
	object(Y,CY,LY),
	X != Y,
	LX <= LY,
	CX != CY,
	not covered(X,T),
	not covered(Y,T),	
	not goal(T).

% operator effects
on(X,Y,T2) :- 
	block(X,CX,LX),
	object(Y,CY,LY),
	nextstate(T2,T1),
	moveop(X,Y,T1).

covered(X,T) :-
	block(Z,CZ,LZ),
	block(X,CX,LX),
	time(T),
    on(Z,X,T).

% frame axioms
on(X,Y,T2) :-
	nextstate(T2,T1),
	block(X,CX,LX),
	object(Y,CY,LY),
    on(X,Y,T1),
    not moving(X,T1).

moving(X,T) :- 
	time(T),
	block(X,CX,LX),
	object(Y,CY,LY),
    moveop(X,Y,T).

% An object cannot be moved on top of an object that is moved
:-block(X,CX,LX), object(Y,CY,LY), block(Z,CZ,LZ), time(T), moveop(X,Y,T), moveop(Z,X,T).

% An object can be moved by one move operation at a time 
:-2{moveop(X,Y,T):block(X,CX,LX)}, object(Y, CY, LY),time(T).

% Two objects cannot be moved on top of the same object by  
% one move operation at a time 
:-2{moveop(X,Y,T):block(Y,CY,LY)}, block(X,CX,LX),time(T).

% pruning rules
% do not move blocks from table to table
:- block(X,CX,LX),
	time(T), 
	moveop(X,table,T), 
	on(X,table,T).

% do not move a block on top of something and then on the table
:- nextstate(T2,T1),
	block(X,CX,LX),
	object(Y,CY,LY), 
	moveop(X,Y,T1), 
	moveop(X,table,T2).


nextstate(Y,X) :- time(X), time(Y), Y = X + 1.


object(X,CX,LX) :- block(X,CX,LX). 

%query(yes):- on(f,e,_).
%query(no):- not query(yes).


%number_of_moveop(M):- M=#count{X,Y,T:moveop(X,Y,T)}.
%#minimize{ M:number_of_moveop(M)}.






%#show query/1.
%#show moveop/3.
%#show goal.

