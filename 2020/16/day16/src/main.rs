use std::env;
use std::fs;
use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;


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

fn find_field(matrix: &Vec<HashMap<&str, u32>>, target: u32) -> Option<(u32, String)> {
    for (i, counts) in matrix.iter().enumerate() {
        let count: Vec<&str> = counts
            .iter()
            .filter(|(s, c)| **c == target)
            .map(|(s, c)| *s)
            .collect();

        if count.len() == 1 {
            return Some((i as u32, String::from(count[0])));
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

    let mut seat_components: HashMap<&str, Vec<(u32, u32)>> = HashMap::new();

    while let Some(line) = lines.next() {
        if line.is_empty() {
            break;
        }

        let tokens: Vec<&str> = line.split(": ").collect();

        let ranges = tokens[1].split(" or ")
            .map(|r| parse_range(r))
            .collect();

        seat_components.insert(tokens[0], ranges);
    }

    println!("{:?}", seat_components);

    lines.next().unwrap();
    // Not sure what to do with this yet
    let my_ticket = lines.next().unwrap();

    lines.next();
    lines.next();

    let mut matrix: Vec<HashMap<&str, u32>> = Vec::new();
    for _ in 0..seat_components.len() {
        matrix.push(HashMap::new());
    }

    let mut total_seats = 0;
    let mut valid_seats = 0;
    while let Some(line) = lines.next() {
        if line.is_empty() {
            break;
        }

        println!("Examining seat: {}", line);
        total_seats += 1;
        let components = line
            .split(",")
            .map(|s| s.parse::<u32>().unwrap());

        let mut component_matches: Vec<HashSet<&str>> = Vec::new();
        for c in components {
            let mut matches: HashSet<&str> = HashSet::new();
            for (name, ranges) in &seat_components {
                if ranges.iter().any(|r| in_range(r, c)) {
                    matches.insert(name);
                }
            }

            component_matches.push(matches);
        }

        total_seats += 1;
        if component_matches.iter().all(|s| !s.is_empty()) {
            for (i, matches) in component_matches.iter().enumerate() {
                let totals = matrix.get_mut(i).unwrap();
                for m in matches {
                    let total = totals.get(m).unwrap_or(&0);
                    totals.insert(m, total + 1);
                }
            }

            valid_seats += 1;
        }
    }

    println!("Matrix: {:?}", matrix);

    let mut lookup: HashMap<String, u32> = HashMap::new();

    while lookup.len() < seat_components.len() {
        let (i, field) = find_field(&matrix, valid_seats).unwrap();
        lookup.insert(field.to_owned(), i);

        // Remove component from all dicts now...
        for counts in matrix.iter_mut() {
            counts.remove(field.to_owned().as_ref() as &str);
        }
    }

    println!("Lookup: {:?}", lookup);

    let my_tix: Vec<u32> = my_ticket
        .split(",")
        .map(|s| s.parse::<u32>().unwrap())
        .collect();

    println!("my_tix: {:?}", my_tix);

    let mut product: u64 = 1;
    for (field, index) in lookup {
        if field.starts_with("departure") {
            println!("Multiplying by {} for {}", my_tix[index as usize], field);
            product *= my_tix[index as usize] as u64;
        }
    }

    println!("product: {}", product);
    println!("{}/{}", valid_seats, total_seats);
}
