from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

columns = ['unit_number','time_(cycles)','operational_setting_1','operational_setting_2',
           'operational_setting_3','T2_Total_temperature_at_fan_inlet_(°R)','T24_Total_temperature_at_LPC_outlet_(°R)',
           'T30_Total_temperature_at_HPC_outlet_(°R)','T50_Total_temperature_at_LPT_outlet_(°R)','P2_Pressure_at_fan_inlet_(psia)',
           'P15_Total_pressure_in_bypass-duct_(psia)','P30_Total_pressure_at_HPC_outlet_(psia)','Nf_Physical_fan_speed_(rpm)',
           'Nc_Physical_core_speed_(rpm)','epr_Engine_pressure_ratio_(P50/P2)','Ps30_Static_pressure_at_HPC_outlet_(psia)',
           'phi_Ratio_of_fuel_flow_to_Ps30_(pps/psi)','NRf_Corrected_fan_speed_(rpm)','NRc_Corrected_core_speed_(rpm)','BPR_Bypass_Ratio',
           'farB_Burner_fuel-air_ratio','htBleed_Bleed_Enthalpy','Nf_dmd_Demanded_fan_speed_(rpm)','PCNfR_dmd_Demanded_corrected_fan_speed_(rpm)',
           'W31_HPT_coolant_bleed_(lbm/s)','W32_LPT_coolant_bleed_(lbm/s)', 26, 27]

nu_column = ['operational_setting_3', 'T2_Total_temperature_at_fan_inlet_(°R)', 'P2_Pressure_at_fan_inlet_(psia)', "P15_Total_pressure_in_bypass-duct_(psia)",
            'epr_Engine_pressure_ratio_(P50/P2)', 'farB_Burner_fuel-air_ratio', 'Nf_dmd_Demanded_fan_speed_(rpm)', 
            'PCNfR_dmd_Demanded_corrected_fan_speed_(rpm)', 'NRc_Corrected_core_speed_(rpm)']

def test_preprocessing(data, feature_to_split, feature_to_drop, window_size = 30):
    
    num_split = np.unique(data[feature_to_split])
    num_features = data.shape[1]-len(feature_to_drop)
    processed_data = np.zeros([0, window_size,num_features])
    
    for i in num_split:
        data_temp = data[data[feature_to_split] == i].drop(feature_to_drop, axis=1)
        singular_output_data = np.zeros([1, window_size,num_features])
        
        singular_output_data[0] = data_temp[-window_size:]
                
        processed_data = np.append(processed_data, singular_output_data, axis=0)

    return processed_data

def run_model():
    test = pd.read_json("app/uploaded_files/test.json",orient='records')
    test.drop(columns=nu_column,inplace=True)
    
    test_scaled = pd.DataFrame(np.c_[test[["unit_number"]], scaler.fit_transform(test.drop(["unit_number","time_(cycles)"], axis=1))])
    test_processed = test_preprocessing(test_scaled, 0, [0], window_size=30)

    model_dir = 'app/ml/FD001_LSTM_s-score_384.88.h5'
    model = load_model(model_dir, compile=False)
    return model.predict(test_processed)

