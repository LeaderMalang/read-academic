# Read Academic

### Requirements:



**System Flow:**

1. **Login Screen:**
    * Display Username and Password fields.
    * If user exists in the database:
        * Validate credentials and grant access based on user type (Candidate or Admin).
    * Else:
        * Redirect to Signup Screen.

2. **Signup Screen:**
    * Allow user to register as Candidate or Admin.
    * Upon successful registration, redirect to Login Screen.

**Candidate Workflow:**

1. **Login:**
    * Authenticate user credentials.
    * On successful login, redirect to Document Upload Screen.

2. **Document Upload Screen:**
    * Display upload fields for required documents:
        * ID Card Picture
        * Matric Certificate (Federal & Rawalpindi Board) - marked as required
        * Fsc Certificate (Federal & Rawalpindi Board)
    * Implement a submit button.
    * Upon submission:
        * Show a loader while data extraction happens.

**Data Extraction (Multithreaded):**

1. Utilize Multithreading for parallel processing of documents.
2. Apply image preprocessing techniques to each uploaded image for improved accuracy.

**Information Extraction using EasyOCR:**

1. Extract specific information from uploaded documents:
    * ID Card:
        * ID Card Number
        * Address
    * Matric Marksheet:
        * Candidate Name
        * Father Name
        * Board of Examination
        * Date of Birth
        * Total Marks
        * Obtained Marks
        * Percentage
        * (Additional info as previously provided)
    * FSC Marksheet:
        * Board
        * Total Marks
        * Obtained Marks
        * Percentage

**Post-processing:**

1. Display two buttons: Submit and Cancel.
    * Submit button:
        * Validate extracted data.
        * Store all extracted information in the database with a unique primary key.
        * Redirect to a success screen or next step (if applicable).
    * Cancel button:
        * Clear extracted data.
        * Return to Document Upload Screen (Step 2).

**Admin Workflow:**

1. **Login:**
    * Authenticate Admin credentials.
    * On successful login, redirect to Admin Dashboard.

2. **Admin Dashboard:**
    * Display a table listing registered users.
    * Include columns for:
        * User Type (Candidate)
        * Upload Status (Completed/Incomplete)
        * Downloadable links for uploaded documents.

**Additional Notes:**

* Implement functionalities like Logout button to return to Login Screen.
* Handle scenarios where a Candidate has already completed the process and redirect them to view their data if they log in again.
* Admin should be able to download uploaded documents from the links displayed in the dashboard.

This refined workflow clarifies the system flow, user roles (Candidate & Admin), and their specific functionalities. It emphasizes data extraction using Multithreading and EasyOCR, data validation, and database storage with a primary key. 
### Installation
#### create virtual environment
``python -m venv env``
#### Activate virtual environment in Linux
``source env/bin/activate``
#### Activate virtual environment in Windows
``.\env\Scripts\activate``

#### install Requirements
``pip install -r requirements.txt``


#### Make Administrator Migrations and migrate
``python manage.py makemigrations``

``python manage.py migrate``

#### Create admin user
``python manage.py createsuperuser``

#### Create admin user
``python manage.py runserver``

#### Goto Page  and login using previously create admin user
``http://127.0.0.1:8000/admin``
``http://127.0.0.1:8000/``



