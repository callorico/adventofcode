use std::fs;
use std::env;
use std::collections::hash_set::HashSet;
use std::collections::hash_map::HashMap;

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
}
