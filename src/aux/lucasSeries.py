# There are many sequences that follow the
# recurrence relation of the Fibonacci sequence (e.g. Lucas series):
# x(n) = x(n-1) + x(n-2),
# but start from any two numbers.
# These sequences all have the property that
# x(n)/x(n-1) -> golden ratio as x -> inf

golden_ratio = 1.61803398875

def makeSequence(x0=1, x1=1, n=20):
    l = [x0, x1]
    ratios = [x1/x0]
    deviations = [ratios[-1] - golden_ratio]
    for i in range(n):
        l.append(l[-2] + l[-1])
        ratios.append(l[-1]/l[-2])
        deviations.append(ratios[-1] - golden_ratio)
    return l, ratios, deviations

if __name__ == "__main__":
    res = makeSequence(20,5)
    print(res[2][-1])

