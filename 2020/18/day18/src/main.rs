use std::env;
use std::fs;


fn apply(operator_stack: &mut Vec<char>, operand_stack: &mut Vec<i64>, start_index: usize) {
    loop {
        let op = operator_stack.last();
        // println!("op: {:?}, operators: {:?}, operands: {:?}, start_index: {}", op, operator_stack, operand_stack, start_index);

        if op != Some(&'+') && op != Some(&'*') {
            // println!("Skipping unknown operator");
            return;
        }

        if operand_stack[start_index..].len() < 2 {
            // println!("Not enough operands available");
            return;
        }

        let op = operator_stack.pop().unwrap();

        let op1 = operand_stack.pop().unwrap();
        let op2 = operand_stack.pop().unwrap();

        if op == '*' {
            operand_stack.push(op1 * op2);
        } else if op == '+' {
            operand_stack.push(op1 + op2);
        }
    }
}

fn eval(equation: &str) -> i64 {
    let mut eq_iter = equation.chars().peekable();

    let mut operand_stack: Vec<i64> = Vec::new();
    let mut operator_stack: Vec<char> = Vec::new();
    let mut blargh: Vec<usize> = Vec::new();
    blargh.push(0);

    while let Some(ch) = eq_iter.next() {
        if ch == '(' {
            operator_stack.push(ch);
            blargh.push(operand_stack.len());
            // println!("start_index: {:?}", blargh);
        } else if ch == ')' {
            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
            // This pops off the opening paren
            let x = operator_stack.pop();
            if x.unwrap() != '(' {
                panic!("Unexpected operator {:?}", x);
            }
            blargh.pop();
            // println!("start_index: {:?}", blargh);
            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
        } else if ch == '*' {
            operator_stack.push(ch);
            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
        } else if ch == '+' {
            operator_stack.push(ch);
            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
        } else if ch.is_ascii_digit() {
            let mut digit = String::new();
            digit.push(ch);
            while let Some(ch) = eq_iter.peek() {
                if !ch.is_ascii_digit() {
                    break;
                }

                digit.push(eq_iter.next().unwrap());
            }

            let parsed: i64 = digit.parse::<i64>().unwrap();
            operand_stack.push(parsed);

            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
        }
    }

    apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
    // println!("operator stack: {:?}", operator_stack);
    // println!("operand_stack: {:?}", operand_stack);
    return operand_stack.pop().unwrap();
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let equations = data.split("\n")
        .filter(|x| !x.is_empty());

    let mut total = 0;
    for eq in equations {
        let result = eval(eq);
        println!("{} -> {}", eq, result);
        total += result;
    }

    println!("Total is {}", total);
}
