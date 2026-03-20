import cv2

def add_text(image,text):

    font=cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(
        image,
        text,
        (50,50),
        font,
        1,
        (255,255,255),
        2,
        cv2.LINE_AA
    )

    return image