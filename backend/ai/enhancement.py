import cv2

def adjust_brightness(image,value=30):
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    h,s,v=cv2.split(hsv)

    v=cv2.add(v,value)
    v[v>255]=255

    final=cv2.merge((h,s,v))
    return cv2.cvtColor(final,cv2.COLOR_HSV2BGR)


def adjust_contrast(image,alpha=1.5):
    return cv2.convertScaleAbs(image,alpha=alpha,beta=0)