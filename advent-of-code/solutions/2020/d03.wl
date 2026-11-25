(* 2020 day 3: https://adventofcode.com/2020/day/3 *)

parse[s_String] := Characters /@ StringSplit[StringTrim[s], "\n"]

(* Trees hit going `right` columns per `down` rows. The pattern repeats to the right forever. *)
countTrees[grid_, {right_, down_}] :=
  With[{height = Length[grid], width = Length[First[grid]]},
    Total@Table[
      Boole[grid[[1 + down i, 1 + Mod[right i, width]]] == "#"],
      {i, 0, Floor[(height - 1)/down]}]]

partA[grid_] := countTrees[grid, {3, 1}]

partB[grid_] := Times @@ (countTrees[grid, #] & /@ {{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}})

runPart[lines_, {name_String, part_}] := Module[{time, answer},
  {time, answer} = AbsoluteTiming[part[lines]];
  Print[answer];
  WriteString["stderr", name, ": ", ToString[Round[time, 0.0001]], "s\n"]]

main[path_String] := With[{grid = parse[Import[path, "Text"]]},
  runPart[grid, {"part_a", partA}];
  runPart[grid, {"part_b", partB}]]

(* Only runs as a script with an input path, so loading this file in a notebook stays quiet. *)
If[Length[$ScriptCommandLine] > 1, main[Last[$ScriptCommandLine]]]
