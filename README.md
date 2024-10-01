# Flask Movie App

A comprehensive web application for movie and TV series enthusiasts, powered by Flask and The Movie Database (TMDb) API. This app allows users to search, discover, and keep track of their favorite movies and TV shows.

## Features

- Search functionality for movies and TV series
- Discover new content based on various criteria
- View trending movies and TV shows
- User authentication (register, login, logout)
- Personalized recommendations with custom ratings
- Responsive design for mobile and desktop

## Tech Stack

- Backend: Flask (Python)
- Database: SQLAlchemy with SQLite (easily adaptable to other databases)
- Frontend: HTML, CSS (Bootstrap), JavaScript
- API: The Movie Database (TMDb)

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- TMDb API key

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flask-movie-app.git
   cd flask-movie-app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   TMDB_API_KEY=your-tmdb-api-key
   ```
   Replace `your-secret-key` with a secure random string and `your-tmdb-api-key` with your actual TMDb API key.

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

7. Open a web browser and navigate to `http://localhost:5000` to see the app running.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing the API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the frontend design