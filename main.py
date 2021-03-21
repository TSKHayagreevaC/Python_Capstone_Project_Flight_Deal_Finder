from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
import flight_search

data_manager = DataManager()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "DEl"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)

for destination in sheet_data:
    flight = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
