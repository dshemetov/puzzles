(* @URL@ *)

example = "";

parse[s_String] := StringSplit[StringTrim[s], "\n"]

partA[lines_] := 0

partB[lines_] := 0

runPart[lines_, {name_String, part_}] := Module[{time, answer},
  {time, answer} = AbsoluteTiming[part[lines]];
  Print[answer];
  WriteString["stderr", name, ": ", ToString[Round[time, 0.0001]], "s\n"]]

main[path_String] := With[{lines = parse[Import[path, "Text"]]},
  runPart[lines, {"part_a", partA}];
  runPart[lines, {"part_b", partB}]]

(* Only runs as a script with an input path, so loading this file in a notebook stays quiet. *)
If[Length[$ScriptCommandLine] > 1, main[Last[$ScriptCommandLine]]]
