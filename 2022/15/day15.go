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

type Range struct {
	min int
	max int
}

type Sensor struct {
	position Coordinate
	distance int
}

func Overlaps(a *Range, b *Range) bool {
	return !(a.max < b.min || b.max < a.min)
}

func Merge(a *Range, b *Range) *Range {
	return &Range{min: min(a.min, b.min), max: max(a.max, b.max)}
}

func ParseCoordinate(rawX, rawY string) Coordinate {
	x, err := strconv.Atoi(rawX)
	check(err)
	y, err := strconv.Atoi(rawY)
	check(err)

	return Coordinate{x: x, y: y}
}

func min(a int, b int) int {
	if a < b {
		return a
	} else {
		return b
	}
}

func max(a int, b int) int {
	if a > b {
		return a
	} else {
		return b
	}
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

func BeaconPosition(sensors []Sensor, targetRow int, maxPos int) int {
	var ranges []*Range

	for _, sensor := range sensors {
		yDelta := abs(targetRow - sensor.position.y)
		maxXDelta := sensor.distance - yDelta
		if maxXDelta > 0 {
			var testMin = max(0, sensor.position.x-maxXDelta)
			var testMax = min(maxPos, sensor.position.x+maxXDelta)
			var r = &Range{min: testMin, max: testMax}
			ranges = append(ranges, r)
		}
	}

	// Merge overlapping ranges until we either have 1 or 2 ranges left
	for true {
		var newRanges []*Range

		var r = ranges[0]
		for i := 1; i < len(ranges); i++ {
			if Overlaps(r, ranges[i]) {
				r = Merge(r, ranges[i])
			} else {
				newRanges = append(newRanges, ranges[i])
			}
		}

		newRanges = append(newRanges, r)
		var reduced bool = len(newRanges) < len(ranges)
		ranges = newRanges
		if !reduced {
			break
		}
	}

	if len(ranges) != 1 && len(ranges) != 2 {
		panic("Should be either 0 or 1 possible locations for the sensor in this row")
	}

	if len(ranges) == 1 {
		return -1
	}

	// Find the hole in the 2 ranges
	fmt.Printf("%v %v\n", ranges[0], ranges[1])
	if ranges[0].max < ranges[1].min {
		return ranges[0].max + 1
	} else {
		return ranges[1].max + 1
	}
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")

	var sensorOutput = regexp.MustCompile(`Sensor at x=([^,]+), y=([^:]+): closest beacon is at x=([^,]+), y=(.+)`)
	var sensors []Sensor
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		matches := sensorOutput.FindStringSubmatch(line)

		// fmt.Println(matches)
		sensor := ParseCoordinate(matches[1], matches[2])
		closestBeacon := ParseCoordinate(matches[3], matches[4])
		distance := ManhattanDistance(&sensor, &closestBeacon)
		fmt.Printf("%v %v %d\n", sensor, closestBeacon, distance)

		sensors = append(sensors, Sensor{position: sensor, distance: distance})
	}

	var maxPos = 4000000
	var x = -1
	var targetRow int
	for targetRow = 0; targetRow <= maxPos; targetRow++ {
		if targetRow%1000000 == 0 {
			fmt.Printf("Checked %d rows\n", targetRow)
		}

		x = BeaconPosition(sensors, targetRow, maxPos)
		if x >= 0 {
			break
		}
	}

	tuningFrequency := x*maxPos + targetRow
	fmt.Printf("Found beacon position %d, %d: %d\n", x, targetRow, tuningFrequency)
}
