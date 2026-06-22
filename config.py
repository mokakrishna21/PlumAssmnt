import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

def load_policy():
    with open(os.path.join(CONFIG_DIR, "policy_terms.json"), "r") as f:
        return json.load(f)

def load_test_cases():
    with open(os.path.join(CONFIG_DIR, "test_cases.json"), "r") as f:
        return json.load(f)

POLICY = load_policy()
TEST_CASES = load_test_cases()
