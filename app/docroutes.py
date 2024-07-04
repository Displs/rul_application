from fastapi import APIRouter, File, UploadFile,  Depends
from fastapi.responses import  StreamingResponse
from app.database.models import Session
import os
from app.database.models import get_db, Documents

router = APIRouter(
    prefix="/documents",
    tags=["Docs"]
)

@router.get("/all")
async def get_stored_docs(db_session: Session = Depends(get_db)):
    try:
        cur_docs = db_session.query(Documents).all()
        return {"status" : "success",
                "data" : cur_docs}
    except Exception as e:
        return{"error": e.args}

@router.post("/upload")
async def upload_stored_doc(man: str, mod: str, upload_file: UploadFile = File(), db_session: Session = Depends(get_db)):
    try:
        file_path = f"{os.getcwd()}/app/uploaded_files/norm_docs/{upload_file.filename}"
        new_doc = Documents(manufacturer = man, model = mod, doc_name = upload_file.filename)
        with open(file_path, "wb") as f:
            f.write(upload_file.file.read())
        db_session.add(new_doc)
        db_session.commit()
        return {"status": f"File saved successfully, saved in {file_path}"}
    except Exception as e:
        return {"error": e.args, "filename" : file_path}
    finally:
        upload_file.file.close()
    
@router.get("/download/{file_name}")
def get_stored_doc(file_name: str):
    try:
        file_path = f'{os.getcwd()}/app/uploaded_files/norm_docs/{file_name}'
        def iterfile():
            with open(file_path, mode="rb") as file_like:
                yield from file_like
        return StreamingResponse(iterfile())
    except Exception as e:
        return{"error": e.args}
    
    

