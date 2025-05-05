(* Mathematica Solution *)
input = Import["input3a.txt"];
parsedInput = StringSplit[input, "\n"];
parsedInput = Map[StringSplit[#, ""] &, parsedInput];
periodicInput = ArrayPad[parsedInput, {{0, 0}, {0, 2400}}, "Periodic"];

(* Part a *)
treeCount = 0;
height = First@Dimensions[parsedInput];
For[i = 0, i < height, i++,
    treeCount += Boole[periodicInput[[1 + i, 1 + 3 i]] == "#"]
]
Print[treeCount]

(* Part b *)
countTreesSlope[right_, down_] := Module[{},
  treeCount = 0;
  height = First@Dimensions[parsedInput];
  For[i = 0, down i < height, i++,
   treeCount += Boole[periodicInput[[1 + down i, 1 + right i]] == "#"]
   ];
  treeCount]
Print[countTreesSlope[1, 1] countTreesSlope[3, 1] countTreesSlope[5, 1] countTreesSlope[7, 1] countTreesSlope[1, 2]]