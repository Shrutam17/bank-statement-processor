from src.classification.ml_classifier import MLClassifier, ModelNotFoundError
from src.classification.rule_based_classifier import RuleBasedClassifier
from src.utils.config_loader import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ClassifierEngine:
    def __init__(self):
        config = load_config()
        self.fallback_category = config["classification"]["fallback_category"]
        self.ml_confidence_threshold = config["classification"]["ml_confidence_threshold"]

        self.rule_classifier = RuleBasedClassifier()

        try:
            self.ml_classifier = MLClassifier()
        except ModelNotFoundError:
            logger.warning("ML model not found, classification will use rules only")
            self.ml_classifier = None

    def classify_transaction(self, description):
        category, confidence = self.rule_classifier.classify(description)
        if category:
            return {"category": category, "confidence": confidence, "method": "rule"}

        if self.ml_classifier:
            category, confidence = self.ml_classifier.classify(description)
            if confidence >= self.ml_confidence_threshold:
                return {"category": category, "confidence": confidence, "method": "ml"}

        return {"category": self.fallback_category, "confidence": 0.0, "method": "fallback"}

    def classify_batch(self, transactions):
        for txn in transactions:
            result = self.classify_transaction(txn.get("description", ""))
            txn["category"] = result["category"]
            txn["classification_confidence"] = result["confidence"]
            txn["classification_method"] = result["method"]
        return transactions
