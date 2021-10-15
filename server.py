from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
# from jinja2 import TemplateNotFound
from PIL import Image
import shutil
import os
import ocr
app = FastAPI()


templates = Jinja2Templates(directory="templates")
# this line is used for integarting templeting inside it

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
#above three lines are called as api end point
#that is after hitting the base url, as soon as we hit the 
#we will be redirected to the given index.html page


@app.post("/extract_text")
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image, path="temp")

    text = await ocr.read_image(temp_file)
    print(text)
    return {"filename": image.filename ,"text": text}

def _save_file_to_disk(uploaded_file, path="."):
    # print(uploaded_file.filename)
    temp_file = os.path.join(path, uploaded_file.filename)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file
