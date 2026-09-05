import yaml
from tabulate import tabulate


def load_cases(path):
    with open(path, encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data["cases"]


def parse(case):
    return [int(x) for x in case] #str поменяла на int


def longest(seq, better):
    if not seq:
        return []
    best_s = start = 0
    best_n = 1
    for i in range(1, len(seq)):
        if better(seq[i], seq[i - 1]):
            n = i - start + 1
            if n > best_n:
                best_s, best_n = start, n
        else:
            start = i
    return seq[best_s:best_s + best_n]


def kadane(seq):
    if not seq:
        return 0, []
    best = cur = seq[0] #инициализация не с нуля а с првого элемента
    bs = cs = be = 0
    for i in range(1, len(seq)):
        if cur + seq[i] < seq[i]:
            cur, cs = seq[i], i
        else:
            cur += seq[i]
        if cur > best:
            best, bs, be = cur, cs, i
    return best, seq[bs:be+1]


def frequencies(seq):
    freq = {} #словарь, где число х - явл ключом, а его частота значением
    for x in seq:
        if x in freq:
            freq[x] +=1
        else:
            freq[x] = 1
    best_x, best_c = None, -1
    for x, c in freq.items():
        if c > best_c or (c == best_c and (best_x is None or x < best_x)):
            best_x, best_c = x, c
    places = [i for i, x in enumerate(seq) if x == best_x] #mode_at должен выводить позиции самого частого числа
    return best_x, places


def solve(seq):
    loc = 0
    for i in range(1, len(seq) - 1):
        if seq[i] > seq[i - 1] and seq[i] > seq[i + 1]: #по условию сторо
            loc += 1
    s, frag = kadane(seq)
    freq, places = frequencies(seq)
    return (
        longest(seq, lambda x, y: x >= y),
        longest(seq, lambda x, y: x < y),
        longest(seq, lambda x, y: x == y),
        s,
        frag,
        loc,
        freq,
        places,
    )


def fmt(xs):
    return ", ".join(str(x) for x in xs)


def main():
    rows = []
    best_n, best_s = None, None
    for n, case in enumerate(load_cases("data.yaml"), 1):
        seq = parse(case)
        inc, dec, eq, s, frag, loc, freq, places = solve(seq)
        rows.append([n, fmt(seq), fmt(inc), fmt(dec), fmt(eq), s, fmt(frag), loc, freq, fmt(places)])
        if best_s is None or s > best_s:
            best_n, best_s = n, s
    print(
        tabulate(
            rows,
            headers=["line", "sequence", "increasing", "decreasing", "equal", "max_sum", "fragment", "local_maxima", "mode", "mode_at"],
            tablefmt="github",
        )
    )
    print("\nBest case: %s, max_sum = %s" % (best_n, best_s))


if __name__ == "__main__":
    main()
