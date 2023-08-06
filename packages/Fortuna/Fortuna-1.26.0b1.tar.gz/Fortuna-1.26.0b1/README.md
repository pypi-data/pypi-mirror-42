# Fortuna: Fast & Flexible Random Value Generators
Fortuna replaces much of the functionality of Python's Random module, often achieving 10x better performance. However, the most interesting bits of Fortuna are found in the high-level abstractions like FlexCat, QuantumMonty and TruffleShuffle.

The core functionality of Fortuna is based on the Mersenne Twister Algorithm by Makoto Matsumoto (松本 眞) and Takuji Nishimura (西村 拓士). Fortuna is not appropriate for cryptography of any kind. Fortuna is for games, data science, AI and experimental programming, not security.

The Fortuna generator was designed to use hardware seeding exclusively. This allows the generator to be completely encapsulated.

Installation: `$ pip install Fortuna` or download and build it from source. Installation on some platforms may require the latest version of Cython, python3 dev tools, and a modern C++17 compiler. Fortuna is designed, built and tested for MacOS X, and also happens to work out-of-the-box with many flavors of Linux and Unix. Fortuna is not supported on Windows.

Fortuna is built for the default CPython implementation standard, other implementations may or may not support c-extensions like Fortuna. A pure Python version of Fortuna is included in the extras folder. The Fortuna c-extension is roughly an order of magnitude faster than the pure Python version, but they offer the same API and functionality.


## Documentation Table of Contents
```
I.   Fortuna Core Functions
        a. Random Numbers
        b. Random Truth
        c. Random Sequence Values
        d. Random Table Values

II.  Fortuna Abstraction Classes
        a. Sequence Wrappers
            1. TruffleShuffle
            2. QuantumMonty
        b. Weighted Table Wrappers
            1. Cumulative Weighted Choice
            2. Relative Weighted Choice
        c. Dictionary Wrapper
            1. FlexCat

III. Test Suite, output distributions and performance data.

IV.  Development Log

V.   Legal Information

```

---

## Fortuna Random Functions
### Random Numbers
`Fortuna.random_range(lo: int, hi: int) -> int`. Returns a random integer in range [lo..hi] inclusive. Up to 15x faster than `random.randint()`. Flat uniform distribution.

`Fortuna.random_below(num: int) -> int`. Returns a random integer in the exclusive range [0..num) for positive values of num. Flat uniform distribution.

`Fortuna.d(sides: int) -> int`. Represents a single die roll of a given size die. Returns a random integer in the range [1..sides]. Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int`. Returns a random integer in range [X..Y] where X = rolls and Y = rolls * sides. The return value represents the sum of multiple rolls of the same size die. Geometric distribution based on the number and size of the dice rolled. Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in range [-num..num]. Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int`. Returns a random integer in range [-num..num]. Zero peak geometric distribution, up triangle.

`Fortuna.plus_or_minus_curve(num: int) -> int`. Returns a random integer in the bounded range [-num..num]. Zero peak gaussian distribution, bounded stretched bell curve: mean = 0, variance = num / pi.

`Fortuna.plus_or_minus_linear_down(num: int) -> int`. Returns a random integer in range [-num..num]. Edge peak geometric distribution, down triangle. Inverted plus_or_minus_linear.

`Fortuna.plus_or_minus_curve_down(num: int) -> int`. Returns a random integer in the range [-num..num]. Edge peak gaussian distribution, upside down bell curve. Inverted plus_or_minus_curve.

`Fortuna.zero_flat(num: int) -> int`. Returns a random integer in range [0..num]. Flat uniform distribution.

`Fortuna.zero_cool(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, geometric distribution, lefthand triangle.

`Fortuna.zero_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, gaussian distribution, half bell curve.

`Fortuna.max_cool(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), geometric distribution, righthand triangle.

`Fortuna.max_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), gaussian distribution, half bell curve.

`Fortuna.mostly_middle(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), geometric distribution, up triangle. Ranges that span an even number of values will have two dominant values in the middle rather than one, this will guarantee that the probability distribution is always symmetrical.

`Fortuna.mostly_center(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), gaussian distribution, bell curve: mean = num / 2, variance = num / pi.

`Fortuna.mostly_not_middle(num: int) -> int`. Returns a random integer in range [0..num]. Edge peaks, geometric distribution, down triangle. Ranges that span an even number of values will have two dominant values in the middle rather than one, this will guarantee that the probability distribution is always symmetrical.

`Fortuna.mostly_not_center(num: int) -> int`. Returns a random integer in range [0..num]. Edge peaks, gaussian distribution, upside down bell curve.

`Fortuna.random_float() -> float`. Returns a random float in range [0.0..1.0) exclusive. Same as random.random().


### Random Truth
`Fortuna.percent_true(num: int) -> bool`. Always returns False if num is 0 or less, always returns True if num is 100 or more. Any value of num in range [1..99] will produce True or False based on the value of num - the probability of True as a percentage.

`Fortuna.percent_true_float(num: float) -> bool`. Always returns False if num is 0.0 or less, always returns True if num is 100.0 or more. It will produce True or False based on the value of num - the probability of True as a percentage. Same as percent_true but with floating point accuracy.


### Random Sequence Values
`Fortuna.random_value(arr) -> value`. Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. Up to 10x faster than random.choice().

`Fortuna.pop_random_value(arr: list) -> value`. Returns and removes a random value from a sequence list, uniform distribution, destructive. Not included in the test suite due to it's destructive nature. This is the only destructive function in the module, use with care. It will raise an error if the list is empty.

`Fortuna.shuffle(arr: list) -> None`. Alternate Fisher-Yates Shuffle Algorithm. More than an order of magnitude faster than random.shuffle().


