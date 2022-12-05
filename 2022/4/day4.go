package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type sections struct {
	min int
	max int
}

func parseSection(encoded string) sections {
	tokens := strings.Split(encoded, "-")
	min, err := strconv.Atoi(tokens[0])
	check(err)
	max, err := strconv.Atoi(tokens[1])
	check(err)

	return sections{min: min, max: max}
}

func fullyContains(a sections, b sections) bool {
	// Returns true if a fully contains b
	return a.min <= b.min && a.max >= b.max
}

func overlaps(a sections, b sections) bool {
	// Returns true if a overlaps at all with b
	return (a.max >= b.min && a.min <= b.min) ||
		(a.min <= b.max && a.max >= b.max)
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	numContains := 0
	numOverlaps := 0

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		ranges := strings.Split(line, ",")

		p1 := parseSection(ranges[0])
		p2 := parseSection(ranges[1])

		if fullyContains(p1, p2) || fullyContains(p2, p1) {
			numContains += 1
		}

		if overlaps(p1, p2) || overlaps(p2, p1) {
			numOverlaps += 1
		}
	}

	fmt.Printf("Total fully contained pairs: %d\n", numContains)
	fmt.Printf("Total overlapping pairs: %d\n", numOverlaps)
}
