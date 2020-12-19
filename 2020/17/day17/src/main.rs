use std::env;
use std::fs;
use std::collections::hash_set::HashSet;

fn bounds(active_cells: &HashSet<(i32, i32, i32)>) -> ((i32, i32), (i32, i32), (i32, i32)) {
    let mut items: Vec<(i32, i32, i32)> = active_cells.iter().map(|(x, y, z)| (*x, *y, *z)).collect();

    items.sort_by_key(|(x, _, _)| *x);

    let x_bounds = (items.first().unwrap_or(&(0,0,0)).0, items.last().unwrap_or(&(0,0,0)).0 + 1);

    items.sort_by_key(|(_, y, _)| *y);

    let y_bounds = (items.first().unwrap_or(&(0,0,0)).1, items.last().unwrap_or(&(0,0,0)).1 + 1);

    items.sort_by_key(|(_, _, z)| *z);
    let z_bounds = (items.first().unwrap_or(&(0,0,0)).2, items.last().unwrap_or(&(0,0,0)).2 + 1);

    return (x_bounds, y_bounds, z_bounds);
}

fn print_space(active_cells: &HashSet<(i32, i32, i32)>) {
    // Find min, max for each axis
    let (x_bounds, y_bounds, z_bounds) = bounds(active_cells);

    for z in z_bounds.0..z_bounds.1 {
        println!("z={}", z);
        for y in y_bounds.0..y_bounds.1 {
            let row: Vec<char> = (x_bounds.0..x_bounds.1)
                .map(|x| match active_cells.contains(&(x, y, z)) {
                    true => '#',
                    false => '.'
                })
                .collect();

            println!("{:?}", row);
        }
    }
}

fn active_neighbors(active_cells: &HashSet<(i32, i32, i32)>, x: i32, y: i32, z: i32) -> u32 {
    let mut total: u32 = 0;

    for cell_x in x-1..x+2 {
        for cell_y in y-1..y+2 {
            for cell_z in z-1..z+2 {
                if cell_x == x && cell_y == y && cell_z == z {
                    // Skip the center point. Only want neighbors
                    continue;
                }

                // println!("  Checking neighbor: {},{},{}", cell_x, cell_y, cell_z);

                if active_cells.contains(&(cell_x, cell_y, cell_z)) {
                    total += 1;
                }
            }
        }
    }

    return total;
}

fn next_step(active_cells: &HashSet<(i32, i32, i32)>) -> HashSet<(i32, i32, i32)> {
    let mut next: HashSet<(i32, i32, i32)> = HashSet::new();

    let (x_bounds, y_bounds, z_bounds) = bounds(&active_cells);

    for x in x_bounds.0 - 1..x_bounds.1 + 2 {
        for y in y_bounds.0 - 1..y_bounds.1 + 2 {
            for z in z_bounds.0 - 1..z_bounds.1 + 2 {
                let cell = (x, y, z);
                let is_curr_active = active_cells.contains(&cell);
                let neighbors = active_neighbors(&active_cells, x, y, z);
                println!(" cell: {:?}, currently active: {}, active neighbors: {}", cell, is_curr_active, neighbors);
                let is_new_active: bool = match (is_curr_active, neighbors) {
                    (true, 2) => true,
                    (true, 3) => true,
                    (false, 3) => true,
                    _ => false
                };

                println!("  new state is {}", is_new_active);
                if is_new_active {
                    next.insert(cell);
                }
            }
        }
    }

    return next;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let mut active_cells: HashSet<(i32, i32, i32)> = data
        .split("\n")
        .enumerate()
        .filter(|(_, s)| !s.is_empty())
        .map(|(y, s)| s
            .chars()
            .enumerate()
            .filter(|(_, c)| *c == '#')
            .map(|(x, _)| (x as i32, y as i32, 0))
            .collect::<Vec<(i32, i32, i32)>>())
        .flatten()
        .collect();

    print_space(&active_cells);

    for i in 0..6 {
        let next = next_step(&active_cells);
        println!("After {} cycles", i + 1);
        print_space(&next);
        active_cells = next;
    }

    println!("Total active: {}", active_cells.len());
}
