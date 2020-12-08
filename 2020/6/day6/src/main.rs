use std::env;
use std::fs;
use std::collections::hash_set::HashSet;

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines = data.split('\n');
    let mut group: HashSet<char> = HashSet::new();
    let mut members = 0;
    let mut yes = 0;

    for l in lines {
        println!("line: {}, current group size: {}", l, members);
        if l == "" {
            println!("Group has {} answers, total yes so far: {}", group.len(), yes);
            yes += group.len();
            group.clear();
            members = 0;
            continue;
        }

        let member: HashSet<char> = l.chars().collect();
        for ch in &member {
            println!("{}", ch);
        }

        members += 1;
        if members == 1 {
            group = member;
        } else {
            group = group.intersection(&member).cloned().collect();
        }

        println!("Group size: {}", group.len());
        for a in &group {
            println!("current group: {}", a);
        }
    }

    println!("Final group has {} answers", group.len());
    yes += group.len();

    println!("Total yes: {}", yes);
}
