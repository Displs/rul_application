from fastapi import APIRouter, File, UploadFile,  Depends
from app.database.models import Session
import os
from app.database.data_transmission import write_to_db, update_rul_results
from app.database.models import get_db, Engine
from app.ml.dlmodel import run_model

router = APIRouter(
    prefix='/test',
    tags=["Data"]
)

@router.post("/upload")
async def create_upload_file(upload_file: UploadFile = File()):
    try:
        file_path = f"{os.getcwd()}/app/uploaded_files/test.json"
        with open(file_path, "wb") as f:
            f.write(upload_file.file.read())
        return {"status": f"File saved successfully, saved in {file_path}"}
    except Exception as e:
        return {"error": e.args, "filename" : file_path}
    finally:
        upload_file.file.close()

@router.post("/upload/confirm")
async def save_data(upload_confirm : bool, man : str, mod : str, db_session: Session = Depends(get_db)):
    if upload_confirm:
        try:
            new_engine = Engine(nservice = False, manufacturer = man, model = mod)
            db_session.add(new_engine)
            db_session.commit()
            write_to_db()
            return {"status": "file saved to db"}
        except Exception as e:
            return {"status": e.args}
    else:
        return {"message" : "file saving aborted"}
    
@router.put("/result")
async def get_rul():
    rul_result = float(format(run_model()[0][0], ".2f"))
    update_rul_results(rul_result)
    return {"status": f" engine's rul result {rul_result} saved to db"}


