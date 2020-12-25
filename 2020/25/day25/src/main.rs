use std::env;
use std::fs;

fn transform(subject_number: u64, loop_size: u32) -> u64 {
    let mut result: u64 = 1;

    for l in 0..loop_size {
        result *= subject_number;
        result = result % 20201227;

        // println!("subj: {}, loop: {}, result: {}", subject_number, l, result);
    }

    return result;
}

fn loop_size(public_key: u64, subject_number: u64) -> u32 {
    let mut counter: u32 = 0;
    let mut result: u64 = 1;
    while result != public_key {
        result *= subject_number;
        result = result % 20201227;
        counter += 1;

        // println!("counter: {} {} {}", counter, result, public_key);
    }

    return counter;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines: Vec<&str> = data.split("\n").filter(|x| !x.is_empty()).collect();
    let card_public_key = lines[0].parse::<u64>().unwrap();
    let door_public_key = lines[1].parse::<u64>().unwrap();

    println!("Card public key: {}", card_public_key);
    println!("Door public key: {}", door_public_key);

    let card_loop_size = loop_size(card_public_key, 7);
    println!("Card loop size: {}", card_loop_size);

    println!("Door test: {}", transform(7, 11));
    let door_loop_size = loop_size(door_public_key, 7);
    println!("Door loop size: {}", door_loop_size);

    println!("encryption key: {}", transform(card_public_key, door_loop_size));
    println!("encryption key: {}", transform(door_public_key, card_loop_size));
}
