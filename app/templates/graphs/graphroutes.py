from fastapi import APIRouter
import plotly.express as px
import pandas as pd

temp_cols = ['T2_Total_temperature_at_fan_inlet_(°R)','T24_Total_temperature_at_LPC_outlet_(°R)', 'T30_Total_temperature_at_HPC_outlet_(°R)', 'T50_Total_temperature_at_LPT_outlet_(°R)']
pres_cols = ['P2_Pressure_at_fan_inlet_(psia)', 'P15_Total_pressure_in_bypass-duct_(psia)', 'Ps30_Static_pressure_at_HPC_outlet_(psia)']
rpm_cols = ['Nf_Physical_fan_speed_(rpm)', 'Nc_Physical_core_speed_(rpm)', 'NRf_Corrected_fan_speed_(rpm)', 'NRc_Corrected_core_speed_(rpm)']
flow_cols = ['W31_HPT_coolant_bleed_(lbm/s)','W32_LPT_coolant_bleed_(lbm/s)']

class cplot():
    width : int
    height : int
    autosize : bool = False
    
    def __init__(self, width : int, height : int) -> None:
        self.width = width
        self.length = height

    def get_size(self):
        return self.autosize
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height


router = APIRouter(
    prefix="/graph",
    tags=["Graphs"]
)

@router.post("/set")
async def set_graphs():
    df = pd.read_json('app/uploaded_files/test.json', orient='records')
    loc_data = df.set_index('time_(cycles)').drop(columns=['unit_number', 'operational_setting_1', 'operational_setting_2', 'operational_setting_3'])
    temp_data = loc_data[temp_cols]
    pres_data = loc_data[pres_cols]
    rpm_data = loc_data[rpm_cols]
    flow_data = loc_data[flow_cols]

    axeslist = list()
    axeslist.append(px.line(temp_data))
    axeslist.append(px.line(pres_data))
    axeslist.append(px.line(rpm_data))
    axeslist.append(px.line(flow_data))

    corr = loc_data.corr().dropna(how="all").dropna(how="all", axis=1).round(2)
    
    #lineplots = cplot(800, 400)
    #heatmaplot = cplot(1000, 800)

    try:     
        for num, fig in enumerate(axeslist):
            fig.update_layout(
                autosize = False,
                width = 700,
                height = 400
            )

            fig.write_html(f'app/templates/graphs/graph{num+1}.html')
        
        fig = px.imshow(corr, text_auto=True)

        fig.update_layout(
            autosize= False,
            width = 1000,
            height = 800
        )

        fig.write_html('app/templates/graphs/graph5.html')
    
    except Exception as e:
        return e.args
    
    return {"status" : "graphs saved successfully to app/templates/graphs"}      

