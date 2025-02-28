import torch
from collections import Counter
from transformers import AutoModelForTokenClassification, AutoTokenizer


model = AutoModelForTokenClassification.from_pretrained("../model/V1/saved_model")
tokenizer = AutoTokenizer.from_pretrained("../model/V1/tokenizer_saved_model")

tags = ["O", "CIT-NUM", "SEX", "B-NAME", "I-NAME", "YEAR", "MONTH", "DAY", "B-DISTRICT", "B-WARD", "B-NO", "I-DISTRICT", "I-WARD", "I-NO"]
id2label = {i: label for i, label in enumerate(tags)}
label2id = {v: k for k, v in id2label.items()}

def get_tags(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    predicted_label_ids = outputs.logits.argmax(-1).squeeze()
    predicted_labels = [id2label[id.item()] for id in predicted_label_ids]

    tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids.squeeze())
    word_ids = inputs.word_ids()


    words = []
    current_word = ""
    current_labels = []

    for token, word_id, label in zip(tokens, word_ids, predicted_labels):
        if word_id is None:
            continue

        if word_id != len(words):

            if current_word:
                label_counts = Counter(current_labels)
                most_common_label = max(label_counts, key=label_counts.get)

                if "O" in label_counts and len(label_counts) > 1:
                    del label_counts["O"]
                    most_common_label = max(label_counts, key=label_counts.get)

                words.append((current_word, most_common_label))

            current_word = token.replace("##", "")
            current_labels = [label]
        else:

            current_word += token.replace("##", "")
            current_labels.append(label)


    if current_word:
        label_counts = Counter(current_labels)
        most_common_label = max(label_counts, key=label_counts.get)

        if "O" in label_counts and len(label_counts) > 1:
            del label_counts["O"]
            most_common_label = max(label_counts, key=label_counts.get)

        words.append((current_word, most_common_label))

    return words
