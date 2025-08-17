import os
import click
from dotenv import load_dotenv
from nasa_client import NasaClient
import db


load_dotenv()

# Whats Click?
# Definition: Click is a Python package used to create command-line interfaces (CLI).
# It allows developers to define commands, options, and arguments in a structured way,
# making it easier to build user-friendly command-line applications.


@click.group()
def cli():
    """NASA APOD CLI Tool"""
    pass


@cli.command()
@click.option("--date", default=None, help="Date for APOD (YYYY-MM-DD)")
def fetch(date):
    """Fetches a single APOD entry and saves it"""
    api_key = os.getenv("NASA_KEY")
    client = NasaClient(api_key)
    data = client.get_apod(date)

    # Save to Supabase
    db.save_apod(data["date"], data["title"], data["explanation"], data["url"])
    click.echo("Created new APOD record successfully!")
    click.echo(f"Date: {data['date']}")
    click.echo(f"Title: {data['title']}")
    click.echo("-" * 200)


@cli.command()
@click.option("--start", required=True, help="Start date for APOD range (YYYY-MM-DD)")
@click.option("--end", required=True, help="End date for APOD range (YYYY-MM-DD)")
def backfill(start, end):
    """Fetches APOD entries for a date range and saves them"""
    api_key = os.getenv("NASA_KEY")
    client = NasaClient(api_key)
    results = client.get_apod_range(start, end)

    for data in results:
        if (
            "date" not in data
            or "title" not in data
            or "explanation" not in data
            or "url" not in data
        ):
            click.echo(f"Skipping incomplete record for date: {data['date']}")
            continue
        db.save_apod(data["date"], data["title"], data["explanation"], data["url"])
        click.echo(f"Saved APOD record for date: {data['date']}")

    click.echo(
        f"Backfilled APOD records from {start} to {end}. ({len(results)} records saved)"
    )


@cli.command()
def list():
    """Lists all APOD records"""
    records = db.get_all_apods()
    click.echo(f"Current record(s) - {len(records)}:")
    for row in records:
        click.echo(f"Date: {row['date']} - Title: {row['title']}")


@cli.command()
@click.option(
    "--filter", required=True, default="", help="Filter records by description keyword"
)
def list(filter):
    """Lists APOD records filtered by a keyword in the explanation"""
    if not filter:
        click.echo("Please provide a filter keyword.")
        return

    records = db.get_filtered_apods(filter)
    click.echo(f"Filtered record(s) - {len(records)}:")
    for row in records:
        click.echo(f"Date: {row['date']} - Title: {row['title']}")


if __name__ == "__main__":
    cli()
