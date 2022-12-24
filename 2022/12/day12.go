package main

import (
	"container/heap"
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Cell struct {
	row int
	col int
}

type Item struct {
	value    Cell
	priority int
	index    int
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority > pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value Cell, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	var grid [][]int
	var start Cell
	var end Cell
	lines := strings.Split(string(dat), "\n")
	for _, line := range lines {
		if len(line) == 0 {
			break
		}
		var row []int
		for col, ch := range line {
			var val int
			if ch == 'S' {
				start = Cell{row: len(grid), col: col}
				val = 0
			} else if ch == 'E' {
				end = Cell{row: len(grid), col: col}
				val = 26
			} else {
				val = int(ch) - int('a')
			}

			row = append(row, val)
		}

		grid = append(grid, row)
	}

	var minSteps = make(map[Cell]int)
	minSteps[start] = 0

	var offsets = []Cell{
		Cell{row: -1, col: 0},
		Cell{row: 1, col: 0},
		Cell{row: 0, col: -1},
		Cell{row: 0, col: 1},
	}

	var cells = make(PriorityQueue, 0)
	heap.Init(&cells)
	item := &Item{
		value:    start,
		priority: 0,
	}
	heap.Push(&cells, item)

	for cells.Len() > 0 {
		// Pop best cell to consider next
		item := heap.Pop(&cells).(*Item)
		current := item.value
		fmt.Printf("Looking at %v (min dist to here is currently %d)\n", current, minSteps[current])

		var currentElevation = grid[current.row][current.col]
		for _, offset := range offsets {
			var newPos = Cell{row: current.row + offset.row, col: current.col + offset.col}
			// Check if we are off the edge of the grid
			if newPos.row < 0 || newPos.row >= len(grid) || newPos.col < 0 || newPos.col >= len(grid[0]) {
				continue
			}

			// Check if the move is legal
			if grid[newPos.row][newPos.col] > currentElevation+1 {
				continue
			}

			// Check if a shorter path has already been found to the destination
			val, ok := minSteps[newPos]
			if ok && item.priority+1 >= val {
				continue
			}

			// Good to go
			minSteps[newPos] = item.priority + 1

			var newItem = &Item{
				value:    newPos,
				priority: item.priority + 1,
			}
			heap.Push(&cells, newItem)
		}
	}

	fmt.Printf("Min steps from %v to %v is %d\n", start, end, minSteps[end])
}
