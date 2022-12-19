"""Gets epa emissions data

NOTE: This source uses 100 year potential. 
"""

import pandas as pd
from pathlib import Path
from typing import List

from delta_e.utils import FileReader

class _ReadEpaEmissions: 
    """Reads in and formats EPA Emission values.
    
    https://www.epa.gov/climateleadership/ghg-emission-factors-hub
    https://www.epa.gov/sites/default/files/2018-03/documents/emission-factors_mar_2018_0.pdf
    """
    def __init__(self) -> None:
        self.file_path = Path("epa_emissions.csv")
        self.raw_data = FileReader(self.file_path).get_data()
        self.data = self._format_epa_data(self.raw_data)

    @staticmethod
    def _format_epa_data(data : pd.DataFrame) -> pd.DataFrame: 
        """Formats raw EPA emission data.
        
        Args: 
            data : pd.DataFrame
                Raw EPA dataframe 

        Returns: 
            pd.DataFrame
                Formatted EPA dataframe 
        """
        data = data.set_index('FUEL')
        emission_type = list(data)
        units = data.iloc[0,:].to_list()
        data = data.iloc[1:,:] # drop non-formatted unit row
        headers = pd.MultiIndex.from_tuples(zip(emission_type, units), names=['EMISSION','UNIT'])
        data.columns = headers
        return data.astype('float')

class EpaEmissions:
    """Processes EPA Emissions."""
    
    def __init__(self) -> None:
        self.data = _ReadEpaEmissions().data
        
    @staticmethod
    def _check_epa_emission(emissions : List[str]): 
        """Error handler for emission type.
        
        Args: 
            emissions : List[str]
                List of emissions to index over

        Raises: 
            Value Error
                If emission is not in set ('co2','n2o','ch4')
        """

        if not all(emission in ['co2','n2o','ch4'] for emission in emissions):
            raise ValueError(
                f"One or more supplied emission of {emissions} are not valid. "
                f"All emissions must be in the set ('co2','n2o','ch4')"
            )

    def get_available_fuels(self) -> List[str]:
        """Gets available fuel types.
        
        Returns:
            List[str]
                Available fuel types in EPA dataset
        """
        return self.data.index.to_list()

    def get_gwp(self, emissions : List[str] = ['co2','n2o','ch4']) -> pd.DataFrame:
        """Gets global warming potential adjusted emissions. 
        
        This function performs unit conversions and collapses the different 
        emission types to a single co2 equivalent value for each fuel. 

        Args: 
            emissions : List[str]
                Emissions from the EPA to include in the gwp calcualtion. 
                Must be in the set ('co2','n2o','ch4')

        Returns: 
            pd.DataFrame
                dataframe where each fuel has a calculated single GWP value 

        Example: 
            >>> epa = EpaEmissions()
            >>> gwp = epa.get_gwp()
            >>> gwp.loc['Natural Gas', ('co2_eq', 'kT/PJ')]
            >>> 50.3 # kT / PJ
        """

        # check user arguments 
        self._check_epa_emission(emissions)

        # Convert co2 factors from kg/mmbtu to MT/PJ 
        # kg/mmbtu * 1mmbtu/1.055GJ * 1000000GJ / PJ * 1T/1000kg * 1kT/1000T
        # Multiply by global warming potential to get co2_eq
        co2 = self.data['co2_factor'].iloc[:,0].astype(float) * (1/1.055) * self.data['co2_gwp'].iloc[:,0].astype(float)

        # Convert ch4 and n2o factors from g/mmbtu to MT/PJ 
        # kg/mmbtu * 1mmbtu/1.055GJ * 1000000GJ / PJ * 1T/1000000g * 1kT/1000T
        # Multiply by global warming potential to get co2_eq
        ch4 = self.data['ch4_factor'].iloc[:,0].astype(float) * (1/1055) * self.data['ch4_gwp'].iloc[:,0].astype(float)
        n2o = self.data['n2o_factor'].iloc[:,0].astype(float) * (1/1055) * self.data['n2o_gwp'].iloc[:,0].astype(float)

        # Find total CO2 equivalent
        fuel_lookup = {'co2':co2, 'ch4':ch4, 'n2o':n2o}
        df = pd.DataFrame(fuel_lookup).set_axis(self.data.index)
        df = df[emissions] # only include user specified emissions 
        df['co2_eq'] = round(df.sum(axis=1),4).astype(float)
        
        # drop all non-co2eq columns and add units 
        co2eq = pd.DataFrame(df['co2_eq']) # keep as df for reindexing 
        headers = pd.MultiIndex.from_tuples(zip(['co2_eq'],['kT/PJ']), names=['EMISSION','UNIT'])
        co2eq.columns = headers
        return co2eq

    def get_osemosys_emissions(
        self,
        epa_fuel : str,
        regions : List[str], 
        technologies : List[str],
        emissions : List[str], 
        modes : List[int],
        years : List[int],
        epa_emissions : List[int] = ['co2','n2o','ch4']
    ) -> pd.DataFrame:
        """Creates emission activity ratio dataframe for OSeMOSYS Models.

        Args: 
            epa_fuel : str,
                Fuel from EPA dataset 
            regions : List[str], 
                Regions in the OSeMOSYS Model 
            technologies : List[str],
                Techs to attach the EAR value to 
            emissions : List[str], 
                Emission set 
            modes : List[int],
                Modes to attach emission value to 
            years : List[int],
                Years to attach emission value to 
            epa_emissions : List[str] = ['co2','n2o','ch4']
                Emissions to include from EPA when calculating global warming
                potential 

        Returns:
            pd.DataFrame
                EmissionActivityRatio otoole formatted dataframe with columns: 
                [REGION, TECHNOLOGY, EMISSION, MODE_OF_OPERATION, YEAR, VALUE] 

        Example: 
            >>> epa = EpaEmissions()
            >>> epa.get_osemosys_emissions(
                    epa_fuel='Natural Gas,
                    regions=['BC'],
                    technologies=['GAS'],
                    emissions=['CO2'], 
                    modes=[1,2],
                    years=[2020,2021])
        """

        self._check_epa_emission(emissions)

        co2_eq = self.get_gwp(epa_emissions)

        df = pd.DataFrame()
        index = pd.MultiIndex.from_product(
            [regions, technologies, emissions, modes, years], 
            names=["REGION", "TECHNOLOGY", "EMISSION", "MODE_OF_OPERATION", "YEAR"]
        )
        df = df.reindex(index)
        df['VALUE'] = co2_eq.loc[epa_fuel]['co2_eq']
        return df.reset_index()[["REGION", "TECHNOLOGY", "EMISSION", "MODE_OF_OPERATION", "YEAR", "VALUE"]]
