include "globals.mzn";

int: W; %chip width
int: n; %number of ciruits
array[1..n, 1..2] of int: dimensions; %size of each circuits


array[1..n] of var 0..1: r; %Flag to handle rotationd

%decreasing area order
array[int] of int: order = arg_sort([-dimensions[i, 1]*dimensions[i, 2] | i in 1..n]); 

array[1..n] of var 1..max(dimensions): w; 
array[1..n] of var 1..max(dimensions): h;

constraint forall(i in order)(
 w[i] == (1-r[i])*dimensions[i, 1] + r[i]*dimensions[i,2] /\ h[i] == (1-r[i])*dimensions[i, 2] + r[i]*dimensions[i,1]); 

int: min_area_h = (sum([dimensions[i, 1]*dimensions[i, 2] | i in 1..n]) div W);
int: h_min = max([dimensions[i,2]|i in order] ++ [min_area_h]);

int: h_max = 2*h_min;
var h_min..h_max: H;

array [1..n] of var 0..W-1: x;
array [1..n] of var 0.. h_max: y;



%no overlapping
constraint diffn(x, y, w, h);

%containment constraint
constraint forall(i in 1..n)(
  x[i] + w[i] <= W /\ y[i] + h[i] <= H);


%no rotation for square circuits
constraint forall(i in 1..n where dimensions[i, 1]=dimensions[i, 2])(r[i]=0);

%implied constraint as suggested in point 2
constraint cumulative(x, w, h, H);
constraint cumulative(y, h, w, W);

%symmetry breaking
constraint x[1] < 1 + (W - w[1]) div 2;
constraint y[1] < 1 + (H - h[1]) div 2;


%symmetry breaking 2
constraint forall(i in 1..n-1, j in 2..n where i != j)(
  (w[i]==w[j] /\ h[i]==h[j]) -> lex_less([x[i], y[i]], [x[j], y[j]])
);
 
%symmetry breaking 3
constraint forall(i in 1..n-1, j in 2..n where i != j)(
  (dimensions[i, 1]== dimensions[j, 2] /\ dimensions[i, 2]==dimensions[j, 1]) -> not(r[i]=1 /\ r[j]=1)
);

solve :: seq_search([
          int_search(y, smallest, indomain_min) :: int_search(x, first_fail, indomain_min),
          int_search([H], input_order, indomain_min),
])

minimize H;





output [concat(["\(W) \(H) \n"]),
        "\(n)\n",
        concat(["\(w[i]) \(h[i]) \(x[i]) \(y[i]) \n" | i in order])
        
        ];
        

        
        
        
      

