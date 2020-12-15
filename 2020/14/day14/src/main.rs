use std::env;
use std::fs;
use std::collections::hash_map::HashMap;
use regex::Regex;

fn apply_mask(mask_template: &str, value: u64) -> u64 {
    let mut masked_value: u64 = value;

    // Set bits in the mask based on the template
    for (i, c) in mask_template.chars().enumerate() {
        let shift = mask_template.len() - i - 1;
        // println!("shift: {}, i: {}, c: {}", shift, i, c);
        let bit_mask = 1_u64 << shift;
        if c == '1' {
            masked_value |= bit_mask;
        } else if c == '0' {
            masked_value &= !bit_mask;
        }
    }

    return masked_value;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines = data.split("\n")
        .filter(|x| !x.is_empty());

    let mut mem: HashMap<u64, u64> = HashMap::new();
    let mut mask: &str = &"X".repeat(36);

    for line in lines {
        let tokens: Vec<&str> =  line.split(" = ").collect();
        if tokens[0] == "mask" {
            mask = tokens[1];
            println!("mask: {}", mask);
        } else {
            let value = tokens[1].parse::<u64>().unwrap();
            println!("{}", tokens[0]);
            let re = Regex::new(r"mem\[(\d+)\]").unwrap();
            let cap = re.captures(tokens[0]).unwrap();
            let index = cap.get(1)
                .unwrap()
                .as_str()
                .parse::<u64>()
                .unwrap();

            println!("index: {}, value: {}, mask: {}", index, value, mask);
            mem.insert(index, apply_mask(mask, value));
       }
    }

    println!("memdump: {:?}", mem);

    let value_sum: u64 = mem.values().sum();
    println!("value sum: {}", value_sum);
}
