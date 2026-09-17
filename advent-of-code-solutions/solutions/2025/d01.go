// https://adventofcode.com/2025/day/1
//
// A 100-position dial starts at 50. Each line turns it right (R) or left (L).
// Part a counts the turns that end on 0, part b counts every pass over 0.
package main

import (
	"fmt"
	"strconv"
	"os"
	"strings"
	"time"
)

const example = ``

func parse(s string) []string {
	return strings.Split(strings.Trim(s, "\n"), "\n")
}

// "R21" -> 21, "L2" -> -2
func parseTurns(lines []string) []int {
	turns := make([]int, len(lines))
	for i, line := range lines {
		n, _ := strconv.Atoi(line[1:])
		if line[0] == 'L' {
			n = -n
		}
		turns[i] = n
	}
	return turns
}

// floorDiv rounds toward negative infinity, unlike Go's `/`.
func floorDiv(a, b int) int {
	q := a / b
	if a%b != 0 && (a < 0) != (b < 0) {
		q--
	}
	return q
}

func partA(lines []string) int {
	pos, count := 50, 0
	for _, turn := range parseTurns(lines) {
		pos = ((pos+turn)%100 + 100) % 100
		if pos == 0 {
			count++
		}
	}
	return count
}

func partB(lines []string) int {
	pos, count := 50, 0
	for _, turn := range parseTurns(lines) {
		next := pos + turn
		// The position stays unwrapped, so a pass over 0 is a multiple of 100
		// crossed. Landing on one counts, leaving one does not.
		if turn > 0 {
			count += floorDiv(next, 100) - floorDiv(pos, 100)
		} else {
			count += floorDiv(pos-1, 100) - floorDiv(next-1, 100)
		}
		pos = next
	}
	return count
}

func main() {
	raw, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	lines := parse(string(raw))
	for _, part := range []struct {
		name string
		fn   func([]string) int
	}{{"part_a", partA}, {"part_b", partB}} {
		start := time.Now()
		fmt.Println(part.fn(lines))
		fmt.Fprintf(os.Stderr, "%s: %.4fs\n", part.name, time.Since(start).Seconds())
	}
}
