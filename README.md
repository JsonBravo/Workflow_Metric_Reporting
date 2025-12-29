# Workflow Metric Reporting
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d4c25232-ee14-4a1d-8679-b149305c1e9d" />

Here I provide a Python script that can be used to assist in visualizing and reporting general workflow metrics. 
<br><br>
Every industry has workflows, and this script leverages the four (4) most basic, universal aspects: workflow ID, workflow title, starting datetimes, and completed datetimes.
<br><br>
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
<img width="593" height="206" alt="image" src="https://github.com/user-attachments/assets/6e7a93b5-6761-4ab9-a3d4-51386a6cf669" />
<br>
<img width="594" height="201" alt="image" src="https://github.com/user-attachments/assets/033087b6-79ab-4876-bddf-01c233f1fd13" />
<br>
<img width="583" height="200" alt="image" src="https://github.com/user-attachments/assets/1557e9b4-b936-4b0e-92c9-2081fa6b7302" />
<br>
<img width="586" height="205" alt="image" src="https://github.com/user-attachments/assets/bcb321f8-8367-4027-a427-e3b1bfe97e84" />
<br>
<img width="549" height="203" alt="image" src="https://github.com/user-attachments/assets/2f805f9a-c7e1-4e73-9577-0562212ac707" />
<br>
<img width="562" height="207" alt="image" src="https://github.com/user-attachments/assets/3cb49e68-2a57-44c9-a85f-6f6de84f5a36" />
<br>
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/111c5d0e-d4d6-4c52-ab20-f4e3b3356a0c" />
