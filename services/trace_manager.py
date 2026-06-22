class TraceManager:
    def __init__(self):
        self._trace = []

    def add(self, message, details=None):
        entry = {"step": message, "details": details or {}}
        self._trace.append(entry)

    def get_trace(self):
        return self._trace.copy()