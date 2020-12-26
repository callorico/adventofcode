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
        for col in 0..rotated.contents[0].len() {
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

fn apply_mask(merged_contents: &mut Vec<String>, monster: &Tile, row: usize, col: usize) {
    // Verify that that mask will fit
    if row + monster.contents.len() >= merged_contents.len() {
        return;
    }

    if col + monster.contents[0].len() >= merged_contents[0].len() {
        return;
    }

    let mut found_monster: bool = true;
    let mut cells: Vec<(usize, usize)> = Vec::new();
    for mask_row in 0..monster.contents.len() {
        for mask_col in 0..monster.contents[0].len() {
            if monster.contents[mask_row].chars().nth(mask_col) == Some('#') {
                let image_row = row + mask_row;
                let image_col = col + mask_col;

                let is_in_image = match merged_contents[image_row].chars().nth(image_col) {
                    Some('#') => true,
                    Some('O') => true,
                    _ => false
                };
                if is_in_image {
                    cells.push((image_row, image_col));
                } else {
                    found_monster = false;
                    break;
                }
            }
        }
    }

    if found_monster {
        println!("Found monster at {}, {}", row, col);
        for (image_row, image_col) in cells.iter() {
            let cell_range = *image_col..*image_col + 1;
            merged_contents[*image_row].replace_range(cell_range, "O");
        }
    }
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
    if !result {
        panic!("Unable to find a solution!");
    }

    for row_index in 0..grid_size {
        for line_index in 0..tiles[0].contents.len() {
            let mut row_output: Vec<&str> = Vec::new();
            for col_index in 0..grid_size {
                row_output.push(&image[row_index][col_index].contents[line_index]);
            }

            println!("{}", row_output.join(" "));
        }

        println!("");
    }


    for row in image.iter() {
        println!("{}", row.iter().map(|r| r.tile_id.to_string()).collect::<Vec<String>>().join(" "));
    }

    // Strip tile borders and generate big tile
    let tile_size = tiles[0].contents.len();
    let mut merged_contents: Vec<String> = Vec::new();
    for row_index in 0..grid_size {
        for line_index in 1..tile_size - 1 {
            let mut merged_row: Vec<&str> = Vec::new();
            for col_index in 0..grid_size {
                let slice: &str = &image[row_index][col_index].contents[line_index][1..tile_size - 1];
                merged_row.push(slice);
            }

            merged_contents.push(merged_row.join(""));
        }
    }

    for line in merged_contents.iter() {
        println!("{}", line);
    }

    let monster: Vec<String> = vec![
        String::from("                  # "),
        String::from("#    ##    ##    ###"),
        String::from(" #  #  #  #  #  #   ")
    ];

    let monster_tile = Tile { tile_id: 0, contents: monster };

    for rotated_monster in orientations(&monster_tile) {
        for row_index in 0..merged_contents.len() {
            for col_index in 0..merged_contents[0].len() {
                apply_mask(&mut merged_contents, &rotated_monster, row_index, col_index);
            }
        }
    }

    for line in merged_contents.iter() {
        println!("{}", line);
    }

    let total_not_monster: usize = merged_contents
        .iter()
        .map(|r| r.chars().filter(|c| c == &'#').count())
        .sum();

    println!("Total not monster cells: {}", total_not_monster);
}