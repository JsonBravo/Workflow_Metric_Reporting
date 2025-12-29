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
`file_location = xlsx_files[0]`
`report_title = "Mock General Issues"`
`select_columns = ['Workflow ID','Workflow Description','Start Datetime','Completed Datetime']`
`df = pr.period_workflows_reporter(file_location, selected_standard_columns = select_columns, report_title=report_title)`
