from names_data import first_names, surnames, districts, wards, Cit_numbers
import random
import json

# Define the tag set and create a mapping from tag name to ID.
TAGS = ["O", "CIT-NO", "SEX", "B-NAME", "I-NAME", "YEAR", "MONTH", "DAY",
        "B-DISTRICT", "B-WARD", "B-NO", "I-DISTRICT", "I-WARD", "I-NO"]
TAG2ID = {tag: i for i, tag in enumerate(TAGS)}

def distort_token(token):
    """
    Simulate OCR-style distortions on a token with increased noise.
    - 40% chance to change the token's case.
    - 20% chance to remove one random character.
    - 20% chance to substitute characters (e.g. 'O' → '0' or 'l' → '1').
    """
    # With a 40% chance, change the case.
    if random.random() < 0.4:
        token = token.lower() if random.random() < 0.5 else token.upper()
    # With a 20% chance, remove one random character (if token length > 1).
    if len(token) > 1 and random.random() < 0.1:
        pos = random.randint(0, len(token) - 1)
        token = token[:pos] + token[pos+1:]
    # With a 20% chance, perform a simple character substitution.
    return token

def random_noise():
    """
    Generate a short random noise word to simulate spurious tokens in noisy OCR output.
    The word will have between 1 and 3 letters.
    """
    length = random.randint(1, 3)
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))

def generate_example():
    # Generate random field values.
    cit_No    = random.choice(Cit_numbers)
    gender    = random.choice(["male", "female"])
    f_name    = random.choice(first_names)
    l_name    = random.choice(surnames)
    DOB_year  = random.randint(1970, 2010)
    DOB_month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    DOB_day   = random.randint(1, 31)
    Birth_Dis = random.choice(districts)
    Birth_ward= random.choice(wards)
    Birth_no  = random.randint(1, 20)
    per_Dis   = random.choice(districts)
    per_ward  = random.choice(wards)
    per_no    = random.randint(1, 20)
    
    # Build the list of (token, tag) pairs in the intended order.
    token_tag_pairs = [
        ("details",          "O"),
        ("Citizenship",      "O"),
        ("Certificate",      "O"),
        ("No",               "O"),
        (cit_No,             "CIT-NO"),
        ("Sex",              "O"),
        (gender,             "SEX"),
        ("Full",             "O"),
        ("Name",             "O"),
        (f_name,             "B-NAME"),
        (l_name,             "I-NAME"),
        ("Date",             "O"),
        ("of",               "O"),
        ("Birth",            "O"),
        ("AD",               "O"),
        (f"Year{DOB_year}",  "YEAR"),
        ("Month",            "O"),
        (DOB_month,          "MONTH"),
        ("Day",              "O"),
        (str(DOB_day),       "DAY"),
        ("Birth",            "O"),
        ("place",            "O"),
        ("District",         "O"),
        (Birth_Dis,          "B-DISTRICT"),
        ("VDC",              "O"),
        (Birth_ward,         "B-WARD"),
        ("Ward",             "O"),
        ("No"+str(Birth_no), "B-NO"),
        ("Permanent",        "O"),
        ("Address",          "O"),
        ("District",         "O"),
        (per_Dis,            "I-DISTRICT"),
        ("Municipality",     "O"),
        (per_ward,           "I-WARD"),
        ("Ward",             "O"),
        ("No" +str(per_no),  "I-NO")
    ]
    
    tokens = []
    ner_tags = []
    
    # Process each token with extra noise insertions.
    for token, tag in token_tag_pairs:
        # With a 30% chance, insert a noise token (word with up to 3 letters) before the current token.
        if random.random() < 0.3:
            noise_token = random_noise()
            tokens.append(noise_token)
            ner_tags.append(TAG2ID["O"])
        
        # Distort the token and add it.
        token_str = str(token)
        distorted_token = distort_token(token_str)
        tokens.append(distorted_token)
        ner_tags.append(TAG2ID[tag])
        
        # With a 30% chance, insert an extra noise token right after the current token.
        if random.random() < 0.3:
            noise_token = random_noise()
            tokens.append(noise_token)
            ner_tags.append(TAG2ID["O"])
    
    return {"tokens": tokens, "ner_tags": ner_tags}

def generate_data(num_examples=2000):
    data = []
    for _ in range(num_examples):
        data.append(generate_example())
    return data

if __name__ == "__main__":
    print("Generating data with increased noise (noise tokens as short words)...")
    data = generate_data()
    with open("noisy_ner_datav3.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Data saved to ner_data.json")
