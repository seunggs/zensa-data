import numpy as np
import datetime
from basecrm import remove_empty_rows, normalize_date_format, keep_cols, sort_by_key

# test_arr = np.array([[5,6,1], [1,2,13], [11,12,2]])
#
# def test_sort_by_index_2d():
#     assert np.array_equiv(sort_by_index_2d(2, test_arr), np.array([['5','6','1'], ['11','12','2'], ['1','2','13']]))

def test_remove_empty_rows():
    rows = np.array([
        ['a-val1', 'b-val1', 'c-val1'],
        [],
        ['a-val3', 'b-val3', 'c-val3'],
    ])
    actual = remove_empty_rows(rows)
    expected = np.array([
        ['a-val1', 'b-val1', 'c-val1'],
        ['a-val3', 'b-val3', 'c-val3'],
    ])
    assert np.array_equiv(actual, expected)

def test_normalize_date_format():
    rows = np.array([
        ['a-val1', '2014-10-09T21:22:53Z', 'c-val1', '2015-10-09T21:22:53Z'],
        ['a-val2', '2014-11-09T21:22:53Z', 'c-val2', '2015-11-09T21:22:53Z'],
        ['a-val3', '2014-12-09T21:22:53Z', 'c-val3', '2015-12-09T21:22:53Z'],
    ])
    actual = normalize_date_format([1, 3], rows)
    expected = np.array([
        ['a-val1', '2014-10-09', 'c-val1', '2015-10-09'],
        ['a-val2', '2014-11-09', 'c-val2', '2015-11-09'],
        ['a-val3', '2014-12-09', 'c-val3', '2015-12-09'],
    ])
    assert np.array_equiv(actual, expected)

def test_keep_cols():
    keys_to_keep = ['a', 'c']
    all_keys = ['a', 'b', 'c', 'd']
    rows = np.array([
        ['a-val1', 'b-val1', 'c-val1', 'd-val1'],
        ['a-val2', 'b-val2', 'c-val2', 'd-val2'],
        ['a-val3', 'b-val3', 'c-val3', 'd-val3'],
    ])
    actual = keep_cols(keys_to_keep, all_keys, rows)
    expected = np.array([
        ['a-val1', 'c-val1'],
        ['a-val2', 'c-val2'],
        ['a-val3', 'c-val3'],
    ])
    assert np.array_equiv(actual, expected)

def test_sort_by_key():
    key = 'last_stage_change_at'
    np_arr_dtype = [
        ('name', '<U255'),
        ('stage_name', '<U255'),
        ('owner', '<U255'),
        ('company_id', 'i4'),
        ('added_on', 'datetime64[D]'),
        ('currency', '<U255'),
        ('decimal_value', 'f4'),
        ('last_stage_change_at', 'datetime64[D]'),
    ]
    np_arr_unstructured = [
        ('Hairless Men', 'Won', 'Nabil Khan', '75273924', '2014-11-18', 'CAD', '200.0', '2014-11-18'),
        ('Studio One Tattoo Supplies', 'Won', 'Nabil Khan', '76611544', '2014-12-04', 'CAD', '200.0', '2014-12-04'),
        ('Lucie Me', 'Won', 'Nabil Khan', '82952285', '2015-02-17', 'CAD', '200.0', '2015-02-17'),
        ('October 14th Tubes', 'Won', 'Nabil Khan', '72511784', '2014-10-15', 'CAD', '60.0', '2014-10-15'),
        ('Second Skin Removal', 'Won', 'Nabil Khan', '73244695', '2014-10-20', 'USD', '360.0', '2014-10-20'),
        ('Obsidian Rose Tattoo', 'Won', 'Nabil Khan', '73926144', '2014-10-30', 'CAD', '480.0', '2014-10-30'),
    ]
    np_arr_structured = np.array(np_arr_unstructured, dtype=np_arr_dtype)
    actual = sort_by_key('last_stage_change_at', np_arr_structured)
    print(actual)
    expected = np.array([
        ('October 14th Tubes', 'Won', 'Nabil Khan', '72511784', '2014-10-15', 'CAD', '60.0', '2014-10-15'),
        ('Second Skin Removal', 'Won', 'Nabil Khan', '73244695', '2014-10-20', 'USD', '360.0', '2014-10-20'),
        ('Obsidian Rose Tattoo', 'Won', 'Nabil Khan', '73926144', '2014-10-30', 'CAD', '480.0', '2014-10-30'),
        ('Hairless Men', 'Won', 'Nabil Khan', '75273924', '2014-11-18', 'CAD', '200.0', '2014-11-18'),
        ('Studio One Tattoo Supplies', 'Won', 'Nabil Khan', '76611544', '2014-12-04', 'CAD', '200.0', '2014-12-04'),
        ('Lucie Me', 'Won', 'Nabil Khan', '82952285', '2015-02-17', 'CAD', '200.0', '2015-02-17'),
    ], dtype=np_arr_dtype)
    assert np.array_equiv(actual, expected)
