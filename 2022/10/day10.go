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

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var currentCycle int = 1
	var x int = 1
	var register = make(map[int]int)
	register[1] = 1

	for _, line := range lines {
		if len(line) == 0 {
			break
		}

		fmt.Println(line)

		tokens := strings.Split(line, " ")
		if tokens[0] == "noop" {
			currentCycle++
			register[currentCycle] = x
		} else if tokens[0] == "addx" {
			amount, err := strconv.Atoi(tokens[1])
			check(err)

			currentCycle++
			register[currentCycle] = x

			currentCycle++
			x += amount
			register[currentCycle] = x
		} else {
			panic(fmt.Sprintf("Unknown instruction %s", tokens))
		}
	}

	fmt.Println(register)

	// Part 1
	var signalStrength int = register[20] * 20
	for cycle := 60; cycle <= currentCycle; cycle += 40 {
		signalStrength += cycle * register[cycle]
	}

	fmt.Printf("Signal strength is %d\n", signalStrength)

	// Part 2
	for row := 0; row < 6; row++ {
		for col := 0; col < 40; col++ {
			cycle := (row * 40) + 1 + col
			position := register[cycle]
			// fmt.Printf("cycle: %d, X: %d\n", cycle, position)
			if col >= position-1 && col <= position+1 {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}

		fmt.Println()
	}
}
