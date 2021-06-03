def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


class Emas:
    def __init__(self, smoothing=2) -> None:
        self.emas = {}
        self.smoothing = smoothing
        self.last_prices = []

    def add_ema(self, key, value):
        if key not in self.emas:
            if len(self.last_prices) < value:
                return False
            self.emas[key] = sum(self.last_prices[-value:]) / value
        return True

    def add_value(self, value):
        smoothing = self.smoothing
        self.last_prices.append(value)
        for k in self.emas.keys():
            key_value = int(k)
            temp = value * (smoothing / (1 + key_value)) + float(self.emas[k]) * (1 - (smoothing / (1 + key_value)))
            self.emas[k] = temp

    def get_tendency(self):
        if '5' in self.emas and '10' in self.emas:
            return self.emas['5'] > self.emas['10']
        return None
