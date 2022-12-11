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
func scenicScore(trees [][]int, row int, col int) int {
	var rows int = len(trees)
	var cols int = len(trees[0])
	var tree int = trees[row][col]

	var north int = 0
	for r := row - 1; r >= 0; r-- {
		north += 1
		if trees[r][col] >= tree {
			break
		}
	}
	if north == 0 {
		return 0
	}

	var south int = 0
	for r := row + 1; r < rows; r++ {
		south += 1
		if trees[r][col] >= tree {
			break
		}
	}
	if south == 0 {
		return 0
	}

	var west int = 0
	for c := col - 1; c >= 0; c-- {
		west += 1
		if trees[row][c] >= tree {
			break
		}
	}
	if west == 0 {
		return 0
	}

	var east int = 0
	for c := col + 1; c < cols; c++ {
		east += 1
		if trees[row][c] >= tree {
			break
		}
	}
	if east == 0 {
		return 0
	}

	return north * south * west * east
}

func isVisible(trees [][]int, row int, col int) bool {
	var rows int = len(trees)
	var cols int = len(trees[0])
	var tree int = trees[row][col]

	// North
	var north bool = true
	for r := 0; r < row; r++ {
		if trees[r][col] >= tree {
			north = false
			break
		}
	}
	if north {
		return true
	}

	var south bool = true
	for r := row + 1; r < rows; r++ {
		if trees[r][col] >= tree {
			south = false
			break
		}
	}
	if south {
		return true
	}

	var west bool = true
	for c := 0; c < col; c++ {
		if trees[row][c] >= tree {
			west = false
			break
		}
	}
	if west {
		return true
	}

	var east bool = true
	for c := col + 1; c < cols; c++ {
		if trees[row][c] >= tree {
			east = false
			break
		}
	}
	if east {
		return true
	}

	return false
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	var trees [][]int
	for _, line := range lines {
		if len(line) == 0 {
			break
		}
		fmt.Println(line)
		var row []int
		for _, digit := range line {
			tree, err := strconv.Atoi(string(digit))
			check(err)
			row = append(row, tree)
		}

		trees = append(trees, row)
	}

	fmt.Println(trees)
	var visible int = 0

	// Part 1
	for row := 0; row < len(trees); row++ {
		for col := 0; col < len(trees[0]); col++ {
			if isVisible(trees, row, col) {
				visible += 1
			}
		}
	}

	fmt.Printf("Visible trees: %d\n", visible)

	// Part 2
	var maxScore int = 0
	for row := 0; row < len(trees); row++ {
		for col := 0; col < len(trees[0]); col++ {
			var score = scenicScore(trees, row, col)
			if score > maxScore {
				maxScore = score
			}
		}
	}

	fmt.Printf("max scenic score: %d\n", maxScore)
}
