
import os
import sys
import uuid
import cv2
import numpy as np

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# ensure ai folder in path
AI_DIR = os.path.dirname(os.path.abspath(__file__))
if AI_DIR not in sys.path:
    sys.path.insert(0, AI_DIR)

from cartoonify import cartoonify_image
from video_cartoon import cartoonify_video
from sticker_generator import generate_sticker
from overlays import add_snow, add_fog, add_rain, add_dust

app = FastAPI(title="Cartoonify AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# Health
# ------------------------------------------------

@app.get("/")
def root():
    return {"status": "AI server running"}

# ------------------------------------------------
# IMAGE CARTOONIFY
# ------------------------------------------------

@app.post("/cartoonify-image")
async def cartoonify_image_api(
    file: UploadFile = File(...),
    style: str = Form("classic"),
    filter: str = Form(""),
    overlay: str = Form(""),
    brightness: int = Form(50),
    contrast: int = Form(50),
    saturation: int = Form(50),
):

    try:

        image_bytes = await file.read()

        # cartoonify using your existing model
        cartoon_bytes = cartoonify_image(image_bytes, style)

        # convert to OpenCV
        npimg = np.frombuffer(cartoon_bytes, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # ---------------------------------
        # brightness / contrast
        # ---------------------------------

        image = cv2.convertScaleAbs(
            image,
            alpha=1 + (int(contrast) - 50) / 50,
            beta=int(brightness) - 50
        )
        # saturation control
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=saturation/50)
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # ---------------------------------
        # filters
        # ---------------------------------

        if filter == "bw":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        elif filter == "invert":
            image = cv2.bitwise_not(image)

        elif filter == "vintage":

            kernel = np.array([
                [0.272,0.534,0.131],
                [0.349,0.686,0.168],
                [0.393,0.769,0.189]
            ])

            image = cv2.transform(image, kernel)

        elif filter == "infrared":
            b,g,r = cv2.split(image)
            image = cv2.merge((r,g,b))

       # ---------------------------------
# overlays (stronger effects)
# ---------------------------------

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        h, w = image.shape[:2]

        if overlay == "rain":

            rain = image.copy()

            for _ in range(800):

                x = np.random.randint(0, w)
                y = np.random.randint(0, h)

                cv2.line(
                    rain,
                    (x, y),
                    (x + 3, y + 15),
                    (180,180,180),
                    1
                )

            image = cv2.addWeighted(image, 0.7, rain, 0.3, 0)


        elif overlay == "snow":

            snow = image.copy()

            for _ in range(900):

                x = np.random.randint(0, w)
                y = np.random.randint(0, h)

                size = np.random.randint(1,3)

                cv2.circle(snow, (x,y), size, (255,255,255), -1)

            snow = cv2.GaussianBlur(snow,(3,3),0)

            image = cv2.addWeighted(image,0.8,snow,0.4,0)


        elif overlay == "fog":

            fog = np.full_like(image,255)

            fog = cv2.GaussianBlur(fog,(31,31),0)

            image = cv2.addWeighted(image,0.6,fog,0.4,0)


        elif overlay == "dust":

            dust = image.copy()

            for _ in range(400):

                x = np.random.randint(0,w)
                y = np.random.randint(0,h)

                cv2.circle(dust,(x,y),1,(200,200,200),-1)

            dust = cv2.GaussianBlur(dust,(5,5),0)

            image = cv2.addWeighted(image,0.9,dust,0.25,0)
        

        # ---------------------------------
        # encode result
        # ---------------------------------

        _, buffer = cv2.imencode(".jpg", image)

        return Response(
            content=buffer.tobytes(),
            media_type="image/jpeg"
        )

    except Exception as e:
        raise HTTPException(500, str(e))

# ------------------------------------------------
# VIDEO CARTOONIFY
# ------------------------------------------------

@app.post("/cartoonify-video")
async def cartoonify_video_api(
    file: UploadFile = File(...),
    style: str = Form("anime")
):

    uid = str(uuid.uuid4())

    input_path = f"temp_in_{uid}.mp4"
    output_path = f"temp_out_{uid}.mp4"

    try:

        with open(input_path,"wb") as f:
            f.write(await file.read())

        cartoonify_video(input_path, output_path, style)

        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename="cartoon_video.mp4"
        )

    finally:

        if os.path.exists(input_path):
            os.remove(input_path)

# ------------------------------------------------
# STICKER
# ------------------------------------------------

@app.post("/generate-sticker")
async def sticker_api(
    file: UploadFile = File(...),
    text: str = Form(""),
    position: str = Form("top")
):

    image_bytes = await file.read()

    sticker_stream = generate_sticker(image_bytes, text, position)

    return StreamingResponse(
        sticker_stream,
        media_type="image/webp"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
