#import pytest
import datetime
from backup import delete, Rule, file_names_to_dates

def test_1_rule_too_few():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert delete(dates, keep) == []

def test_1_rule_exact():
    keep = [Rule(5, 1)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
    ]

    assert delete(dates, keep) == []

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
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
    }

    assert set(delete(dates, keep)) == to_delete

def test_1_rule_interval_2_too_few_consecutive():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]

    assert delete(dates, keep) == []

def test_1_rule_interval_2_too_few_skipping():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
    ]

    assert delete(dates, keep) == []

def test_1_rule_interval_2_exact_consecutive():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 5),
    ]

    assert delete(dates, keep) == []

def test_1_rule_interval_2_exact_skipping():
    keep = [Rule(5, 2)]

    dates = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 5),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
    ]

    assert delete(dates, keep) == []

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
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 4),
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 11),
    }

    assert set(delete(dates, keep)) == to_delete

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
        datetime.date(2022, 1, 11),
    }

    assert set(delete(dates, keep)) == to_delete

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == []

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

    assert delete(dates, keep) == [datetime.date(2022, 1, 6)]

def test_2_rules_1_too_many_2nd_skipping_delete_first():
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
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 12),
    ]

    assert delete(dates, keep) == [datetime.date(2022, 1, 6)]

def test_2_rules_1_too_many_2nd_skipping_keep_first():
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
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 13),
    ]

    assert delete(dates, keep) == [datetime.date(2022, 1, 13)]

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

    assert set(delete(dates, keep)) == {
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 8),
    }

def test_2_rules_2_too_many_2nd_skipping():
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
        datetime.date(2022, 1, 8),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 14),
    ]

    assert set(delete(dates, keep)) == {
        datetime.date(2022, 1, 6),  # Too close to the previous date
        datetime.date(2022, 1, 14), # Oldest
    }

def test_2_rules_2_too_many_2nd_skipping_2():
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
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 11),
        datetime.date(2022, 1, 13),
        datetime.date(2022, 1, 15),
    ]

    assert set(delete(dates, keep)) == {
        datetime.date(2022, 1, 13),
        datetime.date(2022, 1, 15),
    }

def test_3_rules():
    keep = [
            Rule(5, 1),
            Rule(3, 3),
            Rule(3, 9),
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

    to_delete = {
        datetime.date(2022, 1, 6),
        datetime.date(2022, 1, 7),
        datetime.date(2022, 1, 9),
        datetime.date(2022, 1, 10),
        datetime.date(2022, 1, 12),
        datetime.date(2022, 1, 13),
        datetime.date(2022, 1, 15),
        datetime.date(2022, 1, 16),
        datetime.date(2022, 1, 17),
        datetime.date(2022, 1, 18),
        datetime.date(2022, 1, 19),
        datetime.date(2022, 1, 20),
        datetime.date(2022, 1, 21),
        datetime.date(2022, 1, 22),
        datetime.date(2022, 1, 24),
        datetime.date(2022, 1, 25),
        datetime.date(2022, 1, 26),
        datetime.date(2022, 1, 27),
        datetime.date(2022, 1, 28),
        datetime.date(2022, 1, 29),
        datetime.date(2022, 1, 30),
        datetime.date(2022, 1, 31),
        datetime.date(2022, 2, 2),
        datetime.date(2022, 2, 3),
        datetime.date(2022, 2, 4),
        datetime.date(2022, 2, 5),
        datetime.date(2022, 2, 6),
        datetime.date(2022, 2, 7),
        datetime.date(2022, 2, 8),
        datetime.date(2022, 2, 9),
        datetime.date(2022, 2, 11),
    }

    deleted = set(delete(dates, keep))
    assert to_delete == deleted

def test_3_rules_2():
    keep = [
        Rule(5, 1),
        Rule(3, 3),
        Rule(3, 9),
    ]

    dates = [
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

    assert delete(dates, keep) == [datetime.date(2023, 2, 19)]


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
