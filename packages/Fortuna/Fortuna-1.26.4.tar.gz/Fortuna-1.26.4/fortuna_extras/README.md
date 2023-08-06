# Fortuna: Fast & Flexible Random Value Generators
Fortuna replaces much of the functionality of Python's Random module, often achieving 10x better performance. However, the most interesting bits of Fortuna are found in the high-level abstractions like FlexCat, QuantumMonty and TruffleShuffle.

The core functionality of Fortuna is based on the Mersenne Twister Algorithm by Makoto Matsumoto (松本 眞) and Takuji Nishimura (西村 拓士). Fortuna is not appropriate for cryptography of any kind. Fortuna is for games, data science, AI and experimental programming, not security.

The Fortuna generator was designed to use hardware seeding exclusively. This allows the generator to be completely encapsulated.

Installation: `$ pip install Fortuna` or you can download and build from source. Building Fortuna requires the latest version of Python3, Cython, python3 dev tools, and a modern C++17 compiler. Fortuna is designed, built and tested for MacOS X, and also happens to work with many flavors of Linux. Fortuna is not officially supported on Windows at this time.

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
Fortuna Extension v1.26.3

Base Cases: Python3 Random Module
-------------------------------------------------------------------------
random.randint(-6, 6):
Time: Min: 1406ns, Mode: 1437ns, Mean: 1473ns, Max: 1843ns
-6: 7.78%
-5: 7.59%
-4: 7.66%
-3: 7.42%
-2: 7.84%
-1: 7.86%
0: 7.79%
1: 8.1%
2: 7.14%
3: 7.56%
4: 7.95%
5: 7.73%
6: 7.58%

random.randrange(-6, 6):
Time: Min: 1250ns, Mode: 1312ns, Mean: 1310ns, Max: 1500ns
-6: 8.33%
-5: 8.32%
-4: 8.34%
-3: 8.29%
-2: 8.56%
-1: 8.06%
0: 8.27%
1: 8.38%
2: 8.37%
3: 8.32%
4: 8.19%
5: 8.57%

random.choice(population):
Time: Min: 843ns, Mode: 843ns, Mean: 954ns, Max: 2687ns
Apple: 14.43%
Banana: 14.3%
Cherry: 14.53%
Grape: 14.05%
Lime: 14.7%
Orange: 13.76%
Pineapple: 14.23%

random.choices(population, cum_weights=cum_weights):
Time: Min: 2125ns, Mode: 2125ns, Mean: 2153ns, Max: 2656ns
Apple: 19.84%
Banana: 11.41%
Cherry: 5.68%
Grape: 28.36%
Lime: 8.37%
Orange: 11.71%
Pineapple: 14.63%

random.choices(population, weights=rel_weights):
Time: Min: 2593ns, Mode: 2625ns, Mean: 2703ns, Max: 4062ns
Apple: 20.05%
Banana: 11.62%
Cherry: 5.47%
Grape: 28.72%
Lime: 8.12%
Orange: 11.68%
Pineapple: 14.34%

random.shuffle(population):
Time: Min: 4812ns, Mode: 5187ns, Mean: 5147ns, Max: 5593ns

random.random():
Time: Min: 31ns, Mode: N/A, Mean: 46ns, Max: 62ns


Test Cases: Fortuna Functions
-------------------------------------------------------------------------
random_range(-6, 6):
Time: Min: 62ns, Mode: 62ns, Mean: 72ns, Max: 93ns
-6: 7.64%
-5: 7.59%
-4: 7.97%
-3: 7.85%
-2: 7.96%
-1: 7.36%
0: 7.82%
1: 7.65%
2: 7.98%
3: 7.57%
4: 7.57%
5: 7.6%
6: 7.44%

random_below(6):
Time: Min: 31ns, Mode: 62ns, Mean: 68ns, Max: 156ns
0: 17.17%
1: 16.82%
2: 16.77%
3: 16.76%
4: 16.29%
5: 16.19%

