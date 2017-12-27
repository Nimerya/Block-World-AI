block(c, red, 1).
on(c, table, 0).
block(b, yellow, 4).
on(b, table, 0).
block(a, green, 3).
on(a, b, 0).
query(yes):- on(a, b, _). 
query(no):- not query(yes).
#show query/1.
