from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
)
from qtpy.QtCore import Qt
import requests
import re
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.config import BACKEND_URL

class OLTConfiguration(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === OLT Connection Block ===
        olt_connection_group = QGroupBox("OLT Connection")
        olt_connection_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_layout = QVBoxLayout()

        # Input Fields for OLT Connection
        self.ip_input = QLineEdit(placeholderText="IP Address")
        self.user_input = QLineEdit(placeholderText="User")
        self.password_input = QLineEdit(placeholderText="Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input

        olt_layout.addWidget(self.ip_input)
        olt_layout.addWidget(self.user_input)
        olt_layout.addWidget(self.password_input)

        self.olt_output = QTextEdit(placeholderText="OLT Connection Output...")
        self.olt_output.setReadOnly(True)

        self.connect_telnet_btn = QPushButton("Connect")
        self.display_telnet_btn = QPushButton("Status")
        self.disconnect_telnet_btn = QPushButton("Disconnect")
        self.connect_telnet_btn.clicked.connect(self.connect_olt_session)
        self.display_telnet_btn.clicked.connect(self.display_olt_session)
        self.disconnect_telnet_btn.clicked.connect(self.disconnect_olt_session)

        olt_button_layout = QHBoxLayout()
        olt_button_layout.addWidget(self.disconnect_telnet_btn)
        olt_button_layout.addWidget(self.display_telnet_btn)
        olt_button_layout.addWidget(self.connect_telnet_btn)

        olt_layout.addWidget(self.olt_output)
        olt_layout.addLayout(olt_button_layout)
        olt_connection_group.setLayout(olt_layout)
        main_layout.addWidget(olt_connection_group)


        # === OLT Port Setting Block ===
        olt_port_group = QGroupBox("OLT Port Setting")
        olt_port_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_port_layout = QVBoxLayout()

        self.olt_port_input = QLineEdit(placeholderText="OLT Port (Frame/Slot/Port)")
        self.vlan_input = QLineEdit(placeholderText="VLAN (1-65535)")
        self.upstream_input = QLineEdit(placeholderText="Upstream Port (Frame/Slot/Port)")

        olt_port_layout.addWidget(self.olt_port_input)
        olt_port_layout.addWidget(self.vlan_input)
        olt_port_layout.addWidget(self.upstream_input)

        self.olt_port_output = QTextEdit(placeholderText="OLT Port Setting Output...")
        self.olt_port_output.setReadOnly(True)

        self.port_config_btn = QPushButton("Config")
        self.port_display_btn = QPushButton("Status")
        self.port_delete_btn = QPushButton("Delete")
        self.port_config_btn.clicked.connect(self.config_port_settings)
        self.port_display_btn.clicked.connect(self.display_port_settings)
        self.port_delete_btn.clicked.connect(self.delete_port_settings)

        port_setting_btn_layout = QHBoxLayout()
        port_setting_btn_layout.addWidget(self.port_delete_btn)
        port_setting_btn_layout.addWidget(self.port_display_btn)
        port_setting_btn_layout.addWidget(self.port_config_btn)

        olt_port_layout.addWidget(self.olt_port_output)
        olt_port_layout.addLayout(port_setting_btn_layout)
        olt_port_group.setLayout(olt_port_layout)
        main_layout.addWidget(olt_port_group)

        # === Next Button ===
        next_button = QPushButton("Next →")
        next_button.setFixedSize(100, 30)
        next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #A5D6A7;
                border: 2px solid #1e90ff;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        next_button.clicked.connect(self.go_to_next)
        main_layout.addWidget(next_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def go_to_next(self):
        """Switch to Second Page"""
        self.stack.setCurrentIndex(1)

    def validate_credentials(self, ip, username, password):
        """Validate IP Address, Username, and Password"""
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

        if not ip or not re.match(ip_pattern, ip):
            return "Invalid IP Address format!"
        if not username:
            return "Username cannot be empty!"
        if len(password) < 4:
            return "Password must be at least 4 characters long!"

        return None

    def connect_olt_session(self):
        """Collect, validate, and send data to the backend"""
        ip = self.ip_input.text().strip()
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        validation_error = self.validate_credentials(ip, username, password)
        if validation_error:
            self.olt_output.setText(validation_error)
            self.olt_output.setStyleSheet("color: red;")
            return

        data = {"ip": ip, "username": username, "password": password}
        try:
            response = requests.post(f"{BACKEND_URL}/olt/connect_telnet", json=data)
            if response.status_code == 200:
                self.olt_output.setText(f"Success: {response.json().get('message')}")
                self.olt_output.setStyleSheet("color: green;")
            else:
                self.olt_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_output.setText(f"Connection Error: {e}")
            self.olt_output.setStyleSheet("color: red;")

    def display_olt_session(self):
        ip = self.ip_input.text().strip()
        data = {"ip": ip}
        try:
            response = requests.post(f"{BACKEND_URL}/olt/display_telnet", json=data)
            if response.status_code == 200:
                self.olt_output.setText(f"Active session is available for {ip}.")
                self.olt_output.setStyleSheet("color: green;")
            else:
                print(f"400 bad request: {response.json()}")
                self.olt_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_output.setText(f"Displaying Error: {e}")
            self.olt_output.setStyleSheet("color: red;")

    def disconnect_olt_session(self):
        ip = self.ip_input.text().strip()
        data = {"ip": ip}
        try:
            response = requests.post(f"{BACKEND_URL}/olt/disconnect_telnet", json=data)
            if response.status_code == 200:
                self.olt_output.setText("Disconnected successfully.")
                self.olt_output.setStyleSheet("color: green;")
            else:
                print(f"400 bad request: {response.json()}")
                self.olt_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_output.setText(f"Disconnection Error: {e}")
            self.olt_output.setStyleSheet("color: red;")


    def validate_port_settings(self, olt_port, vlan_id, uplink_port):
        port_pattern = r"^\d{1,2}/\d{1,2}/\d{1,2}$"
        vlan_pattern = r"^\d{1,5}$"

        if not re.match(port_pattern, olt_port):
            return "Invalid OLT Port format! Use Frame/Slot/Port."
        if not re.match(vlan_pattern, vlan_id) or not (1 <= int(vlan_id) <= 65535):
            return "Invalid VLAN ID! Range: 1-65535."
        if not re.match(port_pattern, uplink_port):
            return "Invalid Upstream Port format! Use Frame/Slot/Port."
        return None

    def config_port_settings(self):
        olt_port = self.olt_port_input.text().strip()
        vlan_id = self.vlan_input.text().strip()
        upstream_port = self.upstream_input.text().strip()
        ip = self.ip_input.text().strip()

        validation_error = self.validate_port_settings(olt_port, vlan_id, upstream_port)
        if validation_error:
            self.olt_port_output.setText(validation_error)
            self.olt_port_output.setStyleSheet("color: red;")
            return

        data = {"olt_port": olt_port, "vlan_id": vlan_id, "upstream_port": upstream_port, "ip": ip}
        print(f"Configuring OLT Port: {olt_port}, VLAN: {vlan_id}, Upstream: {upstream_port}, IP: {ip}")
        try:
            response = requests.post(f"{BACKEND_URL}/olt/configure_port_setting", json=data)
            print(f"Response: {response.json()}")
            if response.status_code == 200:
                self.olt_port_output.setText(f"Success: {response.json().get('message')}")
                self.olt_port_output.setStyleSheet("color: green;")
            else:
                self.olt_port_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_port_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_port_output.setText(f"Connection Error: {e}")
            self.olt_port_output.setStyleSheet("color: red;")

    def display_port_settings(self):
        olt_port = self.olt_port_input.text().strip()
        vlan_id = self.vlan_input.text().strip()
        upstream_port = self.upstream_input.text().strip()
        ip = self.ip_input.text().strip()

        validation_error = self.validate_port_settings(olt_port, vlan_id, upstream_port)
        if validation_error:
            self.olt_port_output.setText(validation_error)
            self.olt_port_output.setStyleSheet("color: red;")
            return

        data = {"olt_port": olt_port, "vlan_id": vlan_id, "upstream_port": upstream_port, "ip": ip}
        print(f"Display Configuring OLT Port: {olt_port}, VLAN: {vlan_id}, Upstream: {upstream_port}, IP: {ip}")
        try:
            response = requests.post(f"{BACKEND_URL}/olt/display_port_setting", json=data)
            print(f"Response: {response.json()}")
            if response.status_code == 200:
                # Use HTML formatting inside QTextEdit
                message = response.json().get("message")
                formatted_text = f"""
                    <p style="color: green; font-weight: bold;">Success: {message}</p>
                """
                self.olt_port_output.setHtml(formatted_text)
                self.olt_port_output.append(f"{response.json().get('output')}")
                self.olt_port_output.setStyleSheet("color: blue;")
            else:
                self.olt_port_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_port_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_port_output.setText(f"Connection Error: {e}")
            self.olt_port_output.setStyleSheet("color: red;")

    def delete_port_settings(self):
        olt_port = self.olt_port_input.text().strip()
        vlan_id = self.vlan_input.text().strip()
        upstream_port = self.upstream_input.text().strip()
        ip = self.ip_input.text().strip()

        validation_error = self.validate_port_settings(olt_port, vlan_id, upstream_port)
        if validation_error:
            self.olt_port_output.setText(validation_error)
            self.olt_port_output.setStyleSheet("color: red;")
            return

        data = {"olt_port": olt_port, "vlan_id": vlan_id, "upstream_port": upstream_port, "ip": ip}
        print(f"UnConfiguring OLT Port: {olt_port}, VLAN: {vlan_id}, Upstream: {upstream_port}, IP: {ip}")
        try:
            response = requests.post(f"{BACKEND_URL}/olt/delete_port_setting", json=data)
            print(f"Response: {response.json()}")
            if response.status_code == 200:
                self.olt_port_output.setText(f"Success: {response.json().get('message')}")
                self.olt_port_output.setStyleSheet("color: green;")
            else:
                self.olt_port_output.setText(f"Error: {response.json().get('detail')}")
                self.olt_port_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_port_output.setText(f"Connection Error: {e}")
            self.olt_port_output.setStyleSheet("color: red;")

