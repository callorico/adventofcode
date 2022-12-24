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
	items        []uint64
	operation    func(x uint64) uint64
	mod          uint64
	test         func(x uint64) int
	inspectCount uint64
}

func main() {

	// No energy to bother trying to parse this
	// dat, err := os.ReadFile("input")
	// check(err)
	// lines := strings.Split(string(dat), "\n")

	// Sample
	// monkeys := []Monkey{
	// 	// Monkey 0
	// 	Monkey{
	// 		items: []uint64{79, 98},
	// 		operation: func(x uint64) uint64 {
	// 			return x * 19
	// 		},
	// 		mod: 23,
	// 		test: func(x uint64) int {
	// 			if x%23 == 0 {
	// 				return 2
	// 			} else {
	// 				return 3
	// 			}
	// 		},
	// 	},
	// 	// Monkey 1
	// 	Monkey{
	// 		items: []uint64{54, 65, 75, 74},
	// 		operation: func(x uint64) uint64 {
	// 			return x + 6
	// 		},
	// 		mod: 19,
	// 		test: func(x uint64) int {
	// 			if x%19 == 0 {
	// 				return 2
	// 			} else {
	// 				return 0
	// 			}
	// 		},
	// 	},
	// 	// Monkey 2
	// 	Monkey{
	// 		items: []uint64{79, 60, 97},
	// 		operation: func(x uint64) uint64 {
	// 			return x * x
	// 		},
	// 		mod: 13,
	// 		test: func(x uint64) int {
	// 			if x%13 == 0 {
	// 				return 1
	// 			} else {
	// 				return 3
	// 			}
	// 		},
	// 	},
	// 	// Monkey 3
	// 	Monkey{
	// 		items: []uint64{74},
	// 		operation: func(x uint64) uint64 {
	// 			return x + 3
	// 		},
	// 		mod: 17,
	// 		test: func(x uint64) int {
	// 			if x%17 == 0 {
	// 				return 0
	// 			} else {
	// 				return 1
	// 			}
	// 		},
	// 	},
	// }

	monkeys := []Monkey{
		// Monkey 0
		Monkey{
			items: []uint64{85, 79, 63, 72},
			operation: func(x uint64) uint64 {
				return x * 17
			},
			mod: 2,
			test: func(x uint64) int {
				if x%2 == 0 {
					return 2
				} else {
					return 6
				}
			},
		},
		// Monkey 1
		Monkey{
			items: []uint64{53, 94, 65, 81, 93, 73, 57, 92},
			operation: func(x uint64) uint64 {
				return x * x
			},
			mod: 7,
			test: func(x uint64) int {
				if x%7 == 0 {
					return 0
				} else {
					return 2
				}
			},
		},
		// Monkey 2
		Monkey{
			items: []uint64{62, 63},
			operation: func(x uint64) uint64 {
				return x + 7
			},
			mod: 13,
			test: func(x uint64) int {
				if x%13 == 0 {
					return 7
				} else {
					return 6
				}
			},
		},
		// Monkey 3
		Monkey{
			items: []uint64{57, 92, 56},
			operation: func(x uint64) uint64 {
				return x + 4
			},
			mod: 5,
			test: func(x uint64) int {
				if x%5 == 0 {
					return 4
				} else {
					return 5
				}
			},
		},
		// Monkey 4
		Monkey{
			items: []uint64{67},
			operation: func(x uint64) uint64 {
				return x + 5
			},
			mod: 3,
			test: func(x uint64) int {
				if x%3 == 0 {
					return 1
				} else {
					return 5
				}
			},
		},
		// Monkey 5
		Monkey{
			items: []uint64{85, 56, 66, 72, 57, 99},
			operation: func(x uint64) uint64 {
				return x + 6
			},
			mod: 19,
			test: func(x uint64) int {
				if x%19 == 0 {
					return 1
				} else {
					return 0
				}
			},
		},
		// Monkey 6
		Monkey{
			items: []uint64{86, 65, 98, 97, 69},
			operation: func(x uint64) uint64 {
				return x * 13
			},
			mod: 11,
			test: func(x uint64) int {
				if x%11 == 0 {
					return 3
				} else {
					return 7
				}
			},
		},
		// Monkey 7
		Monkey{
			items: []uint64{87, 68, 92, 66, 91, 50, 68},
			operation: func(x uint64) uint64 {
				return x + 2
			},
			mod: 17,
			test: func(x uint64) int {
				if x%17 == 0 {
					return 4
				} else {
					return 3
				}
			},
		},
	}

	var primeDivisor uint64 = 1
	for _, monkey := range monkeys {
		primeDivisor *= monkey.mod
	}

	for round := 0; round < 10000; round++ {
		// fmt.Printf("----- Round %d ------\n", round+1)
		for i := 0; i < len(monkeys); i++ {
			// fmt.Printf("Monkey %d:\n", i)
			for _, item := range monkeys[i].items {
				// fmt.Printf("  Monkey inspects an item with a worry level of %d,\n", item)
				worryLevel := monkeys[i].operation(item)
				// fmt.Printf("    New worry level is %d\n", worryLevel)
				// worryLevel = worryLevel / 3
				// fmt.Printf("    Monkey gets bored with item. Worry level is divided by 3 to %d\n", worryLevel)
				destinationMonkey := monkeys[i].test(worryLevel)

				worryLevel = worryLevel % primeDivisor
				// fmt.Printf("    Item with worry level %d is thrown to monkey %d\n", worryLevel, destinationMonkey)
				monkeys[destinationMonkey].items = append(monkeys[destinationMonkey].items, worryLevel)
			}

			monkeys[i].inspectCount += uint64(len(monkeys[i].items))
			monkeys[i].items = nil
		}

		// fmt.Printf("After round %d, the monkeys are holding items with these worry levels:\n", round+1)
		// for i, monkey := range monkeys {
		// 	fmt.Printf("Monkey %d: %v\n", i, monkey.items)
		// }
		fmt.Printf("== After round %d ==\n", round+1)
		for i, monkey := range monkeys {
			// fmt.Printf("Monkey %d items %v\n", i, monkey.items)
			fmt.Printf("Monkey %d inspected items %d times\n", i, monkey.inspectCount)
		}
	}

	// for i, monkey := range monkeys {
	// 	fmt.Printf("Monkey %d inspected items %d times.\n", i, monkey.inspectCount)
	// }

	sort.Slice(monkeys, func(i int, j int) bool { return monkeys[i].inspectCount > monkeys[j].inspectCount })
	monkeyBusiness := monkeys[0].inspectCount * monkeys[1].inspectCount
	fmt.Printf("Monkey business: %d\n", monkeyBusiness)
}
