# Support SLA Analysis

This project analyzes support ticket performance against a service-level agreement (SLA) threshold. It combines source data, SQL schema work, and Python-based analytics to measure operational performance across departments, teams, and ticket channels.

## 1. Project objective

The goal is to identify where support operations are underperforming and which teams or departments are most likely to miss service expectations.

The analysis answers the following questions:

- Which departments have the longest average resolution times?
- Which teams breach the SLA threshold most often?
- Which support channels contribute the highest number of breaches?
- Are there missing or malformed team-to-ticket relationships in the data?
- How do resolution times vary across months?

## 2. Business context

This dataset models a support operation where tickets are assigned to teams, teams belong to departments, and each ticket has a recorded resolution time. A ticket breaches the SLA if it takes more than 24 hours to resolve.

The business value of the project is to:

- track service health
- prioritize underperforming teams
- identify process bottlenecks
- review channel-level issues
- support operational reporting and decision-making

## 3. Repository structure

```text
Project_2/
├── Data/
│   ├── raw.csv
│   ├── teams.csv
│   └── tickets.csv
├── excel/
├── output/
│   ├── diagnostic_query.csv
│   ├── S2a — Average resolution time by department.csv
│   ├── S2b — Teams breaching SLA.csv
│   └── S2c — Top two channels by breach count.csv
├── powerBI/
├── python/
│   ├── analysis.py
│   └── outputs/
│       └── python_chart.png
├── sql/
│   ├── queries.sql
│   └── setup.sql
├── readme.md
└── ...
```

## 4. Data sources

### Data/raw.csv
This is the raw support ticket dataset. It contains operational records used for fault analysis, SLA measurement, and trend evaluation.

### Data/teams.csv
This file maps each team to its department. It is used to join ticket data with team metadata and to calculate department-level metrics.

### Data/tickets.csv
This file stores ticket-level details such as the ticket identifier, month, team, channel, resolution time, and operational flag fields.

## 5. Data dictionary

### Teams table
The teams dataset contains the following core fields:

- team_id: unique identifier for each team
- team: team name
- department: department associated with the team

### Tickets table
The ticket dataset contains the following core fields:

- ticket_id: unique identifier for the ticket
- month: month of the ticket record
- team_id: identifier of the ticket's assigned team
- channel: ticket submission channel
- resolution_hours: total time taken to resolve the ticket
- department: department derived from the ticket or team mapping
- satisfaction: customer satisfaction score
- breach_flag: binary indicator showing whether the ticket exceeded SLA

## 6. SQL workflow

The SQL layer creates the relational model and validates the relationship between teams and tickets.

### 6.1 Schema setup
File: sql/setup.sql

This script does the following:

- creates the database named SupportAnalysis
- creates the Teams table
- creates the Tickets table
- defines the foreign key relationship between Tickets.team_id and Teams.team_id

This ensures integrity between ticket records and team master data.

### 6.2 Data validation and analysis queries
File: sql/queries.sql

The queries cover:

1. Average resolution time by department
   - groups tickets by department
   - calculates the average resolution_hours
   - orders the results by average duration

2. Team-level averages
   - calculates average resolution hours by team_id and department
   - identifies which teams are slower on average

3. SLA breach counts by channel
   - filters where resolution_hours > 24
   - aggregates by channel
   - returns the top two channels by breach count

4. Unmatched team diagnosis
   - left joins tickets to teams
   - checks for any team_id values without a matching team record

This is important because data quality problems can distort the final operational KPI results.

## 7. Python analysis workflow

File: python/analysis.py

The Python script acts as the main analytical pipeline for the project. It reads the CSV data, validates the schema assumptions, merges the ticket and team information, calculates KPI metrics, and produces a visual output.

### 7.1 Data loading
The script loads the raw ticket and team datasets using pandas:

- tickets = pd.read_csv("../data/raw.csv")
- teams = pd.read_csv("../data/teams.csv")

### 7.2 Data type validation
It checks whether the numeric columns are stored as numeric types and converts them if needed:

- resolution_hours
- satisfaction

This is important because certain datasets may store numbers as strings, which would break calculation logic.

### 7.3 Duplicate removal
The script removes exact duplicate rows:

- tickets = tickets.drop_duplicates().copy()

This reduces the chance of inflated counts or distorted breach rates.

### 7.4 Merge and data integrity checks
The script joins tickets to teams on team_id using a left join:

- merged = tickets.merge(teams, on="team_id", how="left")

It then validates that:

- the merged dataset contains the expected row count
- all team_id values have a matching department entry

If either condition fails, the script raises an assertion error.

### 7.5 SLA breach flag logic
A breach flag is created using a threshold of 24 hours:

- breach_flag = 1 when resolution_hours > 24
- breach_flag = 0 otherwise

This is the core logic used throughout the SLA analysis.

### 7.6 Aggregations
The script calculates:

- department summary: total tickets, breached count, SLA breach rate
- team summary: total tickets, breached count, breach rate
- monthly average resolution hours by month

These aggregate views support both operational and executive reporting.

### 7.7 Visualization
The final stage creates a monthly resolution-time bar chart and saves it to:

- python/outputs/python_chart.png

This visual allows stakeholders to quickly assess whether resolution times are improving or worsening over time.

## 8. KPI definitions

The project uses a few core metrics:

### SLA breach rate
The share of tickets that exceed the 24-hour threshold.

Formula:

breach_rate = (breached_count / total_tickets) * 100

### Average resolution time
The mean resolution_hours aggregated for a department, team, or month.

### Breach count
The number of tickets above the SLA threshold.

## 9. Output files

The project exports its main results to the output folder.

### output/S2a — Average resolution time by department.csv
Department-level summary of average resolution times.

### output/S2b — Teams breaching SLA.csv
Shows which teams are breaching SLA thresholds and to what extent.

### output/S2c — Top two channels by breach count.csv
Highlights the channels producing the highest volume of breach incidents.

### output/diagnostic_query.csv
Useful for validating joins, checking mismatches, and reviewing data-quality issues.

### python/outputs/python_chart.png
Monthly trend chart for average resolution time.

## 10. How to run the project

### Step 1: Set up the database
Run the SQL setup script in sql/setup.sql to create the database schema.

Example:

```sql
CREATE DATABASE SupportAnalysis;
USE SupportAnalysis;
SOURCE setup.sql;
```

### Step 2: Run the SQL analysis
Execute the queries in sql/queries.sql to review department-level and breach-level results.

### Step 3: Run the Python analysis
From the project root:

```bash
python python/analysis.py
```

If you are inside the python folder:

```bash
python analysis.py
```

### Step 4: Review the results
Check the generated files in:

- output/
- python/outputs/

## 11. Interpretation of results

The outputs can be interpreted as follows:

- high departmental average resolution times often indicate workload pressure or systemic delay
- teams with high breach rates may need workflow changes, staffing attention, or escalation rules
- channels with repeated breaches may require route optimization or better queue handling
- monthly trend visuals help identify whether the support process is improving over time

## 12. Tools used

- Python
- pandas
- matplotlib
- SQL / relational schema design
- CSV-based reporting outputs

## 13. Summary

This project is a focused support analytics workflow designed to evaluate SLA compliance, find operational bottlenecks, and summarize team and department performance. It demonstrates a standard business-intelligence pipeline using raw data, relational validation, KPI aggregation, and final output reporting.
