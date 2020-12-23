use std::env;
use std::fs;
use std::collections::hash_map::HashMap;
use std::collections::hash_set::HashSet;

fn maybe_allergen(allergen_map: &HashMap<&str, HashSet<&str>>, ingredient: &str) -> bool {
    return allergen_map.values().any(|i| i.contains(ingredient));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let filename = &args[1];

    println!("Opening {}", filename);

    let data = fs::read_to_string(filename).expect("Unable to read file");
    let lines = data.split("\n").filter(|x| !x.is_empty());

    let mut allergen_map: HashMap<&str, HashSet<&str>> = HashMap::new();
    let mut ingredient_counts: HashMap<&str, u32> = HashMap::new();

    for line in lines {
        let tokens: Vec<&str> = line.split(" (contains ").collect();
        let ingredients: Vec<&str> = tokens[0].split_whitespace().collect();
        let allergens: Vec<&str> = tokens[1].trim_end_matches(')').split(", ").collect();

        println!("Ingredients: {:?}, Allergens: {:?}", ingredients, allergens);

        for ingredient in &ingredients {
            let new_count = ingredient_counts.get(ingredient).unwrap_or(&0) + 1;
            ingredient_counts.insert(ingredient, new_count);
        }

        for allergen in &allergens {
            let mut possible_matches: HashSet<&str> = ingredients.iter().map(|i| *i).collect();

            let existing_ingredients = allergen_map.get(allergen);
            if existing_ingredients.is_some() {
                possible_matches = existing_ingredients.unwrap().intersection(&possible_matches).map(|i| *i).collect();
            }

            allergen_map.insert(allergen, possible_matches);
        }

    }

    println!("Ingredient counts: {:?}", ingredient_counts);

    let mut total: u32 = 0;

    for (ingredient, count) in ingredient_counts.iter() {
        if !maybe_allergen(&allergen_map, ingredient) {
            println!("{} cannot contain an allergen", ingredient);
            total += count;
        }
    }

    println!("Total: {}", total);

    println!("{:?}", allergen_map);

    // Make repeated passes over the map to figure out mapping
    let mut translation: Vec<(&str, &str)> = Vec::new();
    while translation.len() < allergen_map.len() {
        let mut resolved: Vec<(&str, &str)> = Vec::new();

        for (allergen, ingredients) in &allergen_map {
            if ingredients.len() == 1 {
                resolved.push((*allergen, ingredients.iter().next().unwrap()));
            }
        }

        for (_, ingredient) in &resolved {
            for ingredients in allergen_map.values_mut() {
                ingredients.remove(ingredient);
            }
        }

        translation.extend(resolved);
    }

    translation.sort_by_key(|k| k.0);
    println!("{:?}", translation);

    println!("{}", translation.iter().map(|k| k.1).collect::<Vec<&str>>().join(","));
}