### Random Table Values
`Fortuna.cumulative_weighted_choice(table) -> value`. Core function for the WeightedChoice base class. Produces a custom distribution of values based on cumulative weights. Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. Weights must be unique positive integers. See WeightedChoice class for a more comprehensive solution that verifies and optimizes the table. Up to 15x faster than random.choices()


## Fortuna Random Classes
### Sequence Wrappers
#### Truffle Shuffle
Returns a random value from the wrapped sequence.

Produces a uniform distribution with a wide spread. Longer sequences will naturally push duplicates even farther apart. This behavior gives rise to output sequences that seem less mechanical than other random sequences.

Flatten: TruffleShuffle will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True. A callable object is any function, method or lambda.

- Constructor takes a copy of a sequence (generator, list or tuple) of arbitrary values.
- Values can be any Python object that can be passed around.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the input sequence.

```python
from Fortuna import TruffleShuffle


truffle_shuffle = TruffleShuffle(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])
truffle_shuffle()  # returns a random value, cycled uniform distribution.
```


#### The Quantum Monty
QuantumMonty is a set of strategies for producing random values from a sequence where the probability of each value is based on the method or "monty" you choose. For example: the mostly_front monty produces random values where the beginning of the sequence is geometrically more common than the back. This always produces a 45 degree slope down no matter how many values are in the data.

The Quantum Monty Algorithm is special, it produces values by overlapping the probability waves of six of the other methods. The distribution it produces is a gentle curve up towards the middle with a distinct bump in the center of the sequence.

