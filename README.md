# Food Donation API

## Overview

The Food Donation API is designed to facilitate the management of food donations, donors and recipients. It provides a secure and efficient way for organizations to track and manage food donations, ensuring that donations reach those in need.

## Features

- **User Management**: Register, authenticate and manage users.
- **Donor Management**: Create, update and delete donors.
- **Recipient Management**: Manage recipients who receive donations.
- **Donation Tracking**: Track and manage food donations.
- **Review System**: All users to leave reviews for donations.

## Technologies
- **FastAPI**: For building the API.
- **MongoDB**: For data storage.
- **JWT**: For secure authentication.
- **Pydantic**: For data validation.

## Key Features

- **Asynchronous Operations**: The use of asynchronous operations (async/await) for handling I/O-bound tasks (e.g., database operations) to improve performance and scalability.
- **Dependency Injection**: FastAPI's dependency injection system is used for injecting dependencies like get_current_user.
- **Modular Design**: The code is modular, with separate functions for creating, retrieving, updating, and deleting donations. This improves maintainability and readability.

## Installation
### Prerequisites
- Python 3.8+
- MongoDB

### Clone Repository
```sh
git clone https://github.com/kevkatam/Food-Donation-App 
cd Food-Donation-App
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

## Run the Server

```sh
uvicorn app.main:app --reload
```

The API wll be available at `http://127.0.0.1:8000`.

## API Documentation

The API documentation is available at http://127.0.0.1:8000/docs (Swagger UI) and http://127.0.0.1:8000/redoc (ReDoc).

## License

The project is license under the MIT License. 

## Acknowledgements

Thanks to the ALX mentors and community for their support and resources throughout the year and also thanks to the FastAPI and MongoDB communities for their support.
