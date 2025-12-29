# Workflow Metric Reporting
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d4c25232-ee14-4a1d-8679-b149305c1e9d" />
Here I provide a Python script that can be used to assist in visualizing and reporting general workflow metrics. 
<br><br>

Every industry has workflows, and this script leverages the four (4) most basic, universal aspects: workflow ID, workflow title, starting datetimes, and completed datetimes.
<br><br>

## EXAMPLE:
<br>
Input (Excel Spreadsheet): <br>
<img width="574" height="376" alt="image" src="https://github.com/user-attachments/assets/f7e14857-6eab-4fc1-880e-84bcbcdde94b" />
<br><br>

Script (see `period_reporting_notebook`): <br>
<img width="984" height="171" alt="image" src="https://github.com/user-attachments/assets/52c3b5e9-cbe2-4fd0-8127-9204f02f265a" />
 <br>
`file_location = xlsx_files[0]` <br>
`report_title = "Mock General Issues"` <br>
`select_columns = ['Workflow ID','Workflow Description','Start Datetime','Completed Datetime']` <br>
`df = pr.period_workflows_reporter(file_location, selected_standard_columns = select_columns, report_title=report_title)` <br>
<br>

Output (see `period_reporting_notebook`): <br>
Mock General Issues
<br>
<img width="558" height="208" alt="image" src="https://github.com/user-attachments/assets/0e724142-3a4d-4902-9b80-e07a0c68c68a" />
<br>
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/111c5d0e-d4d6-4c52-ab20-f4e3b3356a0c" />
<br> 

`print(df)`
<br> 
<img width="575" height="164" alt="image" src="https://github.com/user-attachments/assets/cdbac50a-41d9-467a-803d-d05c1317cab8" />


