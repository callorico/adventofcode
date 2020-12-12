use std::env;
use std::fs;
use std::collections::hash_set::HashSet;
use std::collections::vec_deque::VecDeque;


fn find_pair(numbers: &VecDeque<i64>, desired_sum: i64) -> Option<(i64, i64)> {
    let mut desired_targets: HashSet<i64> = HashSet::new();
    for n in numbers {
        let target = desired_sum - *n;
        if desired_targets.contains(&target) {
            return Some((*n, target))
        }
        desired_targets.insert(*n);
    }

    None
}


fn part1(stream: &Vec<i64>) -> Option<i64> {
    let mut buffer: VecDeque<i64> = stream[0..25].iter().copied().collect();

    for n in &stream[25..] {
        let result = find_pair(&buffer, *n);

        if result.is_none() {
            return Some(*n);
        }

        let (a, b) = result.unwrap();
        println!("{} + {} = {}", a, b, n);

        buffer.pop_front();
        buffer.push_back(*n);
    }

    None
}

fn part2(stream: &Vec<i64>, target: i64) -> Option<(usize, usize)> {
    let mut sums: Vec<i64> = Vec::new();

    for (i, n) in stream.iter().enumerate() {
        let sum = match sums.len() {
            0 => *n,
            x => sums[x - 1] + *n
        };

        for (i2, prev_sum) in sums.iter().enumerate() {
            println!("Range ({} - {}) sum: {}", i2, i, sum - prev_sum);
            if sum - prev_sum == target {
                return Some((i2 + 1, i));
            }
        }

        sums.push(sum);
        println!("Sum is {} index: {}", sum, i);
    }

    None
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let stream: Vec<i64> = data.split('\n')
        .filter(|x| !x.is_empty())
        .map(|x| x.parse::<i64>().unwrap())
        .collect();

    let result = part1(&stream).unwrap();
    println!("No 2 number sum found for {}", result);


    let range = part2(&stream, result).unwrap();
    println!("Range {} {}", range.0, range.1);

    let mut sum = 0;
    for n in &stream[range.0..range.1 + 1] {
        sum += *n;
    }

    println!("Sum is {}", sum);

    let mut contiguous = stream[range.0..range.1 + 1].to_vec();
    contiguous.sort();

    println!("Sum is {}", contiguous[0] + contiguous[contiguous.len() - 1]);
}