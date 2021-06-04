from constants import ABAJO
from constants import ARRIBA
from ema import Emas


class Pair:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.emas = Emas()
        self.last_ema = 0
        self.last_tendency = None

    def init_emas(self, klines):
        i = 0
        while i <= 10:
            self.emas.add_value(float(klines[i][4]))
            i = i + 1
        self.emas.add_ema('5', 5)
        self.emas.add_ema('10', 10)
        while i < len(klines):
            self.emas.add_value(float(klines[i][4]))
            i = i + 1

        self.last_ema = float(klines[-1][0])

    def add_ema_value(self, time, value):
        if time > self.last_ema:
            self.emas.add_value(value)
            self.last_ema = time
            return True
        return False

    def tendency_has_changed(self):
        res = False
        direction = ARRIBA
        tendency = self.emas.get_tendency()
        if self.last_tendency is not None:
            res = self.last_tendency != tendency
            if res:
                if self.last_tendency is True and tendency is False:
                    direction = ABAJO
        self.last_tendency = tendency
        return res, direction