d(6):
Time: Min: 31ns, Mode: 62ns, Mean: 62ns, Max: 93ns
1: 16.73%
2: 16.62%
3: 17.5%
4: 16.07%
5: 16.37%
6: 16.71%

dice(3, 6):
Time: Min: 93ns, Mode: 125ns, Mean: 122ns, Max: 156ns
3: 0.41%
4: 1.2%
5: 2.5%
6: 4.61%
7: 7.14%
8: 10.07%
9: 11.6%
10: 12.32%
11: 12.52%
12: 11.76%
13: 9.49%
14: 7.23%
15: 4.55%
16: 2.88%
17: 1.29%
18: 0.43%

plus_or_minus(6):
Time: Min: 31ns, Mode: 62ns, Mean: 64ns, Max: 93ns
-6: 7.34%
-5: 7.28%
-4: 7.1%
-3: 7.6%
-2: 8.22%
-1: 7.47%
0: 7.56%
1: 8.11%
2: 7.6%
3: 8.28%
4: 7.42%
5: 8.17%
6: 7.85%

plus_or_minus_linear(6):
Time: Min: 62ns, Mode: 93ns, Mean: 84ns, Max: 125ns
-6: 1.98%
-5: 4.12%
-4: 6.22%
-3: 8.27%
-2: 10.62%
-1: 12.03%
0: 14.27%
1: 11.74%
2: 10.65%
3: 8.25%
4: 5.99%
5: 3.91%
6: 1.95%

plus_or_minus_curve(6):
Time: Min: 125ns, Mode: 125ns, Mean: 139ns, Max: 156ns
-6: 0.18%
-5: 0.75%
-4: 2.51%
-3: 6.11%
-2: 12.11%
-1: 18.27%
0: 20.15%
1: 17.64%
2: 12.24%
3: 6.65%
4: 2.5%
5: 0.67%
6: 0.22%

plus_or_minus_linear_down(6):
Time: Min: 187ns, Mode: N/A, Mean: 205ns, Max: 250ns
-6: 12.67%
-5: 11.21%
-4: 8.96%
-3: 7.57%
-2: 5.63%
-1: 3.75%
0: 2.0%
1: 3.85%
2: 5.4%
3: 7.08%
4: 9.01%
5: 10.89%
6: 11.98%

plus_or_minus_curve_down(6):
Time: Min: 250ns, Mode: 281ns, Mean: 279ns, Max: 343ns
-6: 16.71%
-5: 15.01%
-4: 9.9%
-3: 5.26%
-2: 2.02%
-1: 0.57%
0: 0.19%
1: 0.57%
2: 1.93%
3: 5.14%
4: 9.65%
5: 15.43%
6: 17.62%

zero_flat(6):
Time: Min: 31ns, Mode: 62ns, Mean: 62ns, Max: 93ns
0: 14.35%
1: 14.01%
2: 14.47%
3: 14.55%
4: 14.05%
5: 14.21%
6: 14.36%

zero_cool(6):
Time: Min: 93ns, Mode: 125ns, Mean: 131ns, Max: 187ns
0: 24.95%
1: 21.33%
2: 18.95%
3: 13.71%
4: 10.61%
5: 7.01%
6: 3.44%

zero_extreme(6):
Time: Min: 156ns, Mode: 187ns, Mean: 200ns, Max: 250ns
0: 34.12%
1: 29.86%
2: 20.19%
3: 10.08%
4: 4.33%
5: 1.06%
6: 0.36%

max_cool(6):
Time: Min: 125ns, Mode: 125ns, Mean: 135ns, Max: 187ns
0: 3.4%
1: 6.84%
2: 11.26%
3: 14.72%
4: 18.26%
5: 21.06%
6: 24.46%

max_extreme(6):
Time: Min: 156ns, Mode: 187ns, Mean: 200ns, Max: 250ns
0: 0.28%
1: 1.33%
2: 3.91%
3: 10.31%
4: 19.71%
5: 30.2%
6: 34.26%

