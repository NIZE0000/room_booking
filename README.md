# Room Booking Project

## Description
The Room Booking Project is a class assignment that allows users to book rooms.

## Prerequisites
- Python 3.x
- Django
- SQLite

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/your-username/room_booking_project.git
    ```

2. Navigate into the project directory:
    ```
    cd room_booking_project
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Configuration
1. Create a `.env` file in the project directory.
2. Add the following environment variables to the `.env` file:
    ```
    DEBUG=TRUE
    SECRET_KEY=your_secret_key_here
    ```

## Database Setup
1. This project uses SQLite as the database.
2. Run migrations:
    ```
    python manage.py migrate
    ```

## Usage
1. Start the development server:
    ```
    python manage.py runserver
    ```

2. Access the project in your web browser at `http://localhost:8000`.

## Contributing
If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

## License
This project is released under the [MIT License](https://opensource.org/licenses/MIT).
