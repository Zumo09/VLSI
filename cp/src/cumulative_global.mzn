include "cumulative.mzn";
include "diffn.mzn";

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

constraint diffn(X, Y, W, H);

constraint cumulative(Y, H, W, width);
constraint cumulative(X, W, H, height); % secondo me va cambiato questo

constraint forall(i in 1..n)(X[i] + W[i] <= width); % forse è inutile o forse no
% constraint che evita l'overlapping sull'asse x

solve minimize height;

% output ["H:" ++ show(height) ++ "\nX: " ++ show(X) ++ "\nY:" ++ show(Y)]