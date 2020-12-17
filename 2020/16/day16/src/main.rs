use std::env;
use std::fs;


fn in_range(range: &(u32, u32), value: u32) -> bool {
    return value >= range.0 && value <= range.1;
}

fn parse_range(range_text: &str) -> (u32, u32) {
    let range: Vec<u32> = range_text.split("-")
        .map(|x| x.parse::<u32>().unwrap())
        .collect();

    return (range[0], range[1]);
}

fn invalid_seat_component(encoded_seat: &str, ranges: &Vec<(u32, u32)>) -> Option<u32> {
    let components = encoded_seat
        .split(",")
        .map(|s| s.parse::<u32>().unwrap());

    for seat in components {
        if !ranges.iter().any(|r| in_range(r, seat)) {
            println!("seat {} was not in any range:.", seat);
            return Some(seat);
        }
    }

    None
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");

    let mut lines = data.split("\n");
    let mut ranges: Vec<(u32, u32)> = Vec::new();

    while let Some(line) = lines.next() {
        if line.is_empty() {
            break;
        }

        let tokens: Vec<&str> = line.split(": ").collect();
        ranges.extend(tokens[1].split(" or ")
            .map(|r| parse_range(r)));
    }

    println!("{:?}", ranges);

    lines.next().unwrap();
    // Not sure what to do with this yet
    let my_ticket = lines.next().unwrap();

    lines.next();
    lines.next();

    let mut scan_error_rate: u32 = 0;
    while let Some(line) = lines.next() {
        if line.is_empty() {
            break;
        }

        println!("Examining seat: {}", line);
        scan_error_rate += invalid_seat_component(line, &ranges).unwrap_or(0);
    }

    println!("Sum of invalid seats: {}", scan_error_rate);
}
