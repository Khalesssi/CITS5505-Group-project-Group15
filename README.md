# CITS5505 Group Project – Group 15

##  1. Project Description

This application is developed to address key inefficiencies and limitations in how NDIS providers currently collect and manage client data. Traditionally, patient records and progress reports are exchanged through emails and scattered documents, resulting in delayed communication, data inconsistency, and difficulty in tailoring effective support plans.

Our platform provides a centralized, role-based data management system that enables Support Workers (SWs) to submit structured and therapist-specific reports. Each report is designed to be simple, multi-dimensional, and compliant with standard data formats. The submitted data is automatically routed to the relevant Therapists (e.g., Occupational, Physical, or Psychological), ensuring data privacy and relevance.

###  Key Features
This platform offers a rich set of features tailored to various user roles in the NDIS ecosystem, including Support Workers, Therapists, Guardians, and Administrators, ensuring seamless collaboration and accurate, role-specific data handling.

**Web Features & User Interface**
-Role-Based Dashboards: Upon login, users are redirected to personalized dashboards based on their roles (Support Worker, Therapist, Guardian, or Admin), each providing targeted tools and data.

-Interactive Home Page: A public homepage introduces the platform’s purpose and allows users to browse before login. Navigation options include returning to the dashboard or logging out.

-Chatbot Guide: An integrated chatbot assistant helps new users understand how to use the platform, guiding them step-by-step through uploading reports, viewing charts, or accessing support plans.

**Authentication & User Flow**
-Secure Login & Registration: Users register with their email and select a role (validated on the server). Email format and role input are checked on both front and backend.

-Session Control: Logged-in users can securely log out, browse the public site, or return to their private dashboard without re-authentication.

**Support Worker Dashboard**
-Structured Report Submission: SWs fill out tailored work reports based on the data requirements of different therapists (e.g., physical, psychological, or occupational).

-Multi-Dimensional Inputs: Report forms provide clear guidance on each input dimension (e.g., social engagement, emotional status, rehabilitation progress).

-Dynamic Personal Info: Real-time display of SW's profile information and submission history for transparency and self-tracking.

-Support Plan Access: SWs can view updated support plans from therapists and adjust care strategies accordingly.

**Therapist Dashboards**
-Data-Specific Input Pipeline: Each therapist receives only the data relevant to their specialty.

-Visual Data Analysis: Radar Chart for general patient health overview. Line/Bar Charts based on specialty metrics (e.g., emotion fluctuation, rehab progress).

-Support Plan Management: Fill out, update, and view support plans.

-Cross-role Sharing: Share relevant parts of a support plan with another therapist to assist in interdisciplinary treatment.

-CSV Download: Export anonymized or full patient data as CSV for documentation or advanced data analysis.

**Guardian Dashboard**
-View Reports: Guardians can view the history of SW-submitted reports for their care recipient.

-Access Support Plans: View historical or current support plans shared by therapists.

-Date Filter: Quickly access support plans by date to monitor progress over time.

**Admin Dashboard**
-User Overview: View a table of all registered users, including:

Name

Registered email

Role

Last login time

-System Monitoring: Helps ensure platform transparency and track platform usage statistics.

---

## 👥 2. Group Members

| Name           | UWA ID    | GitHub Username   |
|----------------|-----------|-------------------|
| Wanqi Zhang    | 24080897  | [@Khalesssi](https://github.com/Khalesssi) |
| Weiyu Xu       | 24233679  | [@Hannah-X0206](https://github.com/Hannah-X0206) |
| Ke-Chung Chen  | 24620249  | [@Elmer1993](https://github.com/Elmer1993) |
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
