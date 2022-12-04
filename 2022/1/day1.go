package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func part1() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	max := 0
	current := 0
	for _, line := range lines {
		if len(line) == 0 {
			if current > max {
				max = current
			}
			current = 0
		} else {
			calories, err := strconv.Atoi(line)
			check(err)
			current += calories
		}
	}

	fmt.Printf("Max calories %d", max)
}

func part2() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var calories []int
	current := 0
	for _, line := range lines {
		if len(line) == 0 {
			calories = append(calories, current)
			current = 0
		} else {
			calories, err := strconv.Atoi(line)
			check(err)
			current += calories
		}
	}

	sort.Sort(sort.Reverse(sort.IntSlice(calories)))
	fmt.Printf("%v\n", calories)

	top3 := calories[0] + calories[1] + calories[2]
	fmt.Printf("Top 3 calories %d\n", top3)
}

func main() {
	part2()
}
