package main

import (
	"container/ring"
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

func PrintRing(ring *ring.Ring) {
	var i = 0
	ring.Do(func(p any) {
		fmt.Printf("%d: %d\n", i, p.(int64))
		i++
	})
}

func Shift(r *ring.Ring, n int64, ringSize int) {
	if n == 0 {
		return
	}

	var normalized int = int(n % int64(ringSize-1))

	var start *ring.Ring = r.Prev()
	var removed = start.Unlink(1)
	var target = start.Move(normalized)
	target.Link(removed)
}

func main() {
	// Part 1
	// var decryptionKey int64 = 1
	// var numIterations int = 1

	// Part 2
	var decryptionKey int64 = 811589153
	var numIterations int = 10

	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	var numbers []int64
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		val, err := strconv.Atoi(line)
		check(err)

		numbers = append(numbers, int64(val)*decryptionKey)
	}

	fmt.Printf("%d numbers in the list\n", len(numbers))

	var pointers []*ring.Ring
	var zero *ring.Ring

	buffer := ring.New(len(numbers))
	for _, val := range numbers {
		buffer.Value = val
		if val == 0 {
			zero = buffer
		}
		pointers = append(pointers, buffer)
		buffer = buffer.Next()
	}

	for mixIter := 0; mixIter < numIterations; mixIter++ {
		fmt.Printf("Mix iteration: %d\n", mixIter+1)

		for i, ptr := range pointers {
			var shiftAmount = ptr.Value.(int64)
			Shift(ptr, shiftAmount, len(numbers))

			if shiftAmount != numbers[i] {
				panic(fmt.Sprintf("Unexpected ptr value at index %d\n", i))
			}
		}
	}

	var sum int64 = 0
	c := zero.Move(1000)
	fmt.Printf("1000 after zero is %d\n", c.Value)
	sum += c.Value.(int64)
	c = c.Move(1000)
	fmt.Printf("2000 after zero is %d\n", c.Value)
	sum += c.Value.(int64)
	c = c.Move(1000)
	fmt.Printf("3000 after zero is %d\n", c.Value)
	sum += c.Value.(int64)

	fmt.Printf("Result is: %d\n", sum)
}
