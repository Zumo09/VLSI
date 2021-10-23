include "globals.mzn";

int: width; % board width
int: n; % number of chhips
array [1..n] of int: chip_w;
array [1..n] of int: chip_h;

% Areas
array [1..n] of int: area = [chip_w[i] * chip_h[i] | i in 1..n];

int: max_area_idx = arg_max(area);

array [1..n] of int: w = chip_w; % renaiming to keep consistency wrt the other model
array [1..n] of int: h = chip_h;

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

solve :: seq_search([
          int_search(y, smallest, indomain_min) :: int_search(x, first_fail, indomain_min),
          int_search([height], input_order, indomain_min),
])

minimize height;

        
        
        
      

