from imutils.video import VideoStream
from imutils.video import FPS
from eye_blur import blur
from live_plot import plot
import argparse
import imutils
import time
import cv2

#python3 object_tracker.py  --video output.mov --tracker kcf


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())
# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
if int(major) == 3 and int(minor) < 3:
	tracker = cv2.Tracker_create(args["tracker"].upper())
# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
else:
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects
	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

#If the video path was not supplied, grab the reference o the web cam
if not args.get('video', False):
	vs = VideoStream(src = 0).start()
	time.sleep(1.0)

	#Otherwide, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args['video'])

fps = None

#Cropping factor
r = None
#These two collect the pupil center
pupil_x = []
pupil_y = []
pupil_count = []
count = 0
while True:
	count += 1
	# Blur the frame first would give us a better result
	frame = vs.read()
	frame = frame[1] if args.get('video', False) else Frame

	if frame is None:
		print('Ending of the analysis')
		break
	frame = blur(frame)
	frame = imutils.resize(frame, width = 500)
	if r != None:
		frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0]+r[2])]
		# #Stupid library only sccepts greyscaled image
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
  #           cv2.THRESH_BINARY,15,2)
	#Crop the image
	# frame = frame[50:5000, 70:300]
	(H, W) = frame.shape[:2]
		# check to see if we are currently tracking an object
	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			# print(x, y, w, h)
			middle_x = x + w/2
			middle_y = y + h/2
			print(middle_x, middle_y)
			pupil_x.append(middle_x)
			pupil_y.append(middle_y)
			pupil_count.append(count)
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
			cv2.circle(frame, (int(middle_x), int(middle_y)),5,
				(255, 0, 0), -1)
		# update the FPS counter
		fps.update()
		fps.stop()
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


		# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'k' key is selected, we are going to "select" a big bounding
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("k"):
		r = cv2.selectROI("Frame", frame, fromCenter=False, 
			showCrosshair=True)

	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)
		fps = FPS().start()

	if key == ord("t"):
		exit()
#Plot the data
plot(pupil_count, pupil_x)