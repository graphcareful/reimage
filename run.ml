let average a b =
  let sum = a +. b in
  sum /. 2.0;;
(* val average : float -> float -> float = <fun> *)

(* Example of how recursive functions must use the rec keyword *)
let rec range a b =
  if a > b then []
  else a :: range (a+1) b;;
(* val range : int -> int -> int list = <fun> *)

average 5. 3.
