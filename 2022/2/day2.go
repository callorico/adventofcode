package main

import (
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type round struct {
	opponent string
	me       string
}

func part1(strategy []round) {
	score := 0
	// A: Rock
	// B: Paper
	// C: Scissors
	// X: Rock
	// Y: Paper
	// Z: Scissors
	results := map[string]map[string]int{
		"A": {
			"X": 3,
			"Y": 6,
			"Z": 0,
		},
		"B": {
			"X": 0,
			"Y": 3,
			"Z": 6,
		},
		"C": {
			"X": 6,
			"Y": 0,
			"Z": 3,
		},
	}

	for _, r := range strategy {
		roundScore := 0
		if r.me == "X" {
			roundScore += 1
		} else if r.me == "Y" {
			roundScore += 2
		} else if r.me == "Z" {
			roundScore += 3
		}

		roundScore += results[r.opponent][r.me]
		score += roundScore
	}

	fmt.Printf("total score: %d\n", score)
}

func part2(strategy []round) {
	score := 0
	// A: Rock
	// B: Paper
	// C: Scissors
	// Rock: 1
	// Paper: 2
	// Scissors: 3
	results := map[string]map[string]int{
		"A": {
			// Lose (Scissors)
			"X": 3,
			// Draw (Rock)
			"Y": 1,
			// Win (Paper)
			"Z": 2,
		},
		"B": {
			// Lose (Rock)
			"X": 1,
			// Draw (Paper)
			"Y": 2,
			// Win (Scissors)
			"Z": 3,
		},
		"C": {
			// Lose (Paper)
			"X": 2,
			// Draw (Scissors)
			"Y": 3,
			// Win (Rock)
			"Z": 1,
		},
	}

	for _, r := range strategy {
		roundScore := 0
		if r.me == "X" {
			roundScore += 0
		} else if r.me == "Y" {
			roundScore += 3
		} else if r.me == "Z" {
			roundScore += 6
		}

		// Now figure out what I am showing
		roundScore += results[r.opponent][r.me]
		score += roundScore
	}

	fmt.Printf("total score: %d\n", score)

}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	var strategy []round
	lines := strings.Split(string(dat), "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		guide := strings.Split(line, " ")
		strategy = append(strategy, round{opponent: guide[0], me: guide[1]})
	}

	part1(strategy)
	part2(strategy)
}
