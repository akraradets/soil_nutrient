from fastapi import FastAPI, UploadFile
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Base64Bytes
from utils.models import *
from utils.logger import *
from PIL import Image 
import io
import base64
import logging

init_logger(name='main', filename='main')
logger = logging.getLogger('main')

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
@app.on_event("startup")
async def startup_model():
    load_model_to_cache()

class PredictOut(BaseModel):
    predict: float
    image: Base64Bytes
    preffix: str
    raw_predict: float
    multiplier: float

    def answer_build(image:Base64Bytes, predict:float, raw_predict:float, multiplier:float):
        answer = {
            "predict":predict,
            "image":image,
            "preffix":"data:image/png;base64,",
            "raw_predict": raw_predict,
            "multiplier": multiplier
        }
        return answer


@app.get("/check")
def get_check():
    return "OK"

@app.get("/build_version")
def get_buildversion():
    import os
    answer = os.environ["BUILD_VERSION"]
    logger.info(f"{answer=}")
    return answer

def decorate_predict(raw_predict:float, multiplier:float) -> float:
    # Cap min
    if(raw_predict < 0.0):
        return 0.0
    elif(raw_predict > 1.0):
        raw_predict = 1.0
        return raw_predict * multiplier
    else:
        return raw_predict * multiplier

@app.post("/predict_k", response_model=PredictOut)
def post_predict_k(image:UploadFile) -> PredictOut:
    multiplier:float = MAXCAP_K
    model = load_model(MODEL_K)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, raw_predict = prediction(model=model, image=image)
    predict = decorate_predict(raw_predict=raw_predict, multiplier=multiplier)
    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)
    logger.info(f"{predict=}|{raw_predict=}|{multiplier=}")
    return PredictOut.answer_build(image=img_str,predict=predict,raw_predict=raw_predict,multiplier=multiplier)

@app.post("/predict_p", response_model=PredictOut)
def post_predict_p(image:UploadFile) -> PredictOut:
    multiplier:float = MAXCAP_P
    model = load_model(MODEL_P)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, raw_predict = prediction(model=model, image=image)
    predict = decorate_predict(raw_predict=raw_predict, multiplier=multiplier)
    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)
    logger.info(f"{predict=}|{raw_predict=}|{multiplier=}")
    return PredictOut.answer_build(image=img_str,predict=predict,raw_predict=raw_predict,multiplier=multiplier)

@app.post("/predict_om", response_model=PredictOut)
def post_predict_om(image:UploadFile) -> PredictOut:
    multiplier:float = MAXCAP_OM
    model = load_model(MODEL_OM)
    model.eval()

    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    image = image.convert("RGB")

    process_image, raw_predict = prediction(model=model, image=image)
    predict = decorate_predict(raw_predict=raw_predict, multiplier=multiplier)
    buffered = io.BytesIO()
    process_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    # javascript
    # resp = answer
    # var image = new Image();
    # image.src = resp.preffix + resp.image
    # document.body.appendChild(image)
    logger.info(f"{predict=}|{raw_predict=}|{multiplier=}")
    return PredictOut.answer_build(image=img_str,predict=predict,raw_predict=raw_predict,multiplier=multiplier)