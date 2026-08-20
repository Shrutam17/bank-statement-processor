import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.classification.rule_based_classifier import RuleBasedClassifier


def test_rule_based_classifier_matches_known_keyword():
    classifier = RuleBasedClassifier()
    category, confidence = classifier.classify("SWIGGY ORDER PAYMENT")
    assert category == "Food & Dining"
    assert confidence == 1.0


def test_rule_based_classifier_returns_none_for_unknown():
    classifier = RuleBasedClassifier()
    category, confidence = classifier.classify("XYZQWERTY UNKNOWN MERCHANT")
    assert category is None
    assert confidence == 0.0
