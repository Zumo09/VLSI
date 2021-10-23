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

% % Alternative model
% array[0..width-1, 0..max_height] of var 0..n: grid2d;

% % Channeling constraint
% constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X[i] <= x /\ x < X_fin[i] /\ Y[i] <= y /\ y < Y_fin[i]) <-> (grid2d[x, y] = i));

% Alternative model
array[1..n, 0..width-1, 0..max_height] of var bool: grid3dbool;

% Channeling constraint
constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) (
              (X[i] <= x /\ x < X_fin[i] /\ Y[i] <= y /\ y < Y_fin[i]) <-> (grid3dbool[i, x, y]));

% problem constraints
constraint diffn(X, Y, W, H); % 2d No Overlap Constraint
constraint forall(i in 1..n)(X[i] + W[i] <= width); % Contraint the block not to exceed the width

% implied constraints
constraint cumulative(Y, H, W, width); % sum of the row less or equal to width
constraint cumulative(X, W, H, height); % sum of the columns less or equal to height

% Symmetry Breaking
% Lexicographic symmetry breaking constraints

constraint lex_greatereq([grid3dbool[1, x, y] | x in 0..width-1, y in 0..max_height-1], [grid3dbool[1, x, y] | x in reverse(0..width-1), y in 0..max_height-1]);


% constraint lex_greatereq([grid3dbool[i, x, y] | i in 1..n, x in 0..width-1, y in 0..max_height-1], [grid3dbool[i, x, y] | i in 1..n, x in reverse(0..width-1), y in 0..max_height-1]); % flip axis X

% constraint lex_greatereq([grid2d[x, y] | x in 0..width-1, y in 0..max_height-1], [grid2d[x, y] | x in 0..width-1, y in reverse(0..max_height-1)]); % flip axis Y
% constraint lex_greatereq([grid2d[x, y] | x in 0..width-1, y in 0..max_height-1], [grid2d[x, y] | x in reverse(0..width-1), y in reverse(0..max_height-1)]); % flip axis Xy

% Symmetry Breaking
% Lexicographic symmetry breaking constraints
% constraint lex_greatereq([grid2d[x, y] | x in 0..width-1, y in 0..max_height-1], [grid2d[x, y] | x in reverse(0..width-1), y in 0..max_height-1]); % flip axis X
% constraint lex_greatereq([grid2d[x, y] | x in 0..width-1, y in 0..max_height-1], [grid2d[x, y] | x in 0..width-1, y in reverse(0..max_height-1)]); % flip axis Y
% constraint lex_greatereq([grid2d[x, y] | x in 0..width-1, y in 0..max_height-1], [grid2d[x, y] | x in reverse(0..width-1), y in reverse(0..max_height-1)]); % flip axis Xy

solve minimize height;

% array [1..n] of var 0..width: X_flip = [width - X[i] - W[i] | i in 1..n];
% array [1..n] of var 0..max_height: Y_flip = [height - Y[i] - H[i] | i in 1..n];

% array[1..n] of var 0..(max_height+width): index;
% array[1..n] of var 0..(max_height+width): indexx;
% array[1..n] of var 0..(max_height+width): indexy;
% array[1..n] of var 0..(max_height+width): indexxy;

% array[0..(width-1)*max_height] of var 0..n: grid;
% array[0..(width-1)*max_height] of var 0..n: gridx;
% array[0..(width-1)*max_height] of var 0..n: gridy;
% array[0..(width-1)*max_height] of var 0..n: gridxy;

% constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X[i] <= x /\ x < (X[i] + W[i]) /\ Y[i] <= y /\ y < (Y[i] + H[i])) <-> (grid[x + width * y] = i));
% constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X_flip[i] <= x /\ x < (X_flip[i] + W[i]) /\ Y[i] <= y /\ y < (Y[i] + H[i])) <-> (gridx[x + width * y] = i));
% constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X[i] <= x /\ x < (X[i] + W[i]) /\ Y_flip[i] <= y /\ y < (Y_flip[i] + H[i])) <-> (gridy[x + width * y] = i));
% constraint forall(i in 1..n, x in 0..width-1, y in 0..height-1) ((X_flip[i] <= x /\ x < (X_flip[i] + W[i]) /\ Y_flip[i] <= y /\ y < (Y_flip[i] + H[i])) <-> (gridxy[x + width * y] = i));

% constraint forall(i in 1..n)(index[i] = X[i]+Y[i]);
% constraint forall(i in 1..n)(indexx[i] = X_flip[i]+Y[i]);
% constraint forall(i in 1..n)(indexy[i] = X[i]+Y_flip[i]);
% constraint forall(i in 1..n)(indexxy[i] = X_flip[i]+Y_flip[i]);

% constraint lex_lesseq([grid2d[x, y] | x in 0..width-1, y in 0..height-1], [grid2d[x, y] | x in reverse(0..width-1), y in 0..height-1]); % flip axis X
% constraint lex_lesseq([grid2d[x, y] | x in 0..width-1, y in 0..height-1], [grid2d[x, y] | x in 0..width-1, y in reverse(0..height-1)]); % flip axis Y
% constraint lex_lesseq([grid2d[x, y] | x in 0..width-1, y in 0..height-1], [grid2d[x, y] | x in reverse(0..width-1), y in reverse(0..height-1)]); % flip axis X and Y

% constraint lex_lesseq(X, X_flip);
% constraint lex_lesseq(Y, Y_flip);

% constraint lex_lesseq(grid, gridx);
% constraint lex_lesseq(grid, gridy);

% constraint lex_lesseq(index, indexxy);
% constraint lex_lesseq(index, indexx);
% constraint lex_lesseq(index, indexy);