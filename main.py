import csv

budget = 5000   #бюджет
dd = 500       #доход с одного пользователя
cost0 = 200

file = "graphcuu.csv"

with open(file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    stroki = list(reader)

header = stroki[0][1:-1]
n = len(header)

# g[i] – в нашем случае это список тех, на кого влияет i
g = [[] for _ in range(n + 1)]
for strk in stroki[1:]:
    if not strk or strk[0] == "":
        continue
    i = int(strk[0])
    for j in range(1, n + 1):
        if strk[j].strip() == "1":
            g[i].append(j)
x`
# распространяем продукт по правилу 20%
def spread(seeds):
    active = [False] * (n + 1)
    for v in seeds:
        active[v] = True
    changed = True
    while changed:
        changed = False
        for v in range(1, n + 1):
            if active[v]:
                continue
            # считаем всех, кто влияет на v
            total = 0
            good = 0
            for u in range(1, n + 1):
                if v in g[u]:
                    total += 1
                    if active[u]:
                        good += 1
            if total == 0:
                continue
            if good * 5 >= total:   # 20% порог
                active[v] = True
                changed = True

    # считаем всех активных
    allact = 0
    for v in range(1, n + 1):
        if active[v]:
            allact += 1
    return allact


# считаем размер аудитории и стоимость
deg = [0] * (n + 1)
for i in range(1, n + 1):
    deg[i] = len(g[i])

# находим лучший вариант среди одиночек и пар
top_seeds = []
top_profit = 0     # без рекламы профит нулевой

# ниже одиночные вершины
for i in range(1, n + 1):
    cost = cost0 * deg[i]
    if cost > budget:
        continue
    allact = spread([i])
    profit = allact * dd      #только выручка
    if profit > top_profit:
        top_profit = profit
        top_seeds = [i]

# ниже пары вершин
for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        cost = cost0 * (deg[i] + deg[j])
        if cost > budget:
            continue
        allact = spread([i, j])
        profit = allact * dd
        if profit > top_profit:
            top_profit = profit
            top_seeds = [i, j]

print("Заключим рекламные контракты с пользователями:", ", ".join(map(str, top_seeds)))
print("Число активных пользователей:", spread(top_seeds))
print("Итоговая прибыль:", top_profit, "рублей")