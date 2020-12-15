use std::env;
use std::fs;
use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;
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

fn float_index(mask_template: &str, index: u64) -> HashSet<u64> {
    let mut x_index: Vec<usize> = Vec::new();
    // First pin the 1's in the mask to 1 and collect the bit index of all the X's
    let mut masked_value: u64 = index;
    for (i, c) in mask_template.chars().enumerate() {
        let shift = mask_template.len() - i - 1;
        // println!("shift: {}, i: {}, c: {}", shift, i, c);
        if c == '1' {
            masked_value |= 1 << shift;
        } else if c == 'X' {
            x_index.push(shift);
        }
    }

    // println!("current masked value: {}, {:b}", masked_value, masked_value);

    // Now go through and set the bits in the X positions
    let mut indices: HashSet<u64> = HashSet::new();
    let combinations = u64::pow(2, x_index.len() as u32);

    // Reversing isn't necessary since we are going over all bit combinations anyway
    x_index.reverse();

    // println!("x_index: {:?}", x_index);

    for val in 0..combinations {
        let mut new_index: u64 = masked_value;
        // println!("val: {}, {:b}", val, val);
        for (i, x) in x_index.iter().enumerate() {
            let val_bit: u64 = (val & (1 << i)) >> i;
            let val_shifted = 1 << x;
            // println!("val_bit: {}, shift: {}, val_shifted: {:b}, new_index: {:b}", val_bit, x, val_shifted, new_index);
            if val_bit == 1 {
                new_index |= val_shifted;
            } else {
                new_index &= !val_shifted;
            }
        }
        println!("new_index: {}, {:b}", new_index, new_index);

        indices.insert(new_index);
    }

    return indices;
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

            for new_index in float_index(mask, index) {
                println!("index: {}, value: {}, mask: {}", new_index, value, mask);
                mem.insert(new_index, value);
            }
       }
    }

    println!("memdump: {:?}", mem);

    let value_sum: u64 = mem.values().sum();
    println!("value sum: {}", value_sum);
}