mostly_middle(6):
Time: Min: 62ns, Mode: 62ns, Mean: 76ns, Max: 125ns
0: 6.61%
1: 12.59%
2: 18.91%
3: 24.89%
4: 18.23%
5: 12.11%
6: 6.66%

mostly_center(6):
Time: Min: 125ns, Mode: 125ns, Mean: 133ns, Max: 156ns
0: 0.37%
1: 5.36%
2: 24.29%
3: 39.77%
4: 24.6%
5: 5.28%
6: 0.33%

mostly_not_middle(6):
Time: Min: 156ns, Mode: 187ns, Mean: 199ns, Max: 625ns
0: 21.55%
1: 15.95%
2: 9.92%
3: 5.13%
4: 10.42%
5: 16.43%
6: 20.6%

mostly_not_center(6):
Time: Min: 218ns, Mode: 250ns, Mean: 247ns, Max: 281ns
0: 28.57%
1: 17.08%
2: 3.8%
3: 0.34%
4: 3.79%
5: 16.9%
6: 29.52%

random_value(population):
Time: Min: 31ns, Mode: 62ns, Mean: 110ns, Max: 656ns
Apple: 13.94%
Banana: 14.59%
Cherry: 14.36%
Grape: 14.78%
Lime: 14.16%
Orange: 14.04%
Pineapple: 14.13%

percent_true(30):
Time: Min: 62ns, Mode: 62ns, Mean: 63ns, Max: 93ns
False: 69.81%
True: 30.19%

percent_true_float(33.33):
Time: Min: 62ns, Mode: 93ns, Mean: 79ns, Max: 125ns
False: 67.25%
True: 32.75%

random_float():
Time: Min: 31ns, Mode: 31ns, Mean: 42ns, Max: 62ns

shuffle(population):
Time: Min: 187ns, Mode: 218ns, Mean: 219ns, Max: 250ns


Test Cases: Fortuna Classes
-------------------------------------------------------------------------
cum_weighted_choice():
Time: Min: 343ns, Mode: 375ns, Mean: 372ns, Max: 718ns
Apple: 19.88%
Banana: 12.03%
Cherry: 5.82%
Grape: 28.99%
Lime: 8.21%
Orange: 11.26%
Pineapple: 13.81%

rel_weighted_choice():
Time: Min: 343ns, Mode: 375ns, Mean: 366ns, Max: 593ns
Apple: 19.81%
Banana: 11.25%
Cherry: 5.78%
Grape: 28.9%
Lime: 8.57%
Orange: 11.62%
Pineapple: 14.07%

truffle_shuffle():
Time: Min: 375ns, Mode: 375ns, Mean: 378ns, Max: 500ns
Apple: 14.33%
Banana: 14.24%
Cherry: 13.97%
Grape: 14.38%
Lime: 14.34%
Orange: 14.17%
Pineapple: 14.57%

quantum_monty.mostly_flat():
Time: Min: 156ns, Mode: 187ns, Mean: 184ns, Max: 406ns
Apple: 14.21%
Banana: 14.25%
Cherry: 13.48%
Grape: 14.62%
Lime: 14.77%
Orange: 14.14%
Pineapple: 14.53%

quantum_monty.mostly_middle():
Time: Min: 187ns, Mode: 187ns, Mean: 195ns, Max: 343ns
Apple: 6.33%
Banana: 12.11%
Cherry: 18.85%
Grape: 24.79%
Lime: 18.74%
Orange: 12.62%
Pineapple: 6.56%

quantum_monty.mostly_center():
Time: Min: 218ns, Mode: 250ns, Mean: 253ns, Max: 468ns
Apple: 0.44%
Banana: 5.13%
Cherry: 23.98%
Grape: 40.28%
Lime: 24.13%
Orange: 5.53%
Pineapple: 0.51%

quantum_monty.mostly_front():
Time: Min: 187ns, Mode: 250ns, Mean: 244ns, Max: 312ns
Apple: 24.71%
Banana: 21.05%
Cherry: 18.19%
Grape: 14.22%
Lime: 10.58%
Orange: 7.38%
Pineapple: 3.87%

