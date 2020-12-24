use std::collections::vec_deque::VecDeque;
use std::env;
use std::fs;


struct Counter {
    value: u32
}

fn next_value(counter: &mut Counter) -> u32 {
    let next = counter.value + 1;
    counter.value = next;
    return next;
}


fn winner(hands: &Vec<(&str, VecDeque<i32>)>) -> Option<usize> {
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


fn matches(hands: &Vec<(&str, VecDeque<i32>)>, prior_rounds: &Vec<Vec<VecDeque<i32>>>) -> bool {
    for prior in prior_rounds.iter() {

        let mut found_match = true;
        for ((x, h1), h2) in hands.iter().zip(prior.iter()) {
            // println!("{}. Current {:?}. Previous: {:?}", x, h1, h2);
            if h1.len() != h2.len() || !h1.iter().zip(h2.iter()).all(|(c1, c2)| c1 == c2) {
                found_match = false;
                break;
            }
        }

        if found_match {
            return true;
        }

    }

    return false;
}


fn combat(hands: &mut Vec<(&str, VecDeque<i32>)>, game_counter: &mut Counter) -> usize {
    let mut prior_rounds: Vec<Vec<VecDeque<i32>>> = Vec::new();

    let game = next_value(game_counter);

    println!("\n=== Game {} ===\n", game);

    return loop {
        let round = prior_rounds.len() + 1;
        println!("-- Round {} (Game {}) --", round, game);

        for (player_id, deck) in hands.iter() {
            println!("{}'s deck: {:?}", player_id, deck);
        }

        // Return index 0 if there was a previous round with the same cards.
        if matches(hands, &prior_rounds) {
            println!("The hands match a previous round. {} is the winner!", hands[0].0);
            return 0;
        }

        let round_copy: Vec<VecDeque<i32>> = hands.iter().map(|(_, c)| c.clone()).collect();
        prior_rounds.push(round_copy);

        let mut cards: Vec<(usize, i32)> = hands.iter_mut()
            .enumerate()
            .map(|(i, (_, h))| (i, h.pop_front().unwrap()))
            .collect();
        for (index, c) in &cards {
            println!("{} plays: {}", hands[*index].0, c);
        }

        // Check to see if we need to recurse
        let winner_index: usize;
        if cards.iter().all(|(i, c)| hands[*i].1.len() >= (*c as usize)) {
            // Recursive combat time!
            println!("Playing a sub-game to determine the winner...");

            let mut hands_copy: Vec<(&str, VecDeque<i32>)> = Vec::new();
            for (i, count) in &cards {
                hands_copy.push(
                    (
                        hands[*i].0,
                        hands[*i].1
                            .iter()
                            .map(|i| *i)
                            .take(*count as usize)
                            .collect()
                    )
                )
            }

            winner_index = combat(&mut hands_copy, game_counter);
            println!("\n...anyway, back to game {}", game);
        } else {
            // otherwise, the winner if the player with the highest card
            cards.sort_by_key(|(_, c)| -(*c));
            let (i, _) = cards.iter().next().unwrap();
            winner_index = *i;
        }

        println!("{} wins round {} of game {}!", hands[winner_index].0, round, game);

        // Winners card goes first.
        cards.sort_by_key(|(index, _)| (*index != winner_index));
        for (_, c) in &cards {
            hands[winner_index].1.push_back(*c);
        }

        let win = winner(&hands);
        if win.is_some() {
            println!("The winner of game {} is {}!", game, hands[winner_index].0);
            break win.unwrap();
        }

        println!("");
    }
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

    let mut counter = Counter { value: 0 };
    let winning_index = combat(&mut hands, &mut counter);
    let winning_hand: &VecDeque<i32> = &hands[winning_index].1;

    println!("Score: {}", score(winning_hand));
}
