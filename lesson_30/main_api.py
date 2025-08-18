import io
import numpy as np
import tensorflow as tf

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()
model = None


@app.on_event("startup")
async def startup_event():
    global model
    model = tf.keras.models.load_model("model/happy.keras")


@app.on_event("shutdown")
async def startup_event():
    print("api is down")


@app.post("/happymodel/")
async def preprocess_image(file: UploadFile = File(...)):
    # check file extension
    if not file.filename.lower().endswith(".jpg"):
        return JSONResponse(
            content={"error": "Only .jpg files are supported"}, status_code=400
        )

    # read image bytes
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # resize ?
    # image = image.resize((64, 64))
    # print(f"debug, image shape: {image.shape}")

    # convert to numpy
    img_array = np.array(image)
    prep_img = np.expand_dims(img_array, axis=0)
    print(f"debug, image shape: {prep_img.shape}")

    # work
    pred = model.predict(prep_img)
    pred_bin = np.where(pred > 0.5, 1, 0)
    print(f"debug, pred_bin: {pred_bin}")

    return {"prediction": int(pred_bin[0][0])}