quantum_monty.mostly_back():
Time: Min: 218ns, Mode: 250ns, Mean: 247ns, Max: 281ns
Apple: 3.76%
Banana: 7.03%
Cherry: 10.86%
Grape: 14.73%
Lime: 18.39%
Orange: 20.81%
Pineapple: 24.42%

quantum_monty.mostly_first():
Time: Min: 281ns, Mode: 312ns, Mean: 321ns, Max: 375ns
Apple: 34.64%
Banana: 29.22%
Cherry: 19.98%
Grape: 10.48%
Lime: 4.13%
Orange: 1.27%
Pineapple: 0.28%

quantum_monty.mostly_last():
Time: Min: 281ns, Mode: 312ns, Mean: 320ns, Max: 375ns
Apple: 0.33%
Banana: 1.19%
Cherry: 4.63%
Grape: 10.23%
Lime: 19.54%
Orange: 30.05%
Pineapple: 34.03%

quantum_monty.mostly_cycle():
Time: Min: 437ns, Mode: 437ns, Mean: 583ns, Max: 2437ns
Apple: 14.6%
Banana: 14.1%
Cherry: 14.12%
Grape: 14.38%
Lime: 14.6%
Orange: 14.04%
Pineapple: 14.16%

quantum_monty.quantum_monty():
Time: Min: 593ns, Mode: 625ns, Mean: 630ns, Max: 750ns
Apple: 12.41%
Banana: 13.17%
Cherry: 15.9%
Grape: 19.11%
Lime: 15.34%
Orange: 12.82%
Pineapple: 11.25%

quantum_monty.mostly_not_middle():
Time: Min: 281ns, Mode: 312ns, Mean: 336ns, Max: 1062ns
Apple: 21.19%
Banana: 16.33%
Cherry: 10.16%
Grape: 5.23%
Lime: 10.04%
Orange: 15.98%
Pineapple: 21.07%

quantum_monty.mostly_not_center():
Time: Min: 343ns, Mode: 375ns, Mean: 370ns, Max: 406ns
Apple: 29.04%
Banana: 17.04%
Cherry: 3.82%
Grape: 0.33%
Lime: 3.74%
Orange: 17.46%
Pineapple: 28.57%

quantum_monty.quantum_not_monty():
Time: Min: 625ns, Mode: 687ns, Mean: 679ns, Max: 875ns
Apple: 19.22%
Banana: 15.1%
Cherry: 10.94%
Grape: 9.28%
Lime: 11.45%
Orange: 15.5%
Pineapple: 18.51%

flex_cat():
Time: Min: 718ns, Mode: 750ns, Mean: 1083ns, Max: 3093ns
A1: 17.14%
A2: 16.6%
A3: 17.02%
B1: 10.71%
B2: 10.88%
B3: 11.12%
C1: 5.41%
C2: 5.5%
C3: 5.62%

flex_cat('Cat_A'):
Time: Min: 468ns, Mode: 500ns, Mean: 682ns, Max: 2343ns
A1: 33.58%
A2: 33.16%
A3: 33.26%

flex_cat('Cat_B'):
Time: Min: 468ns, Mode: 500ns, Mean: 682ns, Max: 3218ns
B1: 32.84%
B2: 33.34%
B3: 33.82%

flex_cat('Cat_C'):
Time: Min: 468ns, Mode: 500ns, Mean: 498ns, Max: 531ns
C1: 33.47%
C2: 33.43%
C3: 33.1%

```


## Fortuna Development Log
##### Fortuna 1.26.4
- Updated documentation for clarity.
- Fixed a minor typo in the test script.

##### Fortuna 1.26.3
- Clean build.

##### Fortuna 1.26.2
- Fixed some minor typos.

##### Fortuna 1.26.1
- Release.

##### Fortuna 1.26.0 beta 2
- Moved README.md and LICENSE files into fortuna_extras folder.

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
Fortuna © 2019 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>
