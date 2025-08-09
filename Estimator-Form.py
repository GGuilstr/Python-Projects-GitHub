
from tokenize import group
from PyQt5.QtCore import * # Qt
from PyQt5.QtGui import *  # QGuiApplication
from PyQt5.QtWidgets import *  # QScroller
from PyQt5.QtSql import *
import sys
import csv
import os
import cv2
from PIL import Image, ImageQt
import time

import sqlite3
from fpdf import FPDF

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from tkinter import filedialog, simpledialog, messagebox

import shutil
from datetime import datetime

# --------------------------------------------------------------------------------

# SELECT THE FOLDER IN WHICH ALL ESTIMATING FILES ARE SAVED TO

global files_folder

# Global variable
files_folder = ""

dict1_item = {}
dict1_user_item = {}
dict1_quantity = {}
dict1_user_quantity = {}
dict1_cost = {}
dict1_user_cost = {}
dict1_user_cost_float = {}

dict1_num1 = {}

dict_floata = {}
dict_tax_amounta = {}
dict_total_with_taxa = {}
dict_tax_rate = {}

dict_labor_amounta = {}
dict_total_with_labora = {}
dict_labora = {}

dict_prepared_estimate = {}

global scroll_layout1
global cust_name_input

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Job Estimator Form")
        #self.setFixedSize(975, 800)  # Locks the window size

        # Get screen dimensions
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window size to 80% of screen size
        window_width = int(screen_width * 0.78)
        window_height = int(screen_height * 0.85)
        self.resize(window_width, window_height)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Disable scrollbars completely (hide them)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # You can leave AsNeeded if you want vertical scroll visible

        # Enable kinetic scrolling for vertical only
        QScroller.grabGesture(self.scroll_area.viewport(), QScroller.TouchGesture)
        scroller = QScroller.scroller(self.scroll_area.viewport())
        properties = scroller.scrollerProperties()

        # Limit to vertical scrolling only
        
        properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        properties.setScrollMetric(QScrollerProperties.FrameRate, QScrollerProperties.Fps60)
        properties.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.05)

        scroller.setScrollerProperties(properties)

        # --------------- Central widget Container ----------------
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setMinimumWidth(self.scroll_area.viewport().width())

        self.container = self.container  # Add this line
        self.scroll_area = self.scroll_area  # Add this line

        # Main background color
        self.scroll_area.setStyleSheet("background-color: #85c1e9;")

        # Layouts inside scroll area
        self.scroll_layout1 = QGridLayout(self.container)
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        
        self.scroll_layout1.setColumnStretch(0, 1)

# ------------------------------------------------------------------------------------------
# ----------------- COMPANY NAME LABEL --------------------

        # Section 1A: QLabel text - Company Name Beaufort Construction
        section1A = QWidget()

#        company_name = QGroupBox("Customer Info Section")
#        company_name.setCheckable(True)
        
        company_name = QGridLayout(section1A)
        company_name.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        #company_name.setContentsMargins(0, 0, 0, 0)
        
        company_name_label = QLabel("Beaufort Construction")

        # Set font and style
        font = QFont("Calibri", 28)
        font.setBold(False)
        company_name_label.setFont(font)

        company_name_label.setStyleSheet("color: black")

        # Optional margins
        company_name_label.setContentsMargins(0, 0, 0, 0)
        #company_name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add both labels side by side in the same row (row=0), different columns (col=0 and col=1)
        company_name.addWidget(company_name_label,0,0)

        # Add all sections to the main layout
        self.scroll_layout1.addWidget(section1A)

# ------------------------------------------------------------------------------------------
# ----------------- CUSTOMER INFO LABEL --------------------

        # Section 1B: QLabel text - Customer Info
        section1B = QWidget()

        customer_info = QGridLayout(section1B)
        customer_info.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        #customer_info.setContentsMargins(0, 0, 0, 0)

        customer_info_label = QLabel("Customer Info")

        # Set font and style
        font = QFont("Calibri", 12)
        font.setBold(True)
        customer_info_label.setFont(font)

        customer_info_label.setStyleSheet("color: black")

        # Optional margins
        customer_info_label.setContentsMargins(20, 0, 0, 0)
        customer_info_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add both labels side by side in the same row (row=0), different columns (col=0 and col=1)
        customer_info.addWidget(customer_info_label,0,0)

        # Add all sections to the main layout
        self.scroll_layout1.addWidget(section1B)

# ------------------------------------------------------------------------------------------
# ----------------- CUSTOMER NAME AND PHONE NUMBER --------------------

        # Section 2: Customer Name and Phone Number
        section2 = QWidget()

        # Grid layout
        cust_info = QGridLayout(section2)
        cust_info.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        #cust_info.setHorizontalSpacing(0)  # Only for Grid Layout
        #cust_info.setVerticalSpacing(50)  # Only for Grid Layout
        cust_info.setContentsMargins(10, 10, 0, 0)

        label_font = QFont("Calibri", 14)

        # First label = Customer Name
        cust_name_label = QLabel("Customer Name:")
        cust_name_label.setFont(label_font)
        cust_name_label.setStyleSheet("color: black;")
        #cust_name_label.setMinimumSize(167, 35)

        cust_name_label.setContentsMargins(0, 0, 0, 0)

        self.cust_name_input = QLineEdit()
        self.cust_name_input.setMinimumSize(180, 35)
        self.cust_name_input.setFont(label_font)

        self.cust_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)
       
        self.cust_name_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cust_name_input.setContentsMargins(0, 0, 0, 0)

        # Second label = Phone Number
        cust_phone_label = QLabel("Phone Number:")
        cust_phone_label.setFont(label_font)
        cust_phone_label.setStyleSheet("color: black;")
        #cust_phone_label.setMinimumSize(150, 35)

        cust_phone_label.setContentsMargins(0, 0, 0, 0)

        self.cust_phone_input = QLineEdit()
        self.cust_phone_input.setMinimumSize(200, 35)
        self.cust_phone_input.setFont(label_font)

        self.cust_phone_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)

        #cust_phone_input.setMinimumSize(210, 35)
        self.cust_phone_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cust_phone_input.setContentsMargins(0, 0, 0, 0)

        # Dummy label for Center Padding
        cust_spacer = QLabel("")
        #cust_spacer.setFixedWidth(100)
        cust_spacer.setMinimumSize(100, 0)
        cust_spacer.setContentsMargins(0, 0, 0, 0)

        # Add widgets to layout
        cust_info.addWidget(cust_name_label, 0, 0)
        cust_info.addWidget(self.cust_name_input, 0, 1)

        #cust_info.addWidget(cust_spacer) #, 2, 2)

        cust_info.addWidget(cust_phone_label, 0, 2)
        cust_info.addWidget(self.cust_phone_input, 0, 3)