Flatten: QuantumMonty will recursively unpack callable objects returned from the data set. Callable objects that require arguments are not called. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence (generator, list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may vary slightly.

```python
from Fortuna import QuantumMonty


quantum_monty = QuantumMonty(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])

# Each of the following methods will return a random value from the sequence.
quantum_monty.mostly_front()        # Mostly from the front of the list (geometric descending)
quantum_monty.mostly_middle()       # Mostly from the middle of the list (geometric pyramid)
quantum_monty.mostly_back()         # Mostly from the back of the list (geometric ascending)
quantum_monty.mostly_first()        # Mostly from the very front of the list (stretched gaussian descending)
quantum_monty.mostly_center()       # Mostly from the very center of the list (stretched gaussian bell curve)
quantum_monty.mostly_last()         # Mostly from the very back of the list (stretched gaussian ascending)
quantum_monty.quantum_monty()       # Quantum Monty Algorithm. Overlapping probability waves.
quantum_monty.mostly_flat()         # Uniform flat distribution (see Fortuna.random_value if this is the only behavior you need.)
quantum_monty.mostly_cycle()        # Cycled uniform flat distribution (see TruffleShuffle)
quantum_monty.mostly_not_middle()   # Mostly from the edges of the list (geometric upside down pyramid)
quantum_monty.mostly_not_center()   # Mostly from the outside edges of the list (inverted gaussian bell curve)
quantum_monty.quantum_not_monty()   # Inverted Quantum Monty Algorithm.
```


### Table Wrappers
#### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values. Both are up to 10x faster than random.choices()

Flatten: Both will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must contain a weight and a value.
- Weights must be positive integers.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance.
The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.


##### Cumulative Weight Strategy
_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cumulative_weighted_choice = CumulativeWeightedChoice([
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
])

cumulative_weighted_choice()  # returns a weighted random value
```


##### Relative Weight Strategy
Relative weights work just like cumulative weights, except each weight is comparable to the others.


```python
from Fortuna import RelativeWeightedChoice


relative_weighted_choice = RelativeWeightedChoice([
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
])

relative_weighted_choice()  # returns a weighted random value
```


### Dictionary Wrappers
#### FlexCat
FlexCat wraps a dictionary of sequences. When the primary method is called it returns a random value from one of the sequences. It takes two optional keyword arguments to specify the algorithms used to make random selections.

By default, FlexCat will use y_bias="front" and x_bias="cycle", this will make the top of the data structure geometrically more common than the bottom and cycle the sequences. This config is known as Top Cat, it produces a descending-step cycled distribution for the data. Many other combinations are possible (12 algorithms, 2 dimensions = 144 possible configurations).

FlexCat generally works best if all sequences in a set are sufficiently large and close to the same size, this is not enforced. Values in a shorter sequence will naturally be more common, since probability balancing between categories is not considered. For example: in a flat/flat set where it might be expected that all values have equal probability (and they would, given sequences with equal length). However, values in a sequence half the size of the others in the set would have exactly double the probability of the other items. This effect scales with the size delta and affects all nine methods. Cross category balancing might be considered for a future release.

Flatten: FlexCat will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.


Algorithm Options: _See QuantumMonty & TruffleShuffle for more details._
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, stretched gaussian descending
- center, stretched gaussian bell
- last, stretched gaussian ascending
- monty, The Quantum Monty
- flat, uniform flat
- cycle, TruffleShuffle uniform flat
- not_middle, favors the top and bottom of the list, geometric upside down pyramid
- not_center, favors the top and bottom of the list, stretched gaussian upside down bell
- not_monty, inverted Quantum Monty

```python
from Fortuna import FlexCat


flex_cat = FlexCat({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}, y_bias="front", x_bias="cycle")

flex_cat()          # returns a random value from a random category
flex_cat("Cat_A")   # returns a random value from "Cat_A"
flex_cat("Cat_B")   #                             "Cat_B"
flex_cat("Cat_C")   #                             "Cat_C"
```


## Fortuna Test Suite
#### Testbed:
- **Software:** _macOS 10.14.3, Python 3.7.2, Fortuna Extension._
- **Hardware:** _Intel 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD._

```
Fortuna Extension v1.25.5

Base Cases: random module
-------------------------------------------------------------------------
random.randint(-6, 6):
Time: Min: 1343ns, Mode: 1406ns, Mean: 1413ns, Max: 1812ns
-6: 7.82%
-5: 7.68%
-4: 7.77%
-3: 7.7%
-2: 8.15%
-1: 7.9%
0: 7.58%
1: 7.69%
2: 7.94%
3: 7.5%
4: 7.42%
5: 7.62%
6: 7.23%

random.randrange(-6, 6):
Time: Min: 1125ns, Mode: 1156ns, Mean: 1174ns, Max: 1687ns
-6: 8.05%
-5: 7.88%
-4: 8.16%
-3: 8.19%
-2: 8.72%
-1: 8.23%
0: 8.2%
1: 8.4%
2: 8.48%
3: 8.44%
4: 8.75%
5: 8.5%

random.choice(population):
Time: Min: 687ns, Mode: 687ns, Mean: 758ns, Max: 1843ns
Apple: 14.09%
Banana: 14.35%
Cherry: 14.29%
Grape: 14.64%
Lime: 14.11%
Orange: 14.48%
Pineapple: 14.04%

random.choices(population, cum_weights=cum_weights):
Time: Min: 1718ns, Mode: 1781ns, Mean: 1817ns, Max: 2406ns
Apple: 20.02%
Banana: 11.5%
Cherry: 5.71%
Grape: 28.45%
Lime: 8.7%
Orange: 11.27%
Pineapple: 14.35%

random.choices(population, weights=rel_weights):
Time: Min: 2125ns, Mode: 2156ns, Mean: 2201ns, Max: 3375ns
Apple: 19.57%
Banana: 11.16%
Cherry: 5.85%
Grape: 29.39%
Lime: 8.65%
Orange: 11.71%
Pineapple: 13.67%

random.shuffle(population):
Time: Min: 4593ns, Mode: 4718ns, Mean: 4774ns, Max: 5468ns

random.random():
Time: Min: 31ns, Mode: 31ns, Mean: 46ns, Max: 93ns


Test Cases: Fortuna Functions
-------------------------------------------------------------------------
random_range(-6, 6):
Time: Min: 62ns, Mode: 62ns, Mean: 68ns, Max: 125ns
-6: 7.92%
-5: 7.66%
-4: 7.73%
-3: 8.17%
-2: 7.8%
-1: 7.63%
0: 7.74%
1: 7.65%
2: 7.81%
3: 7.84%
4: 7.1%
5: 7.37%
6: 7.58%

random_below(6):
Time: Min: 62ns, Mode: 62ns, Mean: 62ns, Max: 93ns
0: 17.57%
1: 15.94%
2: 16.2%
3: 16.62%
4: 16.82%
5: 16.85%

d(6):
Time: Min: 31ns, Mode: 62ns, Mean: 62ns, Max: 93ns
1: 16.92%
2: 15.99%
3: 16.75%
4: 17.14%
5: 16.09%
6: 17.11%

dice(3, 6):
Time: Min: 93ns, Mode: 125ns, Mean: 161ns, Max: 1562ns
3: 0.34%
4: 1.51%
5: 2.7%
6: 4.5%
7: 7.1%
8: 9.66%
9: 11.06%
10: 12.76%
11: 12.41%
12: 12.14%
13: 9.67%
14: 6.66%
15: 4.58%
16: 2.84%
17: 1.62%
18: 0.45%

plus_or_minus(6):
Time: Min: 62ns, Mode: 62ns, Mean: 65ns, Max: 93ns
-6: 7.54%
-5: 8.01%
-4: 8.11%
-3: 7.14%
-2: 7.39%
-1: 7.47%
0: 7.69%
1: 7.79%
2: 8.07%
3: 7.71%
4: 7.54%
5: 7.93%
6: 7.61%

plus_or_minus_linear(6):
Time: Min: 62ns, Mode: 93ns, Mean: 85ns, Max: 93ns
-6: 2.27%
-5: 3.68%
-4: 5.78%
-3: 8.01%
-2: 10.09%
-1: 12.48%
0: 14.45%
1: 12.16%
2: 10.32%
3: 8.0%
4: 6.51%
5: 4.16%
6: 2.09%

plus_or_minus_curve(6):
Time: Min: 125ns, Mode: 125ns, Mean: 131ns, Max: 156ns
-6: 0.22%
-5: 0.62%
-4: 2.36%
-3: 6.05%
-2: 11.68%
-1: 18.23%
0: 21.39%
1: 17.82%
2: 11.85%
3: 6.17%
4: 2.66%
5: 0.72%
6: 0.23%

plus_or_minus_linear_down(6):
Time: Min: 187ns, Mode: 218ns, Mean: 244ns, Max: 968ns
-6: 12.98%
-5: 10.83%
-4: 9.38%
-3: 7.22%
-2: 5.07%
-1: 3.43%
0: 1.76%
1: 3.88%
2: 5.65%
3: 7.94%
4: 8.99%
5: 10.29%
6: 12.58%

plus_or_minus_curve_down(6):
Time: Min: 250ns, Mode: 281ns, Mean: 314ns, Max: 906ns
-6: 16.81%
-5: 14.92%
-4: 10.16%
-3: 4.75%
-2: 2.08%
-1: 0.65%
0: 0.12%
1: 0.63%
2: 2.18%
3: 5.29%
4: 10.92%
5: 14.71%
6: 16.78%

zero_flat(6):
Time: Min: 31ns, Mode: 62ns, Mean: 63ns, Max: 93ns
0: 13.62%
1: 14.76%
2: 14.21%
3: 14.98%
4: 13.96%
5: 14.58%
6: 13.89%

zero_cool(6):
Time: Min: 93ns, Mode: 125ns, Mean: 129ns, Max: 156ns
0: 25.23%
1: 21.32%
2: 18.44%
3: 14.28%
4: 10.45%
5: 6.76%
6: 3.52%

zero_extreme(6):
Time: Min: 156ns, Mode: 187ns, Mean: 204ns, Max: 281ns
0: 33.34%
1: 30.23%
2: 20.55%
3: 10.16%
4: 4.31%
5: 1.15%
6: 0.26%

max_cool(6):
Time: Min: 93ns, Mode: 125ns, Mean: 158ns, Max: 718ns
0: 3.74%
1: 6.65%
2: 10.61%
3: 14.82%
4: 18.11%
5: 21.07%
6: 25.0%

max_extreme(6):
Time: Min: 156ns, Mode: 187ns, Mean: 204ns, Max: 250ns
0: 0.3%
1: 1.03%
2: 3.76%
3: 10.13%
4: 20.44%
5: 30.85%
6: 33.49%

mostly_middle(6):
Time: Min: 62ns, Mode: 93ns, Mean: 79ns, Max: 93ns
0: 6.35%
1: 12.14%
2: 18.48%
3: 25.08%
4: 18.8%
5: 13.16%
6: 5.99%

mostly_center(6):
Time: Min: 125ns, Mode: 125ns, Mean: 133ns, Max: 156ns
0: 0.55%
1: 5.34%
2: 23.82%
3: 40.03%
4: 24.11%
5: 5.68%
6: 0.47%

mostly_not_middle(6):
Time: Min: 156ns, Mode: 187ns, Mean: 180ns, Max: 218ns
0: 21.4%
1: 15.45%
2: 10.26%
3: 5.26%
4: 10.79%
5: 15.23%
6: 21.61%

mostly_not_center(6):
Time: Min: 187ns, Mode: 250ns, Mean: 250ns, Max: 281ns
0: 28.4%
1: 17.32%
2: 3.68%
3: 0.32%
4: 4.08%
5: 17.59%
6: 28.61%

random_value(population):
Time: Min: 31ns, Mode: 62ns, Mean: 56ns, Max: 93ns
Apple: 14.31%
Banana: 14.29%
Cherry: 14.24%
Grape: 13.82%
Lime: 14.52%
Orange: 14.26%
Pineapple: 14.56%

percent_true(30):
Time: Min: 31ns, Mode: 62ns, Mean: 62ns, Max: 93ns
False: 70.11%
True: 29.89%

percent_true_float(33.33):
Time: Min: 62ns, Mode: 62ns, Mean: 76ns, Max: 125ns
False: 67.07%
True: 32.93%

random_float():
Time: Min: 31ns, Mode: 31ns, Mean: 43ns, Max: 62ns

shuffle(population):
Time: Min: 187ns, Mode: 218ns, Mean: 266ns, Max: 1062ns


Test Cases: Fortuna Classes
-------------------------------------------------------------------------
cum_weighted_choice():
Time: Min: 343ns, Mode: 343ns, Mean: 369ns, Max: 750ns
Apple: 19.54%
Banana: 11.89%
Cherry: 6.26%
Grape: 29.02%
Lime: 8.17%
Orange: 11.17%
Pineapple: 13.95%

rel_weighted_choice():
Time: Min: 343ns, Mode: N/A, Mean: 371ns, Max: 718ns
Apple: 20.38%
Banana: 10.98%
Cherry: 5.88%
Grape: 28.29%
Lime: 8.54%
Orange: 11.55%
Pineapple: 14.38%

truffle_shuffle():
Time: Min: 343ns, Mode: 375ns, Mean: 421ns, Max: 1250ns
Apple: 14.42%
Banana: 14.29%
Cherry: 14.39%
Grape: 14.31%
Lime: 14.12%
Orange: 14.19%
Pineapple: 14.28%

quantum_monty.mostly_flat():
Time: Min: 156ns, Mode: 187ns, Mean: 188ns, Max: 531ns
Apple: 14.37%
Banana: 13.98%
Cherry: 14.59%
Grape: 14.28%
Lime: 14.47%
Orange: 14.5%
Pineapple: 13.81%

quantum_monty.mostly_middle():
Time: Min: 187ns, Mode: 187ns, Mean: 199ns, Max: 375ns
Apple: 6.01%
Banana: 12.77%
Cherry: 18.67%
Grape: 24.98%
Lime: 19.16%
Orange: 12.19%
Pineapple: 6.22%

quantum_monty.mostly_center():
Time: Min: 218ns, Mode: 250ns, Mean: 304ns, Max: 875ns
Apple: 0.44%
Banana: 5.55%
Cherry: 24.16%
Grape: 39.92%
Lime: 24.05%
Orange: 5.49%
Pineapple: 0.39%

quantum_monty.mostly_front():
Time: Min: 218ns, Mode: 218ns, Mean: 238ns, Max: 312ns
Apple: 24.69%
Banana: 21.34%
Cherry: 18.35%
Grape: 14.67%
Lime: 10.44%
Orange: 6.77%
Pineapple: 3.74%

quantum_monty.mostly_back():
Time: Min: 218ns, Mode: 250ns, Mean: 244ns, Max: 281ns
Apple: 3.73%
Banana: 7.01%
Cherry: 11.03%
Grape: 14.92%
Lime: 18.24%
Orange: 20.51%
Pineapple: 24.56%

quantum_monty.mostly_first():
Time: Min: 281ns, Mode: 312ns, Mean: 310ns, Max: 406ns
Apple: 34.37%
Banana: 29.73%
Cherry: 20.36%
Grape: 10.01%
Lime: 4.17%
Orange: 1.12%
Pineapple: 0.24%

quantum_monty.mostly_last():
Time: Min: 281ns, Mode: 312ns, Mean: 315ns, Max: 343ns
Apple: 0.34%
Banana: 1.3%
Cherry: 4.07%
Grape: 10.68%
Lime: 19.97%
Orange: 29.55%
Pineapple: 34.09%

quantum_monty.mostly_cycle():
Time: Min: 406ns, Mode: 437ns, Mean: 485ns, Max: 1281ns
Apple: 14.48%
Banana: 14.01%
Cherry: 14.6%
Grape: 14.09%
Lime: 14.22%
Orange: 14.47%
Pineapple: 14.13%

quantum_monty.quantum_monty():
Time: Min: 593ns, Mode: 625ns, Mean: 624ns, Max: 812ns
Apple: 11.56%
Banana: 13.03%
Cherry: 15.52%
Grape: 19.19%
Lime: 16.32%
Orange: 12.9%
Pineapple: 11.48%

quantum_monty.mostly_not_middle():
Time: Min: 281ns, Mode: 312ns, Mean: 302ns, Max: 343ns
Apple: 21.41%
Banana: 15.47%
Cherry: 10.05%
Grape: 5.39%
Lime: 10.88%
Orange: 15.88%
Pineapple: 20.92%

quantum_monty.mostly_not_center():
Time: Min: 312ns, Mode: 375ns, Mean: 360ns, Max: 406ns
Apple: 29.27%
Banana: 17.14%
Cherry: 4.24%
Grape: 0.35%
Lime: 3.75%
Orange: 16.71%
Pineapple: 28.54%

quantum_monty.quantum_not_monty():
Time: Min: 625ns, Mode: 687ns, Mean: 668ns, Max: 781ns
Apple: 18.22%
Banana: 15.56%
Cherry: 11.41%
Grape: 9.57%
Lime: 11.05%
Orange: 15.37%
Pineapple: 18.82%

flex_cat():
Time: Min: 718ns, Mode: 750ns, Mean: 805ns, Max: 1625ns
A1: 17.28%
A2: 16.98%
A3: 16.52%
B1: 10.82%
B2: 10.8%
B3: 11.15%
C1: 5.53%
C2: 5.42%
C3: 5.5%

flex_cat('Cat_A'):
Time: Min: 468ns, Mode: 500ns, Mean: 493ns, Max: 687ns
A1: 33.06%
A2: 33.41%
A3: 33.53%

flex_cat('Cat_B'):
Time: Min: 468ns, Mode: 468ns, Mean: 484ns, Max: 531ns
B1: 33.29%
B2: 32.92%
B3: 33.79%

flex_cat('Cat_C'):
Time: Min: 468ns, Mode: 500ns, Mean: 526ns, Max: 1593ns
C1: 33.24%
C2: 33.13%
C3: 33.63%

```


## Fortuna Development Log
##### Fortuna 1.26.0 beta 1
- Dynamic version scheme implemented. 
- The Fortuna Extension now requires the fortuna_extras package, previously it was optional.

##### Fortuna 1.25.4
- Fixed some minor typos in the test script.

##### Fortuna 1.25.3
- Since version 1.24 Fortuna requires Python 3.7 or higher. This patch corrects an issue where the setup script incorrectly reported requiring Python 3.6 or higher. 

##### Fortuna 1.25.2
- Updated test suite.
- Major performance update for TruffleShuffle.
- Minor performance update for QuantumMonty & FlexCat: cycle monty.

##### Fortuna 1.25.1
- Important bug fix for TruffleShuffle, QuantumMonty and FlexCat.

##### Fortuna 1.25
- Full 64bit support.
- The Distribution & Performance Tests have been redesigned.
- Bloat Control: Two experimental features have been removed.
    - RandomWalk
    - CatWalk
- Bloat Control: Several utility functions have been removed from the top level API. These function remain in the Fortuna namespace for now, but may change in the future without warning.
    - stretch_bell, internal only.
    - min_max, not used anymore.
    - analytic_continuation, internal only.
    - flatten, internal only.

##### Fortuna 1.24.3
- Low level refactoring, non-breaking patch.

##### Fortuna 1.24.2
- Setup config updated to improve installation.

##### Fortuna 1.24.1
- Low level patch to avoid potential ADL issue. All low level function calls are now qualified.

##### Fortuna 1.24
- Documentation updated for even more clarity.
- Bloat Control: Two naïve utility functions that are no longer used in the module have been removed.
    - n_samples -> use a list comprehension instead. `[f(x) for _ in range(n)]`
    - bind -> use a lambda instead. `lambda: f(x)`

##### Fortuna 1.23.7
- Documentation updated for clarity.
- Minor bug fixes.
- TruffleShuffle has been redesigned slightly, it now uses a random rotate instead of swap.
- Custom `__repr__` methods have been added to each class.

##### Fortuna 1.23.6
- New method for QuantumMonty: quantum_not_monty - produces the upside down quantum_monty.
- New bias option for FlexCat: not_monty.

##### Fortuna 1.23.5.1
- Fixed some small typos.

##### Fortuna 1.23.5
- Documentation updated for clarity.
- All sequence wrappers can now accept generators as input.
- Six new functions added:
    - random_float() -> float in range [0.0..1.0) exclusive, uniform flat distribution.
    - percent_true_float(num: float) -> bool, Like percent_true but with floating point precision.
    - plus_or_minus_linear_down(num: int) -> int in range [-num..num], upside down pyramid.
    - plus_or_minus_curve_down(num: int) -> int in range [-num..num], upside down bell curve.
    - mostly_not_middle(num: int) -> int in range [0..num], upside down pyramid.
    - mostly_not_center(num: int) -> int in range [0..num], upside down bell curve.
- Two new methods for QuantumMonty:
    - mostly_not_middle
    - mostly_not_center
- Two new bias options for FlexCat, either can be used to define x and/or y axis bias:
    - not_middle
    - not_center

##### Fortuna 1.23.4.2
- Fixed some minor typos in the README.md file.

##### Fortuna 1.23.4.1
- Fixed some minor typos in the test suite.

##### Fortuna 1.23.4
- Fortuna is now Production/Stable!
- Fortuna and Fortuna Pure now use the same test suite.

##### Fortuna 0.23.4, first release candidate.
- RandomCycle, BlockCycle and TruffleShuffle have been refactored and combined into one class: TruffleShuffle.
- QuantumMonty and FlexCat will now use the new TruffleShuffle for cycling.
- Minor refactoring across the module.

##### Fortuna 0.23.3, internal
- Function shuffle(arr: list) added.

##### Fortuna 0.23.2, internal
- Simplified the plus_or_minus_curve(num: int) function, output will now always be bounded to the range [-num..num].
- Function stretched_bell(num: int) added, this matches the previous behavior of an unbounded plus_or_minus_curve.

##### Fortuna 0.23.1, internal
- Small bug fixes and general clean up.

##### Fortuna 0.23.0
- The number of test cycles in the test suite has been reduced to 10,000 (down from 100,000). The performance of the pure python implementation and the c-extension are now directly comparable.
- Minor tweaks made to the examples in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.22.2, experimental features
- BlockCycle class added.
- RandomWalk class added.
- CatWalk class added.

##### Fortuna 0.22.1
- Fortuna classes no longer return lists of values, this behavior has been extracted to a free function called n_samples.

##### Fortuna 0.22.0, experimental features
- Function bind added.
- Function n_samples added.

##### Fortuna 0.21.3
- Flatten will no longer raise an error if passed a callable item that it can't call. It correctly returns such items in an uncalled state without error.
- Simplified `.../fortuna_extras/fortuna_examples.py` - removed unnecessary class structure.

##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Function flatten added.
- Flatten: The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random.choices()
- Added Base Case for randint_dice()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna

##### Dice 0.1.x - 0.9.x
- Experimental Phase


## Legal Information
Fortuna © 2018 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>

```
License
-------

THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE
COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE"). THE WORK IS PROTECTED BY
COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS
AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.

BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO BE
BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT THIS LICENSE MAY BE
CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED HERE
IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.

1. Definitions

  a. "Adaptation" means a work based upon the Work, or upon the Work and other
  pre-existing works, such as a translation, adaptation, derivative work,
  arrangement of music or other alterations of a literary or artistic work, or
  phonogram or performance and includes cinematographic adaptations or any
  other form in which the Work may be recast, transformed, or adapted
  including in any form recognizably derived from the original, except that a
  work that constitutes a Collection will not be considered an Adaptation for
  the purpose of this License. For the avoidance of doubt, where the Work is a
  musical work, performance or phonogram, the synchronization of the Work in
  timed-relation with a moving image ("synching") will be considered an
  Adaptation for the purpose of this License.

  b. "Collection" means a collection of literary or artistic works, such as
  encyclopedias and anthologies, or performances, phonograms or broadcasts, or
  other works or subject matter other than works listed in Section 1(f) below,
  which, by reason of the selection and arrangement of their contents,
  constitute intellectual creations, in which the Work is included in its
  entirety in unmodified form along with one or more other contributions, each
  constituting separate and independent works in themselves, which together
  are assembled into a collective whole. A work that constitutes a Collection
  will not be considered an Adaptation (as defined above) for the purposes of
  this License.

  c. "Distribute" means to make available to the public the original and
  copies of the Work or Adaptation, as appropriate, through sale or other
  transfer of ownership.

  d. "Licensor" means the individual, individuals, entity or entities that
  offer(s) the Work under the terms of this License.

  e. "Original Author" means, in the case of a literary or artistic work, the
  individual, individuals, entity or entities who created the Work or if no
  individual or entity can be identified, the publisher; and in addition (i)
  in the case of a performance the actors, singers, musicians, dancers, and
  other persons who act, sing, deliver, declaim, play in, interpret or
  otherwise perform literary or artistic works or expressions of folklore;
  (ii) in the case of a phonogram the producer being the person or legal
  entity who first fixes the sounds of a performance or other sounds; and,
  (iii) in the case of broadcasts, the organization that transmits the
  broadcast.

  f. "Work" means the literary and/or artistic work offered under the terms of
  this License including without limitation any production in the literary,
  scientific and artistic domain, whatever may be the mode or form of its
  expression including digital form, such as a book, pamphlet and other
  writing; a lecture, address, sermon or other work of the same nature; a
  dramatic or dramatico-musical work; a choreographic work or entertainment in
  dumb show; a musical composition with or without words; a cinematographic
  work to which are assimilated works expressed by a process analogous to
  cinematography; a work of drawing, painting, architecture, sculpture,
  engraving or lithography; a photographic work to which are assimilated works
  expressed by a process analogous to photography; a work of applied art; an
  illustration, map, plan, sketch or three-dimensional work relative to
  geography, topography, architecture or science; a performance; a broadcast;
  a phonogram; a compilation of data to the extent it is protected as a
  copyrightable work; or a work performed by a variety or circus performer to
  the extent it is not otherwise considered a literary or artistic work.

  g. "You" means an individual or entity exercising rights under this License
  who has not previously violated the terms of this License with respect to
  the Work, or who has received express permission from the Licensor to
  exercise rights under this License despite a previous violation.

  h. "Publicly Perform" means to perform public recitations of the Work and to
  communicate to the public those public recitations, by any means or process,
  including by wire or wireless means or public digital performances; to make
  available to the public Works in such a way that members of the public may
  access these Works from a place and at a place individually chosen by them;
  to perform the Work to the public by any means or process and the
  communication to the public of the performances of the Work, including by
  public digital performance; to broadcast and rebroadcast the Work by any
  means including signs, sounds or images.

  i. "Reproduce" means to make copies of the Work by any means including
  without limitation by sound or visual recordings and the right of fixation
  and reproducing fixations of the Work, including storage of a protected
  performance or phonogram in digital form or other electronic medium.

2. Fair Dealing Rights. Nothing in this License is intended to reduce, limit,
or restrict any uses free from copyright or rights arising from limitations or
exceptions that are provided for in connection with the copyright protection
under copyright law or other applicable laws.

3. License Grant. Subject to the terms and conditions of this License,
Licensor hereby grants You a worldwide, royalty-free, non-exclusive, perpetual
(for the duration of the applicable copyright) license to exercise the rights
in the Work as stated below:

  a. to Reproduce the Work, to incorporate the Work into one or more
  Collections, and to Reproduce the Work as incorporated in the Collections;

  b. to create and Reproduce Adaptations provided that any such Adaptation,
  including any translation in any medium, takes reasonable steps to clearly
  label, demarcate or otherwise identify that changes were made to the
  original Work. For example, a translation could be marked "The original work
  was translated from English to Spanish," or a modification could indicate
  "The original work has been modified.";

  c. to Distribute and Publicly Perform the Work including as incorporated in
  Collections; and,

  d. to Distribute and Publicly Perform Adaptations.

The above rights may be exercised in all media and formats whether now known
or hereafter devised. The above rights include the right to make such
modifications as are technically necessary to exercise the rights in other
media and formats. Subject to Section 8(f), all rights not expressly granted
by Licensor are hereby reserved, including but not limited to the rights set
forth in Section 4(d).

4. Restrictions. The license granted in Section 3 above is expressly made
subject to and limited by the following restrictions:

  a. You may Distribute or Publicly Perform the Work only under the terms of
  this License. You must include a copy of, or the Uniform Resource Identifier
  (URI) for, this License with every copy of the Work You Distribute or
  Publicly Perform. You may not offer or impose any terms on the Work that
  restrict the terms of this License or the ability of the recipient of the
  Work to exercise the rights granted to that recipient under the terms of the
  License. You may not sublicense the Work. You must keep intact all notices
  that refer to this License and to the disclaimer of warranties with every
  copy of the Work You Distribute or Publicly Perform. When You Distribute or
  Publicly Perform the Work, You may not impose any effective technological
  measures on the Work that restrict the ability of a recipient of the Work
  from You to exercise the rights granted to that recipient under the terms of
  the License. This Section 4(a) applies to the Work as incorporated in a
  Collection, but this does not require the Collection apart from the Work
  itself to be made subject to the terms of this License. If You create a
  Collection, upon notice from any Licensor You must, to the extent
  practicable, remove from the Collection any credit as required by Section
  4(c), as requested. If You create an Adaptation, upon notice from any
  Licensor You must, to the extent practicable, remove from the Adaptation any
  credit as required by Section 4(c), as requested.

  b. You may not exercise any of the rights granted to You in Section 3 above
  in any manner that is primarily intended for or directed toward commercial
  advantage or private monetary compensation. The exchange of the Work for
  other copyrighted works by means of digital file-sharing or otherwise shall
  not be considered to be intended for or directed toward commercial advantage
  or private monetary compensation, provided there is no payment of any
  monetary compensation in connection with the exchange of copyrighted works.

  c. If You Distribute, or Publicly Perform the Work or any Adaptations or
  Collections, You must, unless a request has been made pursuant to Section
  4(a), keep intact all copyright notices for the Work and provide, reasonable
  to the medium or means You are utilizing: (i) the name of the Original
  Author (or pseudonym, if applicable) if supplied, and/or if the Original
  Author and/or Licensor designate another party or parties (e.g., a sponsor
  institute, publishing entity, journal) for attribution ("Attribution
  Parties") in Licensor's copyright notice, terms of service or by other
  reasonable means, the name of such party or parties; (ii) the title of the
  Work if supplied; (iii) to the extent reasonably practicable, the URI, if
  any, that Licensor specifies to be associated with the Work, unless such URI
  does not refer to the copyright notice or licensing information for the
  Work; and, (iv) consistent with Section 3(b), in the case of an Adaptation,
  a credit identifying the use of the Work in the Adaptation (e.g., "French
  translation of the Work by Original Author," or "Screenplay based on
  original Work by Original Author"). The credit required by this Section 4(c)
  may be implemented in any reasonable manner; provided, however, that in the
  case of a Adaptation or Collection, at a minimum such credit will appear, if
  a credit for all contributing authors of the Adaptation or Collection
  appears, then as part of these credits and in a manner at least as prominent
  as the credits for the other contributing authors. For the avoidance of
  doubt, You may only use the credit required by this Section for the purpose
  of attribution in the manner set out above and, by exercising Your rights
  under this License, You may not implicitly or explicitly assert or imply any
  connection with, sponsorship or endorsement by the Original Author, Licensor
  and/or Attribution Parties, as appropriate, of You or Your use of the Work,
  without the separate, express prior written permission of the Original
  Author, Licensor and/or Attribution Parties.

  d. For the avoidance of doubt:

    i. Non-waivable Compulsory License Schemes. In those jurisdictions in
    which the right to collect royalties through any statutory or compulsory
    licensing scheme cannot be waived, the Licensor reserves the exclusive
    right to collect such royalties for any exercise by You of the rights
    granted under this License;

    ii. Waivable Compulsory License Schemes. In those jurisdictions in which
    the right to collect royalties through any statutory or compulsory
    licensing scheme can be waived, the Licensor reserves the exclusive right
    to collect such royalties for any exercise by You of the rights granted
    under this License if Your exercise of such rights is for a purpose or use
    which is otherwise than noncommercial as permitted under Section 4(b) and
    otherwise waives the right to collect royalties through any statutory or
    compulsory licensing scheme; and,

    iii. Voluntary License Schemes. The Licensor reserves the right to collect
    royalties, whether individually or, in the event that the Licensor is a
    member of a collecting society that administers voluntary licensing
    schemes, via that society, from any exercise by You of the rights granted
    under this License that is for a purpose or use which is otherwise than
    noncommercial as permitted under Section 4(c).

  e. Except as otherwise agreed in writing by the Licensor or as may be
  otherwise permitted by applicable law, if You Reproduce, Distribute or
  Publicly Perform the Work either by itself or as part of any Adaptations or
  Collections, You must not distort, mutilate, modify or take other derogatory
  action in relation to the Work which would be prejudicial to the Original
  Author's honor or reputation. Licensor agrees that in those jurisdictions
  (e.g. Japan), in which any exercise of the right granted in Section 3(b) of
  this License (the right to make Adaptations) would be deemed to be a
  distortion, mutilation, modification or other derogatory action prejudicial
  to the Original Author's honor and reputation, the Licensor will waive or
  not assert, as appropriate, this Section, to the fullest extent permitted by
  the applicable national law, to enable You to reasonably exercise Your right
  under Section 3(b) of this License (right to make Adaptations) but not
  otherwise.

5. Representations, Warranties and Disclaimer

UNLESS OTHERWISE MUTUALLY AGREED TO BY THE PARTIES IN WRITING, LICENSOR OFFERS
THE WORK AS-IS AND MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND
CONCERNING THE WORK, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE, INCLUDING,
WITHOUT LIMITATION, WARRANTIES OF TITLE, MERCHANTIBILITY, FITNESS FOR A
PARTICULAR PURPOSE, NONINFRINGEMENT, OR THE ABSENCE OF LATENT OR OTHER
DEFECTS, ACCURACY, OR THE PRESENCE OF ABSENCE OF ERRORS, WHETHER OR NOT
DISCOVERABLE. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF IMPLIED
WARRANTIES, SO SUCH EXCLUSION MAY NOT APPLY TO YOU.

6. Limitation on Liability. EXCEPT TO THE EXTENT REQUIRED BY APPLICABLE LAW,
IN NO EVENT WILL LICENSOR BE LIABLE TO YOU ON ANY LEGAL THEORY FOR ANY
SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE OR EXEMPLARY DAMAGES ARISING OUT
OF THIS LICENSE OR THE USE OF THE WORK, EVEN IF LICENSOR HAS BEEN ADVISED OF
THE POSSIBILITY OF SUCH DAMAGES.

7. Termination

  a. This License and the rights granted hereunder will terminate
  automatically upon any breach by You of the terms of this License.
  Individuals or entities who have received Adaptations or Collections from
  You under this License, however, will not have their licenses terminated
  provided such individuals or entities remain in full compliance with those
  licenses. Sections 1, 2, 5, 6, 7, and 8 will survive any termination of this
  License.

  b. Subject to the above terms and conditions, the license granted here is
  perpetual (for the duration of the applicable copyright in the Work).
  Notwithstanding the above, Licensor reserves the right to release the Work
  under different license terms or to stop distributing the Work at any time;
  provided, however that any such election will not serve to withdraw this
  License (or any other license that has been, or is required to be, granted
  under the terms of this License), and this License will continue in full
  force and effect unless terminated as stated above.

8. Miscellaneous

  a. Each time You Distribute or Publicly Perform the Work or a Collection,
  the Licensor offers to the recipient a license to the Work on the same terms
  and conditions as the license granted to You under this License.

  b. Each time You Distribute or Publicly Perform an Adaptation, Licensor
  offers to the recipient a license to the original Work on the same terms and
  conditions as the license granted to You under this License.

  c. If any provision of this License is invalid or unenforceable under
  applicable law, it shall not affect the validity or enforceability of the
  remainder of the terms of this License, and without further action by the
  parties to this agreement, such provision shall be reformed to the minimum
  extent necessary to make such provision valid and enforceable.

  d. No term or provision of this License shall be deemed waived and no breach
  consented to unless such waiver or consent shall be in writing and signed by
  the party to be charged with such waiver or consent.

  e. This License constitutes the entire agreement between the parties with
  respect to the Work licensed here. There are no understandings, agreements
  or representations with respect to the Work not specified here. Licensor
  shall not be bound by any additional provisions that may appear in any
  communication from You. This License may not be modified without the mutual
  written agreement of the Licensor and You.

  f. The rights granted under, and the subject matter referenced, in this
  License were drafted utilizing the terminology of the Berne Convention for
  the Protection of Literary and Artistic Works (as amended on September 28,
  1979), the Rome Convention of 1961, the WIPO Copyright Treaty of 1996, the
  WIPO Performances and Phonograms Treaty of 1996 and the Universal Copyright
  Convention (as revised on July 24, 1971). These rights and subject matter
  take effect in the relevant jurisdiction in which the License terms are
  sought to be enforced according to the corresponding provisions of the
  implementation of those treaty provisions in the applicable national law. If
  the standard suite of rights granted under applicable copyright law includes
  additional rights not granted under this License, such additional rights are
  deemed to be included in the License; this License is not intended to
  restrict the license of any rights under applicable law.
```
