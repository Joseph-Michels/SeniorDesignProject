import face_recognition
import cv2

FILE_SEPARATOR = "/"
IMG_WIDTH=640

video_capture = cv2.VideoCapture(0)


if __name__ == "__main__":
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    rf = open("out/"+input("file name: "), 'w')
    # rf.write(f"{IMG_WIDTH}\n")

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locs = face_recognition.face_locations(rgb_small_frame)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left) in face_locs:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            rf.write(f"{(left+right)/IMG_WIDTH - 1} {(right-left)/IMG_WIDTH}\n")
            # loc(-1,1) width(fraction/1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    rf.close()
    video_capture.release()
    cv2.destroyAllWindows()