# ------------------------------------------------------------------------------------------
# ----------------- CUSTOMER ADDRESS AND DATE --------------------

        label_font = QFont("Calibri", 14)

        # First label = Address
        address_label = QLabel("Address:")
        address_label.setFont(label_font)
        address_label.setStyleSheet("color: black;")
        #address_label.setMinimumSize(157, 35)

        address_label.setContentsMargins(75, 0, 0, 20)

        self.address_input = QTextEdit()
        self.address_input.setMinimumSize(180, 80)
        self.address_input.setFont(label_font)

        self.address_input.setStyleSheet("""
            QTextEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QTextEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)
       
        self.address_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.address_input.setContentsMargins(0, 0, 0, 0)

        # Second label = Date
        date_label = QLabel("Date:")
        date_label.setFont(label_font)
        date_label.setStyleSheet("color: black;")
        #date_label.setMinimumSize(150, 35)

        date_label.setContentsMargins(95, 0, 0, 0)

        self.date_input = QLineEdit()
        self.date_input.setMinimumSize(200, 35)
        self.date_input.setFont(label_font)

        self.date_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)
       
        self.date_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.date_input.setContentsMargins(0, 0, 0, 0)

        # Dummy label for Center Padding
        address_date_spacer = QLabel("")
        address_date_spacer.setMinimumSize(120, 35)

        address_date_spacer.setContentsMargins(0, 0, 0, 0)

        # Add widgets to layout
        cust_info.addWidget(address_label, 1, 0)
        cust_info.addWidget(self.address_input, 1, 1)

        #address_date.addWidget(address_date_spacer) #, 2, 2)

        cust_info.addWidget(date_label, 1, 2)
        cust_info.addWidget(self.date_input, 1, 3)

        # Add all sections to the main layout
        self.scroll_layout1.addWidget(section2)

# ------------------------------------------------------------------------------------------
# ----------------- CUSTOMER EMAIL --------------------

        # Section 3: Email
        section3 = QWidget()

        # Grid layout
        email = QGridLayout(section3)
        email.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        #email.setHorizontalSpacing(0)  # Only for Grid Layout
        #email.setVerticalSpacing(50)  # Only for Grid Layout
        email.setContentsMargins(385, 0, 0, 0)

        label_font = QFont("Calibri", 14)

        # First label = Email
        email_label = QLabel("Email:")
        email_label.setFont(label_font)
        email_label.setStyleSheet("color: black;")
        #email_label.setMinimumSize(128, 35)

        email_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        email_label.setContentsMargins(63, 0, 0, 0)

        self.email_input = QLineEdit()
        self.email_input.setMinimumSize(280, 35)
        self.email_input.setFont(label_font)

        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)
      
        self.email_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.email_input.setContentsMargins(0, 0, 0, 0)

        # Dummy label for Center Padding
        email_spacer = QLabel("")
        email_spacer.setMinimumSize(200, 35)

        email_spacer.setContentsMargins(0, 0, 0, 0)

        #email.addWidget(email_spacer, 0, 0)
        email.addWidget(email_label, 0, 1)
        email.addWidget(self.email_input, 0, 2)

        # Add all sections to the main layout
        self.scroll_layout1.addWidget(section3)

# ------------------------------------------------------------------------------------------
# ----------------- SPACER - NOT USED --------------------

        # Section 4: Spacer
        section4 = QWidget()

        # Grid layout
        spacer_1 = QGridLayout(section4)
        spacer_1.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        spacer_1.setContentsMargins(20, 20, 0, 0)

        label_font = QFont("Calibri", 14)

        # Dummy label for Section Spacer
        one_spacer = QLabel("--------------------------------------------------------------------------------------------------------------------------------------------")
        one_spacer.setMinimumSize(510, 0)
        
        one_spacer.setContentsMargins(0, 0, 0, 0)

        spacer_1.addWidget(one_spacer,0,0)

        # Add all sections to the main layout
        #self.scroll_layout1.addWidget(section4)

# ------------------------------------------------------------------------------------------
# ----------------- DESCRIPTION OF WORK FOR JOB --------------------

        # Section 5: Description of Job
        section5 = QWidget()

        # Grid layout
        job_description = QGridLayout(section5)
        job_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        #job_description.setHorizontalSpacing(0)  # Only for Grid Layout
        #job_description.setVerticalSpacing(50)  # Only for Grid Layout
        job_description.setContentsMargins(0, 20, 0, 0)

        label_font = QFont("Calibri", 14)

        # First label = Job Description
        job_label = QLabel("Job Description:")
        job_label.setFont(label_font)
        job_label.setStyleSheet("color: black;")
        #job_label.setMinimumSize(250, 100)

        job_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        job_label.setContentsMargins(20, 0, 0, 0)

        self.job_input = QTextEdit()
        self.job_input.setMinimumSize(280, 100)
        self.job_input.setFont(label_font)

        self.job_input.setStyleSheet("""
            QTextEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QTextEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
            }
        """)
        
        self.job_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.job_input.setContentsMargins(0, 0, 0, 0)

        # Dummy label for Center Padding
        job_spacer = QLabel("")
        job_spacer.setMinimumSize(200, 35)

        job_spacer.setContentsMargins(0, 0, 0, 0)

        #job.addWidget(job_spacer, 0, 0)
        job_description.addWidget(job_label, 0, 1)
        job_description.addWidget(self.job_input, 0, 2)

        # Add all sections to the main layout
        self.scroll_layout1.addWidget(section5)

# ------------------------------------------------------------------------------------------
# ----------------- SPACER - NOT USED --------------------

        # Section 6: Spacer
        section6 = QWidget()

        # Grid layout
        spacer_2 = QGridLayout(section6)
        spacer_2.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        spacer_2.setContentsMargins(20, 20, 0, 0)

        label_font = QFont("Calibri", 14)

        # Dummy label for Section Spacer
        two_spacer = QLabel("--------------------------------------------------------------------------------------------------------------------------------------------")
        two_spacer.setMinimumSize(510, 0)
        
        two_spacer.setContentsMargins(0, 0, 0, 0)

        spacer_2.addWidget(two_spacer,0,0)

        # Add all sections to the main layout
        #self.scroll_layout1.addWidget(section6)

# ------------------------------------------------------------------------------------------
#       CONTAINER SCROLLING CALLS
# -----------------------------------

        # Set main scroll widget
        self.scroll_area.setWidget(self.container)
        self.setCentralWidget(self.scroll_area)

        # Center the window on the screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.container.adjustSize()
        self.scroll_area.ensureVisible(0, 0)

# ------------------------------------------------------------------------------------------
#       CLASS AND FUNCTION INVOCATIONS
# -----------------------------------

    # ----------------------
        # Set the Default Folder for all Files
#        self.file_app = FolderSelector()
#        self.scroll_layout1.addWidget(self.file_app)

#       - ----CLASS----
        self.files_folder = FilesFolder().files_folder
#        self.files_folder = FolderSelector().files_folder
    # ----------------------
        # Add PhotoCaptureApp section - ----CLASS----
#        self.photo_app = PhotoCaptureApp()
        self.photo_app = PhotoCaptureApp(files_folder=self.files_folder)
        self.scroll_layout1.addWidget(self.photo_app)
    # ----------------------
        # Add 10 - Items , Quantity and Cost
        self.add_items_loop1()
    # ----------------------
        # Add Material Cost, Material Tax, total Cost of Material with Tax, Labor Cost and Total Cost of Project
        self.add_cost_tax_labor()
    # ----------------------
#       - ----CLASS----
        self.dbscsvpdf_app = Savedbs_csv_pdf(self.cust_name_input,
                 self.cust_phone_input,
                 self.address_input,
                 self.date_input,
                 self.email_input,
                 self.job_input,
                 self.prepared_estimate_entrya,
                 self.material_result_entrya,
                 self.tax_rate_entrya,
                 self.material_total_with_tax_entry,
                 self.labor_amount_entrya,
                 self.project_total_with_labor_entry,
                 files_folder=self.files_folder)

        self.scroll_layout1.addWidget(self.dbscsvpdf_app)
    # ----------------------
        # After CSV import click Save to DataBase
        self.after_import_csv()
    # ----------------------

# -----------------------------------
    def add_items_loop1(self):
# -----------------------------------

        global user_costa

        global num1
        self.num1 = 1

        text1 = "items"
        number = self.num1
        item = text1 + str(number)
        text2 = "user_itema"
        user_itema = text2 + str(number)

        text1 = "quantities"
        number = self.num1
        quantity = text1 + str(number)
        text2 = "user_quantitya"
        user_quantitya = text2 + str(number)

        text1 = "costs"
        number = self.num1
        cost = text1 + str(number)
        text2 = "user_costa"
        user_costa = text2 + str(number)

        # --------------------------------------------
        items_section = QWidget()
        items_layout = QGridLayout(items_section)
        items_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        # --------------------------------------------

#        items_layout.setContentsMargins(0, 10, 0, 0)

# -------------- 1ST GROUPBOX TO CONTAIN ITEMS -----------------

        itemsbox = QGroupBox("Items Needed For Project")
        itemsbox.setCheckable(True)
#        itemsbox.addWidget(row1_layout)
        
        for ig1 in range(10):

            # --------------------------------------------
            #row1_widget = QWidget()
            #row1_layout = QGridLayout(row1_widget)

            row1_widget = QGroupBox("Item Needed For Project")
            row1_layout = QHBoxLayout(row1_widget)

                    # Set custom font
            font = QFont("Calibri", 9)  # Change "Arial" to any font name you prefer, and 12 to desired size
            font.setBold(True)  # Optional: makes the font bold
            row1_widget.setFont(font)

            # --------------------------------------------

            #row_layout.setHorizontalSpacing(5)  # Only for Grid Layout
            #row_layout.setVerticalSpacing(50)  # Only for Grid Layout

            self.font = QFont("Calibri", 14)

            text1 = "items"
            number = self.num1
            item = text1 + str(number)
            text2 = "user_itema"
            user_itema = text2 + str(number)

            # Create widgets...
            item_label = QLabel("Item Needed:")
            user_itema = QTextEdit()
          
            item_label.setMinimumSize(125, 35)
            user_itema.setMinimumSize(180, 70)

            item_label.setFont(self.font)
            user_itema.setFont(self.font)
            item_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            user_itema.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            #user_itema.setContentsMargins(0, 0, 0, 0)

            text1 = "quantities"
            number = self.num1
            quantity = text1 + str(number)
            text2 = "user_quantitya"
            user_quantitya = text2 + str(number)

            quantity_label = QLabel("Quantity:")
            user_quantitya = QLineEdit()
            
            quantity_label.setMinimumSize(90, 35)
            user_quantitya.setMinimumSize(80, 35)
            user_quantitya.setStyleSheet("background-color: #F0F0F0;")
            quantity_label.setFont(self.font)
            user_quantitya.setFont(self.font)
            quantity_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            user_quantitya.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            #user_quantitya.setContentsMargins(0, 0, 0, 0)

            text1 = "costs"
            number = self.num1
            cost = text1 + str(number)
            text2 = "user_costa"
            user_costa = text2 + str(number)

            cost_label = QLabel("Cost:")
            user_costa = QLineEdit()

            # ------------------------------------------------------------
            # MAKE CONNECTION TO MATERIAL_RESULT_ENTYRA AUTOMATICALLY
            user_costa.textChanged.connect(self.update_material_total_box)
            # ------------------------------------------------------------

            cost_label.setMinimumSize(50, 35)
            user_costa.setMinimumSize(90, 35)
            user_costa.setStyleSheet("background-color: #F0F0F0;")
            cost_label.setFont(self.font)
            user_costa.setFont(self.font)
            cost_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            user_costa.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# --------------- STYLE THE BOXES WITH HIGHLIGHT ------------------

            items_layout.setContentsMargins(0, 10, 0, 0)

            user_itema.setStyleSheet("""
                QTextEdit {
                    color: black;
                    background-color: #F0F0F0;
                    border: 2px solid gray;
                    border-radius: 5px;
                    padding: 1px;
                }
                QTextEdit:focus {
                    background-color: #efdf94;  /* Highlight box color */
                    border: 2px solid black;
                }
            """)

            user_quantitya.setStyleSheet("""
                QLineEdit {
                    background-color: #F0F0F0;
                    border: 2px solid gray;
                    border-radius: 5px;
                    padding: 1px;

                }
                QLineEdit:focus {
                    background-color: #efdf94;
                    border: 2px solid black;
                }
            """)

            user_costa.setStyleSheet("""
                QLineEdit {
                    background-color: #F0F0F0;
                    border: 2px solid gray;
                    border-radius: 5px;
                    padding: 1px;

                }
                QLineEdit:focus {
                    background-color: #efdf94;
                    border: 2px solid black;
                }
            """)

# -----------------------------------------------------

            #user_costa.setContentsMargins(0, 0, 0, 0)

            # Add to row layout
            row1_layout.addWidget(item_label)#,0,0)
            row1_layout.addWidget(user_itema)#,0,1)
            row1_layout.addWidget(quantity_label)#,0,2)
            row1_layout.addWidget(user_quantitya)#,0,3)
            row1_layout.addWidget(cost_label)#,0,4)
            row1_layout.addWidget(user_costa)#,0,5)

# ---------------------------------------------------------------

            # QLineEdit: use .text()  # to get the text.
            # QTextEdit: use .toPlainText() # to get the text.

            global user_cost_floata

            text_value = user_costa.text()
            user_cost_float = float(text_value) if text_value.strip() else 0
            user_cost_floata = round(user_cost_float, 2)

            global user_quantity_floata

            text_value = user_quantitya.text()
            user_quantity_float = float(text_value) if text_value.strip() else 0
            user_quantity_floata = round(user_quantity_float, 2)

# ---------------------------------------------------------------

            # Store references in dictionary
            dict1_item[f"item{self.num1}"] = item
            dict1_user_item[f"user_itema{self.num1}"] = user_itema

            dict1_quantity[f"quantity{self.num1}"] = quantity
            dict1_user_quantity[f"user_quantitya{self.num1}"] = user_quantitya

            dict1_cost[f"cost{self.num1}"] = cost
            dict1_user_cost[f"user_costa{self.num1}"] = user_costa

            dict1_user_cost_float[f"user_cost_floata{user_cost_float}"] = user_cost_floata

            dict1_num1[self.num1] = self.num1

            self.num1 += 1

            # Add row to items layout
            items_layout.addWidget(row1_widget)

        #items_layout.addStretch()  # Optional for spacing
        self.scroll_layout1.addWidget(items_section)

        print(user_costa)
        print(user_cost_floata)
        print(user_quantitya)
        print(user_quantity_floata)

# ---------------------------------------------------------------

# -----------------------------------
    def update_material_total_box(self):
# -----------------------------------

        values = []
        for i in range(1, self.num1):
            key = f"user_costa{i}"
            widget = dict1_user_cost.get(key)
            if widget:
                try:
                    value = float(widget.text().strip()) if widget.text().strip() else 0
                except ValueError:
                    value = 0
                values.append(round(value, 2))
            else:
                values.append(0)

        self.material_total_floata = round(sum(values), 2)
        self.matrl_total_floata = round(sum(values), 2)

        print(f"Value of matrl_total_floata: '{self.matrl_total_floata}'")

        if hasattr(self, 'material_result_entrya'):
            formatted1 = ('{:.2f}'.format(self.material_total_floata)).rstrip('0').rstrip('.')
            self.material_result_entrya.setText(formatted1) # RETRIEVES AND SETS material_result_entrya FOR EACH COST BOX
            self.material_result_entrya.repaint()

            return self.matrl_total_floata

# ---------------------------------------------------------------

# -----------------------------------
    def update_total_with_tax_entry(self):
# -----------------------------------

        self.entry_value = self.tax_rate_entrya.text()
        self.tax_rate = round(float(self.entry_value), 2) / 100 if self.entry_value else 0

        self.tax_amounta = round(self.material_total_floata * self.tax_rate, 2)
        self.total_with_taxa = round(self.material_total_floata + self.tax_amounta, 2)

        formatted = ('{:.2f}'.format(self.total_with_taxa)).rstrip('0').rstrip('.')
        self.material_total_with_tax_entry.setText(formatted)
        self.material_total_with_tax_entry.repaint()

# ---------------------------------------------------------------

# -----------------------------------
    def update_total_with_labor_entry(self):
# -----------------------------------

        self.entry_value = self.labor_amount_entrya.text()
        self.labor_amounta = round(float(self.entry_value), 2) if self.entry_value else 0

        self.total_project_with_labora = round(self.total_with_taxa + self.labor_amounta, 2)

        formatted = ('{:.2f}'.format(self.total_project_with_labora)).rstrip('0').rstrip('.')
        self.project_total_with_labor_entry.setText(formatted)
        self.project_total_with_labor_entry.repaint()

# ---------------------------------------------------------------

# -----------------------------------
    def after_import_csv(self):
# -----------------------------------

        # Section: After importing CSV file
        csvimport = QWidget()

        # Grid layout
        csvimportl = QVBoxLayout(csvimport)
        csvimportl.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        csvimportl.setContentsMargins(240, 0, 0, 20)

        label_font = QFont("Calibri", 15)

        after_csv_import = QLabel("After Importing CSV file and making changes.\nClick the \"Save Inputs to Data Base\" Button again.")
        after_csv_import.setFont(label_font)
        after_csv_import.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
      
        after_csv_import.setContentsMargins(0, 0, 0, 0)

        csvimportl.addWidget(after_csv_import) #, 0, 0)
        self.scroll_layout1.addWidget(csvimport) # ONTO MAIN SCROLLING CONTAINER

# -----------------------------------
    def add_cost_tax_labor(self):
# -----------------------------------

        # --------------------------------------------
        self.cst_tx_lbr_section = QWidget()
        self.cst_tx_lbr_layout = QVBoxLayout(self.cst_tx_lbr_section)
        self.cst_tx_lbr_layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        # --------------------------------------------

        self.cst_tx_lbr_layout.setContentsMargins(300, 0, 0, 0)

# ------------------------------------------------

        self.setStyleSheet("""
                QLineEdit {
                    color: black;
                    background-color: #F0F0F0;
                    border: 2px solid gray;
                    border-radius: 5px;
                    padding: 1px;
                    QFont("Calibri", 14);
                }
            """)

# ------------------------------------------------

        # Set a custom stylesheet to add a border and styling
        self.setStyleSheet("""
            groupbox {
                color: black;
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 5px;
                margin-top: 10px; /* space above title */
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* align title */
                padding: 0 3px;
                font-weight: bold;
                font-size: 14px;
                color: black;
            }
        """)

# ------------------------------------------------
# -------------- 2ND GROUPBOX TO CONTAIN FINAL CALCULATION RESULTS -----------------

        groupbox = QGroupBox("Estimate Totals")
        groupbox.setCheckable(True)
        self.cst_tx_lbr_layout.addWidget(groupbox)
        
        # Set custom font
        font = QFont("Calibri", 12)  # Change "Arial" to any font name you prefer, and 12 to desired size
        font.setBold(True)  # Optional: makes the font bold
        groupbox.setFont(font)
# ------------------------------------------------

        # --------------------------------------------
        row2_widget = QWidget()
        row2_widget_layout = QGridLayout(groupbox)
        row2_widget_layout.setContentsMargins(0, 0, 0, 0)
        # --------------------------------------------

        self.font = QFont("Calibri", 14)

# ---------- MATERIAL COST SECTION -----------

        # Total calculation
        self.material_total_floata1 = 0  #self.matrl_total_floata  #round(sum(values), 2) # + item_cost11_float
        self.material_total_floata = round(self.material_total_floata1, 2)

        #print(f"Value of floata1: '{self.material_total_floata1}'")
        #print(f"Value of floata: '{self.material_total_floata}'")

        global material_result_entrya

        self.material_result_labela = QLabel("Material Cost:")
        self.material_result_labela.setMinimumSize(120, 35)
        self.material_result_labela.setFont(self.font)
        self.material_result_labela.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.material_result_entrya = QLineEdit()
        self.material_result_entrya.setMinimumSize(60, 35)
        self.material_result_entrya.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.material_result_entrya.setStyleSheet("background-color: #F0F0F0;")
        self.material_result_entrya.setFont(QFont("Calibri", 14))

        self.material_result_entrya.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
#            QLineEdit:focus {
#                background-color: #efdf94;
#                border: 2px solid black;
#                }
        """)

        self.material_result_labela.setContentsMargins(0, 0, 0, 0)
        self.material_result_entrya.setContentsMargins(0, 0, 0, 0)

        global material_floata

        # Store references in dictionary
        dict_floata[f"material_total_floata{self.num1}"] = self.material_total_floata
        print(f"Value of dict_floata: '{dict_floata}'")

        # Update QLineEdit result field
        #if self.material_result_entrya:
        #    formatted = ('{:.2f}'.format(material_total_floata1)).rstrip('0').rstrip('.')
        #    self.material_result_entrya.setText(formatted)
        #    self.material_result_entrya.repaint()  # optional for immediate UI update

        #print(self.material_result_entrya.text())

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.material_result_labela,0,0)
        row2_widget_layout.addWidget(self.material_result_entrya,0,1)

