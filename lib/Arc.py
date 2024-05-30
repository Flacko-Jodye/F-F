class Arc:
    def __init__(self, from_node, to_node, cost, lower_bound, upper_bound):
        self.from_node = from_node # i
        self.to_node = to_node # j
        self.cost = cost # bzw. Distanz
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        # Für FF später
        # self.flow = 0
        # self.reverse = None