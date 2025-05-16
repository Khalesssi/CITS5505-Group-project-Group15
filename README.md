# CITS5505 Group Project – Group 15

## 1.Project Description and Key Features

This application is developed to address key inefficiencies and limitations in how NDIS providers currently collect and manage client data. Traditionally, patient records and progress reports are exchanged through emails and scattered documents, resulting in delayed communication, data inconsistency, and difficulty in tailoring effective support plans.

Our platform provides a centralized, role-based data management system that enables Support Workers (SWs) to submit structured and therapist-specific reports. Each report is designed to be simple, multi-dimensional, and compliant with standard data formats. The submitted data is automatically routed to the relevant Therapists (e.g., Occupational, Physical, or Psychological), ensuring data privacy and relevance.

---

This platform offers a rich set of features tailored to various user roles in the **NDIS ecosystem**, including **Support Workers**, **Therapists**, **Guardians**, and **Administrators**, ensuring seamless collaboration and accurate, role-specific data handling.

### Web Features & User Interface

- **Role-Based Dashboards**  
  Upon login, users are redirected to personalized dashboards based on their roles (Support Worker, Therapist, Guardian, or Admin), each providing targeted tools and data.

- **Interactive Home Page**  
  A public homepage introduces the platform’s purpose and allows users to browse before login. Navigation options include returning to the dashboard or logging out.

- **Chatbot Guide**  
  An integrated chatbot assistant helps new users understand how to use the platform, guiding them step-by-step.

---

### Authentication & User Flow

- **Secure Login & Registration**  
  Users register with their email and select a role (validated on the server). Email format and role input are checked on both the frontend and backend.

- **Session Control**  
  Logged-in users can:
  - Log out securely
  - Browse the public site
  - Return to their private dashboard without re-authentication

---

### Support Worker Dashboard

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

### Therapist Dashboards

**1. Profile**  
Displays the therapist’s basic information such as name, email, specialty, and login history.  
Used as a landing section for identity confirmation and personal record tracking.

**2. Patient Info**  
Each therapist only receives data relevant to their specialty for focused analysis.  
Patient records include medical background and therapeutic relevance.

**3. Support Plan**  
Therapists can create, edit, and review support plans tailored to patient needs.  
Plans are version-controlled and can be shared with Guardians or Support Workers.

**4. Report Record**  
Displays daily reports submitted by Support Workers assigned to each patient.

**5. Data Analysis**  
Visual charts assist in analyzing patient trends and therapy effectiveness.  
Includes:

- Radar Chart: Shows the patient’s general health overview
- Line & Bar Charts: Highlight specialty-specific metrics such as emotional fluctuation or rehab progress  
  Also supports CSV export for documentation and external analysis.

### Guardian Dashboard

**1. Personal Info**  
Displays the guardian’s personal profile information including name, email, and account activity.  
Used to verify identity and personalize access to patient data.

**2. Patient Info**  
Shows the assigned care recipient’s basic information and health background.  
Provides context for guardians to better understand therapy needs and progress.

**3. Report Record**  
Guardians can see the history of work reports submitted by Support Workers for their care recipient.  
Each entry includes submission date, summary, and report type.

**4. Shared Support Plan**  
View current and historical plans shared by therapists.  
These plans outline therapy goals, care instructions, and notes on patient needs.

### Admin Dashboard

**1. User Overview Table**  
 Admins can view a summary table of all registered users, including:

- Name
- Registered email
- Role
- Register time

---

## 2.👥 Group Members

