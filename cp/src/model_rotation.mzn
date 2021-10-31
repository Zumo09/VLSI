include "globals.mzn";

int: width; % board width
int: n; % number of rectangle
array [1..n] of int: chip_w;
array [1..n] of int: chip_h;

% Areas
array [1..n] of int: area = [chip_w[i] * chip_h[i] | i in 1..n];

int: max_area_idx = arg_max(area);

% rotation
array[1..n] of var 0..1: r; % Flag to handle rotationd

array[1..n] of var int: w; 
array[1..n] of var int: h;

constraint forall(i in 1..n)(
 w[i] == (1-r[i])*chip_w[i] + r[i]*chip_h[i] /\ 
 h[i] == (1-r[i])*chip_h[i] + r[i]*chip_w[i]
); 

% minimum and maximum height
int: h_min_area = ceil(sum(area)/width);

int: h_min = max(chip_h ++ [h_min_area]);
int: h_max = 2*h_min;

% objective
var h_min..h_max: height;

% position variables
array [1..n] of var 0..width-1: x;
array [1..n] of var 0..h_max: y;

% no overlapping constraint
constraint diffn(x, y, w, h);

% containment constraint
constraint forall(i in 1..n)(x[i] + w[i] <= width /\ y[i] + h[i] <= height);
  
% implied constraint as suggested in point 2
constraint cumulative(x, w, h, height);
constraint cumulative(y, h, w, width);

% symmetry breaking - Steinberg
constraint x[max_area_idx] < 1 + (width - w[max_area_idx]) div 2;
constraint y[max_area_idx] < 1 + (height - h[max_area_idx]) div 2;

% symmetry breaking - chip with same dimensions
constraint forall(i in 1..n-1, j in 2..n where i<j)(
  (w[i]==w[j] /\ h[i]==h[j]) -> lex_less([x[i], y[i]], [x[j], y[j]]));

% symmetry breaking 3
constraint forall(i in 1..n-1, j in 2..n where i != j)(
  (chip_w[i] == chip_h[j] /\ chip_h[i] == chip_w[j]) -> not(r[i]=1 /\ r[j]=1)
);

% symmetry breaking - don't rotate square chips
constraint forall(i in 1..n)(
  (chip_w[i] == chip_h[i]) -> r[i] = 0
);

solve :: seq_search([
          int_search(y, smallest, indomain_min) :: int_search(x, first_fail, indomain_min),
          int_search([height], input_order, indomain_min),
])

minimize height;

        
        
        
      

