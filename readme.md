# Superhero API pipeline

## Overview
A pipeline to retrieve data from the Superhero API, and export it to a csv file. You can read more about this API here: https://superheroapi.com/index.html.  This project includes the pipeline script, a simple test suite, and a scheduled action/cron job script

## Steps to run
1. A Github access token is required to authenticate with the API. You can quickly login to your Github and generate one using the link above.
2. If you do not have a Python virtual env set up, run `python -m venv /path/to/new/virtual/environment` to create it, and activate it by running `./<venv>\Scripts\activate` on windows or `<venv>\Scripts\activate.bat` on linux
3. Run `pip install -r requirements.txt`
4. To run the pipeline, run `python transformation.py` from the project directory and follow the prompts. The csv will be generated in the same directory

## Architectural overview
All main pipeline code is confined to one python script, for simplicity. The script is divided into functions for: API calls, data manipulation, and exporting. If this project were to grow, I envision a more modular, scaled setup with individual packages for each of the functions I listed. 