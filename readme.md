# Storm Surge Barrier Closure Data Project

This project provides a system to store and manage data related to storm surge barrier closures. At the heart of the project is a FastAPI application that exposes endpoints for various CRUD operations on the data, including retrieving barrier details, adding new barriers, fetching closure events, and more. Specialized endpoints for rule-of-three calculations and beta distribution evaluations are also provided. The underlying data is stored in a PostgreSQL database, which can be managed using DBeaver.

## Introduction

The rise of sea levels and the increasing frequency of storm surges necessitate the construction and monitoring of storm surge barriers. These barriers are crucial for preventing flooding in low-lying areas. This project aims to provide a database for recording when these barriers are closed and the circumstances surrounding such closures. The FastAPI framework is utilized to offer a simple, yet powerful, API for interacting with this database, making it easy for users to add, retrieve, and analyze barrier closure data.

## Setting Up Development Environment

### Creating a Python Virtual Environment

1. Open your terminal and navigate to the project directory.
2. Run the following command to create a virtual environment named `venv`:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - **Windows**:
        ```bash
        .\\venv\\Scripts\\Activate
        ```

    - **macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```

### Installing Required Packages

1. Create a `requirements.txt` file and list all the necessary packages, such as:
    ```
    fastapi
    uvicorn
    sqlalchemy
    python-dotenv
    ```

2. Install the packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Running the FastAPI application

1. FastAPI is a modern web framework that's built on top of Starlette and Pydantic. It's designed to create web APIs quickly and efficiently.
2. Uvicorn is an ASGI server that serves as the interface between FastAPI and the outside world. It handles incoming requests and sends them to FastAPI for processing.
3. To run the FastAPI application, use the following command:

    ```bash
    uvicorn your_fastapi_app:app --reload
    ```

   Replace `your_fastapi_app` with the name of your FastAPI application file, without the `.py` extension.
4. The application will now be accessible at `http://127.0.0.1:8000`. 

## Generating a Database

### Installing and Setting up DBeaver

1. Download DBeaver from [the official website](https://dbeaver.io/).
2. Install and open DBeaver.
3. Click on `Database` in the menu bar and then `New Database Connection`.
4. Select `PostgreSQL` and enter your PostgreSQL server credentials.

### Creating a Local PostgreSQL Server in DBeaver

1. In DBeaver, right-click on `Databases` in the `Database Navigator`.
2. Select `Create` -> `Database`.
3. Name the new database `stormSurgeBarrierClosureData`.
4. Set other properties if necessary, and click `OK`.

### Running the Database Initialization Script

1. Make sure your `.env` file is properly configured with the database credentials.
2. Open a terminal and navigate to the project directory.
3. Activate the Python virtual environment:
    - **Windows**:
        ```bash
        .\\venv\\Scripts\\Activate
        ```

    - **macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```

4. Run the database initialization script:
    ```bash
    python create_database.py
    ```

This will create the tables in the `stormSurgeBarrierClosureData` database as per the models defined.

## Adding Records to the Database

To add a large number of records to the database:

1. Prepare a JSON file with all the records. Each record should follow this format:

    ```json
    {
        "StartDate": "YYYY-MM-DD",
        "StartTime": "HH:MM:SS",
        "EndDate": "YYYY-MM-DD",
        "EndTime": "HH:MM:SS",
        "WaterLevel": "+X.XX",
        "ClosureEventType": "EVENT_TYPE",
        "ClosureEventResult": "EVENT_RESULT"
    }
    ```

2. Use the provided API endpoints (or any tool like `curl` or Postman) to send the records to the server. Make sure to handle rate limits and chunk your data if necessary.
