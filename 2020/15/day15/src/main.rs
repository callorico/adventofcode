use std::collections::hash_map::HashMap;
use std::collections::vec_deque::VecDeque;


fn main() {
    let input: Vec<u32> = vec![16,1,0,18,12,14,19];
    // let input: Vec<u32> = vec![1,3,2];

    let mut guesses: HashMap<u32, VecDeque<u32>> = HashMap::new();

    for (i, g) in input.iter().enumerate() {
        let mut guess_turn = VecDeque::new();
        guess_turn.push_front((i + 1) as u32);

        guesses.insert(*g, guess_turn);
    }

    println!("Initial guess map: {:?}", guesses);
    // let limit = 2020;
    let limit = 30_000_000;
    let mut most_recent: u32 = *input.iter().last().unwrap();
    for turn in guesses.len() + 1..limit + 1 {
        let mut guess_turn = guesses.entry(most_recent).or_insert(VecDeque::new());

        // println!("Most recent guess {}, Previous answers {:?}", most_recent, guess_turn);

        let guess = match guess_turn.len() {
            0 | 1 => 0,
            _ => guess_turn[0] - guess_turn[1]
        };

        guess_turn = guesses.entry(guess).or_insert(VecDeque::new());
        guess_turn.push_front(turn as u32);
        if guess_turn.len() > 2 {
            guess_turn.pop_back();
        }

        // println!("Guess on turn {} is {}", turn, guess);
        // let mut blargh: Vec<(&u32, &VecDeque<u32>)> = guesses.iter().collect();
        // blargh.sort_by_key(|x| x.0);
        // for (guess, turns) in &blargh {
            // println!("  {}: {:?}", guess, turns);
        // }
        most_recent = guess;
    }

    println!("Guess {} on turn {}", most_recent, limit);
}
