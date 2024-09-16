

class Result:
    def __init__(self):
        self.result = None
        self.channel = None
        self.obs_ratio = None
        self.exp_ratio = None

    def __str__(self):
        #if for T
        return (
            f"Exclusion result: {self.result} (1 allowed, 0 excluded)\n"
            f"Channel         : {self.channel}\n"
            f"Observed ratio  : {self.obs_ratio}\n"
            f"Expected Ratio  : {self.exp_ratio}"
        )
        #else for B

    def __repr__(self):
        return (
            f"Result("
            f"result={self.result!r}, "
            f"channel={self.channel!r}, "
            f"obs_ratio={self.obs_ratio!r}, "
            f"exp_ratio={self.exp_ratio!r})"
        )




