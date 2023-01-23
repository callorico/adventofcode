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
		fmt.Printf("%d: %d\n", i, p.(int))
		i++
	})
}

func Shift(r *ring.Ring, n int, ringSize int) {
	if n == 0 {
		return
	}

	var start *ring.Ring = r.Prev()
	var removed = start.Unlink(1)
	var target = start.Move(n)
	target.Link(removed)
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	var numbers []int
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		val, err := strconv.Atoi(line)
		check(err)

		numbers = append(numbers, val)
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

	for i, ptr := range pointers {
		var shiftAmount = ptr.Value.(int)
		Shift(ptr, shiftAmount, len(numbers))

		if shiftAmount != numbers[i] {
			panic(fmt.Sprintf("Unexpected ptr value at index %d\n", i))
		}
	}

	var sum = 0
	c := zero.Move(1000)
	fmt.Printf("1000 after zero is %d\n", c.Value)
	sum += c.Value.(int)
	c = c.Move(1000)
	fmt.Printf("2000 after zero is %d\n", c.Value)
	sum += c.Value.(int)
	c = c.Move(1000)
	fmt.Printf("3000 after zero is %d\n", c.Value)
	sum += c.Value.(int)

	fmt.Printf("Result is: %d\n", sum)
}
