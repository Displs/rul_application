from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import requests
import pandas as pd

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

temp_cols = ['T2_Total_temperature_at_fan_inlet_(°R)','T24_Total_temperature_at_LPC_outlet_(°R)', 'T30_Total_temperature_at_HPC_outlet_(°R)', 'T50_Total_temperature_at_LPT_outlet_(°R)']
pres_cols = ['P2_Pressure_at_fan_inlet_(psia)', 'P15_Total_pressure_in_bypass-duct_(psia)', 'Ps30_Static_pressure_at_HPC_outlet_(psia)']
rpm_cols = ['Nf_Physical_fan_speed_(rpm)', 'Nc_Physical_core_speed_(rpm)', 'NRf_Corrected_fan_speed_(rpm)', 'NRc_Corrected_core_speed_(rpm)']
flow_cols = ['W31_HPT_coolant_bleed_(lbm/s)','W32_LPT_coolant_bleed_(lbm/s)']

templates = Jinja2Templates(directory="app/templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/graphs")
def get_base_page(request: Request):
    return templates.TemplateResponse("graphs.html", {"request": request})

@router.get("/graphs/update")
def get_base_page(request: Request):
    requests.post('http://localhost:8000/graph/set')
    return templates.TemplateResponse("graphs.html", {"request": request})

@router.get("/data")
def get_data_page(request: Request):
    return templates.TemplateResponse("data.html", {"request": request})

@router.get("/docs")
def get_docs_page(request: Request):
    return templates.TemplateResponse("docs.html", {"request": request})

@router.get("/docs/get-all")
def get_docs_table(request: Request):
    data = requests.get('http://localhost:8000/documents/all').json()
    return templates.TemplateResponse("docs_table.html", {"request": request,"query" : data['data']})

@router.get("/data/get-all")
def get_docs_table(request: Request):
        df = pd.read_json('app/uploaded_files/test.json', orient='records')
        loc_data = df.set_index('time_(cycles)').drop(columns=['unit_number', 'operational_setting_1', 'operational_setting_2', 'operational_setting_3']).round(2)
        temp_data = loc_data[temp_cols].to_dict()
        pres_data = loc_data[pres_cols].to_dict()
        rpm_data = loc_data[rpm_cols].to_dict()
        flow_data = loc_data[flow_cols].to_dict()
        index = loc_data.index.to_list()
        return templates.TemplateResponse(
            "data_table.html",
            {"request": request,
             "index_query" : index,
             "temp_query" : temp_data,
             "pres_query" : pres_data,
             "rpm_query" : rpm_data,
             "flow_query" : flow_data})

@router.get("/image")
async def get_image():
    try:
        image_path = "app/templates/logo2.png"
        return FileResponse(image_path)
    except Exception as e:
        return {"error" : e.args}