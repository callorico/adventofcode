use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;

struct Node {
    value: u32,
    next: Option<u32>,
    prev: Option<u32>
}

fn cups_string(cups: &HashMap<u32, Node>, first_value: u32, target_cup: u32) -> String {
    let mut node: &Node = cups.get(&first_value).unwrap();
    let mut labels: Vec<String> = Vec::new();
    loop {
        if node.value == target_cup {
            labels.push(format!("({})", node.value));
        } else {
            labels.push(node.value.to_string());
        }

        node = cups.get(&node.next.unwrap()).unwrap();
        if node.value == first_value {
            break;
        }
    }

    return labels.join(" ");
}

fn main() {
    let labelling = "459672813";
    // let labelling = "389125467";

    let mut initial_cups = labelling
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .chain((labelling.len() + 1..=1_000_000).map(|i| i as u32));

    let first_value = initial_cups.next().unwrap();
    let mut first_cup = Node { value: first_value, next: None, prev: None };

    let mut cups: HashMap<u32, Node> = HashMap::new();

    let mut previous_cup = &mut first_cup;
    while let Some(cup) = initial_cups.next() {
        let new_cup = Node { value: cup, next: None, prev: Some(previous_cup.value) };
        previous_cup.next = Some(cup);
        cups.insert(new_cup.value, new_cup);

        previous_cup = cups.get_mut(&cup).unwrap();
    }

    // Complete the loop back to the initial cup
    previous_cup.next = Some(first_value);
    first_cup.prev = Some(previous_cup.value);
    cups.insert(first_value, first_cup);

    let biggest_value: u32 = *cups.keys().max().unwrap();
    let smallest_value: u32 = *cups.keys().min().unwrap();

    let moves: u32 = 10_000_000;

    let mut current_value = first_value;
    for curr_move in 1..=moves {
        if curr_move % 500_000 == 0 {
            println!("-- move {} --", curr_move);
        }
        // println!("cups: {}", cups_string(&cups, first_value, current_value));

        let mut picked_up: HashSet<u32> = HashSet::new();
        let first_cup_value = cups[&current_value].next.unwrap();
        picked_up.insert(first_cup_value);

        let mut last_cup_value: u32 = first_cup_value;
        for _ in 0..2 {
            last_cup_value = cups[&last_cup_value].next.unwrap();
            picked_up.insert(last_cup_value);
        }

        // println!("pick up: {:?}", picked_up);

        // Find destination cup
        let mut possible_destination = current_value - 1;
        while picked_up.contains(&possible_destination) {
            possible_destination -= 1;
        }

        let mut current_smallest = smallest_value;
        while picked_up.contains(&current_smallest) {
            current_smallest += 1;
        }

        if possible_destination < current_smallest {
            let mut current_biggest = biggest_value;
            while picked_up.contains(&current_biggest) {
                current_biggest -= 1;
            }
            possible_destination = current_biggest;
        }
        let destination_cup_value: u32 = possible_destination;
        let after_destination_cup_value: u32 = cups[&destination_cup_value].next.unwrap();

        // println!("destination: {}\n", destination_cup_value);

        // Do the linked list splicing
        let mut destination_cup = cups.get_mut(&destination_cup_value).unwrap();
        destination_cup.next = Some(first_cup_value);

        let after_last_value = cups[&last_cup_value].next.unwrap();
        let mut current_cup = cups.get_mut(&current_value).unwrap();
        current_cup.next = Some(after_last_value);

        let mut first_cup = cups.get_mut(&first_cup_value).unwrap();
        first_cup.prev = Some(destination_cup_value);

        let mut last_cup = cups.get_mut(&last_cup_value).unwrap();
        last_cup.next = Some(after_destination_cup_value);

        let mut after_destination_cup = cups.get_mut(&after_destination_cup_value).unwrap();
        after_destination_cup.prev = Some(last_cup_value);

        current_value = cups[&current_value].next.unwrap();
    }

    // println!("-- final --");
    // println!("cups: {}", cups_string(&cups, first_value, current_value));

    let cup1 = cups[&1].next.unwrap();
    let cup2 = cups[&cup1].next.unwrap();

    println!("{} * {} = {}", cup1, cup2, (cup1 as u64) * (cup2 as u64));
}
