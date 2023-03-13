import datetime, os, re, shutil
from dataclasses import dataclass

@dataclass()
class Rule:
    count: int
    interval: int

#   rules = [Rule(30, 1),       # History to keep - Array of [number of files, period]
#            Rule(10, 7),       # Example: On file per day for the most recent 30,
#            Rule(10, 28)]      #   then oldest 1 for each 7 days, keeping 10 backed-up,
#                               #   then 1 for each 28 days, keeping 10 backed-up.
#                               # NOTE: Each interval must be a multiple of the
#                               #   previous one.

def log(msg):
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{dt}] {msg}')


def get_delete_dates(dates: list[datetime.date], rules: list[Rule]) -> list[datetime.date]:
    if len(dates) == 0:
        return []

    if len(rules) == 0:
        raise ValueError('Must have at least 1 rule')

    dates = dates.copy()
    dates.sort()
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


def get_delete_file_names(file_list: list[str], rules: list[Rule]) -> list[str]:
    files_with_dates = file_names_to_dates(file_list)
    dates = list({f[1] for f in files_with_dates}) # set to list conversion to remove duplicates
    delete_dates = set(get_delete_dates(dates, rules))
    out = []
    for fname, fdate in files_with_dates:
        if fdate in delete_dates:
            out.append(fname)

    return out


def do_move(origin, destination):
    '''shutil.move wrapper to allow testing'''
    shutil.move(origin, destination)


def do_listdir(path) -> list[str]:
    '''os.listdir wrapper to allow testing'''
    return os.listdir(path)


def do_remove(path):
    '''os.remove wrapper to allow testing'''
    os.remove(path)


def do_backup(backups_dir: str, uploads_dir: str, expected_files_prefix: list[str], rules: list[Rule]) -> bool:
    uploaded_files = do_listdir(uploads_dir)

    if len(uploaded_files) != len(expected_files_prefix):
        log(f'Expected {len(expected_files_prefix)} files. Found {len(uploaded_files)}')
        return False

    # Check file name prefixes
    expected_files_prefix.sort()
    uploaded_files.sort()
    for i in range(len(expected_files_prefix)):
        if not uploaded_files[i].startswith(expected_files_prefix[i]):
            log(f'Unexpected file uploaded: {uploaded_files[i]}')
            return False

    # Check if the uploaded files would override files already stored
    existing_files = set(do_listdir(backups_dir))
    for f in uploaded_files:
        if f in existing_files:
            log(f'File {f} already exists')
            return False

    for f in uploaded_files:
        do_move(os.path.join(uploads_dir, f), os.path.join(backups_dir, f))

    del_list = get_delete_file_names(do_listdir(backups_dir), rules)
    for f in del_list:
        do_remove(os.path.join(backups_dir, f))

    return True


if __name__ == "__main__":
    backups_dir = '/backup/backups'
    uploads_dir = '/backup/importacao/upload'
    expected_files_prefix = ['AN_ERP_', 'Contas_', 'Contas_LEO']
    rules = [
        Rule(30, 1),
        Rule(16, 7),
        Rule(18, 28)
    ]

    do_backup(backups_dir, uploads_dir, expected_files_prefix, rules)
