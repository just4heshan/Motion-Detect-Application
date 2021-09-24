import cv2, pandas as pd
from datetime import datetime

# Start Video Capture
video = cv2.VideoCapture(0)

# initialize first frame
first_frame = None

df = pd.DataFrame(columns=['Start Time', 'End Time'])

status_list = [None, None]
times = []


while True:

    # read the image
    capture, frame = video.read()

    # to identify status of the object
    status = 0

    # convert to Gray frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert a Gray frame into Gaussian Blur to reduce noise and improve accuracy
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        status_list.append(0)
        first_frame = gray_frame
        continue

    # delta frame - to compare current situation with initial situation
    delta_frame = abs(first_frame - gray_frame)

    # threshold frame - to identify object
    threshold_frame = cv2.threshold(delta_frame, 177, 255, cv2.THRESH_BINARY)[1]
    # make threshold frame smoother to remove black holes
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=3)

    # find contours ( to detect the object)
    (cnts,_) = cv2.findContours(threshold_frame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 50000:
            continue

        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 230, 0), 3)

    # append the status after each iteration
    status_list.append(status)

    status_list= status_list[-2:]

    if status_list[-2]==0 and status_list[-1]==1:
        times.append(datetime.now())
    if status_list[-2]==1 and status_list[-1]==0:
        times.append(datetime.now())

    cv2.imshow("Color Frame", frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Delta Frame", delta_frame)

    key = cv2.waitKey(1)
    if key == ord('q'): # press 'q' to exit the window
        if status==1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df=df.append({'Start': times[i], 'End': times[i+1]},ignore_index=True)

df.to_csv("Times.csv")
print(status_list)
video.release()
cv2.destroyAllWindows()
