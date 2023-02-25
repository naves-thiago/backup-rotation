import datetime, os, re
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


def file_names_to_dates(file_list: list[str]) -> list[tuple[str, datetime.date]]:
    regex = re.compile(r'.+_([0-9]{4})_([0-9]{2})_([0-9]{2})-[0-9]{2}_[0-9]{2}\.fdb')
    out = []
    for file in file_list:
        m = regex.match(file)
        if not m:
            # report?
            continue
        out.append((file, datetime.date(*map(int, m.groups()))))
    return out


def list_files(base_dir: str) -> list[tuple[str, datetime.date]]:
    return file_names_to_dates(os.listdir(base_dir))

