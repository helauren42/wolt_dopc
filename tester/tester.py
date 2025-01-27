import subprocess
import math
import time

print("\n")

venue_slugs = [
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo"
]

venue_coordinates = [
    [24.77798142454613, 60.057872481327195],  # helsinki
    [18.0314984, 59.3466978],                # stockholm
    [13.3190913296482, 52.5237706165925],    # berlin
    [139.7115264, 35.6459122]                # tokyo
]

cart_values = [100, 500, 700, 1000, 2500]

print(" " * 50 + "Test Delivery impossible")
print("-" * 150)

cart_value = 10
user_lat = 10
user_lon = 10

for venue_slug in venue_slugs:

    """
    We run the curl command twice, once to retrive the status code, once to retrieve the response body
    """
    
    print(f"Test for venue: {venue_slug}")
    

    try:
        url = f"http://localhost:8000/api/v1/delivery-order-price?venue_slug={venue_slug}&cart_value={cart_value}&user_lat={user_lat}&user_lon={user_lon}"
        
        status_command = [
            "curl",
            "-w", "%{http_code}",
            "-o", "/dev/null",
            url
        ]
        result = subprocess.run(status_command, capture_output=True, text=True, check=True)
        status_code = result.stdout.strip()  # HTTP status code
        print("Status Code:", status_code)

        # Now get the body of the response
        response_command = [
            "curl",
            url
        ]
        body_result = subprocess.run(response_command, capture_output=True, text=True, check=True)
        print("Response Body:", body_result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
    print("-" * 50)

print("\n\n")

print(" " * 50 + "Complete test")
print("-" * 150)

def generate_coordinates(lon: float, lat: float) -> list[list[float]]:
    coordinates = []
    coordinates.append([lon + 5, lat + 5])    
    coordinates.append([lon + 10, lat + 10])
    coordinates.append([lon + 30, lat + 30])
    return coordinates

for i in range(len(venue_slugs)):
    venue_slug = venue_slugs[i] 
    venue_coordinate: list[float] = venue_coordinates[i]
    print("\n" + "-" * 100)
    
    print(f"VENUE: ", venue_slug.split("-")[-1])
    print("-" * 100 + "\n")

    user_coordinates = generate_coordinates(venue_coordinate[0], venue_coordinate[1])
    test_num = 1
    for user_coordinate in user_coordinates:
        print(f"USER COORDINATES TEST: {test_num}")
        user_lon = user_coordinate[0]
        user_lat = user_coordinate[1]
        
        for cart_value in cart_values:

            print(f"cart value: {cart_value}")

            url = f"http://localhost:8000/api/v1/delivery-order-price?venue_slug={venue_slug}&cart_value={cart_value}&user_lat={user_lat}&user_lon={user_lon}"

            curl_command = [
                "curl",
                "-w", "%{http_code}",
                "-o", "/dev/null",
                url
            ]

            try:
                result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
                status_code = result.stdout.strip()  # HTTP status code
                print("HTTP Status Code:", status_code)

                # Now get the body of the response
                response_command = [
                    "curl",
                    url
                ]
                body_result = subprocess.run(response_command, capture_output=True, text=True, check=True)
                print("Response Body:", body_result.stdout)
                print("")

            except subprocess.CalledProcessError as e:
                print("Error occurred:", e)
        test_num += 1
        print("-" * 50)
    # to handle the home assignment api's rate limiting we need to sleep
    print("sleeping 40 seconds")
    time.sleep(40)

print("FINISHED")

''' 
This attempt did not work, but I feel like if it's possible to generate coordinates at a desired distance from a venue, that would provide ideal testing
'''
# def generate_coordinates(lon: float, lat: float) -> list[list[float]]:
#     """
#     Generate coordinates at specific distances in meters from the input origin which would be the venue's coordinates
#     """
#     R = 6371000
#     distances = [0, 1, 499, 500, 501, 999, 1000, 1500, 1999, 2000]
#     bearing = 0

#     coordinates = []

#     for distance in distances:
#         angular_distance = distance / R
#         lat_rad = math.radians(lat)
#         lon_rad = math.radians(lon)

#         new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(angular_distance) + math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing))

#         new_lon_rad = lon_rad + math.atan2(math.sin(bearing) * math.sin(angular_distance) * math.cos(lat_rad), math.cos(angular_distance) - math.sin(lat_rad) * math.sin(new_lat_rad))

#         new_lat = math.degrees(new_lat_rad)
#         new_lon = math.degrees(new_lon_rad)

#         coordinates.append([new_lon, new_lat])

#     return coordinates