use std::fs;
use std::env;
use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;

#[derive(Debug)]
struct Tile {
    tile_id: u32,
    contents: Vec<String>
}

fn orientations(tile: &Tile) -> Vec<Tile> {
    let mut positions: Vec<Tile> = Vec::new();
    let mut rotated: &Tile = tile;

    // Generate rotations
    for _ in 0..4 {
        let mut rotated_contents: Vec<String> = Vec::new();
        for col in 0..rotated.contents.len() {
            let r: String = rotated.contents
                .iter()
                .rev()
                .map(|s| s.chars().nth(col).unwrap())
                .collect();

            rotated_contents.push(r);
        }
        positions.push(Tile { tile_id: tile.tile_id, contents: rotated_contents });
        rotated = positions.last().unwrap();
    }

    // Flip each of the rotations
    for i in 0..4 {
        let mut flipped_contents: Vec<String> = Vec::new();
        for row in positions[i].contents.iter() {
            let f = row
                .chars()
                .rev()
                .collect();

            flipped_contents.push(f);
        }
        positions.push(Tile { tile_id: tile.tile_id, contents: flipped_contents });
    }

    return positions;
}

fn print_tile(tile: &Tile) {
    println!("Tile {}:", tile.tile_id);
    for line in &tile.contents {
        println!("{}", line);
    }
}

fn solve<'a>(image: &mut Vec<Vec<&'a Tile>>, remaining_tiles: &mut HashSet<u32>, tile_orientations: &'a HashMap<u32, Vec<Tile>>, row_index: usize, col_index: usize, grid_size: usize) -> bool {
    if remaining_tiles.is_empty() {
        return true;
    }

    if image.len() <= row_index {
        image.push(Vec::new());
    }

    let mut possible_tiles: Vec<&Tile> = Vec::new();

    for (tile_id, orientations) in tile_orientations.iter() {
        if remaining_tiles.contains(tile_id) {
            for tile in orientations.iter() {
                // Does tile fit?

                // Find tiles that match constraints for the cell
                if row_index > 0 {
                    let above = image[row_index - 1][col_index];
                    if bottom_edge(&above) != top_edge(&tile) {
                        continue;
                    }
                }

                if col_index > 0 {
                    let left = image[row_index][col_index - 1];
                    if right_edge(&left) != left_edge(&tile) {
                        continue;
                    }
                }

                possible_tiles.push(tile);
            }
        }
    }

    // println!("r: {}, c: {}, tiles: {}", row_index, col_index, possible_tiles.len());

    for t in possible_tiles {
        let row = image.get_mut(row_index).unwrap();
        row.push(t);
        remaining_tiles.remove(&t.tile_id);

        let next_col = (col_index + 1) % grid_size;
        let next_row: usize;
        if next_col == 0 {
            next_row = row_index + 1;
        } else {
            next_row = row_index;
        }

        if solve(
            image,
            remaining_tiles,
            tile_orientations,
            next_row,
            next_col,
            grid_size
        ) {
            return true;
        } else {
            // Re-add the id to remaining tiles
            remaining_tiles.insert(t.tile_id);
            image.get_mut(row_index).unwrap().pop();
        }
    }

    return false;
}

fn top_edge(tile: &Tile) -> &str {
    return &tile.contents[0];
}

fn left_edge(tile: &Tile) -> String {
    return tile.contents.iter().map(|s| s.chars().next().unwrap()).collect();
}

fn right_edge(tile: &Tile) -> String {
    return tile.contents.iter().map(|s| s.chars().last().unwrap()).collect();
}

fn bottom_edge(tile: &Tile) -> &str {
    return tile.contents.iter().last().unwrap();
}

fn main() {
   let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let mut lines = data.split("\n");

    let mut tiles: Vec<Tile> = Vec::new();

    while let Some(line) = lines.next() {
        if line.is_empty() {
            continue;
        }

        let raw_tokens: Vec<&str> = line.split(" ").collect();
        let tile_id: u32 = raw_tokens[1].trim_end_matches(':').parse::<u32>().unwrap();

        let mut contents: Vec<String> = Vec::new();
        while let Some(row) = lines.next() {
            if row.is_empty() {
                break;
            }
            contents.push(String::from(row));
        }

        tiles.push(Tile { tile_id: tile_id, contents: contents });
    }

    println!("# Tiles: {}", tiles.len());

    let grid_size: usize = (tiles.len() as f64).sqrt() as usize;
    println!("Grid width: {}", grid_size);

    let tile_orientations: HashMap<u32, Vec<Tile>> = tiles.iter()
        .map(|t| (t.tile_id, orientations(t)))
        .collect();

    let mut image: Vec<Vec<&Tile>> = Vec::new();
    let mut remaining_tiles: HashSet<u32> = tile_orientations
        .keys()
        .map(|k| *k)
        .collect();

    let result = solve(&mut image, &mut remaining_tiles, &tile_orientations, 0, 0, grid_size);
    if result {
        for row in image.iter() {
            println!("{}", row.iter().map(|r| r.tile_id.to_string()).collect::<Vec<String>>().join(" "));
        }
    }
}