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

type Position struct {
	x int
	y int
	z int
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var positions []*Position
	var lookup = make(map[Position]bool)

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		coordinates := strings.Split(line, ",")
		if len(coordinates) != 3 {
			panic("Improperly formed coordinate")
		}

		x, err := strconv.Atoi(coordinates[0])
		check(err)
		y, err := strconv.Atoi(coordinates[1])
		check(err)
		z, err := strconv.Atoi(coordinates[2])
		check(err)

		position := Position{x: x, y: y, z: z}
		lookup[position] = true
		positions = append(positions, &position)
	}

	fmt.Printf("Number of cubes %v\n", len(positions))
	var totalUnconnectedSides int = 0
	var deltas = [3]int{-1, 1}

	for _, pos := range positions {
		var unconnectedSides = 0
		// For each side. Is is adjacent to anoter cuboid?
		for _, xDelta := range deltas {
			// Does a cuboid exist at this position
			_, exists := lookup[Position{x: pos.x + xDelta, y: pos.y, z: pos.z}]
			if !exists {
				unconnectedSides += 1
			}
		}

		for _, yDelta := range deltas {
			_, exists := lookup[Position{x: pos.x, y: pos.y + yDelta, z: pos.z}]
			if !exists {
				unconnectedSides += 1
			}
		}

		for _, zDelta := range deltas {
			_, exists := lookup[Position{x: pos.x, y: pos.y, z: pos.z + zDelta}]
			if !exists {
				unconnectedSides += 1
			}
		}

		fmt.Printf("Unconnected sides for %v is %d\n", pos, unconnectedSides)
		totalUnconnectedSides += unconnectedSides
	}

	fmt.Printf("Unconnected sides: %d\n", totalUnconnectedSides)
}
