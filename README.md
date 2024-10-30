# Project Overview

If you want to monitor and analyze the latest games published on gaming platforms, check this out: https://github.com/aishawn/game-website-monitor.git.
If you don't know how to run Python code, refer to the directly executable files in the repository.

## Python File Descriptions

In the root directory of this project, there are several important Python files:

- `step1_game_monitor.py`: This file contains the `GameSiteMonitor` class, which is responsible for monitoring game websites. It initializes with a list of sites, sets up logging, and provides methods to build Google search URLs for the specified sites.

- `step2_key_extract.py`: This script processes the results from the game monitor, extracting keywords from game names and titles. It reads a CSV file containing the monitoring results, appends a new column for keywords, and saves the updated data to a new CSV file.

- `step3_trends_analyse.py`: This file analyzes trends in the gaming industry using data collected from the monitoring process. It utilizes libraries like `pandas` and `matplotlib` to visualize trends over time, helping users understand which games are gaining popularity.

- `step1_game_monitor_gui.py`: This file provides a graphical user interface (GUI) for the game monitoring tool, allowing users to interact with the application more easily. It includes the same core functionality for loading sites and building search URLs, along with additional logging capabilities.
