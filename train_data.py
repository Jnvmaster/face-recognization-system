from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFile
import tkinter as tk
from tkinter import messagebox
import cv2
import os
import numpy as np

# Set the maximum image pixels limit to avoid DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1930x1005+0+0")
        self.root.title("Train Data")

        title_lbl = Label(self.root, text="TRAIN DATA SET", font=("Times New Roman", 35, "bold"),
                          bg="black", fg="darkgreen", bd=5)
        title_lbl.place(x=0, y=0, width=1530, height=90)

        img1 = Image.open(r"C:\Users\HP\Downloads\train data.jpg")
        img1 = img1.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lbl1 = Label(self.root, image=self.photoimg1)
        lbl1.place(x=0, y=95, width=1530, height=325)

        img2 = Image.open(r"C:\Users\HP\Downloads\train data.jpg")
        img2 = img2.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lbl2 = Label(self.root, image=self.photoimg2)
        lbl2.place(x=0, y=500, width=1530, height=325)

        train_btn = Button(self.root, text="TRAIN DATA", width=17, font=("Times New Roman", 25, "bold"),
                           bd=5, bg="blue", command=self.train_classifier) # Linked to the new function
        train_btn.place(x=0, y=420,width=1530,height=90)

    def train_classifier(self):
        data_dir = "data"
        # Ensure the 'data' directory exists and contains your pre-cropped face images
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "The 'data' directory does not exist. Please ensure it contains your pre-cropped face images.", parent=self.root)
            return

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        if not path:
            messagebox.showerror("Error", "No image files found in the 'data' directory. Please ensure it contains your pre-cropped face images.", parent=self.root)
            return

        for image_path in path:
            # Skip any non-image files or directories if present
            if not os.path.isfile(image_path) or not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                continue

            # Load the image and convert to grayscale
            # Assuming these images are ALREADY cropped to just the face
            img = Image.open(image_path).convert('L') # Convert to grayscale
            image_np = np.array(img, 'uint8') # Convert PIL image to numpy array

            # Extract ID from filename (e.g., user.1.1.jpg -> ID = 1)
            # The format is expected to be 'user.<student_id>.<image_id>.jpg'
            filename_parts = os.path.basename(image_path).split('.')
            if len(filename_parts) >= 2: # Check if there are enough parts
                id_str = filename_parts[1]
            else:
                print(f"Skipping file with unexpected name format: {image_path}")
                continue # Skip files that don't match the expected naming convention

            try:
                id_val = int(id_str)
            except ValueError:
                print(f"Skipping file with invalid ID (not an integer): {image_path}")
                continue

            # In this version, we assume image_np is already a cropped face, so no detection is needed.
            # We also ensure the image is not empty (e.g., from a corrupt file)
            if image_np.size > 0:
                faces.append(image_np)
                ids.append(id_val)
            else:
                print(f"Skipping empty or corrupt image: {image_path}")

        if not faces:
            messagebox.showerror("Error", "No valid face images found or processed in the 'data' directory. Ensure images are valid and correctly named.", parent=self.root)
            return

        # Convert lists to numpy arrays
        faces = np.array(faces)
        ids = np.array(ids)

        # Train the LBPH Face Recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        
        try:
            clf.train(faces, ids)
            # Save the trained model
            clf.write("classifier.xml")
            messagebox.showinfo("Success", "Training dataset completed successfully!", parent=self.root)
        except cv2.error as e:
            messagebox.showerror("Training Error", f"Error during training: {e}\n"
                                                 "Ensure you have enough unique photo samples for each student ID and that the images are grayscale.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during training: {e}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()