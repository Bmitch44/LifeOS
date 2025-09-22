

class MapperError(Exception):
    def __init__(self, source: str, target: str, e: Exception):
        self.source = source
        self.target = target
        self.e = e

    def __str__(self):
        return f"Failed to map {self.source} to {self.target}: {self.e}"

    def __repr__(self):
        return f"MapperError(source={self.source}, target={self.target}, e={self.e})"