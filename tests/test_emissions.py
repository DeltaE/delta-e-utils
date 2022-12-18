import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from pytest import fixture, raises, mark
from delta_e.epa_emissions import EpaEmissions, _ReadEpaEmissions

@fixture
def raw_epa_data() -> pd.DataFrame:
    """Raw input from EPA csv"""

    data = pd.DataFrame(
        [
            ["UNIT",'kg_per_mmBtu','g_per_mmBtu','g_per_mmBtu',np.NaN,np.NaN,np.NaN],
            ["Anthracite Coal",103.69,11,1.6,1,25,298],
            ['Bituminous Coal',93.28,11,1.6,1,25,298],
            ['Sub-bituminous Coal',97.17,11,1.6,1,25,298]
        ],
        columns=['FUEL','co2_factor','ch4_factor','n2o_factor','co2_gwp','ch4_gwp','n2o_gwp']
    )
    return data

@fixture
def formatted_epa_data() -> pd.DataFrame:
    columns = [
        ('co2_factor','kg_per_mmBtu'),
        ('ch4_factor','g_per_mmBtu'),
        ('n2o_factor','g_per_mmBtu'),
        ('co2_gwp',np.NaN),
        ('ch4_gwp',np.NaN),
        ('n2o_gwp',np.NaN),
    ]
    df = pd.DataFrame(
        [
            ["Anthracite Coal",103.69,11,1.6,1,25,298],
            ['Bituminous Coal',93.28,11,1.6,1,25,298],
            ['Sub-bituminous Coal',97.17,11,1.6,1,25,298]
        ]).set_index(0).rename_axis('FUEL')
    df.columns = pd.MultiIndex.from_tuples(columns, names=['EMISSION','UNIT'])
    return df.astype('float')

class TestReadEpaEmissions:
    def test_format_epa_data(self, raw_epa_data, formatted_epa_data):
        dummy_epa = _ReadEpaEmissions()
        actual = dummy_epa._format_epa_data(raw_epa_data)
        expected = formatted_epa_data
        assert_frame_equal(actual, expected)

class TestEpaEmissions:
    def test_get_available_fuels(self, formatted_epa_data): 
        epa = EpaEmissions()
        epa.data = formatted_epa_data
        actual = epa.get_available_fuels()
        expected = ["Anthracite Coal", 'Bituminous Coal', 'Sub-bituminous Coal']
        assert actual == expected

    @mark.parametrize("test_emission",[(['h2o']), (['co2', 'h2o'])], ids=['Single emission', 'Multiple emission'])
    def test_check_epa_emission_fail(self, formatted_epa_data, test_emission):
        epa = EpaEmissions()
        epa.data = formatted_epa_data
        with raises(ValueError):
            epa._check_epa_emission(emissions=test_emission)
            
    @mark.parametrize("test_emission,expected", [(['co2'], None), (['co2','n2o','ch4'], None)], ids=['Single emission', 'Multiple emission'])
    def test_check_epa_emission_passes(self, formatted_epa_data, test_emission, expected):
        epa = EpaEmissions()
        epa.data = formatted_epa_data
        actual = epa._check_epa_emission(emissions=test_emission)
        assert actual == expected

    @mark.parametrize("test_emission,expected", [(['co2'], 98.2844), (['co2','n2o','ch4'], 98.997)], ids=['Single emission', 'Multiple emission'])
    def test_get_gwp(self, formatted_epa_data, test_emission, expected):
        epa = EpaEmissions()
        epa.data = formatted_epa_data
        gwp = epa.get_gwp(emissions=test_emission)
        actual = gwp.loc['Anthracite Coal',('co2_eq', 'kT/PJ')]
        assert actual == expected

