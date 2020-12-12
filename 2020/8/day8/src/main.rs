use std::env;
use std::fs;
use std::collections::hash_set::HashSet;

fn parse_instruction(line: &str) -> (&str, i32) {
    let tokens: Vec<&str> = line.split(" ").collect();
    let op = tokens[0];
    let sign = tokens[1].chars().next().unwrap();
    let mut amount = tokens[1][1..].parse::<i32>().unwrap();
    if sign == '-' {
        amount = amount * -1;
    }
    return (op, amount);
}

fn execute(instructions: &Vec<(&str, i32)>) -> (i32, bool) {
    let mut acc = 0;
    let mut seen: HashSet<i32> = HashSet::new();

    let mut line: i32 = 0;
    let result = loop {
        let instruction = instructions.get(line as usize).unwrap();
        if seen.contains(&line) {
            break (acc, false);
        }

        seen.insert(line);
        let op = instruction.0;
        let amount = instruction.1;
        let mut step = 1;

        if op == "acc" {
            acc += amount;
        } else if op == "jmp" {
            step = amount;
        }

        println!("{}: {} {}, acc: {} ({})", line, op, amount, acc, step);
        line += step;
        if line as usize >= instructions.len() {
            break (acc, true);
        }
    };
    return result;
}

fn brute(instructions: &Vec<(&str, i32)>) {

    for (i, instruction) in instructions.iter().enumerate() {
       let flipped_op = match instruction.0 {
           "jmp" => "nop",
           "nop" => "jmp",
           _ => instruction.0
       };

       if flipped_op != instruction.0 {
            let mut modified = instructions.clone();
            modified[i] = (flipped_op, instruction.1);
            let (acc, exited_cleanly) = execute(&modified);
            if exited_cleanly {
                println!("Modified line {}. acc: {}", i, acc);
                return;
            }
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines = data.split("\n");

    let instructions: Vec<(&str, i32)> = lines
        .filter(|x| x.len() > 0)
        .map(|x| parse_instruction(x))
        .collect();

    // let result = execute(&instructions);
    // println!("Current acc value: {}", result.0);

    brute(&instructions);

}
