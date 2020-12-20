use std::env;
use std::fs;


fn apply(operator_stack: &mut Vec<char>, operand_stack: &mut Vec<i64>, start_index: usize) -> bool {
    let op = operator_stack.last();
    // println!("op: {:?}, operators: {:?}, operands: {:?}, start_index: {}", op, operator_stack, operand_stack, start_index);

    if op != Some(&'+') && op != Some(&'*') {
        // println!("Skipping unknown operator");
        return false;
    }

    if operand_stack[start_index..].len() < 2 {
        // println!("Not enough operands available");
        return false;
    }

    let op = operator_stack.pop().unwrap();

    let op1 = operand_stack.pop().unwrap();
    let op2 = operand_stack.pop().unwrap();

    if op == '*' {
        operand_stack.push(op1 * op2);
    } else if op == '+' {
        operand_stack.push(op1 + op2);
    }

    return true;
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
        } else if ch == ')' {
            loop {
                let result = apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
                if !result {
                    break;
                }
            }
            // This pops off the opening paren
            let x = operator_stack.pop();
            if x.unwrap() != '(' {
                panic!("Unexpected operator {:?}", x);
            }
            blargh.pop();
        } else if ch == '*' {
            apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
            operator_stack.push(ch);
        } else if ch == '+' {
            // Evaluate previously pushed operand if it is are of lower
            // precedence.
            if operator_stack.last().unwrap_or(&'+') != &'*' {
                apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
            }
            operator_stack.push(ch);
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
        }
    }

    loop {
        let result = apply(&mut operator_stack, &mut operand_stack, *blargh.last().unwrap());
        if !result {
            break;
        }
    }
    // println!("operator stack: {:?}", operator_stack);
    // println!("operand_stack: {:?}", operand_stack);
    if operand_stack.len() != 1 {
        panic!("Should have just 1 operand left");
    }
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
