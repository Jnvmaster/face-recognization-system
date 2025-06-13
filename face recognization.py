from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student # Make sure 'student.py' exists and contains the 'Student' class
from train_data import Train
import os 
import csv
import cv2
from face_frame import Face_dector

# --- Placeholder Classes for other modules (you'll replace these with your actual implementations) ---

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.title("Admin Panel")
        Label(self.root, text="Welcome to the Admin Panel!", font=("times new roman", 20, "bold")).pack(pady=50)
        Label(self.root, text="Add your admin functionalities here.", font=("times new roman", 14)).pack()

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.title("Attendance System")
        Label(self.root, text="Attendance Management Interface", font=("times new roman", 20, "bold")).pack(pady=50)
        Label(self.root, text="Implement attendance tracking and reporting here.", font=("times new roman", 14)).pack()



class PhotosViewer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.title("Photo Samples")
        Label(self.root, text="Photo Samples Viewer", font=("times new roman", 20, "bold")).pack(pady=50)
        Label(self.root, text="You can display and manage captured face photos here.", font=("times new roman", 14)).pack()

class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.title("Help Desk")
        Label(self.root, text="Help Desk and Support", font=("times new roman", 20, "bold")).pack(pady=50)
        Label(self.root, text="Provide user guides, FAQs, or contact information here.", font=("times new roman", 14)).pack()

# --- Main Application Class ---
class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x710+0+0")
        self.root.title("Face Recognition System")

        # === Top Header Images ===
        img = Image.open(r"C:\Users\HP\Downloads\pes.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=500, height=130)

        img1 = Image.open(r"C:\Users\HP\Downloads\logo.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=500, y=0, width=500, height=130)

        img2 = Image.open(r"C:\Users\HP\Downloads\pes.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=1000, y=0, width=500, height=130)

        # === Background ===
        img3 = Image.open(r"C:\Users\HP\Downloads\face.jpg").resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg3 = Label(self.root, image=self.photoimg3)
        bg3.place(x=0, y=130, width=1530, height=710)

        # === Title ===
        Label(bg3, text="FACE RECOGNITION ATTENDANCE SYSTEM",
              font=("times new roman", 30, "bold"), bg="white", fg="red").place(x=0, y=0, width=1530, height=45)

        # === Button Definitions ===
        buttons = [
            ("STUDENT DETAILS", r"C:\Users\HP\Downloads\student2.jpg", self.student_details),
            ("ADMIN", r"C:\Users\HP\Downloads\admin2.jpg", self.admin_panel), # Linked to new method
            ("FACE DETECTOR", r"C:\Users\HP\Downloads\face detector.jpg", self.face_data),
            ("ATTENDANCE", r"C:\Users\HP\Downloads\attendence.jpg", self.attendance_system), # Linked to new method
            ("TRAIN DATA", r"C:\Users\HP\Downloads\traindata.jpg", self.train_data), # Linked to new method
            ("PHOTOS", r"C:\Users\HP\Downloads\photos.jpg", self.open_img), # Linked to new method
            ("HELP DESK", r"C:\Users\HP\Downloads\help desk.jpg", self.help_desk), # Linked to new method
            ("EXIT", r"C:\Users\HP\Downloads\exit.jpg", self.exit_system),
        ]

        # === Button Grid Placement (2 rows × 4 columns, centered) ===
        button_width = 180
        button_height = 180
        text_height = 35
        total_columns = 4
        h_spacing = 100
        y_positions = [70, 340]  # Row Y positions

        # Centered X start position based on 1530 screen width
        start_x = (1530 - (button_width * total_columns + h_spacing * (total_columns - 1))) // 2

        for index, (text, img_path, command) in enumerate(buttons):
            row = index // total_columns
            col = index % total_columns
            x = start_x + col * (button_width + h_spacing)
            y = y_positions[row]

            img = Image.open(img_path).resize((button_width, button_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            setattr(self, f"photoimg_{index}", photo)  # Keep reference to prevent garbage collection

            # Image Button
            Button(bg3, image=photo, command=command).place(
                x=x, y=y, width=button_width, height=button_height)

            # Text Button
            Button(bg3, text=text, command=command, # No need for lambda: None if command is always callable
                   font=("times new roman", 12, "bold"), bg="blue", fg="white").place(
                x=x, y=y + button_height + 5, width=button_width, height=text_height)

    # --- Methods for opening different sections ---
    def student_details(self):
        """Opens the Student Management System window."""
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def face_data(self):
        """Opens the Face Detector window."""
        self.new_window = Toplevel(self.root)
        self.app = Face_dector(self.new_window)

    def admin_panel(self):
        """Opens the Admin Panel window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = AdminPanel(self.new_window) # Using the placeholder class

    def attendance_system(self):
        """Opens the Attendance System window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = AttendanceSystem(self.new_window) # Using the placeholder class

    def open_img(self):
        """Opens the 'data' folder where photo samples are stored."""
        # Check if the 'data' directory exists before trying to open it
        if os.path.exists("data") and os.path.isdir("data"):
            os.startfile("data")
        else:
            messagebox.showinfo("Info", "The 'data' folder does not exist or is not a directory.", parent=self.root)

    
    def train_data(self):
        """Opens the Help Desk window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)        


    def help_desk(self):
        """Opens the Help Desk window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = HelpDesk(self.new_window) # Using the placeholder class

    def exit_system(self):
        """Closes the main application window."""
        self.root.destroy()

    

# === Main Entry Point ===
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()