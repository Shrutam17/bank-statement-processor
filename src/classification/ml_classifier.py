import os

import joblib

from src.utils.config_loader import load_config, resolve_path


class ModelNotFoundError(Exception):
    pass


class MLClassifier:
    def __init__(self):
        config = load_config()
        model_path = resolve_path(config["paths"]["ml_model_file"])
        vectorizer_path = resolve_path(config["paths"]["vectorizer_file"])

        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise ModelNotFoundError(
                "Trained model not found. Run scripts/train_classifier.py first."
            )

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def classify(self, description):
        features = self.vectorizer.transform([description])
        probabilities = self.model.predict_proba(features)[0]
        best_index = probabilities.argmax()
        category = self.model.classes_[best_index]
        confidence = float(probabilities[best_index])
        return category, confidence
