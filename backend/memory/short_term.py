class ShortTermMemory:
    def __init__(self):
        self.memory = []

    def add(self, item):
        self.memory.append(item)

    def get_recent(self, n=5):
        return self.memory[-n:]
