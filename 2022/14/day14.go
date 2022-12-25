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
	x int
	y int
}

func Equals(left, right *Coordinate) bool {
	return left.x == right.x && left.y == right.y
}

func ParseCoordinate(input string) Coordinate {
	tokens := strings.Split(input, ",")
	x, ok := strconv.Atoi(tokens[0])
	check(ok)
	y, ok := strconv.Atoi(tokens[1])
	check(ok)

	return Coordinate{x: x, y: y}
}

func increment(start, end int) int {
	if start > end {
		return -1
	} else {
		return 1
	}
}

func nextPos(current Coordinate, grid map[Coordinate]rune) Coordinate {
	// Try down
	// Then down-left
	// Then down-right
	for _, deltaX := range [3]int{0, -1, 1} {
		next := Coordinate{x: current.x + deltaX, y: current.y + 1}
		if grid[next] != 'o' && grid[next] != '#' {
			return next
		}
	}

	return current
}

func printGrid(grid map[Coordinate]rune, xMax int, yMax int) {
	for y := 0; y <= yMax; y++ {
		for x := 490; x <= xMax; x++ {
			ch, ok := grid[Coordinate{x: x, y: y}]
			if !ok {
				ch = '.'
			}
			fmt.Printf("%c", ch)
		}
		fmt.Println()
	}
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)

	var sparseGrid = make(map[Coordinate]rune)
	var xMin int = math.MaxInt
	var xMax int = 0
	var yMax int = 0

	lines := strings.Split(string(dat), "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		tokens := strings.Split(line, " -> ")
		start := ParseCoordinate(tokens[0])
		for i := 1; i < len(tokens); i++ {
			end := ParseCoordinate(tokens[i])
			// Fill in the rocks between start and end. Update max grid size
			for x := start.x; x != end.x; x += increment(start.x, end.x) {
				sparseGrid[Coordinate{x: x, y: start.y}] = '#'
				if x > xMax {
					xMax = x
				} else if x < xMin {
					xMin = x
				}
			}

			for y := start.y; y != end.y; y += increment(start.y, end.y) {
				sparseGrid[Coordinate{x: start.x, y: y}] = '#'
				if y > yMax {
					yMax = y
				}
			}
			sparseGrid[end] = '#'

			for _, coord := range [2]Coordinate{start, end} {
				if coord.x > xMax {
					xMax = coord.x
				} else if coord.y > yMax {
					yMax = coord.y
				}
			}

			start = end
		}
	}

	fmt.Printf("xmax: %d, ymax: %d\n", xMax, yMax)
	// printGrid(sparseGrid, xMax, yMax)

	var grains int = 0
	var steady bool = false
	for !steady {
		// Simulate sand falling from the top
		sandPos := Coordinate{x: 500, y: 0}
		for true {
			next := nextPos(sandPos, sparseGrid)
			if next.y > yMax {
				// Sand has fallen off the bottom
				fmt.Printf("Sand has fallen off the bottom of the grid\n")
				steady = true
				break

			} else if Equals(&sandPos, &next) {
				// Sand is stuck
				sparseGrid[sandPos] = 'o'
				grains += 1
				break
			}

			sandPos = next
		}

		// fmt.Printf("==== Grains %d ====\n", grains)
		// printGrid(sparseGrid, xMax, yMax)
	}

	fmt.Printf("Units of sand: %d\n", grains)
}
