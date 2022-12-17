package main

import (
	"fmt"
	"sort"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Monkey struct {
	items        []int
	operation    func(x int) int
	test         func(x int) int
	inspectCount int
}

func main() {

	// No energy to bother trying to parse this
	// dat, err := os.ReadFile("input")
	// check(err)
	// lines := strings.Split(string(dat), "\n")

	monkeys := []Monkey{
		// Monkey 0
		Monkey{
			items: []int{85, 79, 63, 72},
			operation: func(x int) int {
				return x * 17
			},
			test: func(x int) int {
				if x%2 == 0 {
					return 2
				} else {
					return 6
				}
			},
		},
		// Monkey 1
		Monkey{
			items: []int{53, 94, 65, 81, 93, 73, 57, 92},
			operation: func(x int) int {
				return x * x
			},
			test: func(x int) int {
				if x%7 == 0 {
					return 0
				} else {
					return 2
				}
			},
		},
		// Monkey 2
		Monkey{
			items: []int{62, 63},
			operation: func(x int) int {
				return x + 7
			},
			test: func(x int) int {
				if x%13 == 0 {
					return 7
				} else {
					return 6
				}
			},
		},
		// Monkey 3
		Monkey{
			items: []int{57, 92, 56},
			operation: func(x int) int {
				return x + 4
			},
			test: func(x int) int {
				if x%5 == 0 {
					return 4
				} else {
					return 5
				}
			},
		},
		// Monkey 4
		Monkey{
			items: []int{67},
			operation: func(x int) int {
				return x + 5
			},
			test: func(x int) int {
				if x%3 == 0 {
					return 1
				} else {
					return 5
				}
			},
		},
		// Monkey 5
		Monkey{
			items: []int{85, 56, 66, 72, 57, 99},
			operation: func(x int) int {
				return x + 6
			},
			test: func(x int) int {
				if x%19 == 0 {
					return 1
				} else {
					return 0
				}
			},
		},
		// Monkey 6
		Monkey{
			items: []int{86, 65, 98, 97, 69},
			operation: func(x int) int {
				return x * 13
			},
			test: func(x int) int {
				if x%11 == 0 {
					return 3
				} else {
					return 7
				}
			},
		},
		// Monkey 7
		Monkey{
			items: []int{87, 68, 92, 66, 91, 50, 68},
			operation: func(x int) int {
				return x + 2
			},
			test: func(x int) int {
				if x%17 == 0 {
					return 4
				} else {
					return 3
				}
			},
		},
	}

	for round := 0; round < 20; round++ {
		fmt.Printf("----- Round %d ------\n", round+1)
		for i := 0; i < len(monkeys); i++ {
			fmt.Printf("Monkey %d:\n", i)
			for _, item := range monkeys[i].items {
				fmt.Printf("  Monkey inspects an item with a worry level of %d,\n", item)
				worryLevel := monkeys[i].operation(item)
				fmt.Printf("    New worry level is %d\n", worryLevel)
				worryLevel = worryLevel / 3
				fmt.Printf("    Monkey gets bored with item. Worry level is divided by 3 to %d\n", worryLevel)
				destinationMonkey := monkeys[i].test(worryLevel)
				fmt.Printf("    Item with worry level %d is thrown to monkey %d\n", worryLevel, destinationMonkey)
				monkeys[destinationMonkey].items = append(monkeys[destinationMonkey].items, worryLevel)
			}

			monkeys[i].inspectCount += len(monkeys[i].items)
			monkeys[i].items = nil
		}

		fmt.Printf("After round %d, the monkeys are holding items with these worry levels:\n", round+1)
		for i, monkey := range monkeys {
			fmt.Printf("Monkey %d: %v\n", i, monkey.items)
		}
	}

	for i, monkey := range monkeys {
		fmt.Printf("Monkey %d inspected items %d times.\n", i, monkey.inspectCount)
	}

	sort.Slice(monkeys, func(i int, j int) bool { return monkeys[i].inspectCount > monkeys[j].inspectCount })
	monkeyBusiness := monkeys[0].inspectCount * monkeys[1].inspectCount
	fmt.Printf("Monkey business: %d\n", monkeyBusiness)
}
