package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type FileSystemObject struct {
	name     string
	size     int
	parent   *FileSystemObject
	children []*FileSystemObject
}

func findChild(children []*FileSystemObject, name string) *FileSystemObject {
	for _, child := range children {
		if child.name == name {
			return child
		}
	}

	return nil
}

func calcSizes(node *FileSystemObject) int {
	if node.size != 0 {
		return node.size
	}

	var total int = 0
	for _, child := range node.children {
		total += calcSizes(child)
	}

	node.size = total
	return total
}

func find(node *FileSystemObject, predicate func(n *FileSystemObject) bool) []*FileSystemObject {
	var results []*FileSystemObject
	if predicate(node) {
		results = append(results, node)
	}

	for _, child := range node.children {
		results = append(results, find(child, predicate)...)
	}

	return results

}

func findBigDirs(node *FileSystemObject, minSize int) []*FileSystemObject {
	var results []*FileSystemObject
	if node.size >= minSize && node.children != nil {
		results = append(results, node)
	}

	for _, child := range node.children {
		results = append(results, findBigDirs(child, minSize)...)
	}

	return results
}

func main() {
	dat, err := os.ReadFile("input")
	check(err)
	lines := strings.Split(string(dat), "\n")
	fs := FileSystemObject{name: "/"}
	var current *FileSystemObject = &fs

	for i := 0; i < len(lines); i++ {
		line := lines[i]
		if len(line) == 0 {
			break
		}

		tokens := strings.Split(line, " ")
		fmt.Println(tokens)
		if tokens[0] != "$" {
			panic("Did not slurp up output from previous command")
		}

		command := tokens[1]

		if command == "cd" {
			dirname := tokens[2]
			if dirname == ".." {
				// Go up
				current = current.parent
			} else if dirname == "/" {
				// Back to root
				current = &fs
			} else {
				// Go down (Find child with dirname)
				child := findChild(current.children, dirname)
				if child == nil {
					panic("Tried to navigate into child that wasn't previously returned by an ls")
				}
				current = child
			}
		} else if command == "ls" {
			var j int
			for j = i + 1; j < len(lines); j++ {
				if len(lines[j]) == 0 {
					break
				}

				output := strings.Split(lines[j], " ")
				fmt.Println(output)
				if output[0] == "$" {
					// Reached next command. End of previous command
					break
				}

				child := findChild(current.children, output[1])
				if child == nil {
					child = &FileSystemObject{name: output[1], parent: current}
					current.children = append(current.children, child)
				}

				if output[0] == "dir" {
					// Nothing else to do here
				} else {
					size, err := strconv.Atoi(output[0])
					check(err)
					child.size = size
				}
			}

			// Move pointer back to the command
			i = j - 1
		} else {
			panic(fmt.Sprintf("Unknown command parsed %s", command))
		}
	}

	// Find all dirs under a certain size (build cache along the way)
	calcSizes(&fs)
	fmt.Println(fs)

	// Part 1
	var total int = 0
	for _, result := range find(&fs, func(n *FileSystemObject) bool { return n.size <= 100000 && n.children != nil }) {
		fmt.Printf("Small dir match %s\n", result.name)
		total += result.size
	}

	fmt.Printf("Sum is %d\n", total)

	// Part 2
	var unusedSpace int = 70000000 - fs.size
	var spaceNeeded int = 30000000 - unusedSpace
	fmt.Printf("Unused space: %d, Need to free up %d\n", unusedSpace, spaceNeeded)

	var matcher = func(n *FileSystemObject) bool {
		return n.size >= 3956976 && n.children != nil
	}

	var matches = find(&fs, matcher)
	sort.Slice(matches, func(i int, j int) bool {
		return matches[i].size < matches[j].size
	})

	fmt.Printf("Smallest dir size: %d\n", matches[0].size)
}
