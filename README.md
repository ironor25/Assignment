# Internship Assignnment

This repository contains completed assignment. It includes code samples, documentation assignment I worked on.

Using SQLAlchemy ORM to use SQLlite for performing database operations.

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ironor25/Assignment.git
    cd Assignment
    ```

2. **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```


4. **Run the project:**
    ```bash
    uvicorn api_routes:app --reload
    ```

5. **Sample Input Data**

        You can use the following sample data to test the database operations:
        Open Postman to test the routes.

        ```json
        
                {
                    "id": 1,
                    "date": "2025-06-10",
                    "time": "10:30:00",
                    "message": "Doctor's appointment"
                },
                {
                    "id": 2,
                    "date": "2025-06-11",
                    "time": "09:00:00",
                    "message": "Team standup meeting"
                }
              
        
        ```
5. **API Routes & Input Methods**

    - **GET**
      - No input required. Simply send a GET request to retrieve data.

    - **POST**
      - Add a new entry by sending JSON data:
         ```json
         {
            "date": "2025-06-10",
            "time": "10:30:00",
            "message": "Doctor's appointment"
         }
         ```

    - **PUT**
      - Update an existing entry by providing the `id` and updated details:
         ```json
         {
            "id": 1,
            "date": "2025-06-10",
            "time": "10:30:00",
            "message": "Therapist appointment"
         }
         ```

    - **DELETE**
      - Delete an entry by specifying the `id`:
         ```json
         {
            "id": 1
         }
         ```

---

*Thank you for checking out my internship work!*