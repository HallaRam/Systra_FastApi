## Systra Workflow Management System (Beta Version)
## Overview
The Systra Workflow Management System is designed to streamline project workflows, enhance collaboration, and improve efficiency for teams. As a beta version, this release includes core features but may have some limitations or areas for improvement. We welcome feedback to help us refine and enhance the system.



# Features
For Admins:
Assign Responsibility: Assign an admin to a workflow to ensure accountability.
Template Creation: Create reusable workflow templates to save time on similar projects.
Manage User Contributions: Delete irrelevant or incorrect user entries for better project management.
For Users:
Activity Tracking: Add activities and subactivities to workflows for detailed project breakdowns.
Workload Estimation: Calculate the time required for tasks to improve planning and efficiency.
Workflow Visibility: View project workflows to understand timelines and progress.
Export Workflows: Download workflows as Excel files for offline access and further analysis.
Edit and Fix: Delete your own work to correct mistakes and keep workflows clean.
Beta Version Disclaimer
This version is a beta release:

Some features may not yet be fully implemented or optimized.
Bugs and issues may occur during use.
Performance enhancements and additional features are planned for future releases.
We value your feedback!

# How to Use
Access the Application: Log in to your account to start managing workflows.
For Admins:
Navigate to the Admin Panel to assign responsibilities and create templates.
Use the Manage Entries feature to delete incorrect user submissions.
For Users:
Add activities and subactivities to workflows via the Workflow Manager.
Use the Time Estimator to plan your workload.
Export workflows using the Download to Excel button.
View your project’s progress in the Workflow Overview section.
Key Benefits
Streamlined Workflow Management: Keep your team aligned and organized with structured workflows.
Detailed Task Planning: Break down tasks into activities and subactivities for clarity and precision.
Accountability Tools: Ensure project ownership with admin assignment features.
Offline Capability: Export workflows to Excel for local editing and sharing.
Error Correction: Flexible tools to delete and update work entries.


## Prerequisites
- Ensure **Python 3.1 and above** and **FastApi** are installed on your system.

# Backend Setup and Running Guide

1. Ensure Python 3.6 or later is installed on your system.

2. Navigate to the Backend Directory:
   cd path/to/backend

3. Create a Virtual Environment:
   python3 -m venv venv

4. Activate the Virtual Environment:
   - On Windows:
     venv\Scripts\activate
   - On macOS/Linux:
     source venv/bin/activate

5. Install Required Dependencies:
   pip install -r requirements.txt

6. Run the FastAPI Server:
   uvicorn main:app --reload

7. Access the Backend:
   - Backend is available at: http://localhost:8000
   - API documentation is available at: http://localhost:8000/docs



