from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFile
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from datetime import datetime
import numpy as np
import csv # Import csv for attendance logging

# Set the maximum image pixels limit to avoid DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

# --- Student Class (Student Management Section) ---
class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student Management")

        # Variables for entry fields
        self.var_dep = StringVar(value="Select Department")
        self.var_course = StringVar(value="Select Course")
        self.var_semester = StringVar(value="Select Semester")
        self.var_year = StringVar(value="Select Year")
        self.var_student_id = StringVar()
        self.var_student_name = StringVar()
        self.var_class_division = StringVar()
        self.var_roll_no = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_gender = StringVar()
        self.var_mentor = StringVar()
        self.var_photo_sample = StringVar(value="no")

        # Images and layout (adjust paths as needed)
        img = Image.open(r"C:\Users\HP\Downloads\pes.jpg")
        img = img.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        lbl = Label(self.root, image=self.photoimg)
        lbl.place(x=0, y=0, width=500, height=130)

        img1 = Image.open(r"C:\Users\HP\Downloads\logo.jpg")
        img1 = img1.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lbl1 = Label(self.root, image=self.photoimg1)
        lbl1.place(x=500, y=0, width=500, height=130)

        img2 = Image.open(r"C:\Users\HP\Downloads\pes.jpg")
        img2 = img2.resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lbl2 = Label(self.root, image=self.photoimg2)
        lbl2.place(x=1000, y=0, width=500, height=130)

        img3 = Image.open(r"C:\Users\HP\Downloads\face.jpg")
        img3 = img3.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg3 = Label(self.root, image=self.photoimg3)
        bg3.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(bg3, text="STUDENT MANAGEMENT SECTION", font=("Times New Roman", 35, "bold"),
                          bg="black", fg="darkgreen", bd=5)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(bg3, bd=2)
        main_frame.place(x=10, y=55, width=1500, height=650)

        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details",
                                font=("Times New Roman", 12, "bold"), bg="white")
        left_frame.place(x=10, y=10, width=720, height=610)

        img_left = Image.open(r"C:\Users\HP\Downloads\pes.jpg")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        lbl = Label(left_frame, image=self.photoimg_left)
        lbl.place(x=5, y=0, width=720, height=130)

        course_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Current Course",
                                  font=("Times New Roman", 15, "bold"), bg="white")
        course_frame.place(x=10, y=100, width=700, height=150)

        dep_lbl = Label(course_frame, text="Department:", font=("Times New Roman", 15, "bold"), bd=5, bg="white")
        dep_lbl.grid(row=0, column=0, padx=10)

        dep_combo = ttk.Combobox(course_frame, textvariable=self.var_dep, font=("Times New Roman", 15, "bold"),
                                 width=13, state="readonly")
        dep_combo["values"] = ("Select Department", "CSE", "ECE", "VLSI", "MECHANICAL", "CIVIL")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10)

        course_lbl = Label(course_frame, text="Course:", font=("Times New Roman", 15, "bold"), bd=5, bg="white")
        course_lbl.grid(row=0, column=2, padx=10)

        cou_combo = ttk.Combobox(course_frame, textvariable=self.var_course, font=("Times New Roman", 15, "bold"),
                                 width=13, state="readonly")
        cou_combo["values"] = ("Select Course", "FY", "SY", "TY", "BE")
        cou_combo.current(0)
        cou_combo.grid(row=0, column=3, padx=2, pady=10)

        sem_lbl = Label(course_frame, text="Semester:", font=("Times New Roman", 15, "bold"), bd=5, bg="white")
        sem_lbl.grid(row=1, column=0, padx=10)

        sem_combo = ttk.Combobox(course_frame, textvariable=self.var_semester, font=("Times New Roman", 15, "bold"),
                                 width=13, state="readonly")
        sem_combo["values"] = ("Select Semester", "1", "2", "3", "4", "5", "6", "7", "8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=2,pady=10)

        year_lbl = Label(course_frame, text="Year:", font=("Times New Roman", 15, "bold"), bd=5, bg="white")
        year_lbl.grid(row=1, column=2, padx=10)

        year_combo = ttk.Combobox(course_frame, textvariable=self.var_year, font=("Times New Roman", 15, "bold"),
                                 width=13, state="readonly")
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25", "2025-26")
        year_combo.current(0)
        year_combo.grid(row=1, column=3, padx=2, pady=10)

        student_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Student Information",
                                   font=("Times New Roman", 15, "bold"), bg="white")
        student_frame.place(x=10, y=250, width=700, height=340)

        labels = ["Student ID:", "Student Name:", "Class Division:", "Roll No:", "DOB:", "Email:",
                  "Phone No:", "Address:", "Gender:", "Mentor Name:"]
        variables = [self.var_student_id, self.var_student_name, self.var_class_division, self.var_roll_no,
                     self.var_dob, self.var_email, self.var_phone, self.var_address, self.var_gender,
                     self.var_mentor]

        positions = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2), (4, 0), (4, 2)]

        for i, (text, var, pos) in enumerate(zip(labels, variables, positions)):
            lbl = Label(student_frame, text=text, font=("Times New Roman", 15, "bold"), bd=5, bg="white")
            lbl.grid(row=pos[0], column=pos[1], padx=10, pady=5, sticky=W)
            if text == "Gender:":
                gender_combo = ttk.Combobox(student_frame, textvariable=var, width=17, font=("Times New Roman", 15, "bold"), state="readonly")
                gender_combo["values"] = ("Male", "Female", "Other")
                gender_combo.current(0)
                gender_combo.grid(row=pos[0], column=pos[1] + 1, padx=10, pady=5, sticky=W)
            else:
                entry = ttk.Entry(student_frame, textvariable=var, width=20, font=("Times New Roman", 15, "bold"))
                entry.grid(row=pos[0], column=pos[1] + 1, padx=10, pady=5, sticky=W)

        radionbtn1 = ttk.Radiobutton(student_frame, text="Take photo sample", variable=self.var_photo_sample, value="yes")
        radionbtn1.grid(row=5, column=0, pady=5, padx=10, sticky=W)

        radionbtn2 = ttk.Radiobutton(student_frame, text="No photo sample", variable=self.var_photo_sample, value="no")
        radionbtn2.grid(row=5, column=1, pady=5, padx=10, sticky=W)

        button_frame = Frame(student_frame, bd=2, relief=RIDGE, bg="white")
        button_frame.place(x=0, y=250, width=695, height=70)

        save_btn = Button(button_frame, text="Save", width=15, font=("Times New Roman", 13, "bold"),
                          bd=5, bg="grey", command=self.save_data)
        save_btn.grid(row=0, column=0, padx=5, pady=5)

        update_btn = Button(button_frame, text="Update", width=15, font=("Times New Roman", 13, "bold"),
                             bd=5, bg="grey", command=self.update_data)
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        delete_btn = Button(button_frame, text="Delete", width=15, font=("Times New Roman", 13, "bold"),
                             bd=5, bg="grey", command=self.delete_data)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)

        reset_btn = Button(button_frame, text="Reset", width=15, font=("Times New Roman", 13, "bold"),
                             bd=5, bg="grey", command=self.reset_data)
        reset_btn.grid(row=0, column=3, padx=5, pady=5)

        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Search Details",
                                 font=("Times New Roman", 12, "bold"), bg="white")
        right_frame.place(x=750, y=10, width=720, height=580)

        img_right = Image.open(r"C:\Users\HP\Downloads\pes.jpg")
        img_right = img_right.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)
        lbl = Label(right_frame, image=self.photoimg_right)
        lbl.place(x=5, y=0, width=720, height=130)

        button_frame1 = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        button_frame1.place(x=0, y=120 , width=695, height=50)

        tps_btn = Button(button_frame1, text="Take Photo Sample", width=28, font=("Times New Roman", 15, "bold"),
                          bd=5, bg="grey", command=self.take_photo_sample)
        tps_btn.grid(row=0, column=0, padx=5, pady=5)

        tps1_btn = Button(button_frame1, text="Train Data", width=28, font=("Times New Roman", 15, "bold"),
                          bd=5, bg="grey", command=self.train_classifier)
        tps1_btn.grid(row=0, column=1, padx=5, pady=5)

        search_frame = LabelFrame(right_frame, bd=2, relief=RIDGE, text="Search Student",
                                  font=("Times New Roman", 12, "bold"), bg="white")
        search_frame.place(x=10, y=180, width=700, height=80)

        search_by_lbl = Label(search_frame, text="Search by:", font=("Times New Roman", 15, "bold"),
                              bd=5, bg="white", fg="red")
        search_by_lbl.grid(row=0, column=0, padx=5, pady=10)

        self.var_search_by = StringVar(value="Search_By")
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("Times New Roman", 15, "bold"),
                                    width=12, state="readonly")
        search_combo["values"] = ("Search_By", "Roll_No", "Student_ID")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10)

        self.var_search_txt = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search_txt, width=15,
                                  font=("Times New Roman", 15, "bold"))
        search_entry.grid(row=0, column=2, padx=5, pady=10)

        search_btn = Button(search_frame, text="Search", width=10, font=("Times New Roman", 15, "bold"),
                            bd=7, bg="grey", command=self.search_data)
        search_btn.grid(row=0, column=3, padx=5)

        show_all_btn = Button(search_frame, text="Show All", width=10, font=("Times New Roman", 15, "bold"),
                               bd=7, bg="grey", command=self.show_all_data)
        show_all_btn.grid(row=0, column=4, padx=5)

        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=10, y=280, width=700, height=280)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame,
                                          columns=("Dep", "Course", "Sem", "Year", "ID", "Name", "Division",
                                                   "Roll", "DOB", "Email", "Phone", "Address", "Gender",
                                                   "Mentor", "Photo"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("Dep", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Sem", text="Semester")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("ID", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Division", text="Division")
        self.student_table.heading("Roll", text="Roll No")
        self.student_table.heading("DOB", text="DOB")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Phone", text="Phone No")
        self.student_table.heading("Address", text="Address")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("Mentor", text="Mentor Name")
        self.student_table.heading("Photo", text="Photo Sample")

        self.student_table["show"] = "headings"

        self.student_table.column("Dep", width=100)
        self.student_table.column("Course", width=100)
        self.student_table.column("Sem", width=80)
        self.student_table.column("Year", width=100)
        self.student_table.column("ID", width=100)
        self.student_table.column("Name", width=150)
        self.student_table.column("Division", width=100)
        self.student_table.column("Roll", width=80)
        self.student_table.column("DOB", width=100)
        self.student_table.column("Email", width=150)
        self.student_table.column("Phone", width=100)
        self.student_table.column("Address", width=150)
        self.student_table.column("Gender", width=80)
        self.student_table.column("Mentor", width=150)
        self.student_table.column("Photo", width=120)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.conn = None
        self.my_cursor = None
        self.connect_database()
        self.show_all_data()

    # --- Database Connection and CRUD Operations ---
    def connect_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Pratik@05", # <<<<<<< IMPORTANT: CHANGE THIS TO YOUR MYSQL PASSWORD >>>>>>>
                database="college",
                auth_plugin='mysql_native_password'
            )
            self.my_cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database:\n{e}", parent=self.root)
            self.conn = None
            self.my_cursor = None

    def save_data(self):
        # Input Validation for mandatory fields
        if (self.var_dep.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_semester.get() == "Select Semester" or
            self.var_year.get() == "Select Year" or
            self.var_student_id.get() == "" or
            self.var_student_name.get() == "" or
            self.var_roll_no.get() == "" or
            self.var_dob.get() == "" or
            self.var_gender.get() == ""):
            messagebox.showerror("Error", "All fields are required. Please fill in all student details and course information.", parent=self.root)
            return

        # Validate DOB format (YYYY-MM-DD)
        try:
            datetime.strptime(self.var_dob.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format (e.g., 2000-01-15)", parent=self.root)
            return

        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return

        try:
            query = "INSERT INTO students (dep, course, semester, year, student_id, name, class_division, roll_no, dob, email, phone, address, gender, mentor, photo_sample) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (self.var_dep.get(), self.var_course.get(), self.var_semester.get(), self.var_year.get(),
                      self.var_student_id.get(), self.var_student_name.get(), self.var_class_division.get(),
                      self.var_roll_no.get(), self.var_dob.get(), self.var_email.get(), self.var_phone.get(),
                      self.var_address.get(), self.var_gender.get(), self.var_mentor.get(), self.var_photo_sample.get())

            self.my_cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Data saved successfully", parent=self.root)
            self.show_all_data()
            self.reset_data()
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e) and "for key 'PRIMARY'" in str(e):
                messagebox.showerror("Error", "Student ID already exists. Please use a unique Student ID or update the existing record.", parent=self.root)
            else:
                messagebox.showerror("Database Error", f"A database integrity error occurred:\n{e}", parent=self.root)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error saving data to database:\n{e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def update_data(self):
        if self.var_student_id.get() == "":
            messagebox.showerror("Error", "Student ID is required to update data", parent=self.root)
            return

        try:
            datetime.strptime(self.var_dob.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "DOB must be in YYYY-MM-DD format (e.g., 2000-01-15)", parent=self.root)
            return

        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return

        try:
            query = "UPDATE students SET dep=%s, course=%s, semester=%s, year=%s, name=%s, class_division=%s, roll_no=%s, dob=%s, email=%s, phone=%s, address=%s, gender=%s, mentor=%s, photo_sample=%s WHERE student_id=%s"
            values = (self.var_dep.get(), self.var_course.get(), self.var_semester.get(), self.var_year.get(),
                      self.var_student_name.get(), self.var_class_division.get(), self.var_roll_no.get(),
                      self.var_dob.get(), self.var_email.get(), self.var_phone.get(), self.var_address.get(),
                      self.var_gender.get(), self.var_mentor.get(), self.var_photo_sample.get(), self.var_student_id.get())

            self.my_cursor.execute(query, values)
            self.conn.commit()
            if self.my_cursor.rowcount == 0:
                messagebox.showwarning("Warning", "No record found with the given Student ID to update.", parent=self.root)
            else:
                messagebox.showinfo("Success", "Data updated successfully", parent=self.root)
            self.show_all_data()
            self.reset_data()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error updating data in database:\n{e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def delete_data(self):
        if self.var_student_id.get() == "":
            messagebox.showerror("Error", "Student ID is required to delete data", parent=self.root)
            return

        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return

        try:
            option = messagebox.askyesno("Confirm Delete", "Do you want to delete this record?", parent=self.root)
            if option:
                query = "DELETE FROM students WHERE student_id=%s"
                self.my_cursor.execute(query, (self.var_student_id.get(),))
                self.conn.commit()
                if self.my_cursor.rowcount == 0:
                    messagebox.showwarning("Warning", "No record found with the given Student ID to delete.", parent=self.root)
                else:
                    messagebox.showinfo("Deleted", "Record deleted successfully", parent=self.root)
                self.show_all_data()
                self.reset_data()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error deleting data from database:\n{e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_semester.set("Select Semester")
        self.var_year.set("Select Year")
        self.var_student_id.set("")
        self.var_student_name.set("")
        self.var_class_division.set("")
        self.var_roll_no.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_gender.set("")
        self.var_mentor.set("")
        self.var_photo_sample.set("no")

    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data = content["values"]
        if data:
            self.var_dep.set(data[0])
            self.var_course.set(data[1])
            self.var_semester.set(data[2])
            self.var_year.set(data[3])
            self.var_student_id.set(data[4])
            self.var_student_name.set(data[5])
            self.var_class_division.set(data[6])
            self.var_roll_no.set(data[7])
            self.var_dob.set(data[8])
            self.var_email.set(data[9])
            self.var_phone.set(data[10])
            self.var_address.set(data[11])
            self.var_gender.set(data[12])
            self.var_mentor.set(data[13])
            self.var_photo_sample.set(data[14])

    def show_all_data(self):
        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return

        try:
            self.my_cursor.execute("SELECT dep, course, semester, year, student_id, name, class_division, roll_no, dob, email, phone, address, gender, mentor, photo_sample FROM students")
            rows = self.my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children())

            if rows:
                for row in rows:
                    self.student_table.insert("", END, values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data:\n{e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def search_data(self):
        if self.var_search_by.get() == "Search_By" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Select search criteria and enter search text", parent=self.root)
            return

        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return

        try:
            query = ""
            value = ()
            if self.var_search_by.get() == "Roll_No":
                query = "SELECT dep, course, semester, year, student_id, name, class_division, roll_no, dob, email, phone, address, gender, mentor, photo_sample FROM students WHERE roll_no LIKE %s"
                value = ("%" + self.var_search_txt.get() + "%",)
            elif self.var_search_by.get() == "Student_ID":
                query = "SELECT dep, course, semester, year, student_id, name, class_division, roll_no, dob, email, phone, address, gender, mentor, photo_sample FROM students WHERE student_id LIKE %s"
                value = ("%" + self.var_search_txt.get() + "%",)
            else:
                messagebox.showerror("Error", "Invalid search criteria", parent=self.root)
                return

            self.my_cursor.execute(query, value)
            rows = self.my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children())

            if rows:
                for row in rows:
                    self.student_table.insert("", END, values=row)
            else:
                messagebox.showinfo("Info", "No records found for the given search criteria.", parent=self.root)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error searching data:\n{e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    # --- OpenCV Functions for Photo Capture and Training ---
    def take_photo_sample(self):
        if self.var_student_id.get() == "" or self.var_student_name.get() == "":
            messagebox.showerror("Error", "Student ID and Name are required to take photo samples.", parent=self.root)
            return

        student_id = self.var_student_id.get()

        # Determine the cascade file path robustly
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

        if not os.path.exists(cascade_path):
            messagebox.showerror("Error", f"Could not find haarcascade_frontalface_default.xml at {cascade_path}. Please ensure OpenCV is installed correctly.", parent=self.root)
            return

        clf = cv2.CascadeClassifier(cascade_path)
        if clf.empty():
            messagebox.showerror("Error", f"Could not load cascade classifier from {cascade_path}. It might be corrupted or malformed.", parent=self.root)
            return

        # Create a directory to save images if it doesn't exist
        if not os.path.exists("face_data"):
            os.makedirs("face_data")

        cap = cv2.VideoCapture(0) # Open the camera (0 is usually the default webcam)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam. Make sure it's connected and not in use by another application.", parent=self.root)
            return

        img_id = 0

        messagebox.showinfo("Info", "Press 'q' to stop capturing, or it will stop automatically after 100 samples.", parent=self.root)

        while True:
            ret, my_frame = cap.read() # Read a frame from the camera
            if not ret:
                messagebox.showerror("Error", "Failed to grab frame from camera. Check camera connection.", parent=self.root)
                break

            gray_frame = cv2.cvtColor(my_frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
            # Detect faces in the grayscale frame
            faces = clf.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(my_frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw rectangle around face
                img_id += 1
                face_roi = gray_frame[y:y+h, x:x+w] # Extract the region of interest (face)
                face_resized = cv2.resize(face_roi, (200, 200)) # Resize face for consistent sample size

                # Save the captured image with student_id and sample_id
                img_path = f"face_data/user.{student_id}.{img_id}.jpg"
                cv2.imwrite(img_path, face_resized)

                # Display sample count on the frame
                cv2.putText(my_frame, f"Sample: {img_id}", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,255,0), 2)

            cv2.imshow("Taking Photo Samples...", my_frame) # Show the live feed

            # Break loop if 'q' is pressed or 100 samples are taken
            if cv2.waitKey(1) & 0xFF == ord('q') or img_id >= 100:
                break

        cap.release() # Release the camera
        cv2.destroyAllWindows() # Close all OpenCV windows

        if img_id > 0:
            messagebox.showinfo("Result", f"Successfully generated {img_id} photo samples!", parent=self.root)
            self.var_photo_sample.set("yes") # Update UI variable
        else:
            messagebox.showwarning("Result", "No photo samples were taken. Ensure your face is clearly visible and within the frame.", parent=self.root)

        # Refresh the table data to reflect photo sample status
        self.show_all_data()

    def train_classifier(self):
        data_dir = "face_data"
        # Check if the directory exists and contains files
        if not os.path.exists(data_dir) or not os.listdir(data_dir):
            messagebox.showerror("Error", "No face data found for training. Please take photo samples first.", parent=self.root)
            return

        # Get all image paths from the face_data directory
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".jpg")]

        faces = []
        ids = []

        for image_path in path:
            # Open image and convert to grayscale
            img = Image.open(image_path).convert('L')
            # Convert PIL image to a NumPy array for OpenCV
            image_np = np.array(img, 'uint8')

            # Extract the student ID from the filename
            # Filename format: user.STUDENT_ID.SAMPLE_ID.jpg
            student_id = int(os.path.basename(image_path).split('.')[1])

            faces.append(image_np)
            ids.append(student_id)

        # Convert the list of IDs to a NumPy array
        ids = np.array(ids)

        if len(faces) == 0:
            messagebox.showerror("Error", "No valid face samples found for training.", parent=self.root)
            return

        # Create and train the LBPH Face Recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.train(faces, ids)
            recognizer.write("classifier.xml") # Save the trained model
            messagebox.showinfo("Success", "Face data trained successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error during training: {str(e)}\nEnsure you have sufficient and diverse samples for each student ID.", parent=self.root)


# --- Face_dector Class (Face Recognition and Attendance) ---
class Face_dector:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="Face Detector", font=("Times New Roman", 35, "bold"),
                                 bg="white", fg="darkgreen", bd=5)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img1 = Image.open(r"C:\Users\HP\Downloads\face me.jpg")
        img1 = img1.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lbl1 = Label(self.root, image=self.photoimg1)
        lbl1.place(x=0, y=55, width=650, height=700)

        img2 = Image.open(r"C:\Users\HP\Downloads\face_d.jpg")
        img2 = img2.resize((950, 700), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lbl1 = Label(self.root, image=self.photoimg2)
        lbl1.place(x=650, y=55, width=950, height=700)

        b1 = Button(lbl1, text="Face Detector", width=15, font=("Times New Roman", 13, "bold"),
                                 bd=5, bg="green", command=self.face_recog)
        b1.place(x=370, y=620, width=200, height=40)

        # Initialize database connection for fetching student names
        self.conn = None
        self.my_cursor = None
        self.connect_database()

    def connect_database(self):
        """Establishes connection to the MySQL database."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Pratik@05", # <<<<<<< IMPORTANT: CHANGE THIS TO YOUR MYSQL PASSWORD >>>>>>>
                database="college",
                auth_plugin='mysql_native_password'
            )
            self.my_cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database:\n{e}", parent=self.root)
            self.conn = None
            self.my_cursor = None

    def get_student_info(self, student_id):
        """Fetches student name and other details from the database based on student_id."""
        if not self.conn or not self.my_cursor:
            self.connect_database()
            if not self.conn:
                return None, None, None # Return None if connection fails

        try:
            query = "SELECT name, roll_no, dep FROM students WHERE student_id = %s"
            self.my_cursor.execute(query, (str(student_id),))
            result = self.my_cursor.fetchone()
            if result:
                return result[0], result[1], result[2] # name, roll_no, dep
            else:
                return "Unknown", "N/A", "N/A" # Default if student not found
        except mysql.connector.Error as e:
            print(f"Database error fetching student info: {e}")
            return "DB Error", "N/A", "N/A"
        except Exception as e:
            print(f"An unexpected error occurred while fetching student info: {e}")
            return "Error", "N/A", "N/A"

    def mark_attendance(self, s_id, r_no, s_name, dep):
        """
        Marks attendance in a daily CSV file.
        Creates a new file daily if it doesn't exist.
        Avoids duplicate entries for the same student on the same day.
        """
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        attendance_file_path = f"attendance_{current_date}.csv"

        # Check if student already marked today
        student_already_marked = False
        if os.path.exists(attendance_file_path):
            with open(attendance_file_path, "r", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None) # Skip header
                for row in reader:
                    if len(row) > 0 and str(row[0]) == str(s_id): # Check if the student ID exists in any row
                        student_already_marked = True
                        break

        if student_already_marked:
            # Only show message if it's a Toplevel window, otherwise it can flood
            # if self.root.winfo_exists(): # Check if window is still active
            # messagebox.showinfo("Attendance Already Marked", f"Attendance already marked for {s_name} today.", parent=self.root)
            return # Don't write if already marked

        # If not marked, proceed to write attendance
        file_exists = os.path.exists(attendance_file_path)

        try:
            with open(attendance_file_path, "a", newline="") as f:
                writer = csv.writer(f)

                # Write header if file is new (or empty)
                if not file_exists or os.stat(attendance_file_path).st_size == 0:
                    writer.writerow(["ID", "Roll_No", "Name", "Department", "Time", "Date"])

                writer.writerow([s_id, r_no, s_name, dep, current_time, current_date])
                messagebox.showinfo("Attendance Marked", f"Attendance marked for {s_name} (ID: {s_id})", parent=self.root)

        except IOError as e:
            messagebox.showerror("File Error", f"Could not write to attendance file: {e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while marking attendance: {e}", parent=self.root)


    def face_recog(self):
        """
        Performs real-time face recognition using the webcam and marks attendance.
        """
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                id, predict_confidence = clf.predict(gray_image[y:y+h, x:x+w])

                # Fetch student name, roll number, and department from the database
                s_name, r_no, dep = self.get_student_info(id)

                if predict_confidence < 500: # Threshold for recognition (lower is better)
                    confidence = int(100 * (1 - (predict_confidence) / 300)) # Simplified confidence calculation
                    if confidence > 60: # Adjust this confidence threshold as needed (e.g., >60% to be recognized)
                        cv2.putText(img, f"ID: {id}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Name: {s_name}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Roll No: {r_no}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Confidence: {confidence}%", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

                        # Mark attendance
                        self.mark_attendance(id, r_no, s_name, dep)
                    else: # Recognized but low confidence, treat as unknown
                        cv2.putText(img, "Unknown", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                        cv2.putText(img, f"ID: {id} (Low Conf)", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                        cv2.putText(img, f"Confidence: {confidence}%", (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                else: # Prediction confidence is too high, definitely unknown
                    cv2.putText(img, "Unknown", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, "No Match", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)


            return img

        # --- Main Face Recognition Logic ---
        # Ensure 'haarcascade_frontalface_default.xml' is in a place OpenCV can find it
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
        face_classifier = cv2.CascadeClassifier(cascade_path)

        if not os.path.exists(cascade_path):
            messagebox.showerror("Error", f"Haar Cascade XML not found: {cascade_path}\nPlease ensure OpenCV is correctly installed or the file is in the right place.", parent=self.root)
            return

        # Check if the trained classifier.xml exists
        if not os.path.exists("classifier.xml"):
            messagebox.showerror("Error", "Trained classifier 'classifier.xml' not found.\nPlease train the data first from the Student Details section.", parent=self.root)
            return

        # Load the trained model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read("classifier.xml")
        except cv2.error as e:
            messagebox.showerror("Error", f"Could not load classifier.xml. It might be corrupted or empty.\nError: {e}\nPlease re-train the data from the Student Details section.", parent=self.root)
            return

        video_cap = cv2.VideoCapture(0) # Open default webcam
        if not video_cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam. Make sure it's connected and not in use.", parent=self.root)
            return

        messagebox.showinfo("Face Detector", "Face Detector is running. Press 'q' to quit.", parent=self.root)

        while True:
            ret, img = video_cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to grab frame from camera. Exiting face detector.", parent=self.root)
                break

            img = draw_boundary(img, face_classifier, 1.1, 10, (255, 255, 255), "Face", recognizer)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit
                break

        video_cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Face Detector", "Face Detector stopped.", parent=self.root)


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

# The main Train Data functionality is now in Student class, so this is just a placeholder if you wanted a separate button
class TrainDataModule:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+100+100")
        self.root.title("Train Data")
        Label(self.root, text="Face Data Training Module", font=("times new roman", 20, "bold")).pack(pady=50)
        Label(self.root, text="This module will handle training of your face recognition model.", font=("times new roman", 14)).pack()
        Label(self.root, text="Note: Training is also available in 'Student Details' section.", font=("times new roman", 10, "italic")).pack()


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


# --- Main Application Class (Dashboard) ---
class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x710+0+0")
        self.root.title("Face Recognition Attendance System")

        # === Top Header Images === (Adjust paths as needed)
        img = Image.open(r"C:\Users\HP\Downloads\pes.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=500, height=130)

        img1 = Image.open(r"C:\Users\HP\Downloads\logo.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=500, y=0, width=500, height=130)

        img2 = Image.open(r"C:\Users\HP\Downloads\pes.jpg").resize((500, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=1000, y=0, width=500, height=130)

        # === Background === (Adjust path as needed)
        img3 = Image.open(r"C:\Users\HP\Downloads\face.jpg").resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg3 = Label(self.root, image=self.photoimg3)
        bg3.place(x=0, y=130, width=1530, height=710)

        # === Title ===
        Label(bg3, text="FACE RECOGNITION ATTENDANCE SYSTEM",
              font=("times new roman", 30, "bold"), bg="white", fg="red").place(x=0, y=0, width=1530, height=45)

        # === Button Definitions === (Adjust image paths as needed)
        buttons = [
            ("STUDENT DETAILS", r"C:\Users\HP\Downloads\student2.jpg", self.open_student_details),
            ("ADMIN", r"C:\Users\HP\Downloads\admin2.jpg", self.open_admin_panel),
            ("FACE DETECTOR", r"C:\Users\HP\Downloads\face detector.jpg", self.open_face_detector),
            ("ATTENDANCE", r"C:\Users\HP\Downloads\attendence.jpg", self.open_attendance_system),
            ("TRAIN DATA", r"C:\Users\HP\Downloads\traindata.jpg", self.open_train_data_module),
            ("PHOTOS", r"C:\Users\HP\Downloads\photos.jpg", self.open_photos_viewer),
            ("HELP DESK", r"C:\Users\HP\Downloads\help desk.jpg", self.open_help_desk),
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
            Button(bg3, text=text, command=command,
                   font=("times new roman", 12, "bold"), bg="blue", fg="white").place(
                x=x, y=y + button_height + 5, width=button_width, height=text_height)

    # --- Methods for opening different sections ---
    def open_student_details(self):
        """Opens the Student Management System window."""
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def open_face_detector(self):
        """Opens the Face Detector window."""
        self.new_window = Toplevel(self.root)
        self.app = Face_dector(self.new_window)

    def open_admin_panel(self):
        """Opens the Admin Panel window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = AdminPanel(self.new_window)

    def open_attendance_system(self):
        """Opens the Attendance System window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = AttendanceSystem(self.new_window)

    def open_train_data_module(self):
        """Opens the Train Data module window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = TrainDataModule(self.new_window)

    def open_photos_viewer(self):
        """Opens a window to view photo samples (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = PhotosViewer(self.new_window)

    def open_help_desk(self):
        """Opens the Help Desk window (placeholder)."""
        self.new_window = Toplevel(self.root)
        self.app = HelpDesk(self.new_window)

    def exit_system(self):
        """Closes the main application window."""
        self.root.destroy()

# === Main Entry Point ===
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()