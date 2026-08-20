import csv
import os
import sys

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.utils.config_loader import load_config, resolve_path  # noqa: E402


def load_training_data(csv_path):
    descriptions, categories = [], []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            descriptions.append(row["description"])
            categories.append(row["category"])
    return descriptions, categories


def main():
    config = load_config()
    csv_path = resolve_path(config["paths"]["training_data"])
    model_path = resolve_path(config["paths"]["ml_model_file"])
    vectorizer_path = resolve_path(config["paths"]["vectorizer_file"])

    if not os.path.exists(csv_path):
        print(f"Training data not found at {csv_path}, run generate_training_data.py first")
        return 1

    descriptions, categories = load_training_data(csv_path)

    x_train, x_test, y_train, y_test = train_test_split(
        descriptions, categories, test_size=0.2, random_state=42, stratify=categories
    )

    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_vec, y_train)

    accuracy = model.score(x_test_vec, y_test)
    print(f"Validation accuracy: {accuracy:.3f}")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print(f"Saved model to {model_path}")
    print(f"Saved vectorizer to {vectorizer_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
