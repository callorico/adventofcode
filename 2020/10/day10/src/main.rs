use std::env;
use std::fs;
use std::collections::hash_map::HashMap;

fn count(cache: &mut HashMap<u32, u64>, voltage_tree: &HashMap<u32, Vec<u32>>, curr_voltage: u32, target_voltage: u32) -> u64 {
    if curr_voltage == target_voltage {
        return 1;
    }

    let cached = cache.get(&curr_voltage);
    if cached.is_some() {
        println!("Hit cache");
        return *cached.unwrap();
    }

    let children = voltage_tree.get(&curr_voltage).unwrap();
    let mut sum = 0;
    for c in children {
        let child_count = count(cache, voltage_tree, *c, target_voltage);
        sum += child_count;
    }

    cache.insert(curr_voltage, sum);

    return sum;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let mut adapters: Vec<u32> = data.split("\n")
        .filter(|x| !x.is_empty())
        .map(|x| x.parse::<u32>().unwrap())
        .collect();

    adapters.sort();
    adapters.insert(0, 0);

    for (i, n) in adapters.iter().enumerate() {
        println!("{}: {}", i, n);
    }

    let mut voltage_tree: HashMap<u32, Vec<u32>> = HashMap::new();
    for (i, voltage) in adapters.iter().enumerate() {
        let children = voltage_tree.entry(*voltage).or_insert(Vec::new());
        let mut new_index = i + 1;
        loop {
            if new_index >= adapters.len() {
                break;
            }

            let new_voltage = adapters[new_index];
            if new_voltage - voltage > 3 {
                break;
            }

            children.push(new_voltage);
            new_index += 1;
        }
    }

    for (k, v) in voltage_tree.iter() {
        println!("{}: {:?}", k, v);
    }
    let target_voltage = adapters.iter().last().unwrap();

    let mut cache = HashMap::new();
    let tree_paths = count(&mut cache, &voltage_tree, 0, *target_voltage);
    println!("Total combinations: {}", tree_paths);


    // Add laptop as the final adapter
    // adapters.push(adapters.iter().last().unwrap() + 3);

    // let mut voltage_diffs: Vec<u32> = Vec::new();
    // for (i, v) in adapters.iter().enumerate() {
    //     let prev_voltage = match i {
    //         0 => 0,
    //         i => adapters[i - 1]
    //     };
    //     voltage_diffs.push(v - prev_voltage);
    // }


    // for (i, a) in adapters.iter().enumerate() {
    //     println!("adapter: {}, diff: {}", a, voltage_diffs[i]);
    // }

    // let one_jolt_diff = voltage_diffs.iter()
    //     .filter(|x| *x == &(1 as u32))
    //     .count();

    // let three_jolt_diff = voltage_diffs.iter()
    //     .filter(|x| *x == &(3 as u32))
    //     .count();

    // let result = one_jolt_diff * three_jolt_diff;

    // println!("{} * {} = {}", one_jolt_diff, three_jolt_diff, result);
}
