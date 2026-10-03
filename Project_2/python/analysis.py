import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


tickets = pd.read_csv("../data/raw.csv")
teams = pd.read_csv("../data/teams.csv")

# Confirm numeric data types
print("Before conversion:")
print("resolution_hours:", tickets["resolution_hours"].dtype)
print("satisfaction:", tickets["satisfaction"].dtype)

# Convert to numeric if necessary
tickets["resolution_hours"] = pd.to_numeric(
    tickets["resolution_hours"], errors="coerce"
)
tickets["satisfaction"] = pd.to_numeric(
    tickets["satisfaction"], errors="coerce"
)

print("\nAfter conversion:")
print("resolution_hours:", tickets["resolution_hours"].dtype)
print("satisfaction:", tickets["satisfaction"].dtype)

# Remove exact duplicate row
tickets = tickets.drop_duplicates().copy()

# Merge tickets with teams using LEFT JOIN
merged = tickets.merge(
    teams,
    on="team_id",
    how="left"
)

# Required assertions
assert len(merged) == 12, f"Expected 12 rows, got {len(merged)}"

assert merged["department"].isna().sum() == 0, (
    "There are unmatched team_id values after the merge."
)

print("\nP1 checks passed.")
print("Merged rows:", len(merged))
print("Unmatched team_id values:", merged["department"].isna().sum())


# Create breach_flag
merged["breach_flag"] = (
    merged["resolution_hours"] > 24
).astype(int)

# Department summary
department_summary = (
    merged
    .groupby("department")
    .agg(
        total_tickets=("breach_flag", "size"),
        breached_count=("breach_flag", "sum")
    )
)

department_summary["sla_breach_rate"] = (
    department_summary["breached_count"]
    / department_summary["total_tickets"]
    * 100
)

print("\nDepartment Summary:")
print(department_summary.reset_index())


# Team breach-rate analysis
team_summary = (
    merged
    .groupby("team_id")
    .agg(
        total_tickets=("breach_flag", "size"),
        breached_count=("breach_flag", "sum")
    )
)

team_summary["breach_rate"] = (
    team_summary["breached_count"]
    / team_summary["total_tickets"]
    * 100
)

# Team with highest breach rate
highest_breach_team = team_summary.sort_values(
    by=["breach_rate", "team_id"],
    ascending=[False, True]
).iloc[0]

print("\nTeam with highest breach rate:")
print("Team ID:", highest_breach_team.name)
print("Breached tickets:", int(highest_breach_team["breached_count"]))
print("Total tickets:", int(highest_breach_team["total_tickets"]))
print("Breach rate:", f"{highest_breach_team['breach_rate']:.2f}%")


month_order = ["Jan", "Feb", "Mar"]

merged["month"] = pd.Categorical(
    merged["month"],
    categories=month_order,
    ordered=True
)

monthly_avg = (
    merged
    .groupby("month", observed=False)["resolution_hours"]
    .mean()
    .reindex(month_order)
)

print("\nMonthly Average Resolution Hours:")
print(monthly_avg)

# Create output directory if it doesn't exist
Path("outputs").mkdir(parents=True, exist_ok=True)

# Plot
plt.figure(figsize=(8, 5))

monthly_avg.plot(kind="bar")

plt.title("Monthly Average Resolution Hours")
plt.xlabel("Month")
plt.ylabel("Average Resolution Hours")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig("outputs/python_chart.png", dpi=300)
plt.show()

print("\nChart saved to: outputs/python_chart.png")