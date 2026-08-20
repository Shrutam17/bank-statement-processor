import json

from src.utils.config_loader import load_config, resolve_path


class RuleBasedClassifier:
    def __init__(self):
        config = load_config()
        keywords_path = resolve_path(config["paths"]["category_keywords"])
        with open(keywords_path, "r") as f:
            self.category_keywords = json.load(f)

    def classify(self, description):
        description_lower = description.lower()
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category, 1.0
        return None, 0.0
