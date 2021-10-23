include "cumulative.mzn";
include "diffn.mzn";
include "lex_greatereq.mzn";

int: width;
int: n;
array [1..n] of int: W;
array [1..n] of int: H;
int: min_height;
int: max_height;

array [1..n] of var 0..width-min(W): X;
array [1..n] of var 0..max_height: Y;

array [1..n] of var min(H)..max_height: Y_fin = [Y[i] + H[i] | i in 1..n];
array [1..n] of var min(W)..width: X_fin = [X[i] + W[i] | i in 1..n];

var min_height..max_height: height = max(Y_fin);

% Alternative model
array[1..n, 0..width-1, 0..max_height] of var bool: grid3dbool;

% Channeling constraint
constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X[i] <= x /\ x < X_fin[i] /\ Y[i] <= y /\ y < Y_fin[i]) <-> (grid3dbool[i, x, y]));

% problem constraints
constraint diffn(X, Y, W, H); % 2d No Overlap Constraint
constraint forall(i in 1..n)(X[i] + W[i] <= width); % Contraint the block not to exceed the width

% implied constraints
constraint cumulative(Y, H, W, width); % sum of the row less or equal to width
constraint cumulative(X, W, H, height); % sum of the columns less or equal to height

solve minimize height;