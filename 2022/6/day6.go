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

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	input := lines[0]

	// windowSize := 4
	windowSize := 14
	for index, ch := range input {
		if index < windowSize-1 {
			continue
		}

		var window = make(map[rune]bool)
		window[ch] = true
		for i := 1; i < windowSize; i++ {
			window[rune(input[index-i])] = true
		}

		if len(window) == windowSize {
			fmt.Printf("pos: %d\n", index+1)
			break
		}
	}
}
