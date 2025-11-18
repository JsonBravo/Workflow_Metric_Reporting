#Required imports
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

#Methods
def plot_period_workflow_metrics(df, workflow_type = '[Describe]', period_variable = 'Period', count_variables = ['Started During', 'Completed During','Open at End'],count_colors = ['darkorange', 'forestgreen', 'maroon']):
    age_statistic_variables = ['Average Age', 'Median Age']

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # --- Bar plot for counts ---
    df.plot(
        x=period_variable,
        y=count_variables,
        kind='bar',
        ax=ax1,
        width=0.8,
        color=count_colors
    )

    # --- Line plot for age stats ---
    ax2 = ax1.twinx()
    x = range(len(df[period_variable]))

    # Plot each age statistic manually
    for col, color, marker in zip(age_statistic_variables, ['black', 'darkgrey'], ['o', 's']):
        ax2.plot(x, df[col], color=color, marker=marker, label=col)

    # --- Labeling and formatting ---
    ax1.set_xlabel('Period')
    ax1.set_ylabel('Counts')
    ax2.set_ylabel('Age (Average and Median)')
    ax1.set_xticks(x)
    ax1.tick_params(axis='x', labelrotation=65)
    ax1.set_xticklabels(df[period_variable].astype(str))  # show readable period labels

    # Legends
    ax1.legend(count_variables, loc='upper left')
    ax2.legend(age_statistic_variables, loc='upper right')

    plt.title(f'{workflow_type} - Counts and Age Statistics by Period')
    plt.tight_layout()
    plt.show()

