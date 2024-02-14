# Messenger Analysis

#### Created in collaboration with:

- [Mikołaj Gałkowski](https://github.com/galkowskim),
- [Laura Hoang](https://github.com/hoanganhlinh),
- [Wiktor Jakubowski](https://github.com/WJakubowsk)

## Description

The project is a part of the course about Visualization at the Warsaw University of Technology. The goal of the project is to analyze the data from the Facebook Messenger application. The data is stored in a JSON file and contains information about the messages sent between the users. The project is divided into two parts: data preprocessing and analysis. The first part includes data cleaning and transformation, while the second part focuses on the analysis of the data.

# Data

In order to run the project you need to download the data from the Facebook Messenger application. Facebook provides data in zip format. Unzip the files (change folder names to unique ones if you have more than one file and put the folders into the `data/messages` directory). The data should be in the following format (in case you had 4 files):

```bash
data/messages
├── messages1 (custom name)
├── messages2 (custom name)
├── messages3 (custom name)
└── messages4 (custom name)
```

To prepare the data for the analysis (run the script `data_preparation.py` inside `data` directory), run the following command:
```bash
python data_preparation.py
```
That would create csv file with you messages data inside `data` directory. (Currently the script works only for LINUX systems, but you can easily modify it to work on Windows as well).

# Web application - setup

## Build the image - inside project directory
```bash
docker build -t image_name .
```
## Run the container
On windows (run run_docker.bat file):
```bash
run_docker.bat
```
On linux:
```bash
./run_docker.sh
```
## Open the web application
Open your browser and go to `http://localhost:8080/`

### Development setup - branch `dev` - for more information

## Project setup
Same procedure as for the web application (**WARNING!** small change in Dockerfile, need to create new image), but `run_docker_dev.sh/.bat` opens the development environment and you go into the container.
Then you can run application after making some changes from folder `src` using `run_app.sh` script.