| Name          | UWA ID   | GitHub Username                                         |
| ------------- | -------- | ------------------------------------------------------- |
| Wanqi Zhang   | 24080897 | [@Khalesssi](https://github.com/Khalesssi)              |
| Weiyu Xu      | 24233679 | [@Hannah-X0206](https://github.com/Hannah-X0206)        |
| Ke-Chung Chen | 24620249 | [@Elmer1993 / Elmer Chen](https://github.com/Elmer1993) |
| Ruilei Wang   | 24328412 | [@idawang142/Ida Wang](https://github.com/idawang142)   |

🔒 **GitHub Repository:** [https://github.com/Khalesssi/CITS5505-Group-project-Group15](https://github.com/Khalesssi/CITS5505-Group-project-Group15)

---

## 3. How to Run

### 📦 1. Set Up the Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### ⚙️ 2. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```ini
SECRET_KEY= yourSecretKey
DATABASE_URL=sqlite:///instance/app.db
FLASK_ENV=development
```

> 🧾 If you downloaded the **project zip file**, this `.env` file is already included and configured. You may skip this step.

---

### 🗃️ 3. Set Up the Database

Apply database migrations:

```bash
flask db upgrade
```

---

### 🧪 4. Insert Dummy Data (Prototype Login Setup)

This system is a **prototype**, so user accounts and data must be pre-inserted into the database for testing. Patients and relationships are not created dynamically in this version.

Run the following data insertion scripts **in order**:

```bash
python3 -m scripts.insert_UserPatient
python3 -m scripts.insert_sp
python3 -m scripts.insert_questionnaire_answers
```

> These scripts will insert demo users, support plans, and questionnaire data for testing role-based functionality.

---

### 👤 5. Test Login Accounts

You can use the following accounts to log in and explore the application:

| Role              | Email                                                         | Password |
| ----------------- | ------------------------------------------------------------- | -------- |
| Guardian          | [guardian@outlook.com](mailto:guardian@outlook.com)           | 112233   |
| Support Worker    | [supportworker@outlook.com](mailto:supportworker@outlook.com) | 12345678 |
| Physiotherapist   | [physio@example.com](mailto:physio@example.com)               | 11223344 |
| Occupational Ther | [OT@outlook.com](mailto:OT@outlook.com)                       | 123456   |
| Psychotherapist   | [psych@outlook.com](mailto:psych@outlook.com)                 | 7654321  |
| Admin             | [admin@outlook.com](mailto:admin@outlook.com)                 | 13579    |

---

### ▶️ 6. Run the Application

```bash
python run.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 4.Tests
### A. Unit Tests

This project uses Python’s built-in `unittest` framework. These tests validate critical backend functionality such as model creation, form validation, and access control.

### 🔧 Run All Tests

To run all unit tests at once:

```bash
python3 -m unittest discover -s tests/unit

```

---

### 📋 Test Case Overview (Total: 10)

| No. | Description                                                            | File                                     | Run Command                                                  |
| --- | ---------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| 1   | ✅ Create a valid Admin user and verify fields                         | `tests/unit/test_user_model.py`          | `python3 -m unittest tests/unit/test_user_model.py`          |
| 2   | ❌ Insert duplicate email, expect `IntegrityError`                     | `tests/unit/test_user_model.py`          | `python3 -m unittest tests/unit/test_user_model.py`          |
| 3   | ✅ Create a Patient with full role bindings (Guardian, SW, Therapists) | `tests/unit/test_patient_model.py`       | `python3 -m unittest tests/unit/test_patient_model.py`       |
| 4   | ✅ Insert valid Support Plan, verify therapist + sharing flags         | `tests/unit/test_support_plan_model.py`  | `python3 -m unittest tests/unit/test_support_plan_model.py`  |
| 5   | ✅ Submit valid QuestionnaireAnswer and verify insertion               | `tests/unit/test_questionnaire_model.py` | `python3 -m unittest tests/unit/test_questionnaire_model.py` |
| 6   | ❌ Insert Support Plan with missing content → trigger `IntegrityError` | `tests/unit/test_support_plan_model.py`  | `python3 -m unittest tests/unit/test_support_plan_model.py`  |
| 7   | ❌ Submit RegisterForm with invalid email (should fail validation)     | `tests/unit/test_auth_form.py`           | `python3 -m unittest tests/unit/test_auth_form.py`           |
| 8   | ✅ Validate SupportPlanForm with correct input and choices             | `tests/unit/test_plan_form.py`           | `python3 -m unittest tests/unit/test_plan_form.py`           |
| 9   | ❌ DailyReportForm fails on invalid score input (out of allowed range) | `tests/unit/test_questionnaire_form.py`  | `python3 -m unittest tests/unit/test_questionnaire_form.py`  |
| 10  | ✅/❌ Guardian access: pass if bound to patient, fail if not bound     | `tests/unit/test_route_authorization.py` | `python3 -m unittest tests/unit/test_route_authorization.py` |

---

### 🛠️ Notes

- All tests use `TestingConfig` with an in-memory SQLite database.
- You can run each test file individually to isolate failures.
- Ensure your virtual environment is activated and dependencies installed before running tests.

---

### B.System Tests

These system tests simulate real user interactions using Selenium WebDriver, and automatically launch a live version of the Flask server (as required by the rubric). Each test runs independently and verifies critical user flows.

⚠️ Due to browser and port constraints, these system tests must be run individually using the provided commands above. Running them all at once with discover is not supported.

### 📂 Test List (Total: 5)

| No.   | File Name                    | Run Command                                                | Description                                                                    |
| ----- | ---------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **1** | `test_login_flow.py`         | `python3 -m unittest tests.system.test_login_flow`         | ✅ Verifies that the login page loads correctly and form fields are present.   |
| **2** | `test_guardian_dashboard.py` | `python3 -m unittest tests.system.test_guardian_dashboard` | ✅ Tests successful login by a Guardian and dashboard content rendering.       |
| **3** | `test_access_control.py`     | `python3 -m unittest tests.system.test_access_control`     | ✅ Ensures unauthenticated users are redirected from protected pages to login. |
| **4** | `test_logout.py`             | `python3 -m unittest tests.system.test_logout`             | ✅ Verifies logout flow for a Support Worker, and redirection to login page.   |
| **5** | `test_register_flow.py`      | `python3 -m unittest tests.system.test_register_flow`      | ✅ Tests user registration form submission and post-registration redirection.  |

> 🔁 All tests automatically start the server and use headless Chrome mode.

---

### ✅ Run Example

```bash
python3 -m unittest tests.system.test_login_flow
```

---

## 5.Reference and Attributions

### AI Assistance Disclosure

This project were developed with the assistance of AI tools, including OpenAI’s ChatGPT. Prompts were written by team members to generate specific sections of Python, JavaScript, HTML, and markdown documentation. All AI-generated outputs were reviewed, modified, and integrated manually to meet the requirements of CITS5505 and the needs of the application.

Example prompt:
"Help me write a Selenium test that checks whether an unauthenticated user is redirected to login."

📖 APA-Style Reference (ChatGPT)
OpenAI. (2024, May 16). ChatGPT [Large language model]. https://chat.openai.com/chat

---

### 📚 Attributions for External Libraries

This project uses the following open-source libraries in accordance with the CITS5505 project requirements:

### 🧩 Core Technologies (permitted by rubric)

| Library                         | Purpose                                                                 |
| ------------------------------- | ----------------------------------------------------------------------- |
| **Flask**                       | Python web framework                                                    |
| **Flask-Login**                 | User session and authentication management                              |
| **Flask-WTF** + **WTForms**     | Form generation and CSRF protection                                     |
| **Flask-SQLAlchemy**            | ORM interface with SQLite                                               |
| **Flask-Migrate** + **Alembic** | Database migrations                                                     |
| **SQLAlchemy**                  | ORM and database abstraction layer                                      |
| **Jinja2**                      | HTML templating engine used with Flask                                  |
| **python-dotenv**               | Loading environment variables from `.env`                               |
| **selenium**                    | Used for system testing via browser automation                          |
| **email_validator**             | Ensures validity of email field input                                   |
| **Chart.js** (CDN)              | For interactive data visualization charts                               |
| **Tailwind CSS** (CDN)          | Responsive front-end UI styling (used as the one allowed CSS framework) |
| **JavaScript + AJAX**           | Used for dynamic data loading and DOM interaction                       |
| **jQuery** (CDN)                | DOM manipulation and AJAX simplification                                |
