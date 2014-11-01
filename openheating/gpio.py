(IN, OUT) = valid_directions = range(2)

class GPIOManager:
    def __init__(self, basedir, managed_ios):
        self.__ios = {}
        for num, direction in managed_ios:
            if num in self.__ios:
                raise HeatingException('duplicate GPIO #'+str(num))
            

class GPIO:
    pass
