use std::env;
use std::fs;
use std::collections::hash_map::HashMap;

fn print_space(space: &HashMap<u32, Vec<Vec<char>>>) {
    // Sort z index
    let mut items: Vec<(&u32, &Vec<Vec<char>>)> = space.iter().collect();
    items.sort_by_key(|(z_index, _)| *z_index);

    // Print matrix
    for (z_index, plane) in items {
        println!("z={}", z_index);
        for line in plane {
            println!("{:?}", line);
        }
    }
}

fn cell(space: &HashMap<u32, Vec<Vec<char>>>, x: u32, y: u32, z: u32) -> char {

}

fn count(space: &HashMap<u32, Vec<Vec<char>>>, x: u32, y: u32, z: u32) -> u32 {

}

fn next_step(space: &HashMap<u32, Vec<Vec<char>>>) -> HashMap<u32, Vec<Vec<char>>> {
    // Sort z index
    let mut items: Vec<(&u32, &Vec<Vec<char>>)> = space.iter().collect();
    items.sort_by_key(|(z_index, _)| *z_index);

    let mut next: HashMap<u32, Vec<Vec<char>>> = HashMap::new();
    // for (z_index, plane) in items {

    // }

    return next;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let plane: Vec<Vec<char>> = data
        .split("\n")
        .filter(|s| !s.is_empty())
        .map(|s| s.chars().collect())
        .collect();

    let mut space: HashMap<u32, Vec<Vec<char>>> = HashMap::new();
    space.insert(0, plane);
    print_space(&space);
}
