#pragma once
#include <random>       // random_device, mt19937_64, uniform_int_distribution, uniform_real_distribution, normal_distribution,
#include <vector>       // vector
#include <algorithm>    // min, max, generate, sort, accumulate
#include <functional>   // greater
#include <cmath>        // abs


namespace Fortuna {
static std::random_device hardware_seed;
static std::mt19937_64 generator(hardware_seed());

long long random_range(long long lo, long long hi) {
    if (lo < hi) {
        std::uniform_int_distribution<long long> distribution(lo, hi);
        return distribution(Fortuna::generator);
    }
    else if (hi == lo) return hi;
    else return Fortuna::random_range(hi, lo);
}

long double random_float() {
    static std::uniform_real_distribution<long double> distribution(0.0, 1.0);
    return distribution(Fortuna::generator);
}

template <typename Function>
long analytic_continuation(Function func, long long num) {
    if (num < 0) return -func(-num);
    else if (num == 0) return 0;
    else return func(num);
}

long long random_below(long long size) {
    if (size > 0) return Fortuna::random_range(0, size - 1);
    else return Fortuna::analytic_continuation(random_below, size);
}

long long d(long long sides) {
    if (sides > 0) return Fortuna::random_range(1, sides);
    else return Fortuna::analytic_continuation(d, sides);
}

long long dice(long long rolls, long long sides) {
    if (rolls > 0) {
        long long total = 0;
        for (auto i=0; i<rolls; ++i) total += Fortuna::d(sides);
        return total;
    }
    else if (rolls == 0) return 0;
    else return -Fortuna::dice(-rolls, sides);
}

bool percent_true(int num) {
    return Fortuna::d(100) <= num;
}

bool percent_true_float(long double num) {
    return Fortuna::random_below(100) + Fortuna::random_float() <= num;
}

long long min_max(long long target, long long lo, long long hi) {
    if (lo < hi) return std::min(std::max(target, lo), hi);
    else if (lo == hi) return hi;
    else return Fortuna::min_max(target, hi, lo);
}

long long plus_or_minus(long long num) {
    return Fortuna::random_range(-num, num);
}

long long plus_or_minus_linear(long long num) {
    const long long n = std::abs(num);
    return Fortuna::dice(2, n + 1) - (n + 2);
}

long long stretched_bell(long long num) {
    const long double PI = 3.14159265359;
    std::normal_distribution<long double> distribution(0.0, num / PI);
    return round(distribution(Fortuna::generator));
}

long long plus_or_minus_curve(long long num) {
    const long long n = std::abs(num);
    long long result = Fortuna::stretched_bell(n);
    while (result < -n or result > n) { result = Fortuna::stretched_bell(n); };
    return result;
}

long long zero_flat(long long num) {
    return Fortuna::random_range(0, num);
}

long long zero_cool(long long num) {
    if (num > 0) {
        long long result = Fortuna::plus_or_minus_linear(num);
        while (result < 0) { result = Fortuna::plus_or_minus_linear(num); };
        return result;
    } else return Fortuna::analytic_continuation(Fortuna::zero_cool, num);
}

long long zero_extreme(long long num) {
    if (num > 0) {
        long long result = Fortuna::plus_or_minus_curve(num);
        while (result < 0) { result = Fortuna::plus_or_minus_curve(num); };
        return result;
    } else return Fortuna::analytic_continuation(Fortuna::zero_extreme, num);
}

long long max_cool(long long num) {
    if (num > 0) return num - Fortuna::zero_cool(num);
    else return Fortuna::analytic_continuation(Fortuna::max_cool, num);
}

long long max_extreme(long long num) {
    if (num > 0) return num - Fortuna::zero_extreme(num);
    else return Fortuna::analytic_continuation(Fortuna::max_extreme, num);
}

long long mostly_middle(long long num) {
    if (num > 0) {
        const long long mid_point = num / 2;
        if (num % 2 == 0) return Fortuna::plus_or_minus_linear(mid_point) + mid_point;
        else if (Fortuna::percent_true(50)) return Fortuna::max_cool(mid_point);
        else return 1 + Fortuna::zero_cool(mid_point) + mid_point;
    } else return Fortuna::analytic_continuation(Fortuna::mostly_middle, num);
}

long long mostly_center(long long num) {
    if (num > 0) {
        const long long mid_point = num / 2;
        if (num % 2 == 0) return Fortuna::plus_or_minus_curve(mid_point) + mid_point;
        else if (Fortuna::percent_true(50)) return Fortuna::max_extreme(mid_point);
        else return 1 + Fortuna::zero_extreme(mid_point) + mid_point;
    } else return Fortuna::analytic_continuation(Fortuna::mostly_center, num);
}

int ability_dice(int num) {
    const int n = Fortuna::min_max(num, 3, 9);
    if (n == 3) return Fortuna::dice(3, 6);
    std::vector<int> theRolls(n);
    std::generate(begin(theRolls), end(theRolls), []() { return Fortuna::d(6); });
    std::sort(begin(theRolls), end(theRolls), std::greater<int>());
    return std::accumulate(begin(theRolls), begin(theRolls) + 3, 0);
}

template <typename Function>
long long half_the_zeros(Function func, long long num) {
    if (Fortuna::percent_true(50)) return func(num);
    else {
        long long t = 0;
        while (t == 0) t = func(num);
        return t;
    }
}

long long plus_or_minus_linear_down(long long num) {
    if (num == 0) return 0;
    const long long n = std::abs(num);
    if (Fortuna::percent_true(50)) return Fortuna::half_the_zeros(Fortuna::max_cool, n);
    else return Fortuna::half_the_zeros(Fortuna::max_cool, -n);
}

long long plus_or_minus_curve_down(long long num) {
    if (num == 0) return 0;
    const long long n = std::abs(num);
    if (Fortuna::percent_true(50)) return Fortuna::half_the_zeros(Fortuna::max_extreme, n);
    else return Fortuna::half_the_zeros(Fortuna::max_extreme, -n);
}

long long mostly_not_middle(long long num) {
    if (num > 0) {
        const long long mid_point = num / 2;
        if (num % 2 == 0) return Fortuna::plus_or_minus_linear_down(mid_point) + mid_point;
        else if (Fortuna::percent_true(50)) return Fortuna::zero_cool(mid_point);
        else return 1 + Fortuna::max_cool(mid_point) + mid_point;
    } else return Fortuna::analytic_continuation(Fortuna::mostly_not_middle, num);
}

long long mostly_not_center(long long num) {
    if (num > 0) {
        const long long mid_point = num / 2;
        if (num % 2 == 0) return Fortuna::plus_or_minus_curve_down(mid_point) + mid_point;
        else if (percent_true(50)) return Fortuna::zero_extreme(mid_point);
        else return 1 + Fortuna::max_extreme(mid_point) + mid_point;
    } else return Fortuna::analytic_continuation(Fortuna::mostly_center, num);
}

} // end namespace Fortuna
