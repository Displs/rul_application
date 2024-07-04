import pandas as pd
import numpy as np
#from app.application import recent_path
from app.database.models import RpmParams, TempParams, PresParams, RatioParams,FlowParams, GeneralParams, Engine, Session
from sqlalchemy.sql.expression import func

temp_cols = ['T2_Total_temperature_at_fan_inlet_(°R)','T24_Total_temperature_at_LPC_outlet_(°R)', 'T30_Total_temperature_at_HPC_outlet_(°R)', 'T50_Total_temperature_at_LPT_outlet_(°R)']
pres_cols = ['P2_Pressure_at_fan_inlet_(psia)', 'P15_Total_pressure_in_bypass-duct_(psia)', 'P30_Total_pressure_at_HPC_outlet_(psia)', 'Ps30_Static_pressure_at_HPC_outlet_(psia)']
rpm_cols = ['Nf_Physical_fan_speed_(rpm)', 'Nc_Physical_core_speed_(rpm)', 'NRf_Corrected_fan_speed_(rpm)', 'NRc_Corrected_core_speed_(rpm)', 'Nf_dmd_Demanded_fan_speed_(rpm)', 'PCNfR_dmd_Demanded_corrected_fan_speed_(rpm)']
flow_cols = ['W31_HPT_coolant_bleed_(lbm/s)', 'W32_LPT_coolant_bleed_(lbm/s)', 'htBleed_Bleed_Enthalpy']
ratio_cols = ['epr_Engine_pressure_ratio_(P50/P2)', 'phi_Ratio_of_fuel_flow_to_Ps30_(pps/psi)', 'BPR_Bypass_Ratio', 'farB_Burner_fuel-air_ratio']
general = ['time_(cycles)']

def get_cols(df_param, cols) -> np.array:
    params = df_param[cols]
    num_arr = params.to_numpy()
    return num_arr

def write_temp_params(dataframe: pd.DataFrame) -> list:
    cols = get_cols(dataframe, temp_cols)
    obj = [TempParams(t2temp=x[0], t24temp=x[1], t30temp=x[2], t50temp=x[3]) for x in cols]
    return obj

def write_pres_params(dataframe: pd.DataFrame) -> list:
    cols = get_cols(dataframe, pres_cols)
    obj = [PresParams(p2pres=x[0], p15pres=x[1], p30pres=x[2], ps30pres=x[3]) for x in cols]
    return obj

def write_flow_params(dataframe: pd.DataFrame) -> list:
    cols = get_cols(dataframe, flow_cols)
    obj = [FlowParams(w31bleed=x[0], w32bleed=x[1], htbleed=x[2]) for x in cols]
    return obj

def write_rpm_params(dataframe: pd.DataFrame) -> list:
    cols = get_cols(dataframe, rpm_cols)
    obj = [RpmParams(nfrpm=x[0], ncrpm=x[1], nrfrpm=x[2], nrcrpm=x[3], nfdrpm=x[4], pcnfr=x[5]) for x in cols]
    return obj

def write_ratio_params(dataframe: pd.DataFrame) -> list:
    cols = get_cols(dataframe, ratio_cols)
    obj = [RatioParams(epr=x[0], phi=x[1], bpr=x[2], farb=x[3]) for x in cols]
    return obj

def write_general_params(dataframe: pd.DataFrame, last_engine: int) -> list:
    cols = get_cols(dataframe, general)
    obj = [GeneralParams(tcycle=int(x[0]), idengine = last_engine) for x in cols]
    return obj

def update_rul_results(rul_result: int) -> None:
    sess = Session()
    max_engine = sess.query(func.max(Engine.idengine)).scalar()
    sess.query(Engine).filter(Engine.idengine == max_engine).update({Engine.calc_rul: rul_result})
    sess.commit()


def write_to_db():
    sess = Session()
    df = pd.read_json('app/uploaded_files/test.json', orient='records')
    max_engine = sess.query(func.max(Engine.idengine)).scalar()
    sess.bulk_save_objects(write_temp_params(df))
    sess.bulk_save_objects(write_pres_params(df))
    sess.bulk_save_objects(write_flow_params(df))
    sess.bulk_save_objects(write_rpm_params(df))
    sess.bulk_save_objects(write_ratio_params(df))
    sess.bulk_save_objects(write_general_params(df, int(max_engine)))
    sess.commit()