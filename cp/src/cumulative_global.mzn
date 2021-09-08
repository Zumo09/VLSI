include "cumulative.mzn";

int: width;
int: n;
array [1..n] of int: W;
array [1..n] of int: H;

int: max_height = sum(H);

array [1..n] of var 0..width: X;
array [1..n] of var 0..max_height: Y;
array [1..n] of var 0..max_height: Y_fin;

var 1..max_height: height = max(Y_fin);

constraint forall(i in 1..n)(Y_fin[i] = Y[i] + H[i]);

constraint cumulative(Y, H, W, width);

constraint cumulative(X, W, H, height);

solve minimize height;

% output ["H:" ++ show(height) ++ "\nX: " ++ show(X) ++ "\nY:" ++ show(Y)]