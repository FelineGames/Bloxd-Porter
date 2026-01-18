from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QFont, QColor, QPalette
from config import *
from logic import load_mapping, process_files
import os

class PNGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Generic Textures")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_dark_theme()

        # Variables
        self.source_path = ""
        self.output_path = ""
        self.mapping_path = ""
        self.mode = "Default"

        # UI setup
        self.init_ui()

    def set_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#171D25"))  # window background
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))  # text color
        self.setPalette(palette)

    def init_ui(self):
        font_label = QFont("Arial", 10)
        font_input = QFont("Arial", 10)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # ---- Source ----
        self.source_input, self.source_btn = self.create_input_row("Source", self.browse_source)
        main_layout.addLayout(self.source_input)

        # ---- Output ----
        self.output_input, self.output_btn = self.create_input_row("Output", self.browse_output)
        main_layout.addLayout(self.output_input)

        # ---- Mapping ----
        self.mapping_input, self.map_btn = self.create_input_row("Mapping", self.browse_mapping, enabled=False)
        main_layout.addLayout(self.mapping_input)

        # ---- Mode dropdown ----
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode")
        mode_label.setFont(font_label)
        mode_label.setStyleSheet("color: #FFFFFF;")
        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems(["Default", "Custom"])
        self.mode_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #1F2F50;
                color: #FFFFFF;
            }
            QComboBox::drop-down {
                border: 0px;
            }
        """)
        self.mode_dropdown.currentTextChanged.connect(self.on_mode_change)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_dropdown)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # ---- Bottom buttons ----
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setFixedWidth(150)
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setStyleSheet("""
            background-color: #1F2F50;
            color: #FFFFFF;
        """)

        self.start_btn = QPushButton("Start Process")
        self.start_btn.setFixedWidth(150)
        self.start_btn.clicked.connect(self.start_process)
        self.start_btn.setStyleSheet("""
            background-color: #1F2F50;
            color: #FFFFFF;
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch(1)  # push Start Process to right
        btn_layout.addWidget(self.start_btn)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ---------------- Helper ----------------
    def create_input_row(self, label_text, browse_func, enabled=True):
        font_label = QFont("Arial", 10)
        font_input = QFont("Arial", 10)
        layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setFont(font_label)
        label.setStyleSheet("color: #FFFFFF;")

        input_field = QLineEdit()
        input_field.setFrame(False)
        input_field.setFont(font_input)
        input_field.setStyleSheet("""
            background-color: #1F2F50;
            color: #FFFFFF;
        """)
        input_field.setReadOnly(True)

        btn = QPushButton("Browse Folder")
        btn.setFont(font_input)
        btn.clicked.connect(browse_func)
        btn.setStyleSheet("""
    QPushButton {
        background-color: #1F2F50;
        color: #FFFFFF;
    }
    QPushButton:disabled {
        background-color: #162333;
        color: #474747;
    }
""")
        btn.setEnabled(enabled)

        layout.addWidget(label)
        layout.addWidget(input_field)
        layout.addWidget(btn)
        return layout, btn

    # ---------------- Logic -----------------
    def on_mode_change(self, value):
        if value == "Custom":
            self.map_btn.setEnabled(True)
            self.map_btn.setStyleSheet("""
                background-color: #1F2F50;
                color: #FFFFFF;
            """)
        else:
            self.map_btn.setEnabled(False)
            self.map_btn.setStyleSheet("""
                background-color: #1F2F50;
                color: #AAAAAA;
            """)
            self.mapping_path = ""
            self.mapping_input.itemAt(1).widget().setText("")

    def browse_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_path = folder
            self.source_input.itemAt(1).widget().setText(folder)

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path = folder
            self.output_input.itemAt(1).widget().setText(folder)

    def browse_mapping(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Mapping Folder")
        if folder and os.path.exists(os.path.join(folder, MAPPING_FILENAME)):
            self.mapping_path = folder
            self.mapping_input.itemAt(1).widget().setText(folder)
        else:
            QMessageBox.critical(self, "Error", f"{MAPPING_FILENAME} not found in this folder.")

    def clear_all(self):
        self.source_path = ""
        self.output_path = ""
        self.mapping_path = ""
        self.mode_dropdown.setCurrentText("Default")
        for layout in [self.source_input, self.output_input, self.mapping_input]:
            layout.itemAt(1).widget().setText("")

    def start_process(self):
        if not self.source_path:
            QMessageBox.critical(self, "Error", "Source folder is required")
            return
        if not self.output_path:
            QMessageBox.critical(self, "Error", "Output folder is required")
            return

        mapping_folder = self.mapping_path if self.mode_dropdown.currentText() == "Custom" else os.path.dirname(os.path.abspath(__file__))
        rules = load_mapping(mapping_folder)
        if not rules:
            QMessageBox.critical(self, "Error", f"{MAPPING_FILENAME} could not be loaded")
            return

        count = process_files(self.source_path, self.output_path, rules)
        if count == 0:
            QMessageBox.warning(self, "Finished", "No files matched whitelist.txt")
        else:
            QMessageBox.information(self, "Success", f"{count} files processed successfully.")
