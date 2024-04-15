# Football Data Platform 
###### _WIP: This project is still under development, more updates to come_

The **Football Data Platform** is a comprehensive data aggregation tool tailored for football enthusiasts, analysts, 
and researchers. It collects football-related data from popular platforms: 
[FBRef](https://fbref.com/), 
[Sofascore](sofascore.com) and 
[Transfermarkt](https://www.transfermarkt.com/). 
Once fetched, it saves the webpages' data as JSON files and subsequently loads it into a PostgreSQL database for 
structured queries and analytics.

---

### Features

- **Data Scraping**: Pulls data from Transfermarkt, Sofascore, and FBRef efficiently and systematically.
- **Data Storage**: Stores raw webpage data as JSON files.
- **Database Loading**: Inserts and structures the scraped data into a PostgreSQL database.

---

### Prerequisites

- Python 3.9+
- Poetry
- Docker

---

### Installation

1. Clone this repository:
```bash
git clone https://github.com/your-github-username/football-data-platform.git
cd football-data-platform
```

2. Create a Poetry virtual environment and install the dependencies:
```bash
poetry shell
poetry install --no-root
```

3. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

4. Build the Docker image and start a container:
```bash
docker compose up -d --build
```

5. Run the database migrations:
```bash
alembic upgrade head
```

---

### Scrapping

#### Sofascore

```bash
scrapy crawl sofascore -a TOURNAMENT_ID=<tournament_id> -a SEASON_ID=<season_id>
```

Where `<tournament_id>` and `<season_id>` are the tournament and season identifiers, respectively.

They can be found in the URL of the tournament page on Sofascore.

Example: LaLiga 23/24

```bash
scrapy crawl sofascore -a TOURNAMENT_ID=8 -a SEASON_ID=52376
```

#### FBRef

```bash
scrapy crawl <spider_name>
```

Where `<spider_name>` is the name of the spider to be executed.
The available spiders are:

- FBrefBRA1
- FBrefEPL
- FBrefUCL

---

### Processing

```bash
python app/processing/sofascore
```

```bash
python app/processing/fbref
```
