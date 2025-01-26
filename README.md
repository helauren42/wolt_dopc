# wolt_dopc

## Introduction

This is a FastAPI-based service that calculates the total price for a delivery order, including the delivery fee and any applicable small order surcharge. The service uses static and dynamic data from the Wolt venue API to determine the delivery distance and pricing. 

Static Data: Fetches and caches static location data for venues at application launch.
Dynamic Data: Fetches dynamic data in real time for venues in response to user requests.
Haversine Formula: Calculates the delivery distance between the user's location and the venue.
Price Calculation: Computes the total price, including the delivery fee and small order surcharge.

The project uses Uvicorn, a high-performance ASGI (Asynchronous Server Gateway Interface) server, to handle requests asynchronously, ensuring efficient processing and scalability. By leveraging ASGI, the server optimizes handling multiple concurrent requests, providing faster response times and allowing the server to scale effectively for high traffic.

### Prerequisites

Before you start make sure you have python installed:
- "python --version" or "python3 --version"

## Installation

Clone the repository "git clone https://github.com/helauren42/wolt_dopc".

For Linux/MacOS:
- Open a terminal and navigate to the project's root directory: cd /path/to/project
- Create a virtual environment: python3 -m venv venv
- Activate the virtual environment: source venv/bin/activate
- Install the required dependencies: pip install -r requirements.txt

For Windows:
- Open a terminal or command prompt and navigate to the project's root directory: cd \path\to\project
- Create a virtual environment: python -m venv venv
- Activate the virtual environment: venv\Scripts\activate
- Install the required dependencies: pip install -r requirements.txt

## Usage

Simply run the application by typing:
- "python main.py" or "python3 main.py"

The api will be accessible through your localhost's port 8000

### API Endpoint

Objective: Calculate Delivery Order Price<br>
Endpoint: GET "/api/v1/delivery-order-price/"<br>
Address: localhost:8000<br>

Parameters:<br>
venue_slug (str): The unique identifier for the venue.<br>
cart_value (int): The shopping cart total value.<br>
user_lat (float): The latitude of the user's location.<br>
user_lon (float): The longitude of the user's location.<br>

Example Request:<br>
curl -X GET "http://0.0.0.0:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1500&user_lat=60.1699&user_lon=24.9384"

Example Response:<br>
{<br>
  "total_price": 1700,<br>
  "small_order_surcharge": 0,<br>
  "cart_value": 1500,<br>
  "delivery": {<br>
    "fee": 200,<br>
    "distance": 1200.5<br>
  }<br>
}<br>
