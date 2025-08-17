from nasa_client import NasaClient
import db
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.getenv("NASA_KEY")

    nasa_client = NasaClient(api_key)
    data = nasa_client.get_apod()

    # Save to Supabase
    db.save_apod(data["date"], data["title"], data["explanation"], data["url"])

    print("Created new APOD record successfully!")
    print("Date: ", data["date"])
    print("Title: ", data["title"])

    print("-" * 200)

    records = db.get_all_apods()
    print(f"Current record(s) - {len(records)}:")

    for row in records:
        print("Date: ", row["date"], " - Title: ", row["title"])


if __name__ == "__main__":
    main()

    # data = db.get_all_apods()
    # for row in data:
    #     print(row)
