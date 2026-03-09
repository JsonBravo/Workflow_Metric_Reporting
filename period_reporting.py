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

def period_workflows_reporter(
    xlsx_file_location='.',
    period_code='Q',             # pandas frequency alias (e.g. 'D','W','W-MON','M','Q','Y',etc.)
    age_code='D',
    selected_standard_columns=None,
    report_title=None,
    top_n_periods=None,
    verbose=True,
    week_anchor='MON',            # optional day name to anchor weeks when using 'W'
    include_current_period=False
):
    """
    This is a period workflow reporting function able to handle arbitrary time periods.

    The function allows for any alias recognised by :func:`pandas.Period` may be supplied.  
    The special ``week_anchor`` argument allows callers to request e.g. ``'MON'``
    semantics without needing to know the pandas notation.

    Parameters
    ----------
    xlsx_file_location : str
        Path to the Excel workbook containing references to the four standard columns 
        (order of the references matter)
            1. ``Key``
            2. ``Title/ Short Description``
            3. ``Date Started``
            4. ``Completion Date``
        If ``selected_standard_columns`` is omitted it defaults to this list (see below).
    
    period_code : str
        Pandas frequency alias used for ``.dt.to_period()``.  
        Examples:
            ``'D'`` (calendar day)
            ``'W'`` (weeks ending on Sunday)
            ``'W-MON'`` (weeks ending on Monday)
            ``'M'`` (monthly) 
            ``'Q'`` (quarterly)
            ``'Y'`` (yearly)
    
    age_code : str
        Alias describing how age is measured; currently only ``'D'`` is used.
    
    selected_standard_columns : list[str]
        Four‑element list giving the column names in the workbook; order is
        ``[
            'Key',
            'Title/ Short Description',
            'Date Started',
            'Completion Date'
        ]``.
        If ``None`` this above default is used.
    
    report_title : str, optional
        Printed heading when ``verbose`` is ``True``.
    
    top_n_periods : int, optional
        When provided, only the most recent *n* completed periods are
        returned.  This is implemented by slicing the period range instead of
        relying on arithmetic with ``Period`` objects.
    
    verbose : bool
        If ``True`` the detailed console output and the plot are emitted.
    
    week_anchor : str, optional
        When ``period_code`` is ``'W'``, this value (e.g. ``'MON'`` or
        ``'SUN'``) will be appended to form the actual frequency string.

    Returns
    -------
    pandas.DataFrame
        Columns: ``['Period','Open at Start','Started During',
        'Completed During','Open at End','Average Age','Median Age']``.
    """

    if selected_standard_columns is None:
        selected_standard_columns = ['Key', 'Title/ Short Description',
                                     'Date Started', 'Completion Date']

    if verbose:
        print(report_title)

    # --- read & normalise data ------------------------------------------------
    df = pd.read_excel(xlsx_file_location)

    standard_column_mapping = {
        'ID': selected_standard_columns[0],
        'Description': selected_standard_columns[1],
        'Started Datetime (UTC)': selected_standard_columns[2],
        'Completed Datetime (UTC)': selected_standard_columns[3]
    }
    df = df[list(standard_column_mapping.values())].copy()
    df.columns = standard_column_mapping

    df['Started Datetime (UTC)'] = pd.to_datetime(df['Started Datetime (UTC)'])
    df['Completed Datetime (UTC)'] = pd.to_datetime(df['Completed Datetime (UTC)'])

    # --- build the effective frequency string -------------------------------
    freq = period_code.upper()
    if freq == 'W' and week_anchor:
        freq = f'W-{week_anchor.upper()}'

    # validate the freq by trying a conversion (pandas will raise if unknown)
    try:
        pd.Timestamp.now().to_period(freq)
    except Exception as exc:  # pragma: no cover - defensive
        raise ValueError(f"unsupported period_code '{freq}'") from exc

    # add period columns to the dataframe
    df[f'Started Period ({freq})'] = df['Started Datetime (UTC)'].dt.to_period(freq)
    df[f'Completed Period ({freq})'] = df['Completed Datetime (UTC)'].dt.to_period(freq)

    # --- determine range of completed periods -------------------------------
    min_period = df[f'Started Period ({freq})'].min()
    max_period = max(df[f'Started Period ({freq})'].max(),
                     df[f'Completed Period ({freq})'].max())

    todays_period = pd.Timestamp.now().to_period(freq)
    if (include_current_period):
        max_period = max(max_period, todays_period)
        
    reporting_periods = pd.period_range(start=min_period, end=max_period, freq=freq)

    if (include_current_period == False):
        # drop the current (incomplete) period if present
        if len(reporting_periods) and reporting_periods[-1] == todays_period:
            reporting_periods = reporting_periods[:-1]

    if top_n_periods is not None:
        reporting_periods = reporting_periods[-top_n_periods:]

    # --- accumulate metrics --------------------------------------------------
    report_data = {k: [] for k in ['Period', 'Open at Start', 'Started During',
                                   'Completed During', 'Open at End',
                                   'Average Age', 'Median Age']}

    for i,rp in enumerate(reporting_periods):
        start_dt = rp.start_time
        end_dt = rp.end_time

        start_logic = df[f'Started Period ({freq})'] <= rp
        end_logic = ((df[f'Completed Period ({freq})'] >= rp) |
                     df[f'Completed Period ({freq})'].isna())

        open_workflows = df[start_logic & end_logic].copy()
        open_workflows['Last Open Date in Period'] = open_workflows['Completed Datetime (UTC)']
        open_workflows.loc[end_logic, 'Last Open Date in Period'] = end_dt
        open_workflows['Age (days)'] = (
            open_workflows['Last Open Date in Period'] -
            open_workflows['Started Datetime (UTC)']).dt.days
        open_workflows['ID: Description'] = (
            open_workflows['ID'] + ': ' + open_workflows['Description'])

        if verbose:
            _print_verbose_period(rp, open_workflows, freq)
            # also dump full lists of completed and still‑open workflows for this period
            if(i==len(reporting_periods)-1):  # only print the full lists for the most recent period to avoid overwhelming the console
                _print_verbose_status_lists(rp, open_workflows, freq)

        report_data['Period'].append(rp)
        report_data['Open at Start'].append(
            len(open_workflows[open_workflows['Started Datetime (UTC)'] < start_dt]))
        report_data['Started During'].append(
            len(open_workflows[open_workflows['Started Datetime (UTC)'] >= start_dt]))
        report_data['Completed During'].append(
            len(open_workflows[open_workflows['Completed Datetime (UTC)'] <= end_dt]))
        report_data['Open at End'].append(
            len(open_workflows[((open_workflows[f'Completed Period ({freq})'] > rp) |
                               open_workflows[f'Completed Period ({freq})'].isna())]))
        report_data['Average Age'].append(round(open_workflows['Age (days)'].mean(), 0))
        report_data['Median Age'].append(open_workflows['Age (days)'].median())

    report_df = pd.DataFrame(report_data)

    if verbose:
        plot_period_workflow_metrics(report_df, report_title)

    return report_df


