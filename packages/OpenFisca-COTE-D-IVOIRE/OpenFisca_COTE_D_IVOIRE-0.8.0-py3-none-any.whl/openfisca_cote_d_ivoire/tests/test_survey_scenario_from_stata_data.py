# -*- coding: utf-8 -*-


import configparser
import logging
import os
import pandas as pd


from openfisca_core import periods
from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_cote_d_ivoire.survey_scenarios import CoteDIvoireSurveyScenario


log = logging.getLogger(__file__)


config_parser = configparser.SafeConfigParser()
config_parser.read(os.path.join(config_files_directory, 'raw_data.ini'))
data_is_available = config_parser.has_section("cote_d_ivoire")
if not data_is_available:
    log.info("No data available for Côte d'Ivoire")


def get_data_file_path():
    file_path_by_year = dict(config_parser.items("cote_d_ivoire"))
    return file_path_by_year['2014']


def create_dataframes_from_stata_data():
    data_file_path = get_data_file_path()
    # import pprint
    # dico_labels = pd.read_stata(data_file_path, iterator=True)
    # pprint.pprint(dico_labels.variable_labels())
    dataframe = pd.read_stata(data_file_path)
    person_variables = [
        'age',
        'formel_informel',
        'hhid',
        'id',
        'inc_act1_ind',
        'link_to_head',
        'sex'
        ]
    person_dataframe = dataframe[person_variables].copy()
    person_dataframe['salaire'] = person_dataframe.inc_act1_ind * (
        (person_dataframe.formel_informel == 1) | (person_dataframe.formel_informel == 1)
        )
    person_dataframe['household_legacy_role'] = (
        0 * (person_dataframe.link_to_head == 'chef de menage')
        + 1 * (person_dataframe.link_to_head == 'epouse ou mari')
        + 2 * (
            (person_dataframe.link_to_head != 'chef de menage') & (person_dataframe.link_to_head != 'epouse ou mari')
            )
        )

    household_id_by_hhid = (person_dataframe.hhid
        .drop_duplicates()
        .sort_values()
        .reset_index(drop = True)
        .reset_index()
        .rename(columns = {'index': 'household_id'})
        .set_index('hhid')
        .squeeze()
        )

    person_dataframe['household_id'] = person_dataframe['hhid'].map(household_id_by_hhid)
    person_dataframe['person_id'] = range(len(person_dataframe))
    person_dataframe = person_dataframe.rename(columns = {
        'inc_pension_ind': 'pension',
        'sex': 'sexe'
        })

    household_dataframe = pd.DataFrame(
        dict(household_id = range(person_dataframe.household_id.max()))
        )
    return person_dataframe, household_dataframe


def create_data_from_stata(create_dataframes = True):
    year = 2017
    data = dict()

    if create_dataframes:
        person_dataframe, household_dataframe = create_dataframes_from_stata_data()
        input_data_frame_by_entity = {
            'person': person_dataframe,
            'household': household_dataframe,
            }
        input_data_frame_by_entity_by_period = {periods.period(year): input_data_frame_by_entity}
        data['input_data_frame_by_entity_by_period'] = input_data_frame_by_entity_by_period

    else:
        data_file_path = get_data_file_path()
        data['stata_file_by_entity'] = dict(
            # household = os.path.join(data_directory, 'household.dta'),
            person = data_file_path,
            )
    return data


def test_survey_scenario(create_dataframes = True):
    circleci = 'CIRCLECI' in os.environ
    if circleci or not data_is_available:
        return

    year = 2017
    data = create_data_from_stata(create_dataframes = create_dataframes)
    survey_scenario = CoteDIvoireSurveyScenario(
        data = data,
        year = year,
        )
    df_by_entity = survey_scenario.create_data_frame_by_entity(
        variables = ['age', 'salaire', 'impot_general_revenu', 'impots_directs']
        )

    for entity, df in df_by_entity.items():
        log.debug(entity)
        log.debug(df)


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)
    test_survey_scenario()
    # test_ceq_survey_scenario()
