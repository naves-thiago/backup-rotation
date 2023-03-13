import pytest
import datetime, os
from typing import Any, Callable
import backup
from backup import get_delete_dates, Rule, file_names_to_dates, get_delete_file_names

class Mock_file_ops:
    def __init__(self):
        self.dir_files: dict[str, list[str]] = {}
        self.calls: dict[str, list[Any]] = {
            'listdir': [],
            'remove': [],
            'move': []
        }

    def listdir(self, path) -> list[str]:
        self.calls['listdir'].append(path)
        return self.dir_files[path].copy()

    def remove(self, path):
        self.calls['remove'].append(path)
        dir_name = os.path.dirname(path)
        file_name = os.path.basename(path)
        self.param_remove_path = path
        self.dir_files[dir_name].remove(file_name)

    def move(self, src: str, dst: str):
        self.calls['move'].append((src, dst))
        self.param_move_src = src
        self.param_move_dst = dst
        src_dir = os.path.dirname(src)
        src_file_name = os.path.basename(src)
        dst_dir = os.path.dirname(dst)
        dst_file_name = os.path.basename(dst)
        assert src_dir in self.dir_files
        assert src_file_name in self.dir_files[src_dir]
        assert dst_dir in self.dir_files
        assert dst_file_name not in self.dir_files[dst_dir]
        self.dir_files[src_dir].remove(src_file_name)
        self.dir_files[dst_dir].append(dst_file_name)


def test_get_delete_dates_empty_dates():
    keep = [Rule(5, 1)]
    assert get_delete_dates([], keep) == []


def test_get_delete_dates_empty_rules():
    with pytest.raises(ValueError):
        get_delete_dates([datetime.date(2022, 1, 1)], [])

def test_1_rule_too_few():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_exact():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_too_many():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete

def test_1_rule_interval_2_too_few_consecutive():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_too_few_skipping():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_exact_consecutive():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_exact_skipping():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_too_many_consecutive():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete

def test_1_rule_interval_2_too_many_skipping():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 11),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete

def test_1_rule_too_few_out_of_order():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_exact_out_of_order():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_too_many_out_of_order():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete

def test_1_rule_interval_2_too_few_consecutive_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_too_few_skipping_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 5),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_exact_consecutive_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 2),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_exact_skipping_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
    ]

    assert get_delete_dates(dates, keep) == []

def test_1_rule_interval_2_too_many_consecutive_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete

def test_1_rule_interval_2_too_many_skipping_out_of_order():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 1),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
    }

    assert set(get_delete_dates(dates, keep)) == to_delete


def test_2_rules_too_few_1st_consecutive():
    keep = [
        Rule(5, 2),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_too_few_1st_skipping():
    keep = [
        Rule(5, 2),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_too_few_2nd():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_too_few_2nd_consecutive():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_too_few_2nd_skipping():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_too_few_2nd_skipping_2():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_exact_2nd_consecutive():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_exact_2nd_skipping():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_exact_2nd_skipping_2():
    keep = [
        Rule(5, 1),
        Rule(3, 4),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 11),
    ]

    assert get_delete_dates(dates, keep) == []

def test_2_rules_1_too_many_2nd_consecutive():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
    ]

    assert get_delete_dates(dates, keep) == [datetime.date(2022, 1, 4)]

def test_2_rules_1_too_many_2nd_skipping_delete_first():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
    ]

    assert get_delete_dates(dates, keep) == [datetime.date(2022, 1, 6)]

def test_2_rules_1_too_many_2nd_skipping_keep_first():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13),
    ]

    assert get_delete_dates(dates, keep) == [datetime.date(2022, 1, 1)]

def test_2_rules_2_too_many_2nd_consecutive():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
    ]

    assert set(get_delete_dates(dates, keep)) == {
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
    }

def test_2_rules_2_too_many_2nd_skipping():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13),
    ]

    assert set(get_delete_dates(dates, keep)) == {
        datetime.date(2022, 1, 8), # Too close to the previous date
        datetime.date(2022, 1, 1), # oldest
    }

def test_2_rules_2_too_many_2nd_skipping_2():
    keep = [
        Rule(5, 1),
        Rule(3, 2),
    ]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13),
        datetime.date(2022, 1, 14),
        datetime.date(2022, 1, 15),
    ]

    assert set(get_delete_dates(dates, keep)) == {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
    }

