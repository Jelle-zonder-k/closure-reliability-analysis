# Storm Surge Barrier Closure Data Project

This README file explains how to set up a development environment for local development and how to generate a database.

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
    sqlalchemy
    python-dotenv
    ```
2. Install the packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

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