#        self.scroll_layout1.addWidget(cst_tx_lbr_section) # ONTO MAIN SCROLLING CONTAINER

# ---------- LOCAL TAX RATE SECTION -----------

        self.tax_rate_labela = QLabel("Local Tax Rate:")
        self.tax_rate_labela.setMinimumSize(100, 35)
        self.tax_rate_labela.setFont(self.font)
        self.tax_rate_labela.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.tax_rate_entrya = QLineEdit()
        self.tax_rate_entrya.setMinimumSize(20, 35)
        self.tax_rate_entrya.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.tax_rate_entrya.setStyleSheet("background-color: #F0F0F0;")
        self.tax_rate_entrya.setFont(QFont("Calibri", 14))
        
        self.tax_rate_entrya.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
                }
        """)

        self.tax_rate_labela.setContentsMargins(0, 0, 0, 0)
        self.tax_rate_entrya.setContentsMargins(0, 0, 0, 0)

        global tax_rate

        self.entry_value = self.tax_rate_entrya.text()
        self.tax_rate = round(float(self.entry_value), 2) / 100 if self.entry_value else 0

        # Store references in dictionary
        dict_tax_rate[f"tax_rate{self.num1}"] = self.tax_rate
        print(f"Value of tax_rate: '{self.tax_rate}'")

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.tax_rate_labela,1,0)
        row2_widget_layout.addWidget(self.tax_rate_entrya,1,1)

#        self.scroll_layout1.addWidget(cst_tx_lbr_section2) # ONTO MAIN SCROLLING CONTAINER

# ---------- MATERIAL COST WITH TAX INCLUDED -----------
       
        self.tax_amounta = round(self.material_total_floata * self.tax_rate, 2)
        self.total_with_taxa = round(self.material_total_floata + self.tax_amounta, 2)

        print(f"Value of total_with_taxa: '{dict_total_with_taxa}'")

        self.material_total_with_tax_label = QLabel("Total Material Cost With Tax:")
        self.material_total_with_tax_label.setMinimumSize(120, 35)
        self.material_total_with_tax_label.setFont(self.font)
        self.material_total_with_tax_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        print(f"Value of material_total_floata: '{self.material_total_floata}'")

        self.material_total_with_tax_entry = QLineEdit()
        self.material_total_with_tax_entry.setMinimumSize(60, 35)
        self.material_total_with_tax_entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.material_total_with_tax_entry.setStyleSheet("background-color: #F0F0F0;")
        self.material_total_with_tax_entry.setFont(QFont("Calibri", 14))

        self.material_total_with_tax_entry.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
#            QLineEdit:focus {
#                background-color: #efdf94;
#                border: 2px solid black;
#                }
        """)
      
        self.material_total_with_tax_label.setContentsMargins(0, 0, 0, 0)
        self.material_total_with_tax_entry.setContentsMargins(0, 0, 0, 0)
        
        # Optionally update the dictionaries
        dict_tax_amounta["dict_tax_amounta"] = self.tax_amounta
        dict_total_with_taxa["dict_total_with_taxa"] = self.total_with_taxa
        dict_tax_rate["dict_tax_rate"] = self.tax_rate

        self.tax_rate_entrya.textChanged.connect(self.update_total_with_tax_entry)

        # NEXT 3 LINES PUT A -0- INTO THE MATERIAL COST PLUS TAX BOX FROM "self.material_total_floata1 = 0"
        formatted = ('{:.2f}'.format(self.total_with_taxa)).rstrip('0').rstrip('.')
        self.material_total_with_tax_entry.setText(formatted)
        self.material_total_with_tax_entry.repaint()

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.material_total_with_tax_label,2,0)
        row2_widget_layout.addWidget(self.material_total_with_tax_entry,2,1)

