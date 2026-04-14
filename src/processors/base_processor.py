class BaseProcessor:
    def process(self, data):
        raise NotImplementedError("process() must be implemented in subclasses.")
