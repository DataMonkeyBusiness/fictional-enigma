from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import smtplib
from pretty_html_table import build_table
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email account credentials
smtp_server = 'smtp.office365.com'
smtp_port = 587
email_address = from_email # Your Microsoft 365 email address
email_password = from_password  # Your Microsoft 365 account password or app password

# Email recipient
to_email = to_email  # Recipient's email address

# Bitbucket credentials and repository details
username = bitbucket_username
app_password = bitbucket_app_password
workspace = workspace_name
repo_slugs = {'repo_name': 'main_branch', 'repo2': 'main'}

# Default arguments for the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'bitbucket_report_dag',
    default_args=default_args,
    description='DAG to fetch Bitbucket data and send email reports',
    schedule_interval='0 * * * 1-5',  # Every hour on weekdays
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Function to get the current date and previous date
def get_dates():
    today = datetime.now().date()
    start_date = today - timedelta(days=5)
    return start_date, today

# Filter by date range
def is_within_date_range(date_str, start_date, end_date):
    date = datetime.fromisoformat(date_str.rstrip('Z')).date()  # Convert to date
    return start_date <= date <= end_date

# Fetch commits from Bitbucket
def fetch_bitbucket_commits(username, app_password, workspace, repo_slug):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/commits/"
    response = requests.get(url, auth=(username, app_password))

    if response.status_code == 200:
        return response.json()['values']
    else:
        print(f"Failed to fetch commits: {response.status_code} - {response.text}")
        return []

# Fetch pull requests from Bitbucket
def fetch_bitbucket_pullrequests(username, app_password, workspace, repo_slug):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/"
    response = requests.get(url, auth=(username, app_password))

    if response.status_code == 200:
        return response.json()['values']
    else:
        print(f"Failed to fetch pull requests: {response.status_code} - {response.text}")
        return []

# Parse and filter the fetched commits
def parse_commits(commits, start_date, end_date):
    data = []
    for commit in commits:
        commit_date = commit['date']
        if is_within_date_range(commit_date, start_date, end_date):
            data.append({
                "Author": commit['author']['raw'].replace(">", "").replace("<", ""),
                "Date": datetime.fromisoformat(commit_date).strftime("%Y-%m-%d %H:%M %Z"),
                "Message": commit['message'],
            })
    return pd.DataFrame(data)

# Parse and filter the fetched pull requests
def parse_pull_requests(pull_requests, start_date, end_date):
    data = []
    for pr in pull_requests:
        pr_date = pr['created_on']
        if is_within_date_range(pr_date, start_date, end_date):
            data.append({
                "Author": pr['author']['display_name'],
                "Date": datetime.fromisoformat(pr_date).strftime("%Y-%m-%d %H:%M %Z"),
                "Title": pr['title'],
                "State": pr['state'],
            })
    return pd.DataFrame(data)

# Function to send an email with the report
def send_mail(smtp_server, smtp_port, email_address, email_password, to_email, msg):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:
            server.starttls()  # Secure the connection
            server.login(email_address, email_password)
            server.sendmail(email_address, to_email, msg.as_string())  # Send and receive
            print("Email sent successfully!")
        except Exception as e:
            print(f"Could not send email: {str(e)}")

# Updated report generation function with custom table styles
def report_gen():
    start_date, end_date = get_dates()
    for repo, branch in repo_slugs.items():
        commits = fetch_bitbucket_commits(username, app_password, workspace, repo)
        pull_requests = fetch_bitbucket_pullrequests(username, app_password, workspace, repo)

        if commits or pull_requests:
            df_commits = parse_commits(commits, start_date, end_date) if commits else pd.DataFrame()
            df_pull_requests = parse_pull_requests(pull_requests, start_date, end_date) if pull_requests else pd.DataFrame()

            # Custom CSS for compact, professional table styling
            table_style = """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                }
                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                    color: #333333;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                tr:hover {
                    background-color: #f1f1f1;
                }
                caption {
                    caption-side: top;
                    text-align: left;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
            </style>
            """

            # Building HTML content for the email
            subject = f'{repo} - Commits and PR Report'
            body = f"""
            <html>
            <head>{table_style}</head>
            <body>
                <p>Hello,<br><br>
                   Please find the report for repository {repo} from {start_date} to {end_date}:</p>
                <h3>Commits:</h3>
                {df_commits.to_html(index=False, justify='left') if not df_commits.empty else '<p>No commits found.</p>'}
                <h3>Pull Requests:</h3>
                {df_pull_requests.to_html(index=False, justify='left') if not df_pull_requests.empty else '<p>No pull requests found.</p>'}
                <p>Thanks and Regards,<br>Lakshana Bhat</p>
            </body>
            </html>
            """

            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, "html"))

            send_mail(smtp_server, smtp_port, email_address, email_password, to_email, msg)
        else:
            print(f"No data found for repository {repo}.")

# Airflow task to run the report generation
def generate_report():
    report_gen()

# Create PythonOperator task to run the report generation function
report_task = PythonOperator(
    task_id='generate_bitbucket_report',
    python_callable=generate_report,
    dag=dag,
)
