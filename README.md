# CITS5505 Group Project – Group 15

## Project Description

This application is developed to address key inefficiencies and limitations in how NDIS providers currently collect and manage client data. Traditionally, patient records and progress reports are exchanged through emails and scattered documents, resulting in delayed communication, data inconsistency, and difficulty in tailoring effective support plans.

Our platform provides a centralized, role-based data management system that enables Support Workers (SWs) to submit structured and therapist-specific reports. Each report is designed to be simple, multi-dimensional, and compliant with standard data formats. The submitted data is automatically routed to the relevant Therapists (e.g., Occupational, Physical, or Psychological), ensuring data privacy and relevance.
---

## Key Features

This platform offers a rich set of features tailored to various user roles in the **NDIS ecosystem**, including **Support Workers**, **Therapists**, **Guardians**, and **Administrators**, ensuring seamless collaboration and accurate, role-specific data handling.

---

###  Web Features & User Interface

- **Role-Based Dashboards**  
  Upon login, users are redirected to personalized dashboards based on their roles (Support Worker, Therapist, Guardian, or Admin), each providing targeted tools and data.

- **Interactive Home Page**  
  A public homepage introduces the platform’s purpose and allows users to browse before login. Navigation options include returning to the dashboard or logging out.

- **Chatbot Guide**  
  An integrated chatbot assistant helps new users understand how to use the platform, guiding them step-by-step through:
  - Uploading reports  
  - Viewing charts  
  - Accessing support plans  

---

###  Authentication & User Flow

- **Secure Login & Registration**  
  Users register with their email and select a role (validated on the server). Email format and role input are checked on both the frontend and backend.

- **Session Control**  
  Logged-in users can:  
  - Log out securely  
  - Browse the public site  
  - Return to their private dashboard without re-authentication  

---

###  Support Worker Dashboard

**1. Personal Info**  
Real-time display of the Support Worker's profile information and submission history.  
Includes details such as name and email

**2. Patient Information**  
Displays assigned patient information relevant to the Support Worker.  
Provides a snapshot of the patient context for ongoing care and report submission.

**3. Daily Report**  
Support Workers fill out tailored work reports based on the data requirements of different therapists.  
Report forms include multi-dimensional input areas such as social engagement, emotional status, and rehabilitation progress.

**4. Report Record**  
Shows a history of submitted daily reports by the Support Worker.  
Enables filtering and quick reference for past entries.

**5. Shared Support Plan**  
View the latest therapist-updated support plans.  
Used to adjust care strategies in alignment with treatment goals.


###  Therapist Dashboards

**1. Profile**  
Displays the therapist’s basic information such as name, email, specialty, and login history.  
Used as a landing section for identity confirmation and personal record tracking.

**2. Patient Info**  
Each therapist only receives data relevant to their specialty for focused analysis.  
Patient records include medical background and therapeutic relevance.

**3. Care Schedule**  
Shows therapy schedules, treatment milestones, and upcoming session reminders.  
Helps therapists plan and track ongoing care timelines efficiently.

**4. Support Plan**  
Therapists can create, edit, and review support plans tailored to patient needs.  
Plans are version-controlled and can be shared with Guardians or Support Workers.

**5. Report Record**  
Displays daily reports submitted by Support Workers assigned to each patient.  
Provides a timeline view of past entries to support therapy evaluation.

**6. Data Analysis**  
Visual charts assist in analyzing patient trends and therapy effectiveness.  
Includes:  
- Radar Chart: Shows the patient’s general health overview  
- Line & Bar Charts: Highlight specialty-specific metrics such as emotional fluctuation or rehab progress  
Also supports CSV export for documentation and external analysis.

###  Guardian Dashboard

**1. Personal Info**  
Displays the guardian’s personal profile information including name, email, and account activity.  
Used to verify identity and personalize access to patient data.

**2. Patient Info**  
Shows the assigned care recipient’s basic information and health background.  
Provides context for guardians to better understand therapy needs and progress.

**3. Care Schedule**  
Displays a table of scheduled care activities for the assigned patient.  
Includes time, task name, and responsible staff member.

**4. Report Record**  
Guardians can see the history of work reports submitted by Support Workers for their care recipient.  
Each entry includes submission date, summary, and report type.

**5. Shared Support Plan**  
View current and historical plans shared by therapists.  
These plans outline therapy goals, care instructions, and notes on patient needs.

**6. Data Analysis(Future work)**  
Presents multiple visualized views that allow guardians to observe key health indicators of the patient.  
Helps build a clearer understanding of the patient’s overall condition through intuitive data presentation.


###  Admin Dashboard

**1. User Overview Table**  
  Admins can view a summary table of all registered users, including:  
  - Name  
  - Registered email  
  - Role  
  - Last login time  

**2. System Monitoring**  
  Admins can monitor platform usage to ensure transparency and performance.

---

## 👥 Group Members

| Name           | UWA ID    | GitHub Username   |
|----------------|-----------|-------------------|
| Wanqi Zhang    | 24080897  | [@Khalesssi](https://github.com/Khalesssi) |
| Weiyu Xu       | 24233679  | [@Hannah-X0206](https://github.com/Hannah-X0206) |
| Ke-Chung Chen  | 24620249  | [@Elmer1993]/[Elmer Chen](https://github.com/Elmer1993) |
| Ruilei Wang    | 24328412  | [@idawang142](https://github.com/idawang142) |

🔒 **GitHub Repository:** [https://github.com/Khalesssi/CITS5505-Group-project-Group15](https://github.com/Khalesssi/CITS5505-Group-project-Group15)

---

How to Run This Project in a Linux terminal

1. Create and activate a virtual environment

`python -m venv venv-test`

`source venv/bin/activate`      

2. Install dependencies

`pip install -r requirements.txt`

3. Run the application

`python run.py`
