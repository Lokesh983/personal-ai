from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel
)
from runner import run_command
import json
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class PersonalAIWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resource_root = self._resource_root()

        icon_path = os.path.join(
            self.resource_root,
            "app_icon.ico"
        )

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Personal AI Assistant")
        self.setGeometry(300, 150, 800, 500)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.theme_button = QPushButton("🌙 Dark Mode")
        top_layout.addWidget(self.theme_button)
        layout.addLayout(top_layout)

        # Title Label
        title = QLabel("INDRA")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(title)

        # Output Console
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setPlaceholderText(
            "System output will appear here..."
        )

        layout.addWidget(self.output_console)

        # Command Input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            "Enter command (e.g., open chrome)"
        )

        layout.addWidget(self.command_input)

        # Buttons Layout
        button_layout = QHBoxLayout()

        self.run_button = QPushButton("Run")
        self.clear_button = QPushButton("Clear")
        self.exit_button = QPushButton("Exit")

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.exit_button)

        layout.addLayout(button_layout)

        # Status Label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        # Connect Buttons
        self.run_button.clicked.connect(self.run_command)
        self.clear_button.clicked.connect(self.clear_console)
        self.exit_button.clicked.connect(self.close)
        self.theme_button.clicked.connect(self.toggle_theme)

        # Enter key support
        self.command_input.returnPressed.connect(
            self.run_command
        )

        self.command_history = []
        self.history_index = -1
        self.settings_path = os.path.join(
            self.resource_root,
            "settings.json"
        )
        self.current_theme = self.load_saved_theme()
        self.load_theme(self.current_theme)

    def _resource_root(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS
        return os.path.dirname(__file__)

    def load_saved_theme(self):

        if os.path.exists(self.settings_path):

            try:
                with open(self.settings_path, "r") as f:

                    data = json.load(f)

                    return data.get("theme", "dark")
            except (json.JSONDecodeError, ValueError):
                return "dark"

        return "dark"

    def save_theme(self):

        data = {
            "theme": self.current_theme
        }

        with open(self.settings_path, "w") as f:

            json.dump(data, f)

    def load_theme(self, theme_name):

        theme_path = os.path.join(
            self.resource_root,
            "themes",
            f"{theme_name}.qss"
        )

        with open(theme_path, "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

    def toggle_theme(self):

        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_button.setText("☀ Light Mode")

        else:
            self.current_theme = "dark"
            self.theme_button.setText("🌙 Dark Mode")

        self.load_theme(self.current_theme)
        self.save_theme()

    def current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def run_command(self):
        command = self.command_input.text().strip()

        if not command:
            return

        self.command_history.append(command)
        self.history_index = len(self.command_history)

        timestamp = self.current_time()

        # Show command in console
        self.output_console.append(
            f"[{timestamp}] >> {command}"
        )

        try:
            result = run_command(command)

            if isinstance(result, dict):

                if result.get("success"):

                    if result.get("summary"):
                        timestamp = self.current_time()
                        self.output_console.append(
                            f"[{timestamp}] {result['summary']}"
                        )

                    else:
                        timestamp = self.current_time()
                        self.output_console.append(
                            f"[{timestamp}] {result.get('message', '')}"
                        )

                else:
                    timestamp = self.current_time()
                    self.output_console.append(
                        f"[{timestamp}] ❌ {result.get('message', 'Execution failed')}"
                    )

            else:
                timestamp = self.current_time()
                self.output_console.append(
                    f"[{timestamp}] {str(result)}"
                )

        except Exception as e:
            timestamp = self.current_time()
            self.output_console.append(
                f"[{timestamp}] Error: {str(e)}"
            )

        self.status_label.setText("Status: Completed")

        self.command_input.clear()

    def clear_console(self):
        self.output_console.clear()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Up:

            if self.command_history:

                self.history_index = max(
                    0,
                    self.history_index - 1
                )

                self.command_input.setText(
                    self.command_history[
                        self.history_index
                    ]
                )
                return

        elif event.key() == Qt.Key_Down:

            if self.command_history:

                self.history_index = min(
                    len(self.command_history) - 1,
                    self.history_index + 1
                )

                self.command_input.setText(
                    self.command_history[
                        self.history_index
                    ]
                )
                return

        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PersonalAIWindow()
    window.show()

    sys.exit(app.exec())