def _print_verbose_period(reporting_period, open_workflows, freq):
    """Helper used by :func:`period_workflows_reporter` for verbose output.

    The existing implementation reports a small set of interesting workflows
    (oldest closed, oldest still open, fastest closed) in a compact table.
    """
    print()
    print(f'Key Workflows at the end of Period {reporting_period}:')
    print_data = {'': [], 'Workflow': [], 'Age (days)': []}

    # oldest closed
    filt = open_workflows[open_workflows[f'Completed Period ({freq})'] == reporting_period]
    if not filt.empty:
        oldest = filt[filt['Age (days)'] == filt['Age (days)'].max()]
        for _, row in oldest.iterrows():
            print_data[''].append('Oldest Workflow Closed:')
            print_data['Workflow'].append(row['ID: Description'])
            print_data['Age (days)'].append(row['Age (days)'])

    # oldest still open
    filt = open_workflows[((open_workflows[f'Completed Period ({freq})'] > reporting_period) |
                           open_workflows[f'Completed Period ({freq})'].isna())]
    if not filt.empty:
        oldest = filt[filt['Age (days)'] == filt['Age (days)'].max()]
        for _, row in oldest.iterrows():
            print_data[''].append('Oldest Workflow Remaining Open:')
            print_data['Workflow'].append(row['ID: Description'])
            print_data['Age (days)'].append(row['Age (days)'])

    # fastest closed
    filt = open_workflows[open_workflows[f'Completed Period ({freq})'] == reporting_period]
    if not filt.empty:
        youngest = filt[filt['Age (days)'] == filt['Age (days)'].min()]
        for _, row in youngest.iterrows():
            print_data[''].append('Fastest / Youngest Workflow Closed:')
            print_data['Workflow'].append(row['ID: Description'])
            print_data['Age (days)'].append(row['Age (days)'])

    print(tabulate(pd.DataFrame(print_data),
                   headers='keys',
                   tablefmt='grid',
                   maxcolwidths=[20, 60, None],
                   showindex=False))


def _print_verbose_status_lists(reporting_period, open_workflows, freq):
    """Print a detailed list of all workflows split by status.

    The first section contains workflows that completed within the
    ``reporting_period``; the second section shows those which remain open
    (either completing in a later period or with a missing completion date).
    This is useful for debugging or when the caller wants the full dataset
    rather than just the summary rows produced by :func:`_print_verbose_period`.
    """
    print()
    print(f'All workflows for Period {reporting_period}:')

    completed = open_workflows[open_workflows[f'Completed Period ({freq})'] == reporting_period].copy()
    if not completed.empty:
        completed["Completed Date"] = completed["Completed Datetime (UTC)"].dt.strftime('%Y-%m-%d')
        completed = completed.sort_values('Completed Datetime (UTC)')
        print('Completed workflows:')
        print(tabulate(
            completed[['ID: Description', 'Completed Date', 'Age (days)']],
            headers=['Workflow', 'Completed Date', 'Age (days)'],
            tablefmt='grid',
            showindex=False,
            maxcolwidths=[60, None]
        ))
    else:
        print('No workflows completed during this period.')

    still_open = open_workflows[((open_workflows[f'Completed Period ({freq})'] > reporting_period) |
                                open_workflows[f'Completed Period ({freq})'].isna())].copy()
    if not still_open.empty:
        still_open["Started Date"] = still_open["Started Datetime (UTC)"].dt.strftime('%Y-%m-%d')
        still_open = still_open.sort_values('Started Datetime (UTC)')
        print('\nStill-open workflows:')
        print(tabulate(
            still_open[['ID: Description', 'Started Date', 'Age (days)']],
            headers=['Workflow', 'Started Date', 'Age (days)'],
            tablefmt='grid',
            showindex=False,
            maxcolwidths=[60, None]
        ))
    else:
        print('No workflows remain open at end of this period.')

    
