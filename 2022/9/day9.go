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

func moveTail(head Coordinate, tail *Coordinate, tailVisits map[Coordinate]int) {
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

	tailVisits[*tail] += 1
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	var head Coordinate = Coordinate{row: 0, col: 0}
	var tail Coordinate = Coordinate{row: 0, col: 0}
	var tailVisits = make(map[Coordinate]int)
	tailVisits[tail] += 1

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
			moveTail(head, &tail, tailVisits)
		}

		for head.col != targetCol {
			head.col += colDelta
			moveTail(head, &tail, tailVisits)
		}
	}

	// Determine the number of positions visited by the tail
	fmt.Printf("Tail visited %d positions\n", len(tailVisits))
}
