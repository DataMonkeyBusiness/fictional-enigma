# Airflow DAG: Bitbucket Commits and Pull Requests Report

This Airflow DAG fetches commits and pull requests from Bitbucket repositories, filters them based on the last 5 days, and emails an HTML report.

## Key Components

### 1. **Airflow DAG**
- **Purpose**: Schedules the task every hour on weekdays.
- The DAG is designed to automate the process of fetching and reporting Bitbucket repository data on a regular basis.

### 2. **Functions**

#### a) `fetch_bitbucket_commits`
- **Description**: Fetches commit data from Bitbucket's API.
- **Usage**: Pulls commit history for the specified repositories.

#### b) `fetch_bitbucket_pullrequests`
- **Description**: Fetches pull request data from Bitbucket's API.
- **Usage**: Retrieves all open and merged pull requests from the repositories.

#### c) `parse_commits`
- **Description**: Filters and formats commit data into a DataFrame.
- **Filter**: Only includes commits from the last 5 days.
  
#### d) `parse_pull_requests`
- **Description**: Filters and formats pull request data into a DataFrame.
- **Filter**: Only includes pull requests from the last 5 days.

#### e) `report_gen`
- **Description**: Generates an HTML report that includes both the filtered commits and pull requests.
- **Usage**: Combines the parsed data into a readable format suitable for emailing.

#### f) `send_mail`
- **Description**: Sends the HTML report via email using SMTP.
- **Usage**: Utilizes SMTP server settings to email the report to the specified recipients.

## Workflow

1. **Scheduling**: The DAG runs every hour on weekdays, ensuring that any new commits or pull requests from the last 5 days are captured.
2. **Fetching Data**: The DAG calls the `fetch_bitbucket_commits` and `fetch_bitbucket_pullrequests` functions to retrieve data.
3. **Data Parsing**: The raw data is filtered by `parse_commits` and `parse_pull_requests` to include only relevant information from the past 5 days.
4. **Report Generation**: The `report_gen` function compiles the parsed data into an HTML report.
5. **Emailing**: The `send_mail` function is triggered to email the HTML report to recipients.

## Notes

- This DAG can be configured to work with multiple repositories.
- SMTP settings need to be correctly configured for the email function to work.
- The scheduling can be modified to run at different intervals as per the requirement.

---

### Example HTML Report
- The HTML report includes tables listing:
  - Commits from the last 5 days
  - Pull requests from the last 5 days
