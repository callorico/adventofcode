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

type Chamber struct {
	rocks   map[int]map[int]rune
	maxCols int
	topRow  int
}

func MakeChamber() Chamber {
	return Chamber{
		rocks:   make(map[int]map[int]rune),
		maxCols: 7,
		topRow:  0,
	}
}

func GetChamber(chamber *Chamber, row int, col int) rune {
	val, ok := chamber.rocks[row]
	if !ok {
		return '.'
	}

	result, ok := val[col]
	if !ok {
		return '.'
	}

	return result
}

func SetRock(chamber *Chamber, row int, col int) {
	val, ok := chamber.rocks[row]
	if !ok {
		val = make(map[int]rune)
		chamber.rocks[row] = val
	}

	val[col] = '#'
	if row >= chamber.topRow {
		chamber.topRow = row + 1
	}
}

func PrintChamber(chamber *Chamber) {
	for r := chamber.topRow; r >= 0; r-- {
		for c := 0; c < chamber.maxCols; c++ {
			fmt.Printf("%c", GetChamber(chamber, r, c))
		}
		fmt.Println()
	}
}

func CanMove(rockRow int, rockCol int, rock [][]rune, chamber *Chamber) bool {
	// rockRow is index of the bottom of the shape
	// rockCol is index of the left edge of the shape
	for r := 0; r < len(rock); r++ {
		for c := 0; c < len(rock[0]); c++ {
			if rock[r][c] == '#' {
				chamberRow := rockRow + (len(rock) - 1 - r)
				chamberCol := rockCol + c
				if chamberRow < 0 || chamberCol < 0 || chamberCol >= chamber.maxCols || GetChamber(chamber, chamberRow, chamberCol) == '#' {
					// Rock has reached the edge of the chamber, the bottom of the chamber, or it has intersected with another rock
					return false
				}
			}
		}
	}
	return true
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	commands := lines[0]

	shapes := [][][]rune{
		{
			{'#', '#', '#', '#'},
		},
		{
			{'.', '#', '.'},
			{'#', '#', '#'},
			{'.', '#', '.'},
		},
		{
			{'.', '.', '#'},
			{'.', '.', '#'},
			{'#', '#', '#'},
		},
		{
			{'#'},
			{'#'},
			{'#'},
			{'#'},
		},
		{
			{'#', '#'},
			{'#', '#'},
		},
	}

	// Row 0 is the bottom of the chamber
	// Row N is the top of the chamber
	chamber := MakeChamber()

	var commandCount = 0
	for rock := 0; rock < 2022; rock++ {
		shapeIndex := rock % len(shapes)
		shape := shapes[shapeIndex]

		// Rock appears (bottom edge is 3 units above the highest rock in the room)
		// rockRow is the row of the bottom of the shape
		rockRow := chamber.topRow + 3
		// rockCol is the column of the left edge of the shape
		rockCol := 2

		for true {
			fmt.Printf("rock %d is at %d, %d\n", rock+1, rockRow, rockCol)
			// PrintChamber(&chamber)

			command := commands[commandCount%len(commands)]
			commandCount++

			// Apply command
			fmt.Printf("command: %c\n", command)
			if command == '<' {
				if CanMove(rockRow, rockCol-1, shape, &chamber) {
					rockCol--
				}
			} else if command == '>' {
				if CanMove(rockRow, rockCol+1, shape, &chamber) {
					rockCol++
				}
			}

			// Drop rock down one
			if CanMove(rockRow-1, rockCol, shape, &chamber) {
				rockRow--
			} else {
				fmt.Printf("rock %d has reached a terminal point of %d, %d\n", rock+1, rockRow, rockCol)
				break
			}
		}

		// Commit the shape into the chamber at the specified location
		for r := 0; r < len(shape); r++ {
			for c := 0; c < len(shape[0]); c++ {
				if shape[r][c] == '#' {
					chamberRow := rockRow + (len(shape) - 1 - r)
					chamberCol := rockCol + c
					SetRock(&chamber, chamberRow, chamberCol)
				}
			}
		}
	}

	fmt.Printf("Rock tower height: %d\n", chamber.topRow)
}
