package main

import (
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
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

	chamber := [][]rune
	var commandIndex = 0
}
