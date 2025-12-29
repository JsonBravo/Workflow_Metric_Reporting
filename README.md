# Workflow Metric Reporting
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d4c25232-ee14-4a1d-8679-b149305c1e9d" />

Here I provide a Python script that can be used to assist in visualizing and reporting general workflow metrics. 
<br>
Every industry has workflows, and this script leverages the four (4) most basic, universal aspects: workflow ID, workflow title, starting datetimes, and completed datetimes.
<br>
EXAMPLE:
<br>
Input (Excel Spreadsheet): <br>
<img width="574" height="376" alt="image" src="https://github.com/user-attachments/assets/f7e14857-6eab-4fc1-880e-84bcbcdde94b" />
<br><br>
Script (see `period_reporting_notebook`): <br>
`file_location = xlsx_files[0]` <br>
`report_title = "Mock General Issues"` <br>
`select_columns = ['Workflow ID','Workflow Description','Start Datetime','Completed Datetime']` <br>
`df = pr.period_workflows_reporter(file_location, selected_standard_columns = select_columns, report_title=report_title)` <br>

<br>
Output (see `period_reporting_notebook`): <br>
<br>
 Mock General Issues<br>

Key Workflows at the end of Period 2024Q1:<br>
+--------------------+----------------------------------------------+--------------+<br>
|                    | Workflow                                     |   Age (days) |<br>
+====================+==============================================+==============+<br>
| Oldest Workflow    | GI-001: Supply chain delay investigation     |           87 |<br>
| Closed:            |                                              |              |<br>
+--------------------+----------------------------------------------+--------------+<br>
| Oldest Workflow    | GI-011: Packaging defect investigation       |           38 |<br>
| Remaining Open:    |                                              |              |<br>
+--------------------+----------------------------------------------+--------------+<br>
| Fastest / Youngest | GI-010: Customer service response time study |           46 |<br>
| Workflow Closed:   |                                              |              |<br>
+--------------------+----------------------------------------------+--------------+<br>
<br>
Key Workflows at the end of Period 2024Q2:<br>
+--------------------+---------------------------------------------+--------------+<br>
|                    | Workflow                                    |   Age (days) |<br>
+====================+=============================================+==============+<br>
| Oldest Workflow    | GI-011: Packaging defect investigation      |          129 |<br>
| Closed:            |                                             |              |<br>
+--------------------+---------------------------------------------+--------------+<br>
| Oldest Workflow    | GI-028: Maintenance backlog deep-dive       |           41 |<br>
| Remaining Open:    |                                             |              |<br>
+--------------------+---------------------------------------------+--------------+<br>
| Fastest / Youngest | GI-027: Product spec variance investigation |           47 |<br>
| Workflow Closed:   |                                             |              |<br>
+--------------------+---------------------------------------------+--------------+<br>
<br>
Key Workflows at the end of Period 2024Q3:<br>
+--------------------+--------------------------------------------+--------------+<br>
|                    | Workflow                                   |   Age (days) |<br>
+====================+============================================+==============+<br>
| Oldest Workflow    | GI-028: Maintenance backlog deep-dive      |          133 |<br>
| Closed:            |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>
| Oldest Workflow    | GI-043: Unexpected customer churn analysis |           51 |<br>
| Remaining Open:    |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>
| Fastest / Youngest | GI-045: Supplier performance audit         |           42 |<br>
| Workflow Closed:   |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>

Key Workflows at the end of Period 2024Q4:
+--------------------+--------------------------------------------+--------------+<br>
|                    | Workflow                                   |   Age (days) |<br>
+====================+============================================+==============+<br>
| Oldest Workflow    | GI-043: Unexpected customer churn analysis |          143 |<br>
| Closed:            |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>
| Oldest Workflow    | GI-060: Unplanned outage post-mortem       |           59 |<br>
| Remaining Open:    |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>
| Fastest / Youngest | GI-059: System access provisioning issues  |           64 |<br>
| Workflow Closed:   |                                            |              |<br>
+--------------------+--------------------------------------------+--------------+<br>

Key Workflows at the end of Period 2025Q1:<br>
+--------------------+---------------------------------------+--------------+<br>
|                    | Workflow                              |   Age (days) |<br>
+====================+=======================================+==============+<br>
| Oldest Workflow    | GI-060: Unplanned outage post-mortem  |          149 |<br>
| Closed:            |                                       |              |<br>
+--------------------+---------------------------------------+--------------+<br>
| Oldest Workflow    | GI-081: Shipping documentation errors |           49 |<br>
| Remaining Open:    |                                       |              |<br>
+--------------------+---------------------------------------+--------------+<br>
| Fastest / Youngest | GI-080: EHS internal audit follow-up  |           55 |<br>
| Workflow Closed:   |                                       |              |<br>
+--------------------+---------------------------------------+--------------+<br>
<br>
Key Workflows at the end of Period 2025Q2:<br>
+--------------------+-----------------------------------------+--------------+<br>
|                    | Workflow                                |   Age (days) |<br>
+====================+=========================================+==============+<br>
| Oldest Workflow    | GI-081: Shipping documentation errors   |          140 |<br>
| Closed:            |                                         |              |<br>
+--------------------+-----------------------------------------+--------------+<br>
| Oldest Workflow    | GI-083: Declining throughput in plant 2 |          130 |<br>
| Remaining Open:    |                                         |              |<br>
+--------------------+-----------------------------------------+--------------+<br>
| Fastest / Youngest | GI-098: Customer onboarding errors      |           55 |<br>
| Workflow Closed:   |                                         |              |<br>
+--------------------+-----------------------------------------+--------------+<br>
<br>
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/111c5d0e-d4d6-4c52-ab20-f4e3b3356a0c" />
