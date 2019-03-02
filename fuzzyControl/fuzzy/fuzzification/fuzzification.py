class Fuzzy:
    def __init__(self, input_amount):
        self.input_amount = input_amount
        self.input_fuzzy = 0

    #     pass variables to this class or get those from data.py by global

    def fuzzification(self, functype, a, b, c, d=0):
        if functype == 'Trapezoid':
            try:
                if a <= self.input_amount <= b:
                    input_fuzzy = float(self.input_amount - a) / float(b - a)
                elif b < self.input_amount < c:
                    input_fuzzy = 1.0
                elif c <= self.input_amount <= d:
                    input_fuzzy = float(self.input_amount - d) / float(c - d)
                else:
                    input_fuzzy = 0.0
                return input_fuzzy
            except ZeroDivisionError:
                input_fuzzy = 1.0
                return input_fuzzy
