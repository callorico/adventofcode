package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Coordinate struct {
	row int
	col int
}

func moveTail(head Coordinate, tail *Coordinate) {
	if math.Abs(float64(head.row-tail.row)) < 2 && math.Abs(float64(head.col-tail.col)) < 2 {
		return
	}

	var rowDelta int = 0
	var colDelta int = 0

	if tail.row < head.row {
		rowDelta = 1
	} else if tail.row > head.row {
		rowDelta = -1
	}

	if tail.col < head.col {
		colDelta = 1
	} else if tail.col > head.col {
		colDelta = -1
	}

	tail.row += rowDelta
	tail.col += colDelta
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	var head Coordinate = Coordinate{row: 0, col: 0}
	var rest []Coordinate
	// Part 1
	// var knotCount int = 1
	// Part 2
	var knotCount int = 9
	for x := 0; x < knotCount; x++ {
		rest = append(rest, Coordinate{row: 0, col: 0})
	}
	var tailVisits = make(map[Coordinate]int)
	tailVisits[rest[len(rest)-1]] += 1

	fmt.Println(tailVisits)

	for _, line := range lines {
		if len(line) == 0 {
			break
		}

		fmt.Println(line)
		tokens := strings.Split(line, " ")
		direction := tokens[0]
		amount, err := strconv.Atoi(tokens[1])
		check(err)

		var rowDelta int = 0
		var targetRow int = head.row
		var colDelta int = 0
		var targetCol int = head.col

		if direction == "U" {
			rowDelta = -1
			targetRow -= amount
		} else if direction == "D" {
			rowDelta = 1
			targetRow += amount
		} else if direction == "L" {
			colDelta = -1
			targetCol -= amount
		} else if direction == "R" {
			colDelta = 1
			targetCol += amount
		}

		// Move the head around and let the tail follow
		for head.row != targetRow {
			head.row += rowDelta

			prev := head
			for idx := range rest {
				moveTail(prev, &rest[idx])
				prev = rest[idx]
			}
			tailVisits[rest[len(rest)-1]] += 1
		}

		for head.col != targetCol {
			head.col += colDelta

			prev := head
			for idx := range rest {
				moveTail(prev, &rest[idx])
				prev = rest[idx]
			}
			tailVisits[rest[len(rest)-1]] += 1
		}
	}

	// Determine the number of positions visited by the tail
	fmt.Printf("Tail visited %d positions\n", len(tailVisits))
}
