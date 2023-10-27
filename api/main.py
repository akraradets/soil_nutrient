from fastapi import FastAPI, UploadFile
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Base64Bytes
from utils.models import *
from utils.logger import *

from PIL import Image 
import io
import base64

init_logger(name="main", filename="main")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model from mlflow
load_model_to_cache()

class PredictOut(BaseModel):
    predict: float
    image: Base64Bytes
    preffix: str

    def answer_build(image:Base64Bytes, predict:float):
        answer = {
            "predict":predict,
            "image":image,
            "preffix":"data:image/png;base64,"
        }
        return answer


@app.get("/check")
def get_check():
    return "OK"

@app.post("/predict_k", response_model=PredictOut)
def post_predict_k(image:UploadFile) -> PredictOut:
    model = load_model(MODEL_K)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, predict = prediction(model=model, image=image)

    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)

    return PredictOut.answer_build(image=img_str,predict=predict)

@app.post("/predict_p", response_model=PredictOut)
def post_predict_p(image:UploadFile) -> PredictOut:
    model = load_model(MODEL_P)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, predict = prediction(model=model, image=image)

    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)

    return PredictOut.answer_build(image=img_str,predict=predict)

@app.post("/predict_om", response_model=PredictOut)
def post_predict_om(image:UploadFile) -> PredictOut:
    model = load_model(MODEL_OM)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, predict = prediction(model=model, image=image)

    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)

    return PredictOut.answer_build(image=img_str,predict=predict)