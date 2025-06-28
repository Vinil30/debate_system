# debate/memory.py
class DebateMemory:
    def __init__(self):
        self.data = {
            "topic": None,
            "history": []
        }

    def set_topic(self, topic: str):
        self.data["topic"] = topic

    def get(self, key: str):
        return self.data.get(key)

    def add_argument(self, speaker: str, argument: str):
        self.data["history"].append((speaker, argument))

    def get_history(self):
        return self.data["history"]
