use std::env;
use std::fs;
use std::f32::consts::PI;


fn parse_command(raw: &str) -> (char, i32) {
    let command: char = raw[..1].chars().next().unwrap();
    let amount: i32 = raw[1..].parse::<i32>().unwrap();

    return (command, amount);
}

fn rotate(rotations: [char; 4], direction: char, amount: i32) -> char {
    let normalized = amount / 90;

    let pos = rotations.iter().position(|x| *x == direction).unwrap();
    let mut new_pos = pos as i32 + normalized;

    if new_pos < 0 {
        new_pos = rotations.len() as i32 + new_pos;
    } else {
        new_pos = new_pos % rotations.len() as i32;
    }

    println!("rot amount: {}, curr_pos: {}, new_pos: {}", normalized, pos, new_pos);
    return rotations[new_pos as usize];
}

fn rotate_trig(amount: i32, waypoint_x: i32, waypoint_y: i32) -> (i32, i32) {
    let radians: f32 = (amount as f32 * PI) / 180_f32;

    let cos = radians.cos();
    let sin = radians.sin();

    let new_waypoint_x = waypoint_x as f32 * cos - waypoint_y as f32 * sin;
    let new_waypoint_y = waypoint_x as f32 * sin + waypoint_y as f32 * cos;

    let rotated = (new_waypoint_x.round() as i32, new_waypoint_y.round() as i32);
    println!("Rotated {} {} by {} => {:?}", waypoint_x, waypoint_y, amount, rotated);

    return rotated;
}


fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let commands: Vec<(char, i32)> = data.split("\n")
        .filter(|x| !x.is_empty())
        .map(|x| parse_command(x))
        .collect();

    let rotations = ['N', 'E', 'S', 'W'];
    let mut direction = 'E';
    let mut ship_x: i32 = 0;
    let mut ship_y: i32 = 0;
    let mut waypoint_x: i32 = 10;
    let mut waypoint_y: i32 = 1;

    for (cmd, amount) in commands {
        println!("cmd: {}, amount: {}", cmd, amount);

        match cmd {
            'F' => {
                ship_x += waypoint_x * amount;
                ship_y += waypoint_y * amount;
            },
            'N' => waypoint_y += amount,
            'S' => waypoint_y -= amount,
            'W' => waypoint_x -= amount,
            'E' => waypoint_x += amount,
            'L' => {
                let result = rotate_trig(amount, waypoint_x, waypoint_y);
                waypoint_x = result.0;
                waypoint_y = result.1;
            }
            'R' => {
                let result = rotate_trig(-amount, waypoint_x, waypoint_y);
                waypoint_x = result.0;
                waypoint_y = result.1;
            }
            _ => panic!("Shouldn't get here.")
        }

        println!("curr ship pos x: {}, y: {}, waypoint pos x: {}, y: {}", ship_x, ship_y, waypoint_x, waypoint_y);
    }

    println!("Distance: {}", ship_x.abs() + ship_y.abs());
}
