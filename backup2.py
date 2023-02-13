import datetime
from dataclasses import dataclass

@dataclass()
class Rule:
    count: int
    interval: int

#   "keep": [[30, 1], [10, 7], [10, 30]]       # History to keep - Array of [number of files, period]
#                                              # Example: Every file for the most recent 30,
#                                              #   then oldest 1 for each 7 older, keeping 10 backed-up,

def delete(dates: list[datetime.date], rules: list[Rule]) -> list[datetime.date]:
    rule_i = 0
    rule = rules[0]
    kept = 1
    last_kept = dates[0]
    delete = []
    for date_i in range(1, len(dates)):
        if kept >= rule.count:
            kept = 0
            rule_i += 1
            if rule_i >= len(rules):
                # Delete older dates
                for d in range(date_i, len(dates)):
                    delete.append(dates[d])
                break
            rule = rules[rule_i]

        if (dates[date_i] - last_kept).days < rule.interval and (len(dates) - date_i) > (rule.count - kept):
            delete.append(dates[date_i])
        else:
            kept += 1
            last_kept = dates[date_i]

    return delete
