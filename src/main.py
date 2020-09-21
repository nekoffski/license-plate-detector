import cv2
import imutils

path = './res/london_footage.wmv'
cap = cv2.VideoCapture(path)


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    screenCnt = None
    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)

    return frame


while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', process_frame(frame))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