#        self.scroll_layout1.addWidget(cst_tx_lbr_section) # ONTO MAIN SCROLLING CONTAINER

# ---------- LABOR COST -----------

        self.labor_amount_labela = QLabel("Labor Cost:")
        self.labor_amount_labela.setMinimumSize(100, 35)
        self.labor_amount_labela.setFont(self.font)
        self.labor_amount_labela.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.labor_amount_entrya = QLineEdit()
        self.labor_amount_entrya.setMinimumSize(20, 35)
        self.labor_amount_entrya.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.labor_amount_entrya.setStyleSheet("background-color: #F0F0F0;")
        self.labor_amount_entrya.setFont(QFont("Calibri", 14))

        self.labor_amount_entrya.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
                }
        """)
        
        self.labor_amount_labela.setContentsMargins(0, 0, 0, 0)
        self.labor_amount_entrya.setContentsMargins(0, 0, 0, 0)

        global labor_amounta

        self.entry_value = self.labor_amount_entrya.text()
        self.labor_amounta = round(float(self.entry_value), 2) if self.entry_value else 0

        # Store references in dictionary
        dict_labor_amounta[f"dict_labor_amounta{self.num1}"] = self.labor_amount_entrya
        print(f"Value of dict_labor_amounta: '{self.labor_amount_entrya}'")

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.labor_amount_labela,3,0)
        row2_widget_layout.addWidget(self.labor_amount_entrya,3,1)

# ---------- TOTAL COST OF PROJECT -----------
       
        #self.project_amounta = round(self.material_total_with_tax_entry + self.labor_amounta, 2)
        self.total_project_with_labora = round(self.total_with_taxa + self.labor_amounta, 2)

        print(f"Value of total_with_labora: '{dict_total_with_labora}'")

        self.project_total_with_labor_label = QLabel("Total Cost of Project:")
        self.project_total_with_labor_label.setMinimumSize(120, 35)
        self.project_total_with_labor_label.setFont(self.font)
        self.project_total_with_labor_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        print(f"Total Cost of total_project_with_labora: '{self.total_project_with_labora}'")

        self.project_total_with_labor_entry = QLineEdit()
        self.project_total_with_labor_entry.setMinimumSize(60, 35)
        self.project_total_with_labor_entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.project_total_with_labor_entry.setStyleSheet("background-color: #F0F0F0;")
        self.project_total_with_labor_entry.setFont(QFont("Calibri", 14))

        self.project_total_with_labor_entry.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
#            QLineEdit:focus {
#                background-color: #efdf94;
#                border: 2px solid black;
#                }
        """)
      
        self.project_total_with_labor_label.setContentsMargins(0, 0, 0, 0)
        self.project_total_with_labor_entry.setContentsMargins(0, 0, 0, 0)
        
        # Optionally update the dictionaries
        dict_labora["dict_labora"] = self.labor_amounta
        dict_total_with_labora["dict_total_with_labora"] = self.total_project_with_labora

        self.labor_amount_entrya.textChanged.connect(self.update_total_with_labor_entry)

        # NEXT 3 LINES PUT A -0- INTO THE PROJECT COST BOX FROM "self.project_total_floata1 = 0"
        formatted = ('{:.2f}'.format(self.total_project_with_labora)).rstrip('0').rstrip('.')
        self.project_total_with_labor_entry.setText(formatted)
        self.project_total_with_labor_entry.repaint()

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.project_total_with_labor_label,4,0)
        row2_widget_layout.addWidget(self.project_total_with_labor_entry,4,1)

