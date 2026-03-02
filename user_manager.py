import json
import os
from typing import List, Dict

class UserManager:
    def __init__(self, storage_path: str = "user_preferences.json"):
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {
            "topics": [],
            "history": []
        }

    def _save_data(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_topic(self, topic: str):
        if topic not in self.data["topics"]:
            self.data["topics"].append(topic)
            self._save_data()

    def get_topics(self) -> List[str]:
        return self.data["topics"]

    def add_to_history(self, query: str):
        self.data["history"].append(query)
        # Keep only last 10
        self.data["history"] = self.data["history"][-10:]
        self._save_data()

    def get_history(self) -> List[str]:
        return self.data["history"]

if __name__ == "__main__":
    # Test stub
    mgr = UserManager()
    mgr.add_topic("AI")
    print(mgr.get_topics())
