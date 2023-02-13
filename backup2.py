import datetime
from dataclasses import dataclass

@dataclass()
class Rule:
    count: int
    interval: int

#   "keep": [[30, 1], [10, 7], [10, 30]]       # History to keep - Array of [number of files, period]
#                                              # Example: Every file for the most recent 30,
#                                              #   then oldest 1 for each 7 older, keeping 10 backed-up,

#keep = [[5, 1], [3, 3], [3, 9]]
keep = [
        Rule(5, 1),
        Rule(3, 3),
        Rule(3, 9),
]

dates1 = [
    datetime.date(2022, 1, 1),
    datetime.date(2022, 1, 2),
    datetime.date(2022, 1, 3),
    datetime.date(2022, 1, 4),
    datetime.date(2022, 1, 5),

    datetime.date(2022, 1, 8),
    datetime.date(2022, 1, 11),
    datetime.date(2022, 1, 14),

    datetime.date(2022, 1, 23),
    datetime.date(2022, 2, 1),
    datetime.date(2022, 2, 10),
    datetime.date(2023, 2, 19), # del
]

dates = [
    datetime.date(2022, 1, 1),
    datetime.date(2022, 1, 2),
    datetime.date(2022, 1, 3),
    datetime.date(2022, 1, 4),
    datetime.date(2022, 1, 5),
    datetime.date(2022, 1, 6), # del
    datetime.date(2022, 1, 7), # del
    datetime.date(2022, 1, 8),
    datetime.date(2022, 1, 9), # del
    datetime.date(2022, 1, 10), # del
    datetime.date(2022, 1, 11),
    datetime.date(2022, 1, 12), # del
    datetime.date(2022, 1, 13), # del
    datetime.date(2022, 1, 14),
    datetime.date(2022, 1, 15), # del
    datetime.date(2022, 1, 16), # del
    datetime.date(2022, 1, 17), # del
    datetime.date(2022, 1, 18), # del
    datetime.date(2022, 1, 19), # del
    datetime.date(2022, 1, 20), # del
    datetime.date(2022, 1, 21), # del
    datetime.date(2022, 1, 22), # del
    datetime.date(2022, 1, 23),
    datetime.date(2022, 1, 24), # del
    datetime.date(2022, 1, 25), # del
    datetime.date(2022, 1, 26), # del
    datetime.date(2022, 1, 27), # del
    datetime.date(2022, 1, 28), # del
    datetime.date(2022, 1, 29), # del
    datetime.date(2022, 1, 30), # del
    datetime.date(2022, 1, 31), # del
    datetime.date(2022, 2, 1),
    datetime.date(2022, 2, 2), # del
    datetime.date(2022, 2, 3), # del
    datetime.date(2022, 2, 4), # del
    datetime.date(2022, 2, 5), # del
    datetime.date(2022, 2, 6), # del
    datetime.date(2022, 2, 7), # del
    datetime.date(2022, 2, 8), # del
    datetime.date(2022, 2, 9), # del
    datetime.date(2022, 2, 10),
    datetime.date(2022, 2, 11), # del
]


print("Entrada:")
for d in dates:
    print(d)

def delete():
    rule_i = 0
    rule = keep[0]
    kept = 1
    last_kept = dates[0]
    for date_i in range(1, len(dates)):
        if kept >= rule.count:
            kept = 0
            rule_i += 1
            if rule_i >= len(keep):
                # Delete older dates
                print('Del remaining')
                for d in range(date_i, len(dates)):
                    print(f'Del {dates[date_i]}')
                break
            rule = keep[rule_i]
            print(f'Rule {rule}')

        if (dates[date_i] - last_kept).days < rule.interval:
            print(f'Del {dates[date_i]}')
        else:
            kept += 1
            last_kept = dates[date_i]


delete()
