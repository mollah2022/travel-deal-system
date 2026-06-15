# Travel Deal Management System

A REST API built with Flask to manage travel deals. You can add deals, view them, search, filter, sort, and track recently viewed deals.

## What this project does

- Add a new travel deal
- See all travel deals
- See one travel deal by ID
- Search deals (partial, case-insensitive)
- Filter deals by price range
- Sort deals by field
- Track recently viewed deals
- Save data permanently (SQLite + SQLAlchemy)
- Log all API activity (console + file)

## Tech used

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite

## Project Structure

## How to Install and Run

Step 1: Clone the project from GitHub

```bash
git clone <your-repo-url>
```

Step 2: Go into the project folder

```bash
cd travel-deal-system
```

Step 3: Create a virtual environment

```bash
python3 -m venv venv
```

Step 4: Turn on the virtual environment

```bash
source venv/bin/activate
```

On Windows:

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

The app will start at: `http://127.0.0.1:5000/`

## Database Info

- Uses SQLite - no separate database software needed
- On first run, a file `travel_deals.db` is created automatically
- Data stays saved even after server restart
- Connection is set in `app.py`:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_deals.db"
```

- Tables are created automatically:

```python
db.create_all()
```

## Logging Info

- All API activity is logged automatically
- Logs appear in terminal and also saved in `logs/app.log` file
- Log format: `[date time] LEVEL - message`
- Example:

## API List

### 1. Add a Travel Deal

**POST** `/deals`

Request body:

```json
{
    "destination": "Dubai",
    "price": 5000,
    "platform": "Booking",
    "rating": 4.5,
    "travel_type": "Luxury"
}
```

Success response (201):

```json
{
    "status": "success",
    "message": "Travel deal created successfully.",
    "data": {
        "id": 1,
        "destination": "Dubai",
        "price": 5000,
        "platform": "Booking",
        "rating": 4.5,
        "travel_type": "Luxury"
    }
}
```

### 2. Get All Deals

**GET** `/deals`

### 3. Get One Deal

**GET** `/deals/<id>`

Example: `/deals/1`

### 4. Search Deals

**GET** `/deals/search`

At least one query parameter required:

### 5. Filter Deals by Price

**GET** `/deals/filter`

### 6. Sort Deals

**GET** `/deals/sort`

### 7. Recently Viewed Deals

**GET** `/deals/recent`

Returns last 10 viewed deals, most recent first.
A deal is tracked when you access `GET /deals/<id>`.

## Validation Rules

### Creating a deal:
- `destination` cannot be empty
- `price` must be more than 0
- `rating` must be between 1 and 5
- `travel_type` must be one of: `Budget`, `Luxury`, `Adventure`, `Family`
- `platform` cannot be empty

### Search:
- At least one of `destination`, `platform`, or `travel_type` required
- If `travel_type` given, must be a valid type

### Filter:
- At least one of `min_price` or `max_price` required
- Both must be positive numbers
- `max_price` cannot be less than `min_price`

### Sort:
- `sort_by` is required, must be: `price`, `rating`, or `destination`
- `order` must be `asc` or `desc`

## Error Responses

```json
{
    "status": "error",
    "message": "Error description",
    "details": ["specific error 1", "specific error 2"]
}
```

Status codes:
- `400` - Bad input / validation error
- `404` - Deal not found
- `405` - Wrong HTTP method
- `500` - Server error