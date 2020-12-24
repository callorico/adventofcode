
fn cups_string(cups: &Vec<u32>, target_cup: u32) -> String {
    let labels: Vec<String> = cups
        .iter()
        .map(|c| if *c == target_cup { format!("({})", c) } else { c.to_string() })
        .collect();

    return labels.join(" ");
}

fn index(cups: &Vec<u32>, target_cup: u32) -> Option<usize> {
    return cups
        .iter()
        .enumerate()
        .filter(|(_, c)| **c == target_cup)
        .map(|(i, _)| i)
        .next();
}

fn main() {
    let labelling = "459672813";
    // let labelling = "389125467";

    let mut cups: Vec<u32> = labelling
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect();

    let moves: u32 = 100;
    let mut current_cup = cups[0];
    let mut destination_cup: u32;

    for curr_move in 1..=moves {
        println!("-- move {} --", curr_move);
        println!("cups: {}", cups_string(&cups, current_cup));

        let current_cup_index = index(&cups, current_cup).unwrap();

        let pick_up: Vec<u32> = (current_cup_index + 1..=current_cup_index + 3)
            .map(|i| cups[i % cups.len()])
            .collect();
        println!("pick up: {:?}", pick_up);

        let mut remaining: Vec<u32> = cups
            .iter()
            .filter(|c| !pick_up.contains(c))
            .map(|c| *c)
            .collect();
        remaining.sort_by_key(|c| *c);
        let biggest_cup: u32 = *remaining.iter().last().unwrap();
        let smallest_cup: u32 = *remaining.iter().next().unwrap();

        // Find destination cup
        let mut possible_destination = cups[current_cup_index] - 1;
        while pick_up.contains(&possible_destination) {
            possible_destination -= 1;
        }

        if possible_destination < smallest_cup {
            possible_destination = biggest_cup;
        }

        destination_cup = possible_destination;
        println!("destination: {}\n", destination_cup);

        // Reform cups
        let mut reformed: Vec<u32> = Vec::new();
        for c in cups.iter() {
            if pick_up.contains(c) {
                continue;
            }

            reformed.push(*c);
            if *c == destination_cup {
                reformed.extend(&pick_up);
            }
        }

        cups = reformed;
        current_cup = cups[(index(&cups, current_cup).unwrap() + 1) % cups.len()];
    }

    println!("-- final --");
    println!("cups: {}", cups_string(&cups, current_cup));
}
