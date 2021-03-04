class PIDController:
    def __init__(self, k_p, k_i, k_d, target):
        self.KP = k_p
        self.KI = k_i
        self.KD = k_d # not using dt as it is essentially constant
        self.TARGET = target
        self.reset()

    def __call__(self, value):
        if self._last_error is None:
            self._last_error = value
            return value
        else:
            error = self.TARGET - value
            self._integral += error
            output = self.KP*error + self.KI*self._integral + self.KD*(error-self._last_error)
            self._last_error = error
            return output

    def reset(self):
        self._last_error = None
        self._integral = 0