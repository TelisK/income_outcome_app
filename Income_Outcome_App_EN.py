import streamlit as st
import datetime
import sqlite3
import pandas as pd
import altair as alt


tabs = ['Record Income','Record Expenses','Show Totals','Show Statistics']
tab1, tab2, tab3, tab4 = st.tabs(tabs)

conn = sqlite3.connect('income_outcome.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS income (
            date TEXT PRIMARY KEY UNIQUE NOT NULL,
            income_cash FLOAT NOT NULL,
            income_pos FLOAT NOT NULL,
            income FLOAT NOT NULL)''')
cur.execute('''CREATE TABLE IF NOT EXISTS outcome (
            date TEXT PRIMARY KEY UNIQUE NOT NULL,
            outcome FLOAT NOT NULL)''')


with tab1:
    sql_cash_and_pos = 0
    sql_date_input = st.date_input("Please select or type the entry date", key=1, format="DD-MM-YYYY", value=datetime.datetime.today())
    sql_date = sql_date_input.strftime("%d-%m-%Y")
    day_tab1 = sql_date_input.strftime("%A")
    st.write("The selected date is:", day_tab1, sql_date)

    # Checking if there is an entry with the same date. If there is one, i show the results and i am informing the user that if he makes a new entry, the old record will be deleted
    cur.execute('SELECT * FROM income WHERE date = ?', (sql_date,))
    rows = cur.fetchall()
    db_result = []
    if rows:
        for row in rows:
            db_result.append(row)
        st.warning(f'An entry was found for the date: {row[0]} : Cash: {row[1]} €, POS: {row[2]} €, Total: {row[3]} €')
        st.error('ATTENTION!!! With a new entry the old record will be deleted!!!')

    else:
        st.write(f'No income record found for the date: {sql_date}')

    # Data Entry
    st.divider()
    sql_cash = st.number_input('Cash:', value=None, min_value=0.0, placeholder='Please enter an amount:')
    st.divider()
    sql_pos = st.number_input('Card:', value=None, min_value=0.0, placeholder='Please enter an amount:')
    st.divider()
    if sql_cash and sql_pos:
        sql_cash_and_pos = st.number_input('Total:', value=sql_cash + sql_pos)
    if sql_cash_and_pos and sql_pos and sql_cash:
        if st.button('Record Income', key=4):
            cur.execute('INSERT OR REPLACE INTO income (date, income_cash, income_pos, income) VALUES (?,?,?,?)', (sql_date,sql_cash,sql_pos,sql_cash_and_pos))
            conn.commit()
            st.success('Saved successfully')

with tab2:
    sql_expences_date_input = st.date_input("Please select or enter the entry date",key=2, format="DD-MM-YYYY", value=datetime.datetime.today())
    sql_expences_date = sql_expences_date_input.strftime("%d-%m-%Y")
    day_tab2 = sql_expences_date_input.strftime("%A")
    st.write("The selected date is:", day_tab2, sql_expences_date)

    # Checking if there is an entry with the same date. If there is one, i show the results and i am informing the user that if he makes a new entry, the old record will be deleted
    cur.execute('SELECT * FROM outcome WHERE date = ?', (sql_expences_date,))
    rows = cur.fetchall()
    db_outcome_result = []
    if rows:
        for row in rows:
            db_outcome_result.append(row)
        st.warning(f'An entry was found for the date {row[0]} : Expenses: {row[1]} €')
        st.error('ATTENTION!!! With a new entry the old record will be deleted!!!')

    else:
        st.write(f'No expense record found for the date {sql_expences_date}')

    # Data Entry
    st.divider()
    sql_expences = st.number_input('Expense Entry', value=None, min_value=0.0, placeholder='Please enter an amount:')
    if st.button('Record Expense', key=6):
        cur.execute('INSERT OR REPLACE INTO outcome (date, outcome) VALUES (?,?)', (sql_expences_date,sql_expences))
        conn.commit()
        st.success('Saved successfully')

with tab3:
    sum_dates_input = st.date_input('Please specify a period:', (datetime.datetime.today(), datetime.datetime.today()), format='DD-MM-YYYY', key=7)
    if len(sum_dates_input) != 2: # I check if both dates are selected; otherwise, an error is shown until the second date is selected.
        st.stop()
    sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
    sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
    st.write(f'You have selected the dates {sum_date1} - {sum_date2}')
    if st.button('Show', key=9):
        cur.execute("SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?", (sum_date1, sum_date2))
        sum_date = list()
        sum_cash = list()
        sum_pos = list()
        sum_cash_pos = list()
        sum_outcome = list()
        st.write('View in detail: ')
        for row in cur.fetchall():
            sum_date.append(row[0])
            sum_cash.append(row[1])
            sum_pos.append(row[2])
            sum_cash_pos.append(row[3])
            if row[4] == None:
                sum_outcome.append(0)
            else:
                sum_outcome.append(row[4])
            st.write(f'{row[0]} -> Cash: {row[1]} € | Card: {row[2]} € | Total: {row[3]} € | Expenses: {row[4] if row[4] is not None else 0} €')

        st.divider()
        st.write('Total: ')
        st.write(f'Cash: {sum(sum_cash)} €')
        st.write(f'Card: {sum(sum_pos)} €')

        try:
            result_avg = (sum(sum_cash_pos))/len(sum_cash_pos) # Add a filter for the average to avoid division by zero errors when selecting dates without entries.
        except ZeroDivisionError:
            result_avg = 0
        st.write(f'Total Receipts: {sum(sum_cash_pos)} €, Daily average: {result_avg:.2f} €')
        st.write(f'Expenses : {sum(sum_outcome)} €')

with tab4:

    col1, col2 = st.columns(2)
    with col1:
        radio_select_1 = st.radio('Select Period:',
                 ['Select Dates', 'By Month', 'By Year'])
    with col2:
        radio_select_2 = st.radio('Select Income - Expenses',
                 ['Income - Expenses','Income Only','Expenses Only'])

    if radio_select_1 == 'Select Dates':
        if radio_select_2 == 'Income - Expenses':

            sum_dates_input = st.date_input('Select Period:', (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=8)
            if len(sum_dates_input) != 2: # I check if both dates are selected; otherwise, an error is shown until the second date is selected.
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Selected Period: {sum_date1} - {sum_date2}')
            if st.button('Show', key=10):
                sql_df = cur.execute("SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?", (sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Titles
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)


                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)


                income_chart = alt.Chart(df_filtered).mark_bar(color='blue', opacity=1).encode(x='date', y='income') #Two different charts for income and expenses
                outcome_chart = alt.Chart(df_filtered).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome') # Problem, when i select dates it shows hours too
                final_chart = alt.layer(income_chart, outcome_chart) # Layer connects the charts
                st.altair_chart(final_chart, use_container_width=True)

        if radio_select_2 == 'Income Only':

            sum_dates_input = st.date_input('Select Period:', (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=16)
            if len(sum_dates_input) != 2:  # I check if both dates are selected; otherwise, an error is shown until the second date is selected.
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Selected Period: {sum_date1} - {sum_date2}')
            if st.button('Show', key=17):
                sql_df = cur.execute(
                    "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?",
                    (sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Titles
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)

                dates_income_chart = alt.Chart(df_filtered).mark_bar().encode(x='date', y='income')
                st.altair_chart(dates_income_chart, use_container_width=True)

        if radio_select_2 == 'Expenses Only':
            sum_dates_input = st.date_input('Select Period:',
                                            (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=18)
            if len(sum_dates_input) != 2: # I check if both dates are selected; otherwise, an error is shown until the second date is selected.
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Selected Period: {sum_date1} - {sum_date2}')
            if st.button('Show', key=19):
                sql_df = cur.execute(
                    "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?",
                    (sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Titles
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)

                dates_outcome_chart = alt.Chart(df_filtered).mark_bar(color='red').encode(x='date', y='outcome')
                st.altair_chart(dates_outcome_chart, use_container_width=True)

    if radio_select_1 == 'By Month':
        sql_df = cur.execute(
            "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date")
        sql_columns = [description[0] for description in sql_df.description]  # Titles
        df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        #st.dataframe(df, hide_index=True)
        df['Month'] = df['date'].dt.month
        df['Year'] = df['date'].dt.year

        years = sorted(df['Year'].unique())  #  Available years from Dataframe
        selected_year = st.radio('Select Year:', years, horizontal=True)

        df_year = df[df['Year'] == selected_year]
        months = sorted(df_year['Month'].unique())  # Available Months with data by year

        if radio_select_2 == 'Income - Expenses':
            radio_select_compare = st.radio('Compare Months?',
                                            ['No', 'Yes'])
            st.divider()

            if radio_select_compare == 'No':
                #st.dataframe(df_year, hide_index=True)
                selected_month = st.radio('Select Month',months ,key=13)
                df_per_month = df_year[df_year['Month'] == selected_month]

                per_month_income_chart = alt.Chart(df_per_month).mark_bar(color='blue', opacity=1).encode(x='date',
                                                                                      y='income')  # Two different Charts
                per_month_outcome_chart = alt.Chart(df_per_month).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome')
                per_month_final_chart = alt.layer(per_month_income_chart, per_month_outcome_chart)  # layer connects the charts
                st.altair_chart(per_month_final_chart, use_container_width=True)


            if radio_select_compare == 'Yes':
                col_comp1, col_comp2 = st.columns(2)

                with col_comp1:
                    selected_month1 = st.radio('Select First Month',months ,key=11)

                with col_comp2:
                    selected_month2 = st.radio('Select Second Month',months ,key=12)

                df_compare_months = df_year[df_year['Month'].isin([selected_month1, selected_month2])]

                compare_month_income_chart = alt.Chart(df_compare_months).mark_bar(opacity=0.6).encode(x='date',
                                                                                                          y='income', color='Month:N')
                compare_month_outcome_chart = alt.Chart(df_compare_months).mark_bar(opacity=0.3).encode(x='date',
                                                                                                            y='outcome', color='Month:N') # Color at encode, to give different color by month
                compare_month_final_chart = alt.layer(compare_month_income_chart,
                                                  compare_month_outcome_chart)  # Layer connects the charts
                st.altair_chart(compare_month_final_chart, use_container_width=True)

        if radio_select_2 == 'Income Only':
            selected_month_income = st.radio('Select Month', months, key=14)
            df_per_month = df_year[df_year['Month'] == selected_month_income]

            month_income_chart = alt.Chart(df_per_month).mark_bar(color='green').encode(x='date', y='income')
            st.altair_chart(month_income_chart, use_container_width=True)

        if radio_select_2 == 'Expenses Only':
            selected_month_outcome = st.radio('Select Month', months, key=15)
            df_per_month = df_year[df_year['Month'] == selected_month_outcome]

            month_outcome_chart = alt.Chart(df_per_month).mark_bar(color='orange').encode(x='date', y='outcome')
            st.altair_chart(month_outcome_chart, use_container_width=True)

    if radio_select_1 == 'By Year':
        sql_df = cur.execute(
            "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date")
        sql_columns = [description[0] for description in sql_df.description]  # Titles
        df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df['Month'] = df['date'].dt.month
        df['Year'] = df['date'].dt.year

        years = sorted(df['Year'].unique())  # Available Years from Dataframe
        selected_year = st.radio('Select Year:', years, horizontal=True)

        df_year = df[df['Year'] == selected_year]

        if radio_select_2 == 'Income - Expenses':

            per_year_income_chart = alt.Chart(df_year).mark_bar(color='green', opacity=1).encode(x='date', y='income')  # Πρεπει να κάνω δύο διαφορετικά charts για να εμφανίσει έσοδα και έξοδα
            per_year_outcome_chart = alt.Chart(df_year).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome')
            per_year_final_chart = alt.layer(per_year_income_chart, per_year_outcome_chart)  # Το layer ενώνει τα charts
            st.altair_chart(per_year_final_chart, use_container_width=True)

        if radio_select_2 == 'Income Only':

            year_income_chart = alt.Chart(df_year).mark_bar(color='green').encode(x='date', y='income')
            st.altair_chart(year_income_chart, use_container_width=True)

        if radio_select_2 == 'Expenses Only':

            year_outcome_chart = alt.Chart(df_year).mark_bar(color='red').encode(x='date', y='outcome')
            st.altair_chart(year_outcome_chart, use_container_width=True)


if 'income_outcome.db' in conn.execute('PRAGMA database_list').fetchone()[2]:
    conn.close()


