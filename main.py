import yaml
from tabulate import tabulate


def load_cases(path):
    with open(path, encoding="utf-8") as file: # по пути
        data = yaml.safe_load(file)
    return data["cases"]


def parse(case):
    return [int(x) for x in case] # Превращает в массив


def longest(seq, better): # Самая длинная непрерывная последовательность по условию
    best_s = start = 0 # best_s - индекс начала самой длинной серии start - индекс начала текущей серии
    best_n = 1 # best_n - наибольшая длина серии
    for i in range(1, len(seq)): # перебор индексов массива
        if better(seq[i], seq[i - 1]): # 
            n = i - start + 1 # + 1 - учесть оба числа
            if n > best_n: # Проверка на рекорд
                best_s, best_n = start, n
        else:
            start = i
    return seq[best_s:best_n + best_s]


def kadane(seq): # Макс сумма
    best = cur = seq[0] # не 0, т к все числа могут быть отрицательными и best = 0 будет неправильно
    bs = cs = be = 0
    for i in range(1, len(seq)):
        if cur + seq[i] < seq[i]:
            cur, cs = seq[i], i
        else:
            cur += seq[i]
        if cur > best:
            best, bs, be = cur, cs, i
    return best, seq[bs:be + 1] # +1 чтоы включить правую границу в срез


def frequencies(seq):
    pos = {} # Словарь для числе и индексов
    for i, x in enumerate(seq):
        if x not in pos: pos[x] = []
        pos[x].append(i)
    best_x, best_c = None, -1
    for x, i in pos.items(): # Число в x, список индексов его в i
        c = len(i)
        if c > best_c or (c == best_c and x < best_x):
            best_x, best_c = x, c
    return best_x, pos[best_x]


def solve(seq):
    loc = 0 # Лок максимумы
    for i in range(1, len(seq) - 1):
        if seq[i] > seq[i - 1] and seq[i] > seq[i + 1]:
            loc += 1
    s, frag = kadane(seq)
    freq, places = frequencies(seq)
    return (
        longest(seq, lambda x, y: x > y),
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
    for n, case in enumerate(load_cases("data.yaml"), 1): # индекс и значение
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