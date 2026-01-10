# 🏭 Manufacturing & Production Dashboard

## 📊 Dashboard Preview
[Production Impact](Dashboard/production_impact.png)
[Cost Management](Dashboard/cost_management.png)
[Equipment Reliability Failure Pattern](Dashboard/equipment-reliability-failure-pattern.png)
[Inventory Management](Dashboard/inventory-management.png)

## 📌 Business Objective
Develop a comprehensive Manufacturing Downtime and Reliability Dashboard to analyze
equipment performance, maintenance costs, and spare parts management.
The goal is to uncover the causes and impact of downtime, optimize maintenance strategies,
control maintenance expenditure, and improve overall equipment effectiveness (OEE)
and plant reliability for Operations, Maintenance, and Finance stakeholders.

## 📊 Data Source
- Integrated maintenance management system
- Historical data across multiple tables:
  - Downtime records (start/end time, cause, production loss)
  - Failure records (failure mode, severity, equipment)
  - Maintenance costs (parts, labor, other costs)
  - Inventory and spare parts data

## 🔍 Analytical Process
- **Data Modeling:** Cleaned, transformed, and structured multi-table data into a robust
  relational model linking failures, maintenance actions, costs, and inventory to equipment.
- **KPI Definition:** Defined KPIs across three pillars:
  - Impact (Total Downtime Hours, Production Loss, Cost of Downtime)
  - Reliability (Total Failures, Average Downtime per Failure – MTTR proxy)
  - Cost & Inventory (Total Maintenance Cost, Parts Cost, Inventory Value)
- **Dashboard Design:** Built a multi-page Power BI dashboard covering downtime,
  reliability, maintenance cost, and inventory management.
- **Visualization:** Used Pareto charts, donut charts, and line charts to analyze
  downtime causes, cost distribution, and failure severity patterns.
- **Interactive Analysis:** Enabled deep drill-down using slicers for equipment,
  location, cause, manufacturer, and severity.

## 📈 Key Insights
- Identified high-impact downtime causes such as wear, corrosion, and seal failure.
- Highlighted critical “bad actor” equipment with the highest cost of downtime.
- Revealed that parts cost represents the majority of total maintenance expenditure.
- Identified inventory risks with parts below reorder levels affecting reliability.

## 🛠 Tools Used
- Microsoft Power BI (Data Modeling, DAX, Interactive Dashboards)
- Microsoft Excel (Data Preparation)

