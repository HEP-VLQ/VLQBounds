
class Result:
    def __init__(self):
        self.allowed_or_excluded = None
        self.channel = None
        self.model_observed_ratio = None

    def __str__(self):
        return f"Top Bounds Result: {self.allowed_or_excluded} (1 allowed, 0 excluded)\n" + \
            f"Channel : {self.channel}\nObserved Ratio : {self.model_observed_ratio}"


