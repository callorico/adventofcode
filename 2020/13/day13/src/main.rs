use std::fs;
use std::env;

fn nearest_arrival(target: u32, schedule: u32) -> u32 {
    let mut arrival = (target / schedule) * schedule;
    if arrival < target {
        arrival += schedule
    }

    return arrival
}

fn matches(time: u64, schedule: (usize, u32)) -> bool {
    let adjusted_time = time + (schedule.0 as u64);
    return adjusted_time % (schedule.1 as u64) == 0;
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
    let mut busses: Vec<(usize, u32)> = lines[1].split(',')
        .enumerate()
        .map(|(i, x)| (i, x.parse::<u32>()))
        .filter(|(_, x)| x.is_ok())
        .map(|(i, x)| (i, x.unwrap()))
        .collect();

    busses.sort_by_key(|x| -(x.1 as i32));
    // busses.sort_by_key(|x| -(x.1 as i32));
    println!("{:?}", busses);

    let slowest = busses[0];
    let second_slowest = busses[1];
    let third_slowest = busses[2];

    let mut multiple: u64 = 1;
    let mut initial_time: u64 = 0;
    loop {
        initial_time = slowest.1 as u64 * multiple - slowest.0 as u64;

        let target_mod = second_slowest.1 as u64 - second_slowest.0 as u64;
        let target_mod2 = third_slowest.1 as u64 - third_slowest.0 as u64;

        if initial_time % second_slowest.1 as u64 == target_mod && initial_time % third_slowest.1 as u64 == target_mod2 {
            println!("Match is {} (multiple: {})", initial_time, multiple);
            break;
        }
        multiple += 1;
    }

    let step: u64 = slowest.1 as u64 * second_slowest.1 as u64 * third_slowest.1 as u64;
    println!("Initial time is: {}, step: {}", initial_time, step);

    let mut time: u64 = initial_time;
    loop {
        time += step;
        if busses.iter().all(|s| matches(time, *s)) {
            break;
        }
    }

    println!("Time is: {}", time);
}