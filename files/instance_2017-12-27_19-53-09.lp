block(aa, red, 2).
on(aa, table, 0).
block(bb, green, 4).
on(bb, aa, 0).
block(cc, green, 3).
on(cc, table, 0).
block(dd, yellow, 1).
on(dd, cc, 0).
block(ee, red, 2).
on(ee, dd, 0).
block(hh, yellow, 1).
on(hh, ee, 0).
block(ff, yellow, 4).
on(ff, table, 0).
block(gg, red, 2).
on(gg, ff, 0).
time(0..16).
goal(T) :- time(T),on(aa, table, T),on(cc, table, T),on(ff, table, T),on(ee, cc, T),on(hh, ee, T),on(bb, ff, T),on(gg, bb, T),on(dd, gg, T).
number_of_moveop(M):- M=#count{X,Y,T: moveop(X,Y,T)}.
#minimize{M: number_of_moveop(M)}.

#show moveop/3.
#show goal.
#include "_block_world_base_engine.lp".
