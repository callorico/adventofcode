use std::collections::vec_deque::VecDeque;
use std::env;
use std::fs;


fn winner(hands: &Vec<(&str, VecDeque<i32>)>) -> Option<usize> {
    /// Return the position of the winning hand, if any.
    let non_empty: Vec<(usize, _)> = hands.iter()
        .enumerate()
        .filter(|(_, pair)| pair.1.len() > 0)
        .collect();

    if non_empty.len() > 1 {
        return None
    } else {
        return Some(*non_empty.first().map(|(i, _)| i).unwrap());
    }
}

fn score(hand: &VecDeque<i32>) -> u32 {
    return hand.iter()
        .rev()
        .enumerate()
        .map(|(i, c)| (i as u32 + 1) * (*c as u32))
        .sum();
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let mut lines = data.split("\n");

    let mut hands: Vec<(&str, VecDeque<i32>)> = Vec::new();

    while let Some(line) = lines.next() {
        let player_id: &str = line.trim_end_matches(':');
        let mut cards: VecDeque<i32> = VecDeque::new();

        while let Some(card) = lines.next() {
            if card.is_empty() {
                break;
            }

            cards.push_back(card.parse::<i32>().unwrap());
        }

        hands.push((player_id, cards));
    }

    println!("Parsed hands: {:?}", hands);

    let mut round: u32 = 1;

    let winning_hand: &VecDeque<i32> = loop {

        println!("--- Round {} ---", round);

        for (player_id, deck) in &hands {
            println!("{}'s deck: {:?}", player_id, deck);
        }

        let mut cards: Vec<(usize, i32)> = hands.iter_mut()
            .enumerate()
            .map(|(i, (_, h))| (i, h.pop_front().unwrap()))
            .collect();
        for (index, c) in &cards {
            println!("{} plays: {}", hands[*index].0, c);
        }

        cards.sort_by_key(|(_, c)| -(*c));
        let (i, _) = cards.iter().next().unwrap();
        println!("{} wins the round!", hands[*i].0);

        for (_, c) in &cards {
            hands[*i].1.push_back(*c);
        }

        let win = winner(&hands).map(|i| &hands[i].1);
        if win.is_some() {
            break win.unwrap();
        }

        println!("");
        round += 1;
    };

    println!("Score: {}", score(winning_hand));
}
