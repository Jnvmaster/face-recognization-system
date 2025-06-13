import csv 
import threading # Import threading for running video capture in a separate thread

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFile
import cv2
import os
import numpy as np
import datetime 
import time # Import time for potential delays or timestamps
from tkinter import messagebox # Import messagebox for showing error/info messages

# Set the maximum image pixels limit to avoid DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

class Face_dector: 
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+150+50") # Set geometry for the Toplevel window
        self.root.title("Face Detector")
        self.root.grab_set() # Make it modal

        self.cap = None # Initialize webcam capture
        self.running = False # Control for the video loop
        self.current_student_id = None # Track the ID of the currently recognized student
        self.last_recognition_time = {} # To prevent rapid attendance marking/db calls

        # Path to the Haar Cascade XML file
        self.haar_cascade_path = 'haarcascade_frontalface_default.xml'
        
        # Check if the Haar Cascade XML file exists
        if not os.path.exists(self.haar_cascade_path):
            messagebox.showerror("Error", 
                                 f"Haar Cascade XML file not found: '{self.haar_cascade_path}'.\n"
                                 "Please ensure 'haarcascade_frontalface_default.xml' is in the same directory as your Python script.", 
                                 parent=self.root)
            self.root.destroy()
            return

        # Initialize Haar Cascade classifier
        self.face_classifier = cv2.CascadeClassifier(self.haar_cascade_path)
        # Additional check for successful loading 
        if self.face_classifier.empty():
            messagebox.showerror("Error", 
                                 f"Could not load Haar Cascade XML file from '{self.haar_cascade_path}'.\n"
                                 "The file might be corrupted or unreadable.", 
                                 parent=self.root)
            self.root.destroy()
            return

        # Initialize LBPH Face Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("classifier.xml")
        except cv2.error as e:
            messagebox.showerror("Error", f"Could not load trained classifier: {e}\nPlease train the data first using 'Train Data' button.", parent=self.root)
            # Do not destroy the window immediately, allow user to train first.
            # However, recognition functionality will be limited until classifier.xml exists.
            # For this scenario, we will destroy as recognition is main purpose.
            self.root.destroy() 
            return

        # --- UI Setup ---
        title_lbl = Label(self.root, text="FACE DETECTOR", font=("Times New Roman", 30, "bold"),
                          bg="navy", fg="white", bd=5)
        title_lbl.pack(fill=X, pady=5)

        # Frame for video feed and details
        main_frame = Frame(self.root, bd=2, relief=RIDGE, bg="lightgray")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Video Feed Canvas
        self.video_canvas = Canvas(main_frame, bg="black", width=640, height=480)
        self.video_canvas.pack(side=LEFT, padx=10, pady=10)

        # Student Details Frame
        details_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details",
                                   font=("Times New Roman", 15, "bold"), fg="blue", bg="white")
        details_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Labels for displaying student info
        self.lbl_id = Label(details_frame, text="Student ID: ", font=("Times New Roman", 14), bg="white", anchor="w")
        self.lbl_id.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.val_id = Label(details_frame, text="", font=("Times New Roman", 14, "bold"), bg="white", anchor="w")
        self.val_id.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.lbl_name = Label(details_frame, text="Name: ", font=("Times New Roman", 14), bg="white", anchor="w")
        self.lbl_name.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.val_name = Label(details_frame, text="", font=("Times New Roman", 14, "bold"), bg="white", anchor="w")
        self.val_name.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.lbl_rollno = Label(details_frame, text="Roll No: ", font=("Times New Roman", 14), bg="white", anchor="w")
        self.lbl_rollno.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.val_rollno = Label(details_frame, text="", font=("Times New Roman", 14, "bold"), bg="white", anchor="w")
        self.val_rollno.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.lbl_dept = Label(details_frame, text="Department: ", font=("Times New Roman", 14), bg="white", anchor="w")
        self.lbl_dept.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.val_dept = Label(details_frame, text="", font=("Times New Roman", 14, "bold"), bg="white", anchor="w")
        self.val_dept.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.status_lbl = Label(details_frame, text="Waiting for face detection...", font=("Times New Roman", 14), bg="white", fg="darkgreen")
        self.status_lbl.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=15)

        # Action Buttons
        button_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        button_frame.pack(fill=X, padx=10, pady=5)

        self.start_btn = Button(button_frame, text="Start Face Detector", command=self.start_face_detector,
                                font=("Times New Roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
        self.start_btn.pack(side=LEFT, padx=10, pady=5, expand=True)

        self.stop_btn = Button(button_frame, text="Stop Face Detector", command=self.stop_face_detector,
                               font=("Times New Roman", 15, "bold"), bg="red", fg="white", cursor="hand2", state=DISABLED)
        self.stop_btn.pack(side=LEFT, padx=10, pady=5, expand=True)
        
        # Bind the close event of the Toplevel window to release resources
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def start_face_detector(self):
        """Starts the webcam feed and the face detection/recognition thread."""
        if not self.running:
            self.cap = cv2.VideoCapture(0) # 0 for default webcam
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam. Please check if it's connected and not in use.", parent=self.root)
                self.cap = None
                return

            self.running = True
            self.start_btn.config(state=DISABLED)
            self.stop_btn.config(state=NORMAL)
            self.status_lbl.config(text="Face Detector started. Looking for faces...")
            self.detector_thread = threading.Thread(target=self._detector_loop)
            self.detector_thread.daemon = True # Allows thread to exit when main program exits
            self.detector_thread.start()

    def stop_face_detector(self):
        """Stops the face detection/recognition thread and releases webcam resources."""
        if self.running:
            self.running = False
            self.start_btn.config(state=NORMAL)
            self.stop_btn.config(state=DISABLED)
            self.status_lbl.config(text="Face Detector stopped.")
            self.release_resources()
            self.clear_details()

    def _detector_loop(self):
        """Main loop for capturing video, detecting faces, and updating the display."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Call the draw_boundary function to process the frame
            img_with_boundaries = self.draw_boundary(frame, gray, self.face_classifier, self.recognizer)

            # Convert frame to PhotoImage for Tkinter
            img_rgb = cv2.cvtColor(img_with_boundaries, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.video_canvas.imgtk = img_tk # Keep a reference
            self.video_canvas.create_image(0, 0, anchor=NW, image=img_tk)
            
            time.sleep(0.01) # Small delay to prevent high CPU usage

        self.release_resources()

    def draw_boundary(self, img, gray_img, face_classifier, recognizer):
        """
        Detects faces in the image, recognizes them, draws boundaries,
        and updates UI details.
        """
        # Initialize id and confidence with default values
        # These will be updated if a face is detected and recognized
        recognized_id = -1 
        recognition_confidence = 0 
        
        faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        found_face_in_frame = False # Flag to check if any face was detected in current frame
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3) # Draw rectangle around detected face
            roi_gray = gray_img[y:y+h, x:x+w] # Region of Interest (face) in grayscale

            # Ensure ROI is not empty before predicting
            if roi_gray.size > 0:
                try:
                    recognized_id, recognition_confidence = recognizer.predict(roi_gray) # Predict ID and confidence
                except cv2.error as e:
                    # Handle cases where prediction might fail (e.g., ROI too small)
                    print(f"Prediction error: {e}")
                    recognized_id = -1 # Mark as unknown
                    recognition_confidence = 0
                
                # Check confidence for recognition (lower confidence value means higher similarity/better match)
                # A common threshold is around 70-100. Lower than 70 is often considered a good match.
                # Adjust this threshold based on your trained model's performance and requirements.
                if recognition_confidence < 100: # Adjust this threshold as needed (e.g., < 80 for stricter match)
                    # Fetch student details from the database
                    student_info = self.fetch_student_details(recognized_id)
                    if student_info:
                        s_name = student_info.get('name', 'N/A')
                        r_no = student_info.get('rollno', 'N/A')
                        dep = student_info.get('department', 'N/A')

                        # Display details on the image
                        cv2.putText(img, f"ID: {recognized_id}", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"RollNo: {r_no}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Name: {s_name}", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Dept: {dep}", (x, y + h + 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        
                        # Mark attendance and update UI details
                        self.mark_attendance(recognized_id, r_no, s_name, dep)
                        self.update_ui_details(recognized_id, s_name, r_no, dep, "Recognized Face", "darkgreen")

                    else:
                        # Recognized ID but no details in DB
                        cv2.putText(img, "Details Not Found (DB)", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                        self.update_ui_details(recognized_id, "N/A", "N/A", "N/A", "Recognized ID, but DB details not found.", "orange")
                        
                    found_face_in_frame = True
                else: 
                    # Confidence is too high, likely an unknown face or poor match
                    cv2.putText(img, "Unknown Face", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                    self.update_ui_details("Unknown", "Unknown", "Unknown", "Unknown", "Unknown Face Detected.", "red")
                    found_face_in_frame = True
            else: 
                # ROI was empty (shouldn't happen with proper detection but good to handle)
                cv2.putText(img, "Invalid ROI", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                self.update_ui_details("N/A", "N/A", "N/A", "N/A", "Invalid ROI for detection.", "red")
                found_face_in_frame = True

        # If no face was found or recognized in the current frame, clear details
        if not found_face_in_frame:
            self.clear_details()
            self.status_lbl.config(text="No face detected or recognized.", fg="darkblue")

        return img # Return the image with drawn boundaries


    def update_ui_details(self, student_id, name, rollno, department, status_text, status_color):
        """Updates the Tkinter labels with recognized student details."""
        self.val_id.config(text=student_id)
        self.val_name.config(text=name)
        self.val_rollno.config(text=rollno) # Display rollno in the appropriate label
        self.val_dept.config(text=department)
        self.status_lbl.config(text=status_text, fg=status_color)

    def clear_details(self):
        """Clears the student details displayed in the UI."""
        self.val_id.config(text="")
        self.val_name.config(text="")
        self.val_rollno.config(text="")
        self.val_dept.config(text="")
        self.current_student_id = None # Reset current recognized ID


    def fetch_student_details(self, student_id):
        """
        Connects to MySQL database and fetches student details.
        Make sure your MySQL server is running and accessible.
        """
        try:
            import mysql.connector # Ensure this import is at the top of face_frame.py
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Pratik@05", # <--- CHANGE THIS TO YOUR MYSQL PASSWORD
                database="college" # <--- CHANGE THIS TO YOUR DATABASE NAME
            )
            cursor = conn.cursor(dictionary=True) # Fetch rows as dictionaries

            # Assuming your 'students' table has columns: id, name, rollno, department
            query = "SELECT id, name, rollno, department FROM students WHERE id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()
            return result
        except ImportError:
            messagebox.showerror("Error", "mysql.connector not found. Please install it: pip install mysql-connector-python", parent=self.root)
            return None
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to MySQL or fetching data in Face Detector: {err}", parent=self.root)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while fetching details in Face Detector: {e}", parent=self.root)
            return None


    def mark_attendance(self, id, r_no, s_name, dep):
        """Marks attendance by writing to a CSV file."""
        now = datetime.datetime.now()
        d1 = now.strftime("%d/%m/%Y")
        dtString = now.strftime("%H:%M:%S")

        # Open the attendance CSV file in append mode
        with open("attendance.csv", "a+", newline="\n") as f:
            writer = csv.writer(f)
            # Check if the header exists, if not, write it
            f.seek(0, os.SEEK_END) # Go to end of file
            if f.tell() == 0: # If file is empty
                writer.writerow(["ID", "RollNo", "Name", "Department", "Date", "Time"])
            
            # Write attendance record
            writer.writerow([id, r_no, s_name, dep, d1, dtString])
            print(f"Attendance marked for ID: {id}, Name: {s_name}") # For debugging


    def release_resources(self):
        """Releases webcam resources and clears canvas."""
        if self.cap:
            self.cap.release()
        self.video_canvas.delete("all")
        self.cap = None

    def on_closing(self):
        """Handles window closing event to stop recognition and destroy window."""
        self.stop_face_detector() # Ensure recognition loop stops and camera is released
        self.root.destroy() # Destroy the Toplevel window

# This block is for testing face_frame.py as a standalone file.
# In your main application, Face_dector will be instantiated as part of FaceRecognitionSystem.
if __name__ == "__main__":
    root = Tk()
    # Adjust geometry for main window if running standalone for testing purposes
    root.geometry("1530x840+0+0") 
    root.title("Face Recognition System (Test Face Detector)")

    # You would typically have a button in your main application to open this.
    # For standalone testing, we just open it directly.
    face_detector_window = Toplevel(root)
    app = Face_dector(face_detector_window)
    root.mainloop()
