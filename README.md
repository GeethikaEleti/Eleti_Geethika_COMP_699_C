# Cloud Cost Leak Finder

## Overview
The **Cloud Cost Leak Finder** is a Python- and Streamlit-based tool developed by CloudOptima Solutions to automatically detect, analyze, and simulate optimizations for cloud cost inefficiencies across multi-cloud environments such as AWS, Azure, and Google Cloud Platform (GCP).  

It enables cloud administrators, IT managers, and finance analysts to upload cloud usage data, identify underutilized or misconfigured resources, and receive actionable recommendations to reduce unnecessary expenses.

---

## Key Features
- **Anomaly Detection** – Automatically identifies idle, oversized, or underutilized cloud resources.  
- **Risk Scoring** – Assigns cost impact scores based on resource inefficiencies.  
- **Savings Estimation** – Calculates potential monthly and yearly savings per resource and overall.  
- **What-if Simulations** – Allows users to simulate resizing, deleting, or consolidating resources.  
- **Multi-Cloud Comparison** – Supports cost pattern analysis across AWS, Azure, and GCP.  
- **Visual Dashboards** – Displays heatmaps, trend charts, and savings summaries.  
- **Exportable Reports** – Generates detailed PDF and CSV reports for audits and management.

---

## System Objectives
- Simplify and automate cloud cost analysis for enterprises.  
- Improve visibility into multi-cloud usage patterns.  
- Reduce manual auditing time by up to 50%.  
- Achieve up to 40% savings on cloud operational expenses.  

---

## Technology Stack
| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| Data Input | CSV Uploads |
| Visualization | Matplotlib / Plotly |
| Reporting | CSV / PDF Exports |
| Security | Role-Based Access Control (RBAC) |

---

## Functional Overview
The system supports three main user roles:
1. **Cloud Administrator** – Upload and analyze usage data, view recommendations, and simulate optimizations.  
2. **IT Manager** – Review and approve optimization actions, view organization-level reports.  
3. **Finance Analyst** – Evaluate savings projections and perform cost analysis based on different scenarios.  

---

## Non-Functional Highlights
- Optimized for datasets up to **500MB**  
- Supports up to **1,000 concurrent users**  
- Delivers reports and dashboards in **under 10 seconds**  
- **99.9% uptime** (excluding maintenance windows)  
- Fully **responsive interface** for desktop and tablet browsers  

---

## Installation and Setup
1. **Clone the Repository**
   git clone https://github.com/<your-username>/cloud-cost-leak-finder.git
   cd cloud-cost-leak-finder

2. **Install Dependencies**
   pip install -r requirements.txt

3. **Run the Application**
   streamlit run app.py

4. **Upload a Sample CSV**
   Use mock cloud usage data (VMs, storage, snapshots) to view anomaly detection and savings reports.
