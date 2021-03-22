from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_DATA = os.environ["ORIGIN_CITY_DATA"]

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_code(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data
}

today = datetime.now() + timedelta(1)
six_month_from_today = datetime.now() + timedelta(6 * 30)

for destination_code in destinations:
    flight = flight_search.check_flight(
        ORIGIN_CITY_DATA,
        destination_code,
        from_time=today,
        to_time=six_month_from_today
    )
    print(flight.price)

    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        message = f"Low Price Alert! Only Rs.{flight.price} To Fly From " \
                  f"{flight.origin_city}-{flight.origin_airport} to " \
                  f"{flight.destination_city}-{flight.destination_airport}, from " \
                  f"{flight.out_data} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"/n/nFlight has {flight.stop_overs}, via {flight.via_city}."

        link = f"https://www.google.co.in/flights?h=en#flt={flight.origin_airport}." \
               f"{flight.destination_airport}.{flight.put_date}*{flight.dsitination_airport}." \
               f"{flight.origin_airport}.{flight.return_date}"

        notification_manager.send_sms(emails, message, link)
