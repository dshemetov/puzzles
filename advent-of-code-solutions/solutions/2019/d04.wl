(* 2019 day 4: https://adventofcode.com/2019/day/4 *)

(* The input is the password range, like "273025-767253". *)
parse[s_String] := ToExpression /@ StringSplit[StringTrim[s], "-"]

(* Every six-digit number whose digits never decrease. *)
candidates = Flatten[Table[FromDigits[{i, j, k, l, m, n}],
                           {i, 1, 9}, {j, i, 9}, {k, j, 9},
                           {l, k, 9}, {m, l, 9}, {n, m, 9}]];

partA[{lo_, hi_}] :=
  Length@Select[candidates, MemberQ[Differences@IntegerDigits[#], 0] && lo <= # <= hi &]

(* Part b: some run of equal digits must be exactly two long. In the differences, all non-zero
   gaps become 1, so an exact pair is a 0 with a 1 (or the edge) on each side. *)
f[n_] := Differences@IntegerDigits[n] /. Thread[Range[2, 9] -> 1]
g[n_] := f[n][[1 ;; 2]] == {0, 1} || f[n][[-2 ;; -1]] == {1, 0} ||
           AnyTrue[Partition[f[n], 3, 1], # == {1, 0, 1} &]

partB[{lo_, hi_}] := Length@Select[candidates, g[#] && lo <= # <= hi &]

runPart[range_, {name_String, part_}] := Module[{time, answer},
  {time, answer} = AbsoluteTiming[part[range]];
  Print[answer];
  WriteString["stderr", name, ": ", ToString[Round[time, 0.0001]], "s\n"]]

main[path_String] := With[{range = parse[Import[path, "Text"]]},
  runPart[range, {"part_a", partA}];
  runPart[range, {"part_b", partB}]]

(* Only runs as a script with an input path, so loading this file in a notebook stays quiet. *)
If[Length[$ScriptCommandLine] > 1, main[Last[$ScriptCommandLine]]]
