// @URL@
package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

const example = ``

func parse(s string) []string {
	return strings.Split(strings.Trim(s, "\n"), "\n")
}

func partA(lines []string) int {
	return 0
}

func partB(lines []string) int {
	return 0
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
