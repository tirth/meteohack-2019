import logging
import pandas as pd

logger = logging.getLogger(__name__)


def read_ac_usage():
    usage_df: pd.DataFrame = pd.read_csv(r'data\ac_usage\38100019.csv')

    standalone_df = usage_df[lambda d: d['Air conditioners'] == 'Stand-alone air conditioner, as a percentage of all households']

    grouped = standalone_df[['REF_DATE', 'GEO', 'VALUE']].groupby('GEO')

    for group in grouped:
        print(group)


def read_ac_consumption() -> pd.DataFrame:
    consumption_df: pd.DataFrame = pd.read_csv(r'data/ac_consumption/010_Data_Données.csv', encoding='windows-1252')

    # brand_groups = consumption_df.groupby('BRAND_NAME')
    #
    # for brand in brand_groups:
    #     print(brand)

    return consumption_df


def ac_values(model_name: str):
    ac_data = read_ac_consumption()

    model_data = ac_data[lambda d: d['MODEL_NUM_1'] == model_name]

    if len(model_data) == 0:
        logger.warning(f'AC {model_name} not found')
        return

    if len(model_data) > 1:
        logger.warning(f'Multiple AC {model_name} found, selecting first')

    ac = model_data.iloc[0]

    return ac['COOL_CAP_BTU'], ac['EE_RATIO']