def test_3_rules():
    keep = [
            Rule(5, 1),
            Rule(3, 3),
            Rule(3, 9),
    ]

    dates = [
        datetime.date(2022, 1, 1), # del
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3), # del
        datetime.date(2022, 1, 4), # del
        datetime.date(2022, 1, 5), # del
        datetime.date(2022, 1, 6), # del
        datetime.date(2022, 1, 7), # del
        datetime.date(2022, 1, 8), # del
        datetime.date(2022, 1, 9), # del
        datetime.date(2022, 1, 10), # del
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 12), # del
        datetime.date(2022, 1, 13), # del
        datetime.date(2022, 1, 14), # del
        datetime.date(2022, 1, 15), # del
        datetime.date(2022, 1, 16), # del
        datetime.date(2022, 1, 17), # del
        datetime.date(2022, 1, 18), # del
        datetime.date(2022, 1, 19), # del
        datetime.date(2022, 1, 20),
        datetime.date(2022, 1, 21), # del
        datetime.date(2022, 1, 22), # del
        datetime.date(2022, 1, 23), # del
        datetime.date(2022, 1, 24), # del
        datetime.date(2022, 1, 25), # del
        datetime.date(2022, 1, 26), # del
        datetime.date(2022, 1, 27), # del
        datetime.date(2022, 1, 28), # del
        datetime.date(2022, 1, 29),
        datetime.date(2022, 1, 30), # del
        datetime.date(2022, 1, 31), # del
        datetime.date(2022, 2, 1),
        datetime.date(2022, 2, 2), # del
        datetime.date(2022, 2, 3), # del
        datetime.date(2022, 2, 4),
        datetime.date(2022, 2, 5), # del
        datetime.date(2022, 2, 6), # del
        datetime.date(2022, 2, 7),
        datetime.date(2022, 2, 8),
        datetime.date(2022, 2, 9),
        datetime.date(2022, 2, 10),
        datetime.date(2022, 2, 11),
    ]

    to_delete = {
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13),
        datetime.date(2022, 1, 14),
        datetime.date(2022, 1, 15),
        datetime.date(2022, 1, 16),
        datetime.date(2022, 1, 17),
        datetime.date(2022, 1, 18),
        datetime.date(2022, 1, 19),
        datetime.date(2022, 1, 21),
        datetime.date(2022, 1, 22),
        datetime.date(2022, 1, 23),
        datetime.date(2022, 1, 24),
        datetime.date(2022, 1, 25),
        datetime.date(2022, 1, 26),
        datetime.date(2022, 1, 27),
        datetime.date(2022, 1, 28),
        datetime.date(2022, 1, 30),
        datetime.date(2022, 1, 31),
        datetime.date(2022, 2, 2),
        datetime.date(2022, 2, 3),
        datetime.date(2022, 2, 5),
        datetime.date(2022, 2, 6),
    }

    deleted = set(get_delete_dates(dates, keep))
    assert to_delete == deleted

def test_3_rules_2():
    keep = [
        Rule(5, 1),
        Rule(3, 3),
        Rule(3, 9),
    ]

    dates = [
        datetime.date(2022, 1, 1), # del
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 19),
        datetime.date(2022, 1, 28),

        datetime.date(2022, 2, 6),
        datetime.date(2022, 2, 9),
        datetime.date(2022, 2, 12),

        datetime.date(2022, 2, 15),
        datetime.date(2022, 2, 16),
        datetime.date(2022, 2, 17),
        datetime.date(2022, 2, 18),
        datetime.date(2022, 2, 19),
    ]

    assert get_delete_dates(dates, keep) == [datetime.date(2022, 1, 1)]


def test_file_names_to_dates_empty():
    assert file_names_to_dates([]) == []


def test_file_names_to_dates_1_file():
    assert file_names_to_dates(['AN_ERP_2022_09_08-22_00.fdb']) == [('AN_ERP_2022_09_08-22_00.fdb', datetime.date(2022, 9, 8))]


def test_file_names_to_dates_multiple_files():
    files = [
            'AN_ERP_2022_09_08-22_00.fdb',
            'AN_ERP_2020_01_09-14_50.fdb',
            'Contas_2022_08_05-22_00.fdb',
            'Contas_LEO_2022_08_13-22_00.fdb']

    out = [
            ('AN_ERP_2022_09_08-22_00.fdb', datetime.date(2022, 9, 8)),
            ('AN_ERP_2020_01_09-14_50.fdb', datetime.date(2020, 1, 9)),
            ('Contas_2022_08_05-22_00.fdb', datetime.date(2022, 8, 5)),
            ('Contas_LEO_2022_08_13-22_00.fdb', datetime.date(2022, 8, 13))]

    assert file_names_to_dates(files) == out


def test_file_names_to_dates_1_invalid_file():
    assert file_names_to_dates(['bla.fdb']) == []


