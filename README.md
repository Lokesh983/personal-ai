# INDRA — Personal AI Desktop Assistant

INDRA is a desktop-based personal AI assistant designed to execute system-level commands, automate workflows, and process user instructions through an interactive graphical interface.

The system combines modular command execution, file processing, and desktop automation into a unified environment. It is designed to evolve into a voice-enabled assistant capable of running continuously and responding to spoken commands.

---

# Overview

INDRA is built as a modular desktop assistant capable of:

- Executing predefined system commands
- Launching applications
- Creating and managing files
- Summarizing document content
- Maintaining persistent configuration
- Running as a standalone executable

The application includes a fully functional graphical user interface with theme switching, command history, and persistent settings.

The current version supports command-based interaction and is packaged as a Windows executable.

---

# Core Features

## Desktop Interface

- Built using PySide6
- Interactive command console
- Light and Dark theme support
- Theme persistence across sessions
- Command history navigation
- Status indicators
- Custom application icon

---

## Command Execution Engine

Supports structured execution of system-level operations such as:

- Opening installed applications
- Creating files with specified content
- Processing user commands
- Executing modular task flows

Example commands:

- open chrome
- create file demo.txt with content hello
- summarize the file resume.pdf


---

## File Processing

INDRA supports document analysis and summarization for:

- PDF files
- DOCX files
- TXT files

Processing includes:

- Text extraction
- Content summarization
- Structured output display

Libraries used:

- python-docx
- PyPDF2

---

## Persistent Settings

The system stores configuration data including:

- Last selected theme
- Runtime settings

Data is saved using:

- settings.json


Theme preferences automatically load during startup.

---

## Standalone Executable

The application is packaged using:

personal-ai/
│
├── runner.py
│ Core execution controller
│
├── ui/
│ ├── main_window.py
│ Graphical interface
│
│ ├── app_icon.ico
│ Application icon
│
│ ├── settings.json
│ Persistent configuration
│
│ └── themes/
│ ├── dark.qss
│ └── light.qss
│
├── INDRA.spec
│ PyInstaller configuration
│
├── requirements.txt
│ Dependency list
│
└── README.md


---

# Technology Stack

## Programming Language

Python

---

## Frameworks and Libraries

- PySide6 — Desktop UI
- PyInstaller — Executable packaging
- python-docx — DOCX file processing
- PyPDF2 — PDF processing

---

## System Components

- Modular command executor
- UI interaction handler
- File processing pipeline
- Persistent configuration manager

---

# Installation and Setup

## Option 1 — Run from Source

Clone the repository:

git clone https://github.com/Lokesh983/personal-ai.git

cd personal-ai

Install dependencies:

pip install -r requirements.txt

Run the application:

python ui/main_window.py


---

## Option 2 — Run Executable

Download the packaged executable from:

Releases → INDRA.exe

Run:

INDRA.exe

No Python installation required.

---

# Usage

Launch the application and enter commands into the command input field.

Example usage:

- open chrome
- create file notes.txt with content meeting at 10am
- summarize the file resume.pdf


Results are displayed in the output console.

---

# Current Capabilities

- Desktop-based command execution
- Application launching
- File creation
- Document summarization
- Theme switching
- Persistent UI configuration
- Standalone executable support

---

# Planned Enhancements

Future development phases include:

## Voice Integration

- Speech-to-text command input
- Text-to-speech responses
- Wake-word activation
- Background listening service

---

## System Intelligence

- Dynamic detection of installed applications
- Context-aware command handling
- Expanded automation capabilities

---

## Installer Support

- Full installation package
- Start Menu integration
- Desktop shortcut creation
- Automatic startup configuration

---

# Development Status

Current Stage:

Executable MVP Completed

Completed Modules:

- UI Engine
- Command Processor
- File Processing Engine
- Theme System
- Persistent Settings
- Executable Packaging

Next Phase:

- Portability validation
- Installer creation
- Voice interaction module

---

# Testing Status

Validated Components:

- UI functionality
- Command execution
- File summarization
- Theme persistence
- Executable packaging

Pending Tests:

- Cross-machine portability
- Multi-system compatibility

---

# Design Goals

INDRA is designed with the following goals:

- Modularity
- Extensibility
- Stability
- System-level interaction capability
- Desktop-native execution

The architecture supports progressive upgrades without requiring system redesign.

---

# License

This project is currently developed for academic and research purposes.

License type can be updated based on distribution requirements.

---

# Author

Lokesh Vettath  
B.Tech Computer Science (AI Specialization)

GitHub Repository:

https://github.com/Lokesh983/personal-ai
