(* Part 1 *)
a = 273025; b = 767253;
t = Flatten[Table[FromDigits[{i, j, k, l, m, n}],
                  {i, 1, 9}, {j, i, 9}, {k, j, 9},
                  {l, k, 9}, {m, l, 9}, {n, m, 9}]];
Length@Select[t, MemberQ[Differences@IntegerDigits[#], 0] && a <= # <= b &]

(* Part 2 *)
f[n_] := Differences@IntegerDigits[n] /. Thread[Range[2, 9] -> 1]
g[n_] := f[n][[1 ;; 2]] == {0, 1} || f[n][[-2 ;; -1]] == {1, 0} ||
             AnyTrue[Partition[f[n], 3, 1], # == {1, 0, 1} &]
Length@Select[t, g[#] && a <= # <= b &]