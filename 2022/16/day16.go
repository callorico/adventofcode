package main

import (
	"container/heap"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Valve struct {
	id       string
	flowRate int
	paths    []string
}

type State struct {
	currentValve string
	timeLeft     int
	closedValves []string
}

// An Item is something we manage in a priority queue.
type Item struct {
	value    State // The value of the item; arbitrary.
	priority int   // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
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
func (pq *PriorityQueue) update(item *Item, value State, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

func calculateMinDistances(current *Valve, dist int, valves map[string]*Valve, distances *map[string]int) {
	for _, path := range current.paths {
		bestSoFar, ok := (*distances)[path]
		if !ok || bestSoFar > dist+1 {
			(*distances)[path] = dist + 1
			calculateMinDistances(valves[path], dist+1, valves, distances)
		}
	}
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var valveData = regexp.MustCompile(`Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)`)

	var valves = make(map[string]*Valve)
	var positiveFlowRates []string
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		matches := valveData.FindStringSubmatch(line)
		valveID := matches[1]
		flowRate, ok := strconv.Atoi(matches[2])
		check(ok)
		paths := strings.Split(matches[3], ", ")
		valves[valveID] = &Valve{id: valveID, flowRate: flowRate, paths: paths}
		if flowRate > 0 {
			positiveFlowRates = append(positiveFlowRates, valveID)
		}

		fmt.Printf("%s, %d, %v\n", valveID, flowRate, paths)
	}

	fmt.Printf("Number of positive flow rate valves: %d\n", len(positiveFlowRates))
	var allDistances = make(map[string]map[string]int)
	for _, valve := range valves {
		var distances = make(map[string]int)
		calculateMinDistances(valve, 0, valves, &distances)
		allDistances[valve.id] = distances
	}

	pq := make(PriorityQueue, 0)
	heap.Init(&pq)

	heap.Push(&pq, &Item{
		value:    State{currentValve: "AA", timeLeft: 30, closedValves: positiveFlowRates},
		priority: 0,
	})

	var bestPressureSoFar int = 0
	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*Item)
		fmt.Printf("%v\n", item)

		for i, nextValve := range item.value.closedValves {
			// Calculate time remaining after moving to a valve and turning it on.
			remainingTime := item.value.timeLeft - allDistances[item.value.currentValve][nextValve] - 1
			if remainingTime > 0 {
				var remainingValves []string
				remainingValves = append(remainingValves, item.value.closedValves[:i]...)
				remainingValves = append(remainingValves, item.value.closedValves[i+1:]...)

				totalPressure := item.priority + remainingTime*valves[nextValve].flowRate
				heap.Push(&pq, &Item{
					value: State{
						currentValve: nextValve,
						timeLeft:     remainingTime,
						closedValves: remainingValves},
					priority: totalPressure,
				})
			}
		}

		if item.priority > bestPressureSoFar {
			bestPressureSoFar = item.priority
		}
	}

	fmt.Printf("Max pressure released: %d\n", bestPressureSoFar)
}
