import cv2
import face_recognition
import mysql.connector
from datetime import datetime, date

reference_images = []

def fetch_images():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='zrp'
    )

    cursor = cnx.cursor()

    query = "SELECT * FROM employees"
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Process the results
    for row in results:
        image_path = row[8]
        label = row[0]
        print(image_path)
        reference_images.append(('images/known_faces/'+image_path, label))

    # Close the cursor and connection
    cursor.close()
    cnx.close()


def checkin(employee_id):
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='zrp'
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Get today's date
    today = date.today()

    query = "SELECT * FROM attendances WHERE employee_id = %s AND DATE(date) = %s"
    cursor.execute(query, (employee_id, today))

    # Fetch the results
    result = cursor.fetchone()

    # Check if the result is not None, meaning the employee_id is present and recorded today
    if result:
        print("Wanted person checked recorded today.")
    else:
        add_time(employee_id)

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()


def add_time(employee_id):
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='zrp'
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Get current time and today's date
    current_time = datetime.now().time()
    today = date.today()

    query = "INSERT INTO attendances (employee_id, time_in, date) VALUES (%s, %s, %s)"
    values = (employee_id, current_time, today)
    cursor.execute(query, values)

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()


# ...

# Load the reference images and labels
fetch_images()

reference_encodings = []
labels = []

for image_path, label in reference_images:
    reference_image = face_recognition.load_image_file(image_path)
    # Check if any faces are detected in the reference image
    reference_face_locations = face_recognition.face_locations(reference_image)
    if len(reference_face_locations) == 0:
        # Skip the image if no faces are detected
        print(f"No faces detected in image: {image_path}")
        continue

    reference_encoding = face_recognition.face_encodings(reference_image, reference_face_locations)[0]
    reference_encodings.append(reference_encoding)
    labels.append(label)

# Initialize the webcam or capture device
cap = cv2.VideoCapture(0)

# ...

# Main loop
while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    # Convert the frame from BGR to RGB (required by face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and their encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Initialize face_detected flag
    face_detected = False

    # Iterate over detected faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face encoding with the reference encodings
        matches = face_recognition.compare_faces(reference_encodings, face_encoding)

        # Check if any reference encoding matches the face encoding
        for i, match in enumerate(matches):
            if match:
                label = labels[i]
                # Face recognized, perform login or other actions
                checkin(label)
                print(f"Face recognized: {label}")
                break

        # Update face_detected flag
        face_detected = True

        # Draw a rectangle around the face
        if matches:
            # Green rectangle for recognized face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Add label text
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # Red rectangle for unrecognized face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Check if no face was detected
    if not face_detected:
        # Display the frame without any rectangles
        cv2.imshow('Face Login', frame)
    else:
        # Display the frame with rectangles
        cv2.imshow('Face Login', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture device and close windows
cap.release()
cv2.destroyAllWindows()
