import mediapipe as mp
import numpy as np
import cv2

# mediapipe used for detection
# cv2 is used for camera purposes(opencv=open computer vision)

mp_drawing = mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic



def bicepcurls():
	cap = cv2.VideoCapture(0)

	# Curl counter variables
	counter = 0
	stage = None

	## Setup mediapipe instance
	with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
		while cap.isOpened():
			ret, frame = cap.read()

			def calculate_angle(a, b, c):
				a = np.array(a)  # First
				b = np.array(b)  # Mid
				c = np.array(c)  # End

				radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
				angle = np.abs(radians * 180.0 / np.pi)

				if angle > 180.0:
					angle = 360 - angle

				return angle
			# Recolor image to RGB
			image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image.flags.writeable = False

			# Make detection
			results = pose.process(image)

			# Recolor back to BGR
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

			# Extract landmarks
			try:
				landmarks = results.pose_landmarks.landmark

				# Get coordinates
				shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x,
							landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
				elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x,
						 landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y]
				wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x,
						 landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y]

				# Calculate angle
				angle = calculate_angle(shoulder, elbow, wrist)

				# Visualize angle
				cv2.putText(image, str(angle),
							tuple(np.multiply(elbow, [640, 480]).astype(int)),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
							)

				# Curl counter logic
				if angle > 140:
					stage = "down"
				if angle < 50 and stage == 'down':
					stage = "up"
					counter += 1
					print(counter)

			except:
				pass

			# Render curl counter
			# Setup status box
			cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

			# Rep data
			cv2.putText(image, 'REPS', (15, 12),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.putText(image, str(counter),
						(10, 60),
						cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

			# Stage data
			cv2.putText(image, 'STAGE', (65, 12),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
			cv2.putText(image, stage,
						(60, 60),
						cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)



			# Render detections

			# 2. Right hand
			mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
									  mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
									  mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
									  )

			# 3. Left Hand
			mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
									  mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
									  mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
									  )

			# 4. Pose Detections
			mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
									  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
									  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
									  )

			cv2.imshow('Mediapipe Feed', image)

			if cv2.waitKey(10) & 0xFF == ord('q'):
				break

		cap.release()



bicepcurls()
