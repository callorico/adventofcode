use std::env;
use std::fs;
use std::collections::hash_map::HashMap;

#[derive(Debug)]
struct Rule {
    sub_rules: Vec<Vec<u32>>,
    pattern: Option<String>
}

fn matches_rule(grammar: &HashMap<u32, Rule>, message: &str, rule_id: u32) -> u32 {
    if message.is_empty() {
        return 0;
    }

    let rule: &Rule = grammar.get(&rule_id).unwrap();
    if rule.pattern.is_some() {
        let pat: &str = rule.pattern.as_ref().unwrap();

        if message.starts_with(pat) {
            return pat.len() as u32;
        }
    } else {
        for rule_set in &rule.sub_rules {
            let mut advance: u32 = 0;
            let mut all_rules_match = true;
            for rule in rule_set {
                let result = matches_rule(grammar, &message[advance as usize..], *rule);
                if result == 0 {
                    all_rules_match = false;
                    break;
                }
                advance += result;
            }

            if all_rules_match {
                return advance;
            }
        }
    }

    return 0;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");

    let mut grammar: HashMap<u32, Rule> = HashMap::new();

    // Parse grammar
    let mut line_iter = data.split("\n");
    while let Some(line) = line_iter.next() {
        if line.is_empty() {
            break;
        }

        let tokens: Vec<&str> = line.split(": ").collect();
        let rule_id = tokens[0].parse::<u32>().unwrap();
        if tokens[1].starts_with("\"") && tokens[1].ends_with("\"") {
            let pattern = String::from(tokens[1].trim_matches('"'));
            grammar.insert(rule_id, Rule { sub_rules: Vec::new(), pattern: Some(pattern) });
        } else {
            let sub_rules: Vec<Vec<u32>> = tokens[1].split(" | ")
                .map(|s| s.split(" ").map(|r| r.parse::<u32>().unwrap()).collect())
                .collect();

            grammar.insert(rule_id, Rule { sub_rules: sub_rules, pattern: None });
        }
    }

    println!("Grammar: {:?}", grammar);

    // Find input lines that match rule 0
    let mut total = 0;
    for line in line_iter.filter(|s| !s.is_empty()) {
        let matches = matches_rule(&grammar, line, 0);
        if matches == line.len() as u32 {
            println!("matches: {}", line);
            total += 1;
        }
    }

    println!("Total matches: {}", total);
}
