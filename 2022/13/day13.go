package main

import (
	"bytes"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type Packet struct {
	value    int
	children []*Packet
}

func MakeIntegerPacket(value int) *Packet {
	return &Packet{value: value}
}

func MakeListPacket() *Packet {
	return &Packet{value: -1}
}

func IsInteger(packet *Packet) bool {
	return packet.value != -1
}

func IntegerToList(packet *Packet) *Packet {
	if !IsInteger(packet) {
		panic("Was not passed an integer")
	}

	var wrapper = MakeListPacket()
	wrapper.children = append(wrapper.children, packet)
	return wrapper
}

func ToString(packet *Packet) string {
	var b bytes.Buffer

	if IsInteger(packet) {
		b.WriteString(fmt.Sprintf("%d", packet.value))
	} else {
		b.WriteRune('[')
		for _, child := range packet.children {
			b.WriteString(ToString(child))
			b.WriteRune(',')
		}
		b.WriteRune(']')
	}

	return b.String()
}

func min(a, b int) int {
	if a < b {
		return a
	}

	return b
}

// Returns 0 if the left == right
// < 0 if the left < right (in the right order)
// > 0 if left > right (not in the right order)
func Compare(left *Packet, right *Packet) int {
	if IsInteger(left) && IsInteger(right) {
		// Both are integers
		return left.value - right.value
	} else if !IsInteger(left) && !IsInteger(right) {
		// Both are lists
		length := min(len(left.children), len(right.children))
		for i := 0; i < length; i++ {
			var cmp int = Compare(left.children[i], right.children[i])
			if cmp != 0 {
				return cmp
			}
		}

		return len(left.children) - len(right.children)
	} else {
		if IsInteger(left) {
			// L is integer
			// R is list
			return Compare(IntegerToList(left), right)
		} else {
			// L is list
			// R is integer
			return Compare(left, IntegerToList(right))
		}
	}
}

func ParsePacket(value string) *Packet {
	var runes []rune = []rune(value)
	var index = 0
	var packet = ParsePacketHelper(runes, &index)

	if index != len(runes) {
		panic("Parsing failure detected")
	}

	return packet
}
func ParsePacketHelper(runes []rune, index *int) *Packet {
	if runes[*index] != '[' {
		panic(fmt.Sprintf("Should have been passed a list. Received: %s", string(runes)))
	}

	// Eat the [
	*index++

	var packet = MakeListPacket()

	for runes[*index] != ']' {
		if runes[*index] == '[' {
			packet.children = append(packet.children, ParsePacketHelper(runes, index))
		} else if unicode.IsDigit(runes[*index]) {
			end := *index
			for unicode.IsDigit(runes[end]) {
				end += 1
			}

			value, ok := strconv.Atoi(string(runes[*index:end]))
			check(ok)
			packet.children = append(packet.children, MakeIntegerPacket(value))
			*index = end
		} else {
			*index += 1
		}
	}

	// Eat the closing bracket for this list
	*index++

	return packet
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)

	lines := strings.Split(string(dat), "\n")
	packetNumber := 1
	inOrderSum := 0
	i := 0
	for i < len(lines) {
		if len(lines[i]) == 0 {
			i += 1
			continue
		}

		fmt.Printf("== Pair %d ==\n", packetNumber)

		var packet1 = ParsePacket(lines[i])
		fmt.Println(ToString(packet1))
		var packet2 = ParsePacket(lines[i+1])
		fmt.Println(ToString(packet1))

		if Compare(packet1, packet2) < 0 {
			fmt.Printf("Pair %d are in the right order\n", packetNumber)
			inOrderSum += packetNumber
		}

		i += 2
		packetNumber += 1
	}

	// TODO: Sum of the pair indices that are in order
	fmt.Printf("In order pair sum %d\n", inOrderSum)
}
