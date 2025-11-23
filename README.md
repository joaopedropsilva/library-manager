# library-manager
(descrever brevemente a aplicação mencionando a stack utilizada)

## Features
(utilizar collapsing por feature para conter os exemplos)

## Setup
(setup padrão com docker)

- Linux setup:
```bash
# Clone this repository
git clone <repository-url>

# Go to project dir
cd library-manager

# Create the virtual environment (make sure you have Python 3.13 installed)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run docker services (make sure you have docker installed)
docker compose -f services-compose.yml up -d

# Run the API
python -m app
```

> [Python 3.14](https://docs.python.org/3/whatsnew/3.14.html) is already out with features that were untested for this project, but it should be fine if you would like to use it.

## Running application tests

## Architectural decisions
This project uses [Architectural Decision Records (ADRs)](https://adr.github.io/) to address the architectural choices made upon development, all ADRs elaborated are located at: [docs/adrs](./docs/adrs/adr.md).
