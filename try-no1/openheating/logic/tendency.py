class Tendency:
    def __init__(self):
        self.__points = []

    def add(self, temperature):
        if len(self.__points) == 10:
            del self.__points[0]
        self.__points.append(temperature)

    def gradient(self):
        if len(self.__points) in (0, 1):
            return 0
        grad = 0
        for i in range(len(self.__points) - 1):
            grad += self.__points[i+1] - self.__points[i]
        return grad / (len(self.__points) - 1)

    def even(self):
        return 0 <= abs(self.gradient()) <= 0.3

    def rising(self):
        return self.gradient() > 0.3

    def falling(self):
        return self.gradient() < -0.3
