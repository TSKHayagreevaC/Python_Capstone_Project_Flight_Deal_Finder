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
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

today = datetime.now() + timedelta(1)
six_month_from_today = datetime.now() + timedelta(6 * 30)

for destination in sheet_data:
    flight = flight_search.check_flight(
        ORIGIN_CITY_DATA,
        destination["iataCode"],
        from_time=today,
        to_time=six_month_from_today
    )

    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low Price Alert! Only Rs.{flight.price} To Fly From "
                    f"{flight.origin_city}-{flight.origin_airport} to "
                    f"{flight.destination_city}-{flight.destination_airport}, from "
                    f"{flight.out_data} to {flight.return_date}."
        )
