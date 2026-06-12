# Travel Deal Management System

This is a simple Flask project. It lets you add and view travel deals using REST APIs.

## What this project does

- Add a new travel deal
- See all travel deals
- See one travel deal by its ID
- Check input data (validation)
- Save data in a database (SQLite + SQLAlchemy)

## Tech used

- Python 3
- Flask
- SQLAlchemy (ORM)
- SQLite (database)

## Project Folders

```
project/
├── app.py              # main file, starts the app
├── routes/             # API endpoints (URLs)
├── services/           # business logic
├── utils/              # validation rules
├── database/           # models and database code
├── requirements.txt    # list of packages
└── README.md
```

## How to Install and Run

Step 1: Clone the project from GitHub

```bash
git clone <your-repo-url>
```

Step 2: Go into the project folder

```bash
cd travel-deal-system
```

Step 3: Create a virtual environment (this keeps packages separate)

```bash
python3 -m venv venv
```

Step 4: Turn on the virtual environment

```bash
source venv/bin/activate
```

On Windows, use this instead:

```bash
venv\Scripts\activate
```

Step 5: Install all packages

```bash
pip install -r requirements.txt
```

Step 6: Run the app

```bash
python app.py
```

The app will start at:

```
http://127.0.0.1:5000/
```

## Database Connection (SQLite)

This project uses **SQLite**. SQLite is a simple database that saves data in one file.

- You do not need to install any database software.
- When you run `python app.py` for the first time, a file named `travel_deals.db` is created automatically inside the project folder.
- This file holds all your travel deals.
- The connection is set up in `app.py` using this line:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_deals.db"
```

- Tables are created automatically with this line:

```python
db.create_all()
```

So you don't need to write any SQL by hand. The data stays saved even after you stop and start the app again.

## API List

### 1. Add a Travel Deal

**POST** `/deals`

Send this as JSON:

```json
{
    "destination": "Dubai",
    "price": 5000,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury"
}
```

### 2. Get All Travel Deals

**GET** `/deals`

### 3. Get One Travel Deal

**GET** `/deals/<id>`

Example: `/deals/1`

## Validation Rules

- `destination` cannot be empty
- `price` must be more than 0
- `rating` must be between 1 and 5
- `travel_type` must be one of: `Budget`, `Luxury`, `Adventure`, `Family`
- `platform` cannot be empty

## Error Responses

If something is wrong, the API gives a clear error message and a status code:

- `400` - Bad input data
- `404` - Deal not found
- `405` - Wrong method used
- `500` - Server error

Example error response:

```json
{
    "status": "error",
    "message": "Validation failed.",
    "details": ["price must be a positive number."]
}
```