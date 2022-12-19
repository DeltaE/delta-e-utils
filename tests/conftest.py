"""
    Dummy conftest.py for delta_e.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from pytest import fixture
import pandas as pd

# otoole formatted fixtures 

@fixture
def year():
    return pd.DataFrame(
        data=[2020, 2021, 2022, 2023, 2024], columns=["VALUE"]
    )

@fixture
def region():
    return pd.DataFrame(data=["BC"], columns=["VALUE"])

@fixture
def technology():    
    return pd.DataFrame(
        data=['GAS', 'HYDRO', 'WIND'], columns=["VALUE"]
    )

@fixture
def emission():    
    return pd.DataFrame(
        data=['CO2', 'N2O'], columns=["VALUE"]
    )

@fixture
def mode_of_operation():    
    return pd.DataFrame(
        data=[1, 2], columns=["VALUE"]
    )

