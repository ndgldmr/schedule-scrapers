# 🏟️ Multi-Sport Schedule Scraper

This project is a collection of Python scripts designed to scrape, clean, and process event schedule data from various sports websites including the **MLB**, **NBA**, **NHL**, **MLS**, **PGA**, **LPGA**, and **NASCAR**.

The project uses `Selenium`, `BeautifulSoup`, and `pandas` to extract and structure broadcast schedules for downstream use in data analysis, visualization, or application pipelines.


⚠️ **Note:** This code was developed for use during the 2023 sports seasons. Due to regular changes in website structures, **some scrapers may no longer work correctly without modification**. Manual inspection and periodic updates are advised.

## 🗂️ Directory Structure

Each subdirectory contains:

* `src/` folder with scrapers and data cleaning utilities
* Time conversion modules (EST to UTC)
* Channel/network ID mappings
* CLI tools for CSV export

## 🚀 Features

* Headless scraping with Selenium
* HTML parsing with BeautifulSoup
* Timezone conversions (EST → UTC)
* Dynamic handling of multiple broadcasters
* CSV output for both raw and cleaned data
* Support for multiple sports with unique schedule formats

## 📌 Dependencies

* `pandas`
* `beautifulsoup4`
* `requests`
* `selenium`
* `pytz`
* `lxml`
* ChromeDriver (installed in `/usr/local/bin/chromedriver`)

## ⚙️ Usage

Each scraper can be run individually by executing the relevant `main()` function. The scripts prompt for necessary inputs such as:

* Schedule URLs
* Event or tournament names
* Date ranges for filename generation

```bash
python schedule-scrapers/mlb/src/mlbscraper.py
python schedule-scrapers/nba/src/nbascraper.py
```


