
import json
import os
from datetime import datetime, date

from missal1962.constants import *
from missal1962.missal import MissalFactory
from missal1962.models import LiturgicalDay


HERE = os.path.abspath(os.path.dirname(__file__))


def _to_date_obj(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None


def test_tempora():
    with open(os.path.join(HERE, 'tempora_fixtures.json')) as fh:
        expected = json.load(fh)

    for year, dates in sorted(expected.items()):
        missal = MissalFactory.create(int(year))
        assert _to_date_obj(dates[0]) == missal.get_day_by_id(TEMPORA_QUADP1_0)[0]
        assert _to_date_obj(dates[1]) == missal.get_day_by_id(TEMPORA_QUADP3_3)[0]
        assert _to_date_obj(dates[2]) == missal.get_day_by_id(TEMPORA_PASC0_0)[0]
        assert _to_date_obj(dates[3]) == missal.get_day_by_id(TEMPORA_PASC5_4)[0]
        assert _to_date_obj(dates[4]) == missal.get_day_by_id(TEMPORA_PASC7_0)[0]
        assert _to_date_obj(dates[5]) == missal.get_day_by_id(TEMPORA_PENT01_4)[0]
        assert _to_date_obj(dates[6]) == missal.get_day_by_id(TEMPORA_ADV1_0)[0]
        # TEMPORA_EPI4_0 might not exist in given year, then None is returned
        actual = missal.get_day_by_id(TEMPORA_EPI4_0)[0] if \
            missal.get_day_by_id(TEMPORA_EPI4_0) else None
        assert _to_date_obj(dates[7]) == actual
        assert _to_date_obj(dates[8]) == missal.get_day_by_id(TEMPORA_PENT_6)[0]
        assert _to_date_obj(dates[9]) == missal.get_day_by_id(NAT2_0)[0]
        assert _to_date_obj(dates[10]) == missal.get_day_by_id(SANCTI_10_DUr)[0]
        # NAT1_0 might not exist in given year, then None is returned
        actual = missal.get_day_by_id(NAT1_0)[0] if \
            missal.get_day_by_id(NAT1_0) else None
        assert _to_date_obj(dates[11]) == actual


def test_semi_sancti_days_all_souls():
    missal = MissalFactory.create(2008)
    assert date(2008, 11, 3) == missal.get_day_by_id(SANCTI_11_02_1)[0]

    missal = MissalFactory.create(2014)
    assert date(2014, 11, 3) == missal.get_day_by_id(SANCTI_11_02_1)[0]

    missal = MissalFactory.create(2015)
    assert date(2015, 11, 2) == missal.get_day_by_id(SANCTI_11_02_1)[0]

    missal = MissalFactory.create(2063)
    assert date(2063, 11, 2) == missal.get_day_by_id(SANCTI_11_02_1)[0]


def test_semi_sancti_days_feb_24_related():
    missal = MissalFactory.create(2012)
    assert date(2012, 2, 25) == missal.get_day_by_id(SANCTI_02_24_1)[0]
    assert date(2012, 2, 28) == missal.get_day_by_id(SANCTI_02_27_1)[0]

    missal = MissalFactory.create(2016)
    assert date(2016, 2, 25) == missal.get_day_by_id(SANCTI_02_24_1)[0]
    assert date(2016, 2, 28) == missal.get_day_by_id(SANCTI_02_27_1)[0]

    missal = MissalFactory.create(2017)
    assert date(2017, 2, 24) == missal.get_day_by_id(SANCTI_02_24_1)[0]
    assert date(2017, 2, 27) == missal.get_day_by_id(SANCTI_02_27_1)[0]

    missal = MissalFactory.create(2018)
    assert date(2018, 2, 24) == missal.get_day_by_id(SANCTI_02_24_1)[0]
    assert date(2018, 2, 27) == missal.get_day_by_id(SANCTI_02_27_1)[0]


def test_concurrency_12_08_conceptione_immaculata_bmv():
    assert [SANCTI_12_08_1, TEMPORA_ADV2_0] == [i.id for i in MissalFactory.create(1907)[date(1907, 12, 8)]]
    assert [SANCTI_12_08_1, TEMPORA_ADV2_0] == [i.id for i in MissalFactory.create(1912)[date(1912, 12, 8)]]
    assert [SANCTI_12_08_1, TEMPORA_ADV2_1] == [i.id for i in MissalFactory.create(1913)[date(1913, 12, 8)]]


def test_concurrency_1_2_class_feast_of_the_lord_occurring_on_sunday_2_class():
    assert [SANCTI_01_06_1] == [i.id for i in MissalFactory.create(2013)[date(2013, 1, 6)]]
    assert [SANCTI_01_06_1] == [i.id for i in MissalFactory.create(2036)[date(2036, 1, 6)]]
    assert [TEMPORA_EPI1_0] == [i.id for i in MissalFactory.create(2013)[date(2013, 1, 13)]]
    assert [TEMPORA_EPI1_0] == [i.id for i in MissalFactory.create(2036)[date(2036, 1, 13)]]
    assert [SANCTI_08_06_1] == [i.id for i in MissalFactory.create(1911)[date(1911, 8, 6)]]
    assert [SANCTI_08_06_1] == [i.id for i in MissalFactory.create(1922)[date(1922, 8, 6)]]


def test_concurrency_nativity_vigil():
    assert [SANCTI_12_24_1] == [i.id for i in MissalFactory.create(1950)[date(1950, 12, 24)]]
    assert [SANCTI_12_24_1] == [i.id for i in MissalFactory.create(2000)[date(2000, 12, 24)]]


def test_liturgical_day_model_simple_case():
    assert LiturgicalDay(TEMPORA_EPI2_3, date(2002, 1, 23)).rank == 4
    assert LiturgicalDay(TEMPORA_EPI2_3, date(2002, 1, 23)).weekday == 2
    assert LiturgicalDay(TEMPORA_QUADP1_0, date(2002, 1, 27)).rank == 2
    assert LiturgicalDay(TEMPORA_QUADP1_0, date(2002, 1, 27)).weekday == 6
    assert LiturgicalDay(TEMPORA_QUADP1_0, date(2002, 1, 28)).weekday == 6


def test_liturgical_day_model_tempora_rank_advent():
    # 2002
    assert LiturgicalDay(TEMPORA_ADV3_1, date(2002, 12, 16)).rank == 3
    assert LiturgicalDay(TEMPORA_ADV3_2, date(2002, 12, 17)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_3, date(2002, 12, 18)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_4, date(2002, 12, 19)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_5, date(2002, 12, 20)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_6, date(2002, 12, 21)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV4_0, date(2002, 12, 22)).rank == 1
    assert LiturgicalDay(TEMPORA_ADV4_1, date(2002, 12, 23)).rank == 2
    # 2015
    assert LiturgicalDay(TEMPORA_ADV3_2, date(2015, 12, 15)).rank == 3
    assert LiturgicalDay(TEMPORA_ADV3_3, date(2015, 12, 16)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_4, date(2015, 12, 17)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_5, date(2015, 12, 18)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV3_6, date(2015, 12, 19)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV4_0, date(2015, 12, 20)).rank == 1
    assert LiturgicalDay(TEMPORA_ADV4_1, date(2015, 12, 21)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV4_2, date(2015, 12, 22)).rank == 2
    assert LiturgicalDay(TEMPORA_ADV4_3, date(2015, 12, 23)).rank == 2


def test_liturgical_day_compare():
    rank_1_1 = LiturgicalDay(TEMPORA_PASC7_0, date(2015, 5, 24))
    rank_1_2 = LiturgicalDay(SANCTI_11_01_1, date(2015, 11, 1))
    rank_2_1 = LiturgicalDay(TEMPORA_EPI1_0, date(2015, 1, 11))
    rank_2_2 = LiturgicalDay(SANCTI_01_13_1, date(2015, 1, 13))
    rank_3_1 = LiturgicalDay(TEMPORA_QUAD5_5, date(2015, 3, 27))
    rank_3_2 = LiturgicalDay(SANCTI_03_28_1, date(2015, 3, 28))
    rank_4_1 = LiturgicalDay(TEMPORA_PENT01_1, date(2015, 6, 1))
    rank_4_2 = LiturgicalDay(SANCTI_08_09_2, date(2015, 8, 9))

    assert rank_1_1 == rank_1_2
    assert rank_1_1 >= rank_1_2
    assert rank_1_1 <= rank_1_2
    assert rank_1_1 != rank_2_1
    assert rank_1_1 > rank_2_1
    assert rank_1_1 > rank_3_1
    assert rank_1_1 > rank_4_1

    assert rank_2_1 < rank_1_1
    assert rank_2_1 == rank_2_2
    assert rank_2_1 >= rank_2_2
    assert rank_2_1 <= rank_2_2
    assert rank_2_1 != rank_3_2
    assert rank_2_1 > rank_3_1
    assert rank_2_1 > rank_4_1

    assert rank_3_1 < rank_1_1
    assert rank_3_1 < rank_2_1
    assert rank_3_1 == rank_3_2
    assert rank_3_1 >= rank_3_2
    assert rank_3_1 <= rank_3_2
    assert rank_3_1 != rank_4_1
    assert rank_3_1 > rank_4_1

    assert rank_4_1 < rank_1_1
    assert rank_4_1 < rank_2_1
    assert rank_4_1 < rank_3_1
    assert rank_4_1 != rank_3_1
    assert rank_4_1 == rank_4_2
    assert rank_4_1 >= rank_4_2
    assert rank_4_1 <= rank_4_2
