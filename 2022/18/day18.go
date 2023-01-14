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

	var min = Position{
		x: math.MaxInt,
		y: math.MaxInt,
		z: math.MaxInt,
	}

	var max = Position{
		x: math.MinInt,
		y: math.MinInt,
		z: math.MinInt,
	}

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

		if x < min.x {
			min.x = x
		} else if x > max.x {
			max.x = x
		}

		if y < min.y {
			min.y = y
		} else if y > max.y {
			max.y = y
		}

		if z < min.z {
			min.z = z
		} else if z > max.z {
			max.z = z
		}
	}

	fmt.Printf("Number of cubes %v\n", len(positions))
	fmt.Printf("Bounds: Min: %v, Max :%v\n", min, max)

	// Starting from the outside, expand in all directions as far as possible.
	// The cubes that are not reached are inside the structure and should not
	// be counted in the surface area calculation.
	var toCheck = make(map[Position]bool)
	for x := min.x - 1; x <= max.x+1; x++ {
		for y := min.y - 1; y <= max.y+1; y++ {
			for z := min.z - 1; z < max.z+1; z++ {
				var space = Position{x: x, y: y, z: z}
				_, exists := lookup[space]
				if !exists {
					toCheck[Position{x: x, y: y, z: z}] = true
				}
			}
		}
	}

	var deltas = [3]int{-1, 1}

	var stack []Position
	stack = append(stack, Position{x: min.x - 1, y: min.y - 1, z: min.z - 1})
	for len(stack) > 0 {
		index := len(stack) - 1
		var pos = stack[index]
		stack = stack[:index]
		// Remove from toCheck
		fmt.Printf("Removing %v from consideration\n", pos)
		delete(toCheck, pos)

		// Can expand if inside toCheck dict and NOT in lookup
		// See if we can expand in any direction
		for _, xDelta := range deltas {
			var newPos = Position{x: pos.x + xDelta, y: pos.y, z: pos.z}
			_, found := toCheck[newPos]
			if !found {
				continue
			}

			stack = append(stack, newPos)
		}

		for _, yDelta := range deltas {
			var newPos = Position{x: pos.x, y: pos.y + yDelta, z: pos.z}
			_, found := toCheck[newPos]
			if !found {
				continue
			}

			stack = append(stack, newPos)
		}

		for _, zDelta := range deltas {
			var newPos = Position{x: pos.x, y: pos.y, z: pos.z + zDelta}
			_, found := toCheck[newPos]
			if !found {
				continue
			}

			stack = append(stack, newPos)
		}
	}

	fmt.Printf("Cubes inside the structure are: %d\n%v\n", len(toCheck), toCheck)
	for pos, _ := range toCheck {
		lookup[pos] = true
	}

	var totalUnconnectedSides int = 0

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
