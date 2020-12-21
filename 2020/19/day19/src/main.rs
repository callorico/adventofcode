use std::env;
use std::fs;
use std::collections::hash_map::HashMap;

#[derive(Debug)]
struct Rule {
    sub_rules: Vec<Vec<u32>>,
    pattern: Option<String>
}

/// Returns the different # of consumed characters in the specified message
fn matches_rule(grammar: &HashMap<u32, Rule>, message: &str, rule_id: u32) -> Vec<u32> {
    if message.is_empty() {
        return vec![0];
    }

    let rule: &Rule = grammar.get(&rule_id).unwrap();
    // println!("message: {}, rule: {} {:?}", message, rule_id, rule);

    if rule.pattern.is_some() {
        let pat: &str = rule.pattern.as_ref().unwrap();

        if message.starts_with(pat) {
            // println!("  Matched terminal {}", pat);
            return vec![pat.len() as u32];
        }
    } else {
        let mut all_advances: Vec<u32> = Vec::new();

        for rule_set in &rule.sub_rules {
            let mut possible_advances: Vec<u32> = vec![0];

            let mut all_rules_match = true;
            for sub_rule_id in rule_set {
                // TODO: Need to attempt next rule with all possible consumptions of
                // previous rule
                let mut next_advances: Vec<u32> = Vec::new();
                for advance in &possible_advances {
                    let result = matches_rule(grammar, &message[*advance as usize..], *sub_rule_id);
                    // println!("  Found result: {:?}", result);
                    if result.len() == 1 && result[0] == 0 {
                        // No matches found
                    } else {
                        next_advances.extend(result.iter().map(|a| a + advance));
                    }
                }

                if next_advances.is_empty() {
                    // Unable to consume sub_rule_id. This rule set is invalid.
                    all_rules_match = false;
                    break;
                }

                possible_advances = next_advances;
            }

            if all_rules_match {
                all_advances.extend(possible_advances);
            }
        }

        if !all_advances.is_empty() {
            // println!("Possible consumptions: {:?}", all_advances);
            return all_advances;
        }
    }

    // println!("  No matches for rule {}", rule_id);
    return vec![0];
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
        // println!("**** Checking {}", line);
        let matches = matches_rule(&grammar, line, 0);
        if matches.iter().any(|s| *s == line.len() as u32) {
            println!("** matches: {}", line);
            total += 1;
        }
    }

    println!("Total matches: {}", total);
}
