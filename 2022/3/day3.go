package main

import (
	"fmt"
	"os"
	"strings"
	"unicode"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func part1(lines []string) {
	priorities := 0

	for _, line := range lines {
		itemCount := len(line)
		if itemCount == 0 {
			continue
		}
		fmt.Println(line)

		bag := make(map[byte]bool)
		perCompartmentCount := itemCount / 2
		for i := 0; i < perCompartmentCount; i++ {
			bag[line[i]] = true
		}

		for i := perCompartmentCount; i < itemCount; i++ {
			if bag[line[i]] {
				var priority int
				if unicode.IsUpper(rune(line[i])) {
					priority = int(line[i]-'A') + 27

				} else {
					priority = int(line[i]-'a') + 1
				}

				fmt.Printf("Found char %c in bag (%d)\n", line[i], priority)
				priorities += priority
				break
			}
		}
	}

	fmt.Printf("Priority sum is %d\n", priorities)
}

func intersect(bag1 map[byte]bool, bag2 map[byte]bool) map[byte]bool {
	bagResult := make(map[byte]bool)
	for item, _ := range bag1 {
		if bag2[item] {
			bagResult[item] = true
		}
	}

	return bagResult
}

func parseBag(line string) map[byte]bool {
	bag := make(map[byte]bool)
	for i := 0; i < len(line); i++ {
		bag[line[i]] = true
	}

	return bag
}

func part2(lines []string) {
	priorities := 0

	for i := 0; i < len(lines); i += 3 {
		itemCount := len(lines[i])
		if itemCount == 0 {
			continue
		}

		bag := parseBag(lines[i])
		bag = intersect(bag, parseBag(lines[i+1]))
		bag = intersect(bag, parseBag(lines[i+2]))
		fmt.Println(bag)

		if len(bag) != 1 {
			panic("Should be only 1 item that matches")
		}

		for key, _ := range bag {
			var priority int
			if unicode.IsUpper(rune(key)) {
				priority = int(key-'A') + 27

			} else {
				priority = int(key-'a') + 1
			}

			fmt.Printf("Found char %c in 3-bag (%d)\n", key, priority)
			priorities += priority
			break
		}
	}

	fmt.Printf("Priority sum is %d\n", priorities)
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	//part1(lines)
	part2(lines)
}