def period_workflows_reporter(xlsx_file_location ='.', period_code = 'Q', age_code = 'D', selected_standard_columns = ['Key', 'Title/ Short Description', 'Date Started', 'Completion Date'], report_title = None, top_n_periods = None, verbose = True):
    """
    Quick Reference Example:
    period_workflows_reporter(xlsx_file_location ='.', 
                              period_code = 'Q', age_code = 'D', 
                              selected_standard_columns = ['Key', 'Title/ Short Description', 'Date Started', 'Completion Date'], 
                              top_n_periods = None, verbose = True)
    
    DOCUMENTATION:
    Given the following six (6) inputs:
        
        INPUTS:
            1. xlsx_file_location: A path to a single xlsx file to read in which has four (4) columns:
                
                COLUMNS:
                    'Key': a workflow key 
                    'Title/ Short Description': a workflow title or short description 
                    'Date Started': a workflow startdate 
                    'Completion Date': a workflow completion date (can be blank)
            
            2. period_code: A single character code to define the reporting period duration. See code options below 
            3. age_code =  A single character code to define workflow ages.
            
                CODES:              Description                 STATUS
                                    
                    B               business day frequency      [Not Implemented]
                    D               calendar day frequency      [Implemented for `age_code` only]
                    W               weekly frequency            [Not Implemented]
                    M               monthly frequency           [Not Implemented]
                    Q               quarterly frequency         [Implemented for `period_code` only]
                    Y               yearly frequency            [Not Implemented]
                    h               hourly frequency            [Not Implemented]
                    min             minutely frequency          [Not Implemented]
                    s               secondly frequency          [Not Implemented]
                
                #As you may note, not all Codes have been implemented at this time...
                #Read more about period aliases through the following link:
                    https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases:~:text=the%20end_date)-,Period%20aliases,-%23
                
            4. selected_standard_columns: Expects a list of the four (4) columns in following order:
                    ['Key', 'Title/ Short Description', 'Date Started', 'Completion Date']
                    
            5. top_n_periods: If provided, report will be limited to only the top 'n' periods in the given xlsx file data 
                (NOTE: will throw error if 'n' is greater than the total number of periods available in given xlsx data)
                
            6. verbose: If `True` then will print the following to console in a verbose report (this report is not returned, just printed):
                
                VERBOSE REPORT:
                    
                    For each period, will print the 'Key', 'Description', and 'Age' of the following:
                        -Oldest Workflow that was closed
                        -Oldest Workflow that remains open
                        -Fastest / youngest Worklflow closed
                    
                    Will print a plot of the xlsx data showing the following for each period:
                        - Count of Started Workflows During Period (yellow bar)
                        - Count of Completed Workflows During Period (green bar)
                        - Count of Workflows Open at the End of a Period (red bar)
                        - Mean average age of workflows in the period (black line)
                        - Median age of workflows in the period (gray line)
    
    ... This method returns the following DataFrame:
        
        RETURNS:
            
            1. report_df: A DataFrame with the following columns:
                
                COLUMNS:
                    
                    'Period':The period value.
                    'Open at Start': A count of open workflows at the start of the period.
                    'Started During': A count of all started workflows in the period.
                    'Completed During': A count of all completed workflows in the period.
                    'Open at End': A count of all workflows remaining open at the end of the period.
                    'Average Age': The average age of all workflows at the end of the period.
                    'Median Age': The median age of all workflows at the end of the period.
    """
    if verbose:
            print(report_title)
            
    #Load data
    file_name = xlsx_file_location
    df = pd.read_excel(file_name)
    
    #Set the table...
    standard_column_mapping = {
        #new:old
        'ID':selected_standard_columns[0],
        'Description':selected_standard_columns[1],
        'Started Datetime (UTC)':selected_standard_columns[2],
        'Completed Datetime (UTC)':selected_standard_columns[3]
    }
    df = df[standard_column_mapping.values()].copy()
    df.columns = standard_column_mapping
    
    #ensure dates are in datetime format
    df['Started Datetime (UTC)'] = pd.to_datetime(df['Started Datetime (UTC)'])
    df['Completed Datetime (UTC)'] = pd.to_datetime(df['Completed Datetime (UTC)'])
    
    #Set period columns
    df[f'Started Period ({period_code})'] = df['Started Datetime (UTC)'].dt.to_period(period_code)
    df[f'Completed Period ({period_code})'] = df['Completed Datetime (UTC)'].dt.to_period(period_code)

    #Find Period Range
    min_period = df[f'Started Period ({period_code})'].min()
    max_period = max(df[f'Started Period ({period_code})'].max(), df[f'Completed Period ({period_code})'].max())
    
    if top_n_periods:
        min_period = max_period-top_n_periods
   
    todays_period = pd.Timestamp.now().to_period(period_code)
    if todays_period == max_period: 
        # ... then set max_period to be one less, as we only want to report on completed periods...
        max_period = max_period - 1

    #build report variables
    report_data = {
        'Period':[],
        'Open at Start': [],
        'Started During':[],
        'Completed During':[],
        'Open at End':[],
        'Average Age':[],
        'Median Age':[]
    }
    oldest_workflows = {}
    fastest_workflows = {}

    reporting_periods = pd.period_range(start=min_period, end=max_period, freq=period_code)
    for reporting_period in reporting_periods:
        #print(reporting_period) # TEST

        #logics
        start_period_logic = (df[f'Started Period ({period_code})'] <= reporting_period)
        end_period_logic = ((df[f'Completed Period ({period_code})'] >= reporting_period) | (df[f'Completed Period ({period_code})'].isna()))

        #Find the open workflows
        open_workflows = df[start_period_logic & end_period_logic].copy()

        #Adjust the completed dates that are older (or still open) to be the end of the period date
        open_workflows['Last Open Date in Period'] = open_workflows['Completed Datetime (UTC)']
        open_workflows.loc[end_period_logic,'Last Open Date in Period'] = reporting_period.end_time

        #Determine age of each workflow in Period
        open_workflows['Age (days)'] = (open_workflows['Last Open Date in Period'] - open_workflows['Started Datetime (UTC)']).dt.days

        #Make a full description column
        open_workflows['ID: Description'] = open_workflows['ID']+": "+ open_workflows['Description']
        
        if verbose:
            #print the following:
            #    -Oldest Workflow that was closed
            #    -Oldest Workflow that remains open
            #    -Fastest / youngest Worklflow closed
            
            print_data = {
                '':[],
                'Workflow':[],
                'Age (days)':[]
            }
            
            print()
            print(f'Key Workflows at the end of Period {reporting_period}:')
            
            #Oldest Workflow that was closed IN THE PERIOD
            filtered = open_workflows[open_workflows[f'Completed Period ({period_code})'] == reporting_period]
            filtered = filtered[filtered['Age (days)'] == filtered['Age (days)'].max()]
            [print_data[''].append("Oldest Workflow Closed:") for x in range(0,len(filtered))]
            #print_data[''].append(("Oldest Workflow Closed:")*len(filtered))
            [print_data['Workflow'].append(x) for x in filtered['ID: Description']]
            [print_data['Age (days)'].append(x) for x in filtered['Age (days)']]
            
            #print_data['Workflow'].append(filtered['ID: Description'])
            #print_data['Age (days)'].append(filtered['Age (days)'])
            
            #Oldest Workflow that remains open
            filtered = open_workflows[(open_workflows[f'Completed Period ({period_code})'] > reporting_period) | 
                                      (open_workflows[f'Completed Period ({period_code})'].isna())
                                     ]
            filtered = filtered[filtered['Age (days)'] == filtered['Age (days)'].max()]
            [print_data[''].append("Oldest Workflow Remaining Open:") for x in range(0,len(filtered))]
            #print_data[''].append(("Oldest Workflow Remaining Open:")*len(filtered))
            [print_data['Workflow'].append(x) for x in filtered['ID: Description']]
            [print_data['Age (days)'].append(x) for x in filtered['Age (days)']]
            
            #Fastest / youngest Worklflow closed
            filtered = open_workflows[open_workflows[f'Completed Period ({period_code})'] == reporting_period]
            filtered = filtered[filtered['Age (days)'] == filtered['Age (days)'].min()]
            [print_data[''].append("Fastest / Youngest Workflow Closed:") for x in range(0,len(filtered))]
            [print_data['Workflow'].append(x) for x in filtered['ID: Description']]
            [print_data['Age (days)'].append(x) for x in filtered['Age (days)']]
            
            print_df = pd.DataFrame(print_data)
            print(tabulate(print_df, 
                           headers = "keys", 
                           tablefmt="grid", 
                           maxcolwidths=[20,60,None],
                           showindex=False
                          )
                 )
        
        #Fill in df Report Data
        report_data['Period'].append(
            reporting_period
        )
        report_data['Open at Start'].append(
            len(open_workflows[open_workflows['Started Datetime (UTC)'] < reporting_period.start_time])
        )
        report_data['Started During'].append(
            len(open_workflows[open_workflows['Started Datetime (UTC)'] >= reporting_period.start_time])
        )
        report_data['Completed During'].append(
            len(open_workflows[open_workflows['Completed Datetime (UTC)'] <= reporting_period.end_time])
        )
        report_data['Open at End'].append(
            len(open_workflows[((open_workflows[f'Completed Period ({period_code})'] > reporting_period) | 
                 (open_workflows[f'Completed Period ({period_code})'].isna()))])
        )
        report_data['Average Age'].append(
            round(open_workflows['Age (days)'].mean(),0)
        )
        report_data['Median Age'].append(
            open_workflows['Age (days)'].median()
        )    

    report_df = pd.DataFrame(report_data)
    
    if verbose:
        plot_period_workflow_metrics(report_df, report_title)

    #report_df['CHECK'] = report_df['Open at Start']+report_df['Started During']-report_df['Completed During']
    return(report_df)
    
