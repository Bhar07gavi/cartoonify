import cv2
import numpy as np


# -------------------------
# SNOW EFFECT (soft flakes)
# -------------------------
def add_snow(image):

    h, w = image.shape[:2]

    snow = np.zeros_like(image)

    num_flakes = int(h * w * 0.002)

    for _ in range(num_flakes):

        x = np.random.randint(0, w)
        y = np.random.randint(0, h)

        size = np.random.randint(1,3)

        cv2.circle(snow,(x,y),size,(255,255,255),-1)

    snow = cv2.GaussianBlur(snow,(5,5),0)

    return cv2.addWeighted(image,0.85,snow,0.35,0)



# -------------------------
# RAIN EFFECT (slanted streaks)
# -------------------------
def add_rain(image):

    h, w = image.shape[:2]

    rain = image.copy()

    num_drops = int(h * w * 0.003)

    for _ in range(num_drops):

        x = np.random.randint(0,w)
        y = np.random.randint(0,h)

        length = np.random.randint(10,20)

        cv2.line(
            rain,
            (x,y),
            (x+3,y+length),
            (200,200,200),
            1
        )

    rain = cv2.blur(rain,(3,3))

    return cv2.addWeighted(image,0.8,rain,0.2,0)



# -------------------------
# FOG EFFECT
# -------------------------
def add_fog(image):

    fog = np.full_like(image,255)

    fog = cv2.GaussianBlur(fog,(31,31),0)

    return cv2.addWeighted(image,0.7,fog,0.3,0)



# -------------------------
# DUST PARTICLES
# -------------------------
def add_dust(image):

    h, w = image.shape[:2]

    dust = np.zeros_like(image)

    num_particles = int(h * w * 0.001)

    for _ in range(num_particles):

        x = np.random.randint(0,w)
        y = np.random.randint(0,h)

        cv2.circle(dust,(x,y),1,(180,180,180),-1)

    dust = cv2.GaussianBlur(dust,(7,7),0)

    return cv2.addWeighted(image,0.9,dust,0.25,0)