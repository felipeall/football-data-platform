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

6. Run the desired spider:
```bash
scrapy crawl <spider_name>
```

---

Currently, the available spiders are:

`FBRefBRA1` 
Fetches data from the 
[Brazilian Serie A 2023](https://fbref.com/en/comps/24/Serie-A-Stats) 
league on FBRef

`FBRefGRE` 
Fetches data from 
[Grêmio](https://fbref.com/en/squads/d5ae3703/Gremio-Stats) 
team on FBRef

`SofascoreBRA1` 
Fetches data from the 
[Brazilian Serie A 2023](https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-a/325#48982) 
league on Sofascore

`SofascoreGRE` 
Fetches data from 
[Grêmio](https://www.sofascore.com/team/football/gremio/5926) 
team on Sofascore

`TransfermarktBRA1` 
Fetches data from the 
[Brazilian Serie A 2023](https://www.transfermarkt.com/campeonato-brasileiro-serie-a/startseite/wettbewerb/BRA1) 
league on Transfermarkt

`TransfermarktGRE` 
Fetches data from 
[Grêmio](https://www.transfermarkt.com/gremio-porto-alegre/startseite/verein/210) 
team on Transfermarkt
