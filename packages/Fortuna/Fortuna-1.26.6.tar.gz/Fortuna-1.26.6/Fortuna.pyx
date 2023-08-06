#!python3
#distutils: language = c++
from time import time_ns
from statistics import mode, mean, StatisticsError
from fortuna_extras import version


cdef extern from "Fortuna.hpp":
    long long _random_range "Fortuna::random_range"(long long, long long)
    long long _random_below "Fortuna::random_below"(long long)
    long double _random_float "Fortuna::random_float"()
    long long _d "Fortuna::d"(long long)
    long long _dice "Fortuna::dice"(long long, long long)
    int _ability_dice "Fortuna::ability_dice"(int)
    int _percent_true "Fortuna::percent_true"(int)
    int _percent_true_float "Fortuna::percent_true_float"(long double)
    long long _plus_or_minus "Fortuna::plus_or_minus"(long long)
    long long _plus_or_minus_linear "Fortuna::plus_or_minus_linear"(long long)
    long long _plus_or_minus_curve "Fortuna::plus_or_minus_curve"(long long)
    long long _stretched_bell "Fortuna::stretched_bell"(long long)
    long long _plus_or_minus_linear_down "Fortuna::plus_or_minus_linear_down"(long long)
    long long _plus_or_minus_curve_down "Fortuna::plus_or_minus_curve_down"(long long)
    long long _zero_flat "Fortuna::zero_flat"(long long)
    long long _zero_cool "Fortuna::zero_cool"(long long)
    long long _zero_extreme "Fortuna::zero_extreme"(long long)
    long long _max_cool "Fortuna::max_cool"(long long)
    long long _max_extreme "Fortuna::max_extreme"(long long)
    long long _mostly_middle "Fortuna::mostly_middle"(long long)
    long long _mostly_center "Fortuna::mostly_center"(long long)
    long long _mostly_not_middle "Fortuna::mostly_not_middle"(long long)
    long long _mostly_not_center "Fortuna::mostly_not_center"(long long)
    long long _min_max "Fortuna::min_max"(long long, long long, long long)


def get_impl() -> str:
    return f"Fortuna Extension v{version}"

def plus_or_minus_linear_down(n):
    return _plus_or_minus_linear_down(n)


def plus_or_minus_curve_down(n):
    return _plus_or_minus_curve_down(n)


def random_float() -> float:
    return _random_float()


def percent_true_float(num: float = 50.0) -> bool:
    return _percent_true_float(num) == 1


def random_range(lo, hi):
    return _random_range(lo, hi)


def random_below(num):
    return _random_below(num)


def d(sides):
    return _d(sides)


def dice(rolls, sides):
    return _dice(rolls, sides)


def ability_dice(num):
    return _ability_dice(num)


def min_max(n, lo, hi):
    return _min_max(n, lo, hi)


def percent_true(int num = 50) -> bool:
    return _percent_true(num) == 1


def plus_or_minus(num):
    return _plus_or_minus(num)


def plus_or_minus_linear(num):
    return _plus_or_minus_linear(num)


def plus_or_minus_curve(num):
    return _plus_or_minus_curve(num)


def stretched_bell(num):
    return _stretched_bell(num)


def zero_flat(num):
    return _zero_flat(num)


def zero_cool(num):
    return _zero_cool(num)


def zero_extreme(num):
    return _zero_extreme(num)


def max_cool(num):
    return _max_cool(num)


def max_extreme(num):
    return _max_extreme(num)


def mostly_middle(num):
    return _mostly_middle(num)


def mostly_center(num):
    return _mostly_center(num)


def mostly_not_middle(num):
    return _mostly_not_middle(num)


def mostly_not_center(num):
    return _mostly_not_center(num)


def random_value(arr):
    size = len(arr)
    return arr[_random_below(size)]


def pop_random_value(list arr):
    size = len(arr)
    return arr.pop(_random_below(size))


def cumulative_weighted_choice(table):
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


def flatten(itm, flat: bool = True):
    if flat is False or not callable(itm):
        return itm
    else:
        try:
            return flatten(itm())
        except TypeError:
            return itm


def shuffle(arr: list):
    size = len(arr)
    for i in range(1, size):
        j = _zero_flat(i)
        arr[i], arr[j] = arr[j], arr[i]


class TruffleShuffle:
    __slots__ = ("data", "flat", "half_len")

    def __init__(self, arr, flat=True):
        self.data = list(arr)
        arr_len = len(self.data)
        assert arr_len is not 0, "Input Error, Empty Container"
        self.flat = flat
        self.half_len = arr_len // 2
        shuffle(self.data)

    def __call__(self):
        return flatten(self.beta_rotate(), self.flat)

    def __repr__(self):
        return f"TruffleShuffle({self.data}, flat={self.flat})"

    def beta_rotate(self):
        result = self.data.pop()
        self.data.insert(_zero_flat(self.half_len), result)
        return result


