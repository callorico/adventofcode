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

func reverse(a []string) {
	n := len(a)
	for i := 0; i < n/2; i++ {
		a[i], a[n-i-1] = a[n-i-1], a[i]
	}
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var crates [9][]string

	i := 0
	for i = 0; i < len(lines); i++ {
		if len(lines[i]) == 0 {
			break
		}

		for crateIndex := 0; crateIndex < len(crates); crateIndex++ {
			lineIndex := 1 + crateIndex*4
			value := string(lines[i][lineIndex])
			if value != " " && lines[i][lineIndex-1] == '[' {
				crates[crateIndex] = append(crates[crateIndex], value)
			}
		}
	}

	for _, stack := range crates {
		reverse(stack)
	}

	fmt.Println(crates)

	// Parse each of the moves now
	for j := i; j < len(lines); j++ {
		if len(lines[j]) == 0 {
			continue
		}
		move := strings.Split(lines[j], " ")
		amount, err := strconv.Atoi(move[1])
		check(err)
		source, err := strconv.Atoi(move[3])
		source--
		check(err)
		dest, err := strconv.Atoi(move[5])
		dest--

		fmt.Printf("Amount: %d, from: %d, to: %d\n", amount, source, dest)

		// Part 1
		// for z := 0; z < amount; z++ {
		// 	// Pop last item from source and push onto dest
		// 	n := len(crates[source]) - 1
		// 	if n < 0 {
		// 		panic("Not enough crates left on the source")
		// 	}
		// 	crates[dest] = append(crates[dest], crates[source][n])
		// 	crates[source] = crates[source][:n]
		// }

		// Part 2
		last := len(crates[source])
		cratesToMove := crates[source][last-amount : last]
		crates[dest] = append(crates[dest], cratesToMove...)
		crates[source] = crates[source][:last-amount]

		fmt.Println(crates)
	}

	for _, stack := range crates {
		fmt.Print(stack[len(stack)-1])
	}
	fmt.Println()
}
