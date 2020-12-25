use std::fs;
use std::env;
use std::collections::hash_set::HashSet;
use std::collections::hash_map::HashMap;

fn neighbors(dir_deltas: &HashMap<&str, (i32, i32)>, cell: (i32, i32)) -> Vec<(i32, i32)> {
    let mut adjacent: Vec<(i32, i32)> = Vec::new();
    for (dx, dy) in dir_deltas.values() {
        adjacent.push((cell.0 + dx, cell.1 + dy));
    }

    return adjacent;
}

fn next_step(dir_deltas: &HashMap<&str, (i32, i32)>, black_tiles: &HashSet<(i32, i32)>) -> HashSet<(i32, i32)> {
    let mut all_neighbors: HashSet<(i32, i32)> = black_tiles.clone();
    for t in black_tiles.iter() {
        all_neighbors.extend(neighbors(dir_deltas, *t));
    }

    let mut new_black_tiles: HashSet<(i32, i32)> = HashSet::new();

    for t in all_neighbors.iter() {
        let num_black_neighbors: usize = neighbors(dir_deltas, *t)
            .iter()
            .filter(|n| black_tiles.contains(*n))
            .count();

        let is_black = black_tiles.contains(t);
        let is_still_black: bool = match (is_black, num_black_neighbors) {
            (true, 0) => false,
            (true, 1) => true,
            (true, 2) => true,
            (true, _) => false,
            (false, 2) => true,
            _ => false
        };

        if is_still_black {
            new_black_tiles.insert(*t);
        }
    }

    return new_black_tiles;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines = data.split("\n").filter(|x| !x.is_empty());

    let mut black_tiles: HashSet<(i32, i32)> = HashSet::new();
    let mut dir_deltas: HashMap<&str, (i32, i32)> = HashMap::new();
    dir_deltas.insert("nw", (-1, -2));
    dir_deltas.insert("ne", (1, -2));
    dir_deltas.insert("e", (2, 0));
    dir_deltas.insert("w", (-2, 0));
    dir_deltas.insert("sw", (-1, 2));
    dir_deltas.insert("se", (1, 2));

    for line in lines {
        let mut directions: Vec<String> = Vec::new();

        let mut it = line.chars();
        while let Some(c) = it.next() {
            let dir: String = match c {
                'n' | 's' => format!("{}{}", c, it.next().unwrap()),
                x => x.to_string()
            };

            directions.push(dir);
        }

        println!("{:?}", directions);

        let (mut x, mut y) = (0, 0);
        for d in directions.iter() {
            let (dx, dy) = dir_deltas[d.as_str()];
            x += dx;
            y += dy;
        }

        if black_tiles.contains(&(x, y)) {
            black_tiles.remove(&(x, y));
        } else {
            black_tiles.insert((x, y));
        }
    }

    println!("Black tiles: {:?}", black_tiles);
    println!("Total black tiles: {}", black_tiles.len());

    for day in 1..=100 {
        black_tiles = next_step(&dir_deltas, &black_tiles);
        println!("Day {}: {}", day, black_tiles.len());
    }
}
