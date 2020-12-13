use std::fs;
use std::env;

fn nearest_arrival(target: u32, schedule: u32) -> u32 {
    let mut arrival = (target / schedule) * schedule;
    if arrival < target {
        arrival += schedule
    }

    return arrival
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines: Vec<&str> = data.split("\n")
        .collect();
    let start = lines[0].parse::<u32>().unwrap();
    let busses: Vec<u32> = lines[1].split(',')
        .filter(|x| *x != "x")
        .map(|x| x.parse::<u32>().unwrap())
        .collect();

    println!("{}", start);
    println!("{:?}", busses);

    let mut arrivals: Vec<(u32, u32)> = busses.iter()
        .map(|x| (*x, nearest_arrival(start, *x)))
        .collect();

    arrivals.sort_by_key(|x| x.1);

    // println!("{:?}", arrivals);
    let (bus_id, arrival) = arrivals[0];
    let wait_minutes = arrival - start;

    println!("bus: {}, wait: {} => {}", bus_id, wait_minutes, bus_id * wait_minutes);
}