class QuantumMonty:
    __slots__ = ("arr", "flat", "data", "max_id", "truffle_shuffle")

    def __init__(self, arr, flat=True):
        self.arr = arr
        self.flat = flat
        self.data = tuple(arr)
        self.max_id = len(self.data) - 1
        self.truffle_shuffle = TruffleShuffle(self.data, flat)

    def __call__(self):
        return self.quantum_monty()

    def __repr__(self):
        return f"QuantumMonty({self.arr}, flat={self.flat})"

    def dispatch(self, quantum_bias="monty"):
        return {
            "monty": self.quantum_monty,
            "cycle": self.truffle_shuffle,
            "front": self.mostly_front,
            "middle": self.mostly_middle,
            "back": self.mostly_back,
            "first": self.mostly_first,
            "center": self.mostly_center,
            "last": self.mostly_last,
            "flat": self.mostly_flat,
            "not_middle": self.mostly_not_middle,
            "not_center": self.mostly_not_center,
            "not_monty": self.quantum_not_monty,
        }[quantum_bias]

    def quantum_monty(self):
        return flatten(random_value((
            self.mostly_front,
            self.mostly_middle,
            self.mostly_back,
            self.mostly_first,
            self.mostly_center,
            self.mostly_last,
        )), self.flat)

    def quantum_not_monty(self):
        return flatten(random_value((
            self.mostly_front,
            self.mostly_not_middle,
            self.mostly_back,
            self.mostly_first,
            self.mostly_not_center,
            self.mostly_last,
        )), self.flat)

    def mostly_flat(self):
        return flatten(random_value(self.data), self.flat)

    def mostly_cycle(self):
        return self.truffle_shuffle()

    def mostly_front(self):
        return flatten(self.data[_zero_cool(self.max_id)], self.flat)

    def mostly_back(self):
        return flatten(self.data[_max_cool(self.max_id)], self.flat)

    def mostly_middle(self):
        return flatten(self.data[_mostly_middle(self.max_id)], self.flat)

    def mostly_first(self):
        return flatten(self.data[_zero_extreme(self.max_id)], self.flat)

    def mostly_last(self):
        return flatten(self.data[_max_extreme(self.max_id)], self.flat)

    def mostly_center(self):
        return flatten(self.data[_mostly_center(self.max_id)], self.flat)

    def mostly_not_center(self):
        return flatten(self.data[_mostly_not_center(self.max_id)], self.flat)

    def mostly_not_middle(self):
        return flatten(self.data[_mostly_not_middle(self.max_id)], self.flat)


class FlexCat:
    __slots__ = ("flat", "x_bias", "y_bias", "data", "random_cat", "random_selection")

    def __init__(self, data, y_bias="front", x_bias="cycle", flat=True):
        self.flat = flat
        self.y_bias = y_bias
        self.x_bias = x_bias
        self.data = data
        self.random_cat = QuantumMonty(tuple(data.keys())).dispatch(y_bias)
        self.random_selection = {
            key: QuantumMonty(sequence, flat).dispatch(x_bias) for key, sequence in data.items()
        }

    def __call__(self, cat_key=None):
        return self.random_selection[cat_key if cat_key else self.random_cat()]()

    def __repr__(self):
        return f"FlexCat({self.data}, y_bias='{self.y_bias}', x_bias='{self.x_bias}', flat={self.flat})"


class RelativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"RelativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


class CumulativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
        self.flat = flat
        data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        optimized_data = sorted(data, key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"CumulativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


def analytic_continuation(func: staticmethod, num):
    if num < 0:
        return -func(-num)
    elif num == 0:
        return 0
    else:
        return func(num)


def timer(func: staticmethod, *args, **kwargs):
    def if_mode(arr):
        try:
            return mode(arr)
        except StatisticsError:
            return False
    tl = []
    outer_cycles = 32
    inner_cycles = 32
    for _ in range(outer_cycles):
        start = time_ns()
        for _ in range(inner_cycles):
            func(*args, **kwargs)
        end = time_ns()
        tl.append((end - start) // inner_cycles)
    output = (
        f"Min: {min(tl)}ns",
        f"Mode: {str(if_mode(tl)) + 'ns' if if_mode(tl) else 'N/A'}",
        f"Mean: {int(mean(tl))}ns",
        f"Max: {max(tl)}ns",
    )
    print("Time: " + ", ".join(output))


def distribution(func: staticmethod, *args, num_cycles=10000, **kwargs):
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    unique_results = list(set(results))
    if all([hasattr(x, "__lt__") for x in unique_results]):
        unique_results.sort()
    result_obj = {
        key: f"{results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f"{key}: {val}")


def distribution_timer(func: staticmethod, *args, **kwargs):
    timer(func, *args, **kwargs)
    distribution(func, *args, **kwargs)
    print("")