def test_file_names_to_dates_multiple_files_with_invalid_mixed():
    files = [
            'AN_ERP_2022_09_08-22_00.fdb',
            'AN_ERP_2020_01_09-14_50.fdb',
            'foo.fdb',
            'Contas_2022_08_05-22_00.fdb',
            '',
            'Contas_LEO_2022_08_13-22_00.fdb']

    out = [
            ('AN_ERP_2022_09_08-22_00.fdb', datetime.date(2022, 9, 8)),
            ('AN_ERP_2020_01_09-14_50.fdb', datetime.date(2020, 1, 9)),
            ('Contas_2022_08_05-22_00.fdb', datetime.date(2022, 8, 5)),
            ('Contas_LEO_2022_08_13-22_00.fdb', datetime.date(2022, 8, 13))]

    assert file_names_to_dates(files) == out


def test_get_delete_file_names():
    keep = [Rule(5, 1)]

    files = [
        'foo_bar_2022_01_01-22_00.fdb',
        'foo_bar_2022_01_02-22_00.fdb',
        'foo_bar_2022_01_03-22_00.fdb',
        'foo_bar_2022_01_04-22_00.fdb',
        'foo_bar_2022_01_05-22_00.fdb',
        'foo_bar_2022_01_06-22_00.fdb',
        'foo_bar_2022_01_07-22_00.fdb',

        'asd_2022_01_01-22_00.fdb',
        'asd_2022_01_02-22_00.fdb',
        'asd_2022_01_03-22_00.fdb',
        'asd_2022_01_04-22_00.fdb',
        'asd_2022_01_05-22_00.fdb',
        'asd_2022_01_06-22_00.fdb',
        'asd_2022_01_07-22_00.fdb',

        'aaa_2022_01_01-22_00.fdb',
        'aaa_2022_01_02-22_00.fdb',
        'aaa_2022_01_03-22_00.fdb',
        'aaa_2022_01_04-22_00.fdb',
        'aaa_2022_01_05-22_00.fdb',
        'aaa_2022_01_06-22_00.fdb',
        'aaa_2022_01_07-22_00.fdb',
    ]

    to_delete = {
        'foo_bar_2022_01_01-22_00.fdb',
        'foo_bar_2022_01_02-22_00.fdb',
        'asd_2022_01_01-22_00.fdb',
        'asd_2022_01_02-22_00.fdb',
        'aaa_2022_01_01-22_00.fdb',
        'aaa_2022_01_02-22_00.fdb',
    }

    assert set(get_delete_file_names(files, keep)) == to_delete


def test_do_backup_first_upload():
    mock = Mock_file_ops()
    orig_do_move: Callable = backup.do_move
    orig_do_remove: Callable = backup.do_remove
    orig_do_listdir: Callable = backup.do_listdir
    backup.do_move = mock.move
    backup.do_remove = mock.remove
    backup.do_listdir = mock.listdir

    files = ['bar_2022_01_06-22_00.fdb', 'foo_2022_01_06-22_00.fdb', 'asd_2022_01_06-22_00.fdb']
    mock.dir_files = {
        'upload': files,
        'backups': []
    }

    rules = [Rule(5, 1)]
    try:
        res = backup.do_backup('backups', 'upload', ['foo', 'bar', 'asd'], rules)
        assert res
    finally:
        backup.do_move = orig_do_move
        backup.do_remove = orig_do_remove
        backup.do_listdir = orig_do_listdir

    assert len(mock.calls['remove']) == 0
    assert len(mock.dir_files['upload']) == 0
    assert len(mock.dir_files['backups']) == 3
    for fname in files:
        assert fname in mock.dir_files['backups']


def test_do_backup_delete_1():
    mock = Mock_file_ops()
    orig_do_move: Callable = backup.do_move
    orig_do_remove: Callable = backup.do_remove
    orig_do_listdir: Callable = backup.do_listdir
    backup.do_move = mock.move
    backup.do_remove = mock.remove
    backup.do_listdir = mock.listdir

    upload = ['bar_2022_01_09-22_00.fdb']
    backups = ['bar_2022_01_06-22_00.fdb',
               'bar_2022_01_07-22_00.fdb',
               'bar_2022_01_08-22_00.fdb']
    mock.dir_files = {
        'upload': upload,
        'backups': backups
    }

    rules = [Rule(3, 1)]
    try:
        res = backup.do_backup('backups', 'upload', ['bar'], rules)
        assert res
    finally:
        backup.do_move = orig_do_move
        backup.do_remove = orig_do_remove
        backup.do_listdir = orig_do_listdir

    assert set(mock.calls['remove']) == set(['backups/bar_2022_01_06-22_00.fdb'])

    backed_up = set([
        'bar_2022_01_07-22_00.fdb',
        'bar_2022_01_08-22_00.fdb',
        'bar_2022_01_09-22_00.fdb'])

    assert len(mock.dir_files['upload']) == 0
    assert set(mock.dir_files['backups']) == backed_up
