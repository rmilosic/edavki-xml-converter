from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import pandas as pd
import io

# from src.parser import parse_csv
# from src.transformer import transform_data
# from src.xml_builder import build_xml

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/")
async def upload_csv(
    year: Annotated[str, Form()],
    broker: Annotated[str, Form()],
    mode: Annotated[str, Form()],
    file: UploadFile = File(...)
):
    # Validate file type
    if not file.filename.endswith('.csv'):
        return {"error": "Only CSV files are allowed"}
    
    # Read CSV into pandas
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    # Log received data
    print(f"Year: {year}, Broker: {broker}, Mode: {mode}")
    print(df.head())
    
    # Perform processing (Placeholder logic)
    processed_data = {
        "year": year, 
        "broker": broker,
        "mode": mode,
        "rows_received": len(df),
        "column_types": df.dtypes.apply(lambda x: x.name).to_dict(),
        "data_preview": df.fillna("").head().to_dict()
    }
    
    print("reload process working")
    
    return {"message": "File processed successfully", "details": processed_data}