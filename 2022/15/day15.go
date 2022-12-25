package main

import (
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

type Coordinate struct {
	x int
	y int
}

func ParseCoordinate(rawX, rawY string) Coordinate {
	x, err := strconv.Atoi(rawX)
	check(err)
	y, err := strconv.Atoi(rawY)
	check(err)

	return Coordinate{x: x, y: y}
}

func abs(a int) int {
	if a < 0 {
		return -a
	} else {
		return a
	}
}

func ManhattanDistance(left *Coordinate, right *Coordinate) int {
	return abs(left.x-right.x) + abs(left.y-right.y)
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var sensorOutput = regexp.MustCompile(`Sensor at x=([^,]+), y=([^:]+): closest beacon is at x=([^,]+), y=(.+)`)
	var targetRow int = 2000000
	// var targetRow = 10
	var beacons []Coordinate
	var noBeacon = make(map[int]bool)
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		matches := sensorOutput.FindStringSubmatch(line)

		fmt.Println(matches)
		sensor := ParseCoordinate(matches[1], matches[2])
		closestBeacon := ParseCoordinate(matches[3], matches[4])
		beacons = append(beacons, closestBeacon)
		distance := ManhattanDistance(&sensor, &closestBeacon)
		fmt.Printf("%v %v %d\n", sensor, closestBeacon, distance)

		yDelta := abs(targetRow - sensor.y)
		maxXDelta := distance - yDelta
		if maxXDelta > 0 {
			// fmt.Printf("Finding x coords for fixed y=%d\n", targetRow)
			var testMin = sensor.x - maxXDelta
			// fmt.Printf("(%d,%d) -> %d\n", testMin, targetRow, ManhattanDistance(&Coordinate{x: testMin, y: targetRow}, &sensor))
			var testMax = sensor.x + maxXDelta
			// fmt.Printf("(%d,%d) -> %d\n", testMax, targetRow, ManhattanDistance(&Coordinate{x: testMax, y: targetRow}, &sensor))
			for i := testMin; i <= testMax; i++ {
				noBeacon[i] = true
			}
		}
	}

	for _, beacon := range beacons {
		// fmt.Printf("%d\n", beacon.y)
		if beacon.y == targetRow {
			// fmt.Println("Removing beacon in target row")
			delete(noBeacon, beacon.x)
		}
	}

	fmt.Printf("Positions without a beacon: %d\n", len(noBeacon))
}
