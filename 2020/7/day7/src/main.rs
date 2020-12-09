use std::env;
use std::fs;
use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;
use regex::Regex;

fn parse_bag(description: &str) -> (u32, &str) {
    let re = Regex::new(r"(\d*)(.+) bags?").unwrap();
    let cap = re.captures(description).unwrap();
    let count = cap.get(1)
        .unwrap()
        .as_str()
        .parse::<u32>()
        .unwrap_or(0);

    let label = cap.get(2).unwrap().as_str().trim();

    return (count, label);
}

fn part1(data: &String) {
    let lines = data.split('\n');

    let mut bags: HashMap<&str, Vec<&str>> = HashMap::new();

    for line in lines {
        let tokens: Vec<&str> = line.split(" contain ").collect();
        if tokens.len() != 2 {
            continue;
        }

        let (_, bag) = parse_bag(tokens[0]);
        println!("outer bag {}", bag);
        let contained_bags: Vec<(u32, &str)> = tokens[1].split(", ")
            .map(|x| parse_bag(x))
            .collect();
        for (count, contained_bag) in contained_bags {
            let enclosing_bags: &mut Vec<&str> = bags.entry(contained_bag).or_insert_with(|| Vec::new());
            enclosing_bags.push(bag);
            println!("  contained bag {} {}", contained_bag, count);
        }
    }

    let mut containers: HashSet<&str> = HashSet::new();
    let mut stack: Vec<&str> = Vec::new();
    stack.push("shiny gold");
    while !stack.is_empty() {
        let bag_style = stack.pop().unwrap();
        let enclosing_bags = bags.get(bag_style);
        if !enclosing_bags.is_some() {
            println!("No bags contain {}", bag_style);
            continue;
        }
        for parent_bag in enclosing_bags.unwrap() {
            if !containers.contains(parent_bag) {
                containers.insert(parent_bag);
                stack.push(parent_bag);
            }
        }
    }

    println!("Total bags: {}", containers.len());

}

fn bag_count(label: &str, bags: &HashMap<&str, Vec<(u32, &str)>>) -> u32 {
    let mut sum = 0;

    println!("Bags inside of a {}", label);
    let nested_bags = bags.get(label);
    if nested_bags.is_none() {
        println!("  No bags inside");
        return 0;
    }

    for (_, nested_bag) in nested_bags.unwrap() {
        println!("{}", nested_bag);
    }

    for (count, nested_bag) in nested_bags.unwrap() {
        println!("  {} {}", count, nested_bag);
        sum += count;
        sum += count * bag_count(nested_bag, bags);
    }
    println!("{} contains {} bags", label, sum);

    return sum;
}

fn part2(data: &String) {
    let lines = data.split('\n');

    let mut bags: HashMap<&str, Vec<(u32, &str)>> = HashMap::new();

    for line in lines {
        let tokens: Vec<&str> = line.split(" contain ").collect();
        if tokens.len() != 2 {
            continue;
        }

        let (_, bag) = parse_bag(tokens[0]);
        let contained_bags: Vec<(u32, &str)> = tokens[1].split(", ")
            .map(|x| parse_bag(x))
            .filter(|(count, _)| count > &0)
            .collect();
        bags.insert(bag, contained_bags);
    }

    println!("Total bags: {}", bag_count("shiny gold", &bags));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    part2(&data);
    // part1(&data);
}