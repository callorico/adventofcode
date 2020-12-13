use std::env;
use std::fs;

fn total_occupied_seats(seats: &Vec<Vec<char>>) -> usize {
    return seats.iter()
        .map(|x| x.iter().filter(|s| **s == '#').count())
        .sum();
}

// fn occupied_seats(seats: &Vec<Vec<char>>, row: usize, col: usize) -> u32 {
//     let mut sum: u32 = 0;

//     let min_row = if row == 0 { 0 } else { row - 1 };
//     let max_row = if row >= seats.len() { row } else { row + 1 };
//     let min_col = if col == 0 { 0 } else { col - 1 };
//     let max_col = if col >= seats[0].len() { col } else { col + 1 };

//     for adjacent_row in min_row..max_row+1 {
//         for adjacent_col in min_col..max_col+1 {
//             if adjacent_row == row && adjacent_col == col {
//                 continue;
//             }

//             if adjacent_row < 0 || adjacent_row >= seats.len() {
//                 continue;
//             }

//             if adjacent_col < 0 || adjacent_col >= seats[0].len() {
//                 continue;
//             }

//             //println!("Looking at {} {}", adjacent_row, adjacent_col);
//             if seats[adjacent_row][adjacent_col] == '#' {
//                 sum += 1;
//             }
//         }
//     }

//     return sum;
// }

fn occupied_seats(seats: &Vec<Vec<char>>, row: usize, col: usize) -> u32 {
    let mut sum: u32 = 0;
    for row_delta in -1..2 {
        for col_delta in -1..2 {
            if row_delta == 0 && col_delta == 0 {
                continue;
            }

            if is_occupied(seats, row, col, row_delta, col_delta) {
                sum += 1;
            }
        }
    }

    return sum;
}

fn is_occupied(seats: &Vec<Vec<char>>, row: usize, col: usize, row_delta: i32, col_delta: i32) -> bool {
    let mut curr_row: i32 = row as i32;
    let mut curr_col: i32 = col as i32;

    return loop {
        let new_row: i32 = curr_row + row_delta;
        let new_col: i32 = curr_col + col_delta;
        // println!("r: {}, c: {}", new_row, new_col);

        if new_row < 0 || new_row >= seats.len() as i32 {
            break false;
        }

        if new_col < 0 || new_col >= seats[0].len() as i32 {
            break false;
        }

        let adjacent_seat = seats[new_row as usize][new_col as usize];
        if adjacent_seat == '#' {
            break true;
        } else if adjacent_seat == 'L' {
            break false;
        }

        curr_row = new_row;
        curr_col = new_col;
    }
}
fn next_step(seats: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut new_seats = Vec::new();
    for row in 0..seats.len() {
        let mut new_row = Vec::new();
        for col in 0..seats[0].len() {
            let seat = seats[row][col];

            // let adjacent_occupied = occupied_seats(seats, row, col);
            // println!("r: {}, c: {}, # occ: {}", row, col, adjacent_occupied);
            let new_seat = match (seat, occupied_seats(seats, row, col)) {
                ('L', 0) => '#',
                // ('#', 4) => 'L',
                ('#', 5) => 'L',
                ('#', 6) => 'L',
                ('#', 7) => 'L',
                ('#', 8) => 'L',
                (s, _) => s
            };

            new_row.push(new_seat);
        }

        new_seats.push(new_row);
    }

    return new_seats;
}

fn equals(seats: &Vec<Vec<char>>, seats2: &Vec<Vec<char>>) -> bool {
    for row in 0..seats.len() {
        for col in 0..seats[0].len() {
            if seats[row][col] != seats2[row][col] {
                return false;
            }
        }
    }

    return true;
}

fn print_seats(seats: &Vec<Vec<char>>) {
    for s in seats {
        println!("{:?}", s);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let mut seats: Vec<Vec<char>> = data.split("\n")
        .filter(|x| !x.is_empty())
        .map(|x| x.chars().collect())
        .collect();

    let mut round = 0;

    let final_seats = loop {
        println!("round: {}", round);
        print_seats(&seats);

        let next_seats = next_step(&seats);
        if equals(&seats, &next_seats) {
            break next_seats;
        }

        seats = next_seats;
        round += 1;
    };

    println!("Occupied seats: {}", total_occupied_seats(&final_seats));
}
