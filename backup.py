import os
import sys
import shutil
import json
import datetime

# Config format
#{
#   "sources": ["test/a.txt", "test/b/b.txt"], # Files to backup - Array of file names
#   "destinations": "test/out",                # Destination directory
#   "keep": [[30, 1], [10, 7], [10, 30]]       # History to keep - Array of [number of files, period]
#                                              # Example: Every file for the most recent 30,
#                                              #   then oldest 1 for each 7 older, keeping 10 backed-up,
#                                              #   then oldest 1 for each 30 older, keeping 10 backed-up
#}

# e.strftime("%d/%m/%Y, %H:%M:%S")

with open('config.json') as c:
    global config
    config = json.load(c)

if not config:
    print('Falha ao carregar as configurações!')
    exit(1)

def get_delete_list2(dates: list, keep: list) -> list:
    out = []
    group_start = 0
    for group in keep:
        count, period = group
        for i in range(group_start, min(len(dates), group_start + count * period)):
            if (i - group_start + 1) % period != 0:
                out.append(dates[i])
        group_start += count * period

    out.extend(dates[group_start:])
    return out

def get_delete_list(dates: list, keep: list) -> list:
    out = []
    group_count = 0
    count, period = keep[0]
    for date in dates:
        
#initial = datetime.datetime(2022, 9, 1)
#files = [*map(lambda x: initial + datetime.timedelta(days=x), range(40))]
files = [*range(40)]
df = get_delete_list(files, config['keep'])
print(f"Rule = {config['keep']}")
print(f"Files = {files}")
print(f"Del = {df}")

ds = set(df)
keep = []
for f in files:
    if f not in ds:
        keep.append(f)
print(f"Keep = {keep}")

