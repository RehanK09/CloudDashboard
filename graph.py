from collections import deque

MAX_POINTS = 60


class SpeedGraph:

    def __init__(self):

        self.values = deque(maxlen=MAX_POINTS)

        for _ in range(MAX_POINTS):
            self.values.append(0)

    def add(self, speed):

        try:
            speed = float(speed)
        except:
            speed = 0

        self.values.append(speed)

    def reset(self):

        self.values.clear()

        for _ in range(MAX_POINTS):
            self.values.append(0)

    def highest(self):

        if len(self.values) == 0:
            return 0

        return max(self.values)

    def average(self):

        if len(self.values) == 0:
            return 0

        return sum(self.values) / len(self.values)

    def latest(self):

        if len(self.values) == 0:
            return 0

        return self.values[-1]

    def points(self):

        return list(self.values)

    def percent(self):

        h = self.highest()

        if h == 0:
            return [0] * len(self.values)

        return [(v / h) * 100 for v in self.values]