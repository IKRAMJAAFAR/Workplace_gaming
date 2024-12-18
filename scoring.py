# Correct bin mapping (example)
correct_bin_mapping = {
    0: "recyclable", 
    1: "non-recyclable"
}

def update_score(item, bin_index, score):
    # Example item-to-type mapping
    trash_type_mapping = {"recyclable": "assets/trash_image.png"}

    # Update score based on the mapping
    if correct_bin_mapping.get(bin_index) == "recyclable":  # Adjust logic as needed
        score += 10
        print("Correct! +10 points")
    else:
        score -= 5
        print("Incorrect! -5 points")
    return score