#        self.scroll_layout1.addWidget(cst_tx_lbr_section) # ONTO MAIN SCROLLING CONTAINER

# ---------- ESTIMATE PREPARED BY -----------

        self.prepared_estimate_labela = QLabel("Job Estimate Prepared By:")
        self.prepared_estimate_labela.setMinimumSize(100, 35)
        self.prepared_estimate_labela.setFont(self.font)
        self.prepared_estimate_labela.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.prepared_estimate_entrya = QLineEdit()
        self.prepared_estimate_entrya.setMinimumSize(150, 35)
        self.prepared_estimate_entrya.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.prepared_estimate_entrya.setStyleSheet("background-color: #F0F0F0;")
        self.prepared_estimate_entrya.setFont(QFont("Calibri", 14))

        self.prepared_estimate_entrya.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QLineEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
                }
        """)
        
        self.prepared_estimate_labela.setContentsMargins(0, 0, 0, 0)
        self.prepared_estimate_entrya.setContentsMargins(0, 0, 0, 0)

        self.entry_value = self.prepared_estimate_entrya.text()

        # Store references in dictionary
        dict_prepared_estimate[f"dict_prepared_estimate{self.num1}"] = self.prepared_estimate_entrya
        print(f"Name of dict_prepared_estimate: '{self.prepared_estimate_entrya}'")

        self.cst_tx_lbr_layout.addWidget(row2_widget)
        row2_widget_layout.addWidget(self.prepared_estimate_labela,5,0)
        row2_widget_layout.addWidget(self.prepared_estimate_entrya,5,1)

        self.scroll_layout1.addWidget(self.cst_tx_lbr_section) # ONTO MAIN SCROLLING CONTAINER

        return self.cst_tx_lbr_section

# ------------------------------------------------------------------------------------------

        self.dbscsvpdf_app = Savedbs_csv_pdf(
            cust_name_input=self.cust_name_input,
            cust_phone_input=self.cust_phone_input,
            address_input=self.address_input,
            date_input=self.date_input,
            email_input=self.email_input,
            job_input=self.job_input,
            prepared_by_input=self.prepared_estimate_entrya,
            material_cost_entry=self.material_result_entrya,
            tax_rate_entry=self.tax_rate_entrya,
            material_tax_entry=self.material_total_with_tax_entry,
            labor_cost_entry=self.labor_amount_entrya,
            project_total_entry=self.project_total_with_labor_entry,
            files_folder=self.files_folder
        )
        self.scroll_layout1.addWidget(self.dbscsvpdf_app)

# ------------------------------------------------------------------------------------------

class ClickableLabel(QLabel):  # ALLOWS LABELS TO BE CLICKABLE
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

# ------------------------------------------------------------------------------------------

class PhotoCaptureApp(QWidget):

#    def __init__(self):
#        super().__init__()

    def __init__(self,files_folder):

        # The super().__init__() calls the constructor of the QWidget parent class — required for proper initialization.

        super().__init__()

        # Save the references
        self.files_folder = files_folder

# ----------------------------------------------------

        self.image_labels = {}     # Dictionary for QLabel references
        self.text_boxes = {}       # Dictionary for QTextEdit references
        self.photo_files = {}      # Dictionary for Stored filenames

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

# ----------------------------------------------------

        self.layoutphotos = QGridLayout()  # PREVIOUSLY WAS HBoxlayout
        self.layoutphotos.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layoutphotos.setContentsMargins(0, 0, 0, 20)
        self.main_layout.addLayout(self.layoutphotos)

        self.gridphotos = QGridLayout()
        self.layoutphotos.addLayout(self.gridphotos,1,0)

# ----------------------------------------------------

        # LABEL CODE TO ANNOUNCE CLICKING ON PHOTOS TO ENLARGE

        self.layoutlabel = QGridLayout()
        self.layoutlabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layoutlabel.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.layoutlabel)
              
        self.enlarge_photo_label = QLabel("Click on Photo to Enlarge") # Click photo to Enlarge
        self.layoutphotos.addWidget(self.enlarge_photo_label,0,0)

        # Set font and style
        self.font = QFont("Calibri", 12)
        self.font.setBold(True)
        self.enlarge_photo_label.setFont(self.font)

        # Optional margins
        self.enlarge_photo_label.setContentsMargins(270, 0, 0, 0)
        self.enlarge_photo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

# ----------------------------------------------------

        # Add 3 rows of 4 photo boxes (total 12)
        photo_num = 1

        for row in range(3):
            for col in range(4):
                self.add_photo_box(photo_num, row, col)
                photo_num += 1

# --------------------- BUTTON CALL -----------------        
        # Add Import All Photos button underneath
        self.main_layout.addLayout(self.import_photos_btn())
# --------------------- BUTTON CALL -----------------        

# -----------------------------------------------

    def import_photos_btn(self):

        layout100 = QHBoxLayout()
        layout100.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout100.setContentsMargins(275, 10, 0, 0)

        import_button = QPushButton("Import All Photos")
        import_button.setStyleSheet("""
            QPushButton {
                background-color: #d6dbdf;
                border: 2px solid #154360;
                border-radius: 5px;
                color: black;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        import_button.setFont(QFont("Calibri", 12))
        import_button.setFixedSize(200, 40)
        import_button.clicked.connect(self.import_all_photos)

        layout100.addWidget(import_button)

        # Hide the import button after clicking
#        import_button.clicked.connect(lambda: [self.import_all_photos(), import_button.hide()])
#        import_button.clicked.connect(lambda: [self.import_all_photos()])

        return layout100 # ADDING LAYOUT FOR BUTTON WITHIN "PhotoCaptureApp" CLASS

        import_photos_btn(self)

# -----------------------------------------------

    def add_photo_box(self, nump, row, col):

        # Image Label
        #label = QLabel("Image Here")

        label = ClickableLabel("Image Here")   # LABEL THAT USES THE CLICKABLE FUNCTION
        label.setFixedSize(173, 140)
        label.setStyleSheet("background-color: #a9dfbf; border: 2px solid black;")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Calibri", 12))

        label.clicked.connect(lambda n=nump: self.show_enlarged_photo(n))

        # Text Box
        text_box = QTextEdit()

        text_box.setStyleSheet("""
            QTextEdit {
                background-color: #F0F0F0;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px;

            }
            QTextEdit:focus {
                background-color: #efdf94;
                border: 2px solid black;
                }
        """)

        #text_box.setMinimumSize(173, 50)
        text_box.setFixedSize(173, 50)
        text_box.setAlignment(Qt.AlignLeft)
        text_box.setFont(QFont("Calibri", 12))

        # Capture Button
        btn = QPushButton(f"Take Photo {nump}")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                border: 2px solid #006400;
                border-radius: 5px;
                color: black;
            }
            QPushButton:hover {
                background-color: #76c776;
            }
        """)
        btn.setFont(QFont("Calibri", 12))
        btn.setFixedSize(173, 50)
        #btn.setMinimumSize(180, 50)
        btn.clicked.connect(lambda checked, n=nump: self.capture_from_webcam(n))

        # Store references
        self.image_labels[nump] = label
        self.text_boxes[nump] = text_box

        # Add widgets to vertical layout
        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 20, 0, 0)

        vbox.addWidget(label)
        vbox.addWidget(text_box)
        vbox.addWidget(btn)
     
        self.gridphotos.addLayout(vbox, row, col)

# -----------------------------------------------

    def capture_from_webcam(self, nump):

        # Get the current working directory
        working_folder = files_folder   #os.getcwd()

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open webcam")
            return

        print(f"Capturing for photo {nump}... Press 'c' to capture, 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame")
                break

            cv2.imshow('Press "c" to capture, "q" to quit', frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                filename = f"Photo_{nump}.jpg"

                # Save the image in prescribed folder
                save_path = os.path.join(working_folder, filename)
                # Save the image
                cv2.imwrite(save_path, frame)

                self.photo_files[nump] = save_path
                print(f"Saved: {save_path}")
                self.update_image_label(nump, frame)
                break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# -----------------------------------------------

    def update_image_label(self, nump, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb_frame, (233, 200))

        h, w, ch = resized.shape
        bytes_per_line = ch * w
        qt_image = QImage(resized.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        self.image_labels[nump].setPixmap(pixmap)
        self.image_labels[nump].setScaledContents(True)

# -----------------------------------------------

    def show_enlarged_photo(self, nump):
        if nump not in self.photo_files:
            print(f"No photo found for {nump}")
            return

        photo_path = self.photo_files[nump]
        if not os.path.exists(photo_path):
            print(f"File does not exist: {photo_path}")
            return

        # Load image
        img = QPixmap(photo_path)
        img = img.scaled(500, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Create popup window
        popup = QDialog(self)
        popup.setWindowTitle(f"Photo {nump}")
        popup.setFixedSize(500, 450)
        popup.setWindowModality(Qt.ApplicationModal)
        popup.setStyleSheet("background-color: white;")

        # Center the popup on screen
        qr = popup.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        popup.move(qr.topLeft())

        # Layout and label
        vbox = QVBoxLayout(popup)
        label = QLabel()
        label.setPixmap(img)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

        popup.exec_()

# -----------------------------------------------

    def import_all_photos(self):

        for nump in range(1, 13):  # 1 to 12
            photo_path = os.path.join(self.files_folder, f"Photo_{nump}.jpg")
            if os.path.exists(photo_path):
                frame = cv2.imread(photo_path)
                if frame is not None:
                    self.photo_files[nump] = photo_path
                    self.update_image_label(nump, frame)
                    print(f"Imported Photo_{nump}.jpg")
                else:
                    print(f"Failed to load: {photo_path}")
            else:
                print(f"Photo_{nump}.jpg not found.")

# ------------------------------------------------------------------------------------------

class Savedbs_csv_pdf(QWidget):

    def __init__(self,
                 cust_name_input,
                 cust_phone_input,
                 address_input,
                 date_input,
                 email_input,
                 job_input,
#                 prepared_by_input,
                 prepared_estimate_entrya,
                 material_cost_entry,
                 tax_rate_entry,
                 material_tax_entry,
                 labor_cost_entry,
                 project_total_entry,
                 files_folder):

        # The super().__init__() calls the constructor of the QWidget parent class — required for proper initialization.

        super().__init__()

        # Save the references
        self.cust_name_input = cust_name_input
        self.cust_phone_input = cust_phone_input
        self.address_input = address_input
        self.date_input = date_input
        self.email_input = email_input
        self.job_input = job_input
        self.prepared_estimate_entrya = prepared_estimate_entrya
#        self.prepared_by_input = prepared_by_input
        self.material_result_entrya = material_cost_entry
        self.tax_rate_entrya = tax_rate_entry
        self.material_total_with_tax_entry = material_tax_entry
        self.labor_amount_entrya = labor_cost_entry
        self.project_total_with_labor_entry = project_total_entry
        self.files_folder = files_folder

            #prepared_by_input=self.prepared_estimate_entrya,
            #material_cost_entry=self.material_result_entrya,
            #tax_rate_entry=self.tax_rate_entrya,
            #material_tax_entry=self.material_total_with_tax_entry,
            #labor_cost_entry=self.labor_amount_entrya,
            #project_total_entry=self.project_total_with_labor_entry

        # UI setup continues here...

# -------------------------------------------------------

#        self.files_folder = files_folder  # Accept as parameter

        self.main_layout1 = QHBoxLayout()
        self.setLayout(self.main_layout1)
        self.main_layout1.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.main_layout1.setContentsMargins(20, 10, 0, 0)
        #self.main_layout.addLayout(self.gridcsv, 1, 0)

        #self.main_layout2 = QHBoxLayout()
        #self.setLayout(self.main_layout2)
        #self.main_layout2.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        #self.main_layout2.setContentsMargins(0, 0, 0, 0)
        #self.main_layout.addLayout(self.gridcsv, 1, 0)

# -------------------------------------------------------------------

        # --------------------- BUTTON CALL -----------------        
        # Save DBS Button
        self.main_layout1.addWidget(self.save_dbs_btn())  #,0,1)
        # --------------------- BUTTON CALL -----------------        

    def save_dbs_btn(self):

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        export_button = QPushButton("Save Inputs to Data Base")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #d6dbdf;
                border: 2px solid #154360;
                border-radius: 5px;
                color: black;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        export_button.setFont(QFont("Calibri", 12))
        export_button.setFixedSize(230, 40)
        export_button.clicked.connect(self.save_to_dbs)

        layout.addWidget(export_button)
        self.main_layout1.addWidget(export_button)
        #return layout

        # --------------------- BUTTON CALL -----------------        
        # Export CSV Button
        self.main_layout1.addWidget(self.export_csv_btn())  #,0,2)
        # --------------------- BUTTON CALL -----------------        

    def export_csv_btn(self):

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        export_button = QPushButton("Export Data to CSV File")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #d6dbdf;
                border: 2px solid #154360;
                border-radius: 5px;
                color: black;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        export_button.setFont(QFont("Calibri", 12))
        export_button.setFixedSize(230, 40)
        export_button.clicked.connect(self.export_to_csv)

        layout.addWidget(export_button)
        self.main_layout1.addWidget(export_button)
        #return layout

        # --------------------- BUTTON CALL -----------------        
        # Export PDF Button
        self.main_layout1.addWidget(self.export_pdf_btn())  #,0,2)
        # --------------------- BUTTON CALL -----------------        

    def export_pdf_btn(self):

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        export_button = QPushButton("Export Data to PDF File")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #d6dbdf;
                border: 2px solid #154360;
                border-radius: 5px;
                color: black;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        export_button.setFont(QFont("Calibri", 12))
        export_button.setFixedSize(230, 40)
        export_button.clicked.connect(self.export_to_pdf)

        layout.addWidget(export_button)
        self.main_layout1.addWidget(export_button)
        #return layout

        # --------------------- BUTTON CALL -----------------        
        # Import all Data Back Into Form Boxes
        self.main_layout1.addWidget(self.import_csv_btn())
        # --------------------- BUTTON CALL -----------------        

    def import_csv_btn(self):

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        import_button = QPushButton("Import CSV Data to Form")
        import_button.setStyleSheet("""
            QPushButton {
                background-color: #d6dbdf;
                border: 2px solid #154360;
                border-radius: 5px;
                color: black;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        import_button.setFont(QFont("Calibri", 12))
        import_button.setFixedSize(230, 40)
        import_button.clicked.connect(self.import_from_csv)

        layout.addWidget(import_button)
        self.main_layout1.addWidget(import_button)

        #return import_button

# ---------------------------------------------------------------------------------

# -------------------------------------------------------------------
# ----------------- DATA BASE INPUTS ------------------
# -------------------------------------------------------------------

    def save_to_dbs(self):

#        delete_job_estimate(self)

        db_path = os.path.join(self.files_folder, 'job_estimate.db')
        backup_path = os.path.join(self.files_folder, 'job_estimate_backup.db')

        # Backup and delete existing database
        if os.path.exists(db_path):
            try:
                # Step 1: Backup the database
                shutil.copy2(db_path, backup_path)

                # Step 2: Delete the original database
                os.remove(db_path)

                #messagebox.showinfo("Success", "Database deleted and backup saved.")
            except Exception as e:
                #messagebox.showerror("Error", f"An error occurred: {str(e)}")
                print(f"Error during backup/delete: {e}")
                return  # Stop if there was an error
        else:
            messagebox.showerror("Error", "Database file not found.")
            print("Database file not found.")
            return  # Stop if DB doesn't exist

# --------------------------------------------------

        # --- Collect customer info ---
        name = self.cust_name_input.text()
        phone = self.cust_phone_input.text()
        address = self.address_input.toPlainText()
        date = self.date_input.text()
        email = self.email_input.text()
        job_description = self.job_input.toPlainText()
        prepared_by = self.prepared_estimate_entrya.text()  #self.prepared_by_input.text()

        # ✅ Create full path to the database inside the selected folder
        self.db_path = os.path.join(self.files_folder, "job_estimate.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                address TEXT,
                date TEXT,
                email TEXT,
                job_description TEXT,
                prepared_by TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                item TEXT,
                quantity REAL,
                cost REAL,
                material_cost REAL,
                tax_rate REAL,
                material_with_tax REAL,
                labor_cost REAL,
                project_total REAL,
                FOREIGN KEY (customer_id) REFERENCES customer_info(id)
            )
        """)

        # --- Insert customer info ---
        cursor.execute("""
            INSERT INTO customer_info (name, phone, address, date, email, job_description, prepared_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, address, date, email, job_description, prepared_by))

        customer_id = cursor.lastrowid

        # --- Get shared values ---
        material_cost = float(self.material_result_entrya.text() or 0)
        tax_rate = float(self.tax_rate_entrya.text() or 0)
        material_with_tax = float(self.material_total_with_tax_entry.text() or 0)
        labor_cost = float(self.labor_amount_entrya.text() or 0)
        project_total = float(self.project_total_with_labor_entry.text() or 0)

        # --- Insert items ---
        for key in dict1_user_item:
            item_text = dict1_user_item[key].toPlainText()

            quantity_key = key.replace("user_itema", "user_quantitya")
            cost_key = key.replace("user_itema", "user_costa")

            quantity_val = dict1_user_quantity[quantity_key].text()
            cost_val = dict1_user_cost[cost_key].text()

            try:
                quantity = float(quantity_val) if quantity_val.strip() else 0
            except:
                quantity = 0.0

            try:
                cost = float(cost_val) if cost_val.strip() else 0
            except:
                cost = 0.0

            cursor.execute("""
                INSERT INTO items (
                    customer_id, item, quantity, cost
                )
                VALUES (?, ?, ?, ?)
            """, (
                customer_id, item_text, quantity, cost
            ))


        cursor.execute("""
            INSERT INTO items (
                customer_id, 
                material_cost, tax_rate, material_with_tax,
                labor_cost, project_total
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id, 
            material_cost, tax_rate, material_with_tax,
            labor_cost, project_total
        ))

        # THE ABOVE INPUT NAMES ARE A TUPLE LIST AFTER CLOSING THE INSERT LIST WITH """, 

        conn.commit()
        conn.close()

        print("Saved to database.")

# ------------------------------------------------------------------------------------------

#        save_button = QPushButton("Save to Database")
#        save_button.clicked.connect(self.save_to_db)
#        self.scroll_layout1.addWidget(save_button)

# ------------------------------------------------------------------------------------------

    def export_to_csv(self, file_name="job_estimate.csv"):

        Csv_File = os.path.join(self.files_folder, "job_estimate.csv")
        self.db_path = os.path.join(self.files_folder, "job_estimate.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.name, c.phone, c.address, c.date, c.email,
                   c.job_description, c.prepared_by,
                   i.item, i.quantity, i.cost,
                   i.material_cost, i.tax_rate, i.material_with_tax,
                   i.labor_cost, i.project_total
            FROM customer_info c
            JOIN items i ON c.id = i.customer_id
        """)

        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

#        with open(Csv_File, mode='w', newline='', encoding='utf-8') as file:
#            writer = csv.writer(file)

        with open(Csv_File, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        conn.close()
        print(f"Exported to CSV at {file_name}")

# ------------------------------------------------------------------------------------------

#        export_csv_btn = QPushButton("Export to CSV")
#        export_csv_btn.clicked.connect(lambda: self.export_to_csv())
#        self.scroll_layout1.addWidget(export_csv_btn)

# ------------------------------------------------------------------------------------------

    def export_to_pdf(self, file_name="job_estimate.pdf"):

        # Define paths
        Pdf_File = os.path.join(self.files_folder, "job_estimate.pdf")
        self.db_path = os.path.join(self.files_folder, "job_estimate.db")

        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the latest customer
        cursor.execute("SELECT * FROM customer_info ORDER BY id DESC LIMIT 1")
        customer = cursor.fetchone()

        if not customer:
            print("No customer data found.")
            return

        customer_id = cursor.execute("SELECT id FROM customer_info ORDER BY id DESC LIMIT 1").fetchone()[0]

        # Get all items for that customer
        cursor.execute("""
            SELECT item, quantity, cost, material_cost, tax_rate, material_with_tax, labor_cost, project_total
            FROM items
            WHERE customer_id = ?
        """, (customer_id,))
        items = cursor.fetchall()

        conn.close()

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Company Header
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 5, 'Beaufort Construction', 0, 1, 'C')
        pdf.set_font('Arial', size=12)
        pdf.cell(0, 8, 'Address: 1234 Anywhere Dr', 0, 1, 'L')
        pdf.cell(0, 5, 'Your City SC 56678', 0, 1, 'L')
        pdf.cell(0, -8, 'Phone: (800) 555-1212', 0, 20, 'C')
        pdf.ln(10)
        
        # Customer Info
        labels = ["Estimate Num", "Name", "Phone", "Address", "Date", "Email", "Job Description", "Prepared By"]
        for i in range(7):
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 8, f"{labels[i]}:", 0, 0)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, str(customer[i]), 0, 1)

        pdf.ln(5)

        # Items Header
        pdf.set_font("Arial", "B", 10)
        item_headers = ["Item Needed", "Qty", "Unit Cost", "Material", "Tax %", "Mat+Tax", "Labor", " Project Total"]
        col_widths = [30, 15, 20, 25, 15, 25, 20, 25]

        for i, header in enumerate(item_headers):
            pdf.cell(col_widths[i], 8, header, 1, 0, 'C')
        pdf.ln()

        # Item Rows and Totals
        pdf.set_font("Arial", "", 10)
        total_material = 0
        total_material_tax = 0
        total_labor = 0
        total_project = 0

        # Item Rows
        pdf.set_font("Arial", "", 10)
        last_item = None  # track last item

        for idx, item in enumerate(items):
            last_item = item  # keep the last item for totals
            for i, value in enumerate(item):
                # On the final row, make values empty except for tax rate
                if idx == len(items) - 1:
                    if i == 4:  # Tax rate column
                        cell_value = str(value)
                    else:
                        cell_value = ""
                else:
                    cell_value = str(value)

                pdf.cell(col_widths[i], 8, cell_value, 1, 0, 'C')
            pdf.ln()

        # Summary Line using last item
        if last_item:
            pdf.ln(2)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(sum(col_widths[:3]), 8, "TOTALS", 1, 0, 'R')
            pdf.set_font("Arial", "", 10)
            pdf.cell(col_widths[3], 8, f"{float(last_item[3]):.2f}", 1, 0, 'C')  # Material
            pdf.cell(col_widths[4], 8, f"{float(last_item[4]):.2f}", 1, 0, 'C')  # Tax rate
            pdf.cell(col_widths[5], 8, f"{float(last_item[5]):.2f}", 1, 0, 'C')  # Material + Tax
            pdf.cell(col_widths[6], 8, f"{float(last_item[6]):.2f}", 1, 0, 'C')  # Labor
            pdf.cell(col_widths[7], 8, f"{float(last_item[7]):.2f}", 1, 1, 'C')  # Total

        # Save PDF
        pdf.output(Pdf_File)
        print(f"PDF exported to: {Pdf_File}")

# ------------------------------------------------------------------------------------------

    def import_from_csv(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            self.files_folder or os.getcwd(),
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data_rows = list(reader)
            
            #print(data_rows)

            if not data_rows:
                print("CSV file is empty.")
                return

            # Use the first row for customer info
            first_row = data_rows[0]

            self.cust_name_input.setText(first_row['name'])
            self.cust_phone_input.setText(first_row['phone'])
            self.address_input.setText(first_row['address'])
            self.date_input.setText(first_row['date'])
            self.email_input.setText(first_row['email'])
            self.job_input.setText(first_row['job_description'])
            self.prepared_estimate_entrya.setText(first_row['prepared_by'])

            self.material_result_entrya.setText(first_row['material_cost'])
            self.tax_rate_entrya.setText(first_row['tax_rate'])
            self.material_total_with_tax_entry.setText(first_row['material_with_tax'])
            self.labor_amount_entrya.setText(first_row['labor_cost'])
            self.project_total_with_labor_entry.setText(first_row['project_total'])

            # Now clear and repopulate item fields
            for i, row in enumerate(data_rows):
                item_key = f"user_itema{i+1}"
                quantity_key = f"user_quantitya{i+1}"
                cost_key = f"user_costa{i+1}"

                if item_key in dict1_user_item:
                    dict1_user_item[item_key].setPlainText(row['item'])
                if quantity_key in dict1_user_quantity:
                    dict1_user_quantity[quantity_key].setText(row['quantity'])
                if cost_key in dict1_user_cost:
                    dict1_user_cost[cost_key].setText(row['cost'])

            print("Data imported from CSV.")

# ------------------------------------------------------------------------------------------

    def delete_job_estimate(self):

        db_path = os.path.join(self.files_folder, 'job_estimate.db')
        backup_path = os.path.join(self.files_folder, 'job_estimate_backup.db')

        # Backup and delete existing database
        if os.path.exists(db_path):
            try:
                # Step 1: Backup the database
                shutil.copy2(db_path, backup_path)

                # Step 2: Delete the original database
                os.remove(db_path)

                messagebox.showinfo("Success", "Database deleted and backup saved.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                print(f"Error during backup/delete: {e}")
                return  # Stop if there was an error
        else:
            messagebox.showerror("Error", "Database file not found.")
            print("Database file not found.")
            return  # Stop if DB doesn't exist

# ------------------------------------------------------------------------------------------

        # Function to delete the job_estimate.db database
    def ddelete_job_estimate():
        if os.path.exists('job_estimate.db'):
            os.remove('job_estimate.db')
            #messagebox.showinfo("Success", "Database deleted successfully!")
        else:
            #messagebox.showerror("Error", "Database file not found.")
            return

    # Function to delete the csv short form file
    def ddelete_csv():
        if os.path.exists('job_estimate.csv'):
            os.remove('job_estimate.csv')
            #messagebox.showinfo("Success", "Database deleted successfully!")
        else:
            #messagebox.showerror("Error", "Database file not found.")
            return

# ------------------------------------------------------------------------------------------

class FilesFolder(QWidget):
    def __init__(self):
        super().__init__()

        # Step 1: Ask the user to select a base folder
        selected_folder = filedialog.askdirectory(
            title="Select Folder to save All Estimating Files",
            initialdir=os.getcwd()
        )

        if not selected_folder:
            raise ValueError("Folder selection was cancelled. Please choose a folder.")

        self.files_folder = str(selected_folder)  # ✅ Make sure it's a string
        print(f"This is the files_folder Chosen: '{self.files_folder}'")

# ------------------------------------------------------------------------------------------

class FolderSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Estimating Files Folder")
        self.initUI()

    def initUI(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to save All Estimating Files",
            os.getcwd(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if folder:
            global files_folder
            self.files_folder = folder
            print("Selected folder:", files_folder)

        self.close()  # Close the folder dialog window

# ------------------------------------------------------------------------------------------

# Run the application
if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

