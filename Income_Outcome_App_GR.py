import streamlit as st
import datetime
import sqlite3
import pandas as pd
import altair as alt


tabs = ['Καταχώρηση Εσόδων','Καταχώρηση Εξόδων','Εμφάνιση Συνόλων','Εμφάνιση Στατιστικών']
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

days_gr = {'Monday' : 'Δευτέρα',
           'Tuesday' : 'Τρίτη',
           'Wednesday' : 'Τετάρτη',
           'Thursday' : 'Πέμπτη',
           'Friday' : 'Παρασκευή',
           'Saturday' : 'Σάββατο',
           'Sunday' : 'Κυριακή'}

with tab1:
    sql_cash_and_pos = 0
    sql_date_input = st.date_input("Επέλεξε ή καταχώρησε ημερομηνία καταχώρησης", key=1, format="DD-MM-YYYY", value=datetime.datetime.today())
    sql_date = sql_date_input.strftime("%d-%m-%Y")
    day_tab1 = days_gr[sql_date_input.strftime("%A")]
    st.write("Η επιλεγμένη ημερομηνία είναι:", day_tab1, sql_date)

    # Ελέγχω εάν υπάρχει ήδη καταχώρηση στη βάση με την ίδια ημερομηνία. Εάν ναί δίνω εμφανίζω τα αποτελέσματα, και ενημερώνω τον χρήστη οτι θα διαγραφεί η εγγραφή εάν κάνει νέα καταχώρηση.
    cur.execute('SELECT * FROM income WHERE date = ?', (sql_date,))
    rows = cur.fetchall()
    db_result = []
    if rows:
        for row in rows:
            db_result.append(row)
        st.warning(f'Βρέθηκε καταχώρηση για την ημερομηνία {row[0]} : Μετρητά: {row[1]} €, Εισπράξεις POS: {row[2]} €, Σύνολο Εισπράξεων: {row[3]} €')
        st.error('ΠΡΟΣΟΧΗ!!! Με νέα καταχώρηση θα διαγραφεί η παλιά καταχώρηση!!!')

    else:
        st.write(f'Δέν βρέθηκε καταχώρηση εσόδων για την ημερομηνία {sql_date}')

    # Καταχώρηση στοιχείων
    st.divider()
    sql_cash = st.number_input('Είσπραξη μετρητών:', value=None, min_value=0.0, placeholder='Δώσε ποσό:')
    st.divider()
    sql_pos = st.number_input('Είσπραξη με κάρτα:', value=None, min_value=0.0, placeholder='Δώσε ποσό:')
    st.divider()
    if sql_cash and sql_pos:
        sql_cash_and_pos = st.number_input('Σύνολο:', value=sql_cash + sql_pos)
    if sql_cash_and_pos and sql_pos and sql_cash:
        if st.button('Καταχώρηση Εσόδων', key=4):
            cur.execute('INSERT OR REPLACE INTO income (date, income_cash, income_pos, income) VALUES (?,?,?,?)', (sql_date,sql_cash,sql_pos,sql_cash_and_pos))
            conn.commit()
            st.success('Έγινε καταχώρηση')
            #st.stop()

with tab2:
    sql_expences_date_input = st.date_input("Επέλεξε ή καταχώρησε ημερομηνία καταχώρησης",key=2, format="DD-MM-YYYY", value=datetime.datetime.today())
    sql_expences_date = sql_expences_date_input.strftime("%d-%m-%Y")
    day_tab2 = sql_expences_date_input.strftime("%A")
    st.write("Η επιλεγμένη ημερομηνία είναι:", day_tab2, sql_expences_date)

    # Ελέγχω εάν υπάρχει ήδη καταχώρηση στη βάση με την ίδια ημερομηνία. Εάν ναί δίνω εμφανίζω τα αποτελέσματα, και ρωτάω τον χρήστη εάν θέλει να κάνει διαγραφή και καταχώρηση νέων στοιχείων
    cur.execute('SELECT * FROM outcome WHERE date = ?', (sql_expences_date,))
    rows = cur.fetchall()
    db_outcome_result = []
    if rows:
        for row in rows:
            db_outcome_result.append(row)
        st.warning(f'Βρέθηκε καταχώρηση για την ημερομηνία {row[0]} : Έξοδα: {row[1]} €')
        st.error('ΠΡΟΣΟΧΗ!!! Με νέα καταχώρηση θα διαγραφεί η παλιά καταχώρηση!!!')

    else:
        st.write(f'Δέν βρέθηκε καταχώρηση εξόδων για την ημερομηνία {sql_expences_date}')

    # Καταχώρηση στοιχείων
    st.divider()
    sql_expences = st.number_input('Καταχώρηση εξόδων', value=None, min_value=0.0, placeholder='Δώσε ποσό:')
    if st.button('Καταχώρηση Εξόδων', key=6):
        cur.execute('INSERT OR REPLACE INTO outcome (date, outcome) VALUES (?,?)', (sql_expences_date,sql_expences))
        conn.commit()
        st.success('Έγινε καταχώρηση')
        #st.stop()

with tab3:
    sum_dates_input = st.date_input('Δώσε μας περίοδο:', (datetime.datetime.today(), datetime.datetime.today()), format='DD-MM-YYYY', key=7)
    if len(sum_dates_input) != 2: # Ελέγχω εάν είναι επιλεγμένες και οι δύο ημερομηνίες, αλλιώς βγάζει σφάλμα μέχρι να επιλέξω τη δεύτερη
        st.stop()
    sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
    sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
    st.write(f'Επέλεξες τις ημερομηνίες {sum_date1} - {sum_date2}')
    if st.button('Εμφάνιση', key=9):
        cur.execute("""
            SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome
            FROM income
            LEFT JOIN outcome ON income.date = outcome.date
            WHERE income.date BETWEEN ? AND ?

            UNION

            SELECT outcome.date, income.income_cash, income.income_pos, income.income, outcome.outcome
            FROM outcome
            LEFT JOIN income ON income.date = outcome.date
            WHERE outcome.date BETWEEN ? AND ?
            """, (sum_date1, sum_date2, sum_date1, sum_date2))
        sum_date = list()
        sum_cash = list()
        sum_pos = list()
        sum_cash_pos = list()
        sum_outcome = list()
        st.write('Αναλυτικά: ')
        for row in cur.fetchall():
            sum_date.append(row[0])
            if row[1] == None:
                sum_cash.append(0)
            else:
                sum_cash.append(row[1])
            if row[2] == None:
                sum_pos.append(0)
            else:
                sum_pos.append(row[2])
            if row[3] == None:
                sum_cash_pos.append(0)
            else:
                sum_cash_pos.append(row[3])
            if row[4] == None:
                sum_outcome.append(0)
            else:
                sum_outcome.append(row[4])
            st.write(f'{row[0]} -> Μετρητά: {row[1] if row[1] is not None else 0} € | Κάρτες: {row[2] if row[2] is not None else 0} € | Σύνολο: {row[3] if row[3] is not None else 0} € | Έξοδα: {row[4] if row[4] is not None else 0} €')

        st.divider()
        st.write('Συνολικά: ')
        st.write(f'Εισπράξεις Μετρητών: {sum(sum_cash)} €')
        st.write(f'Εισπράξεις Καρτών: {sum(sum_pos)} €')

        try:
            result_avg = (sum(sum_cash_pos))/len(sum_cash_pos) # Φίλτρο για το μέσο όρο, επειδή εάν επιλέξω ημερομηνία χωρίς καταχώρηση βγάζει σφάλμα διαίρεσης με το μηδέν.
        except ZeroDivisionError:
            result_avg = 0
        st.write(f'Συνολικές Εισπράξεις: {sum(sum_cash_pos)} €, Μέσος όρος ανα ημέρα: {result_avg:.2f} €')
        st.write(f'Έξοδα : {sum(sum_outcome)} €')

with tab4:
    # ΕΠΙΛΟΓΗ ΧΡΗΣΤΗ, ΤΡΕΧΟΝ ΕΤΟΣ, ΕΠΙΛΟΓΗ ΕΤΟΥΣ, ΤΡΕΧΟΝ ΜΗΝΑΣ, ΣΥΓΚΕΚΡΙΜΕΝΕΣ ΗΜΕΡΟΜΗΝΙΕΣ
    # ΕΠΙΣΗΣ ΣΥΓΚΡΙΤΙΚΟ ΜΕ ΠΡΟΗΓΟΥΜΕΝΑ ΕΤΗ
    col1, col2 = st.columns(2)
    with col1:
        radio_select_1 = st.radio('Επέλεξε Περίοδο:',
                 ['Επέλεξε Ημερομηνίες', 'Ανα Μήνα', 'Ανα Έτος'])
    with col2:
        radio_select_2 = st.radio('Επέλεξε Έσοδα - Έξοδα',
                 ['Έσοδα και Έξοδα','Μόνο Έσοδα','Μόνο Έξοδα'])

    if radio_select_1 == 'Επέλεξε Ημερομηνίες':
        if radio_select_2 == 'Έσοδα και Έξοδα':

            sum_dates_input = st.date_input('Δώσε μας περίοδο:', (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=8)
            if len(sum_dates_input) != 2: # Ελέγχω εάν είναι επιλεγμένες και οι δύο ημερομηνίες, αλλιώς βγάζει σφάλμα μέχρι να επιλέξω τη δεύτερη
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Επέλεξες τις ημερομηνίες {sum_date1} - {sum_date2}')
            if st.button('Εμφάνιση', key=10):
                sql_df = cur.execute("""
                SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome
                FROM income
                LEFT JOIN outcome ON income.date = outcome.date
                WHERE income.date BETWEEN ? AND ?
            
                UNION
            
                SELECT outcome.date, income.income_cash, income.income_pos, income.income, outcome.outcome
                FROM outcome
                LEFT JOIN income ON income.date = outcome.date
                WHERE outcome.date BETWEEN ? AND ?
                """, (sum_date1, sum_date2, sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Τίτλοι στηλών
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)


                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)


                income_chart = alt.Chart(df_filtered).mark_bar(color='blue', opacity=1).encode(x='date', y='income') #Πρεπει να κάνω δύο διαφορετικά charts για να εμφανίσει έσοδα και έξοδα
                outcome_chart = alt.Chart(df_filtered).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome') # ΠΡΟΒΛΗΜΑ, ΟΤΑΝ ΕΠΙΛΕΓΩ ΛΙΓΕΣ ΗΜΕΡΟΜΗΝΙΕΣ ΜΟΥ ΒΓΑΖΕΙ ΚΑΙ ΤΙΣ ΩΡΕΣ
                final_chart = alt.layer(income_chart, outcome_chart) # Το layer ενώνει τα charts
                st.altair_chart(final_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έσοδα':

            sum_dates_input = st.date_input('Δώσε μας περίοδο:', (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=16)
            if len(sum_dates_input) != 2:  # Ελέγχω εάν είναι επιλεγμένες και οι δύο ημερομηνίες, αλλιώς βγάζει σφάλμα μέχρι να επιλέξω τη δεύτερη
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Επέλεξες τις ημερομηνίες {sum_date1} - {sum_date2}')
            if st.button('Εμφάνιση', key=17):
                sql_df = cur.execute(
                    "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?",
                    (sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Τίτλοι στηλών
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)

                dates_income_chart = alt.Chart(df_filtered).mark_bar().encode(x='date', y='income')
                st.altair_chart(dates_income_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έξοδα':
            sum_dates_input = st.date_input('Δώσε μας περίοδο:',
                                            (datetime.datetime.today(), datetime.datetime.today()),
                                            format='DD-MM-YYYY', key=18)
            if len(sum_dates_input) != 2:  # Ελέγχω εάν είναι επιλεγμένες και οι δύο ημερομηνίες, αλλιώς βγάζει σφάλμα μέχρι να επιλέξω τη δεύτερη
                st.stop()
            sum_date1 = sum_dates_input[0].strftime("%d-%m-%Y")
            sum_date2 = sum_dates_input[1].strftime("%d-%m-%Y")
            st.write(f'Επέλεξες τις ημερομηνίες {sum_date1} - {sum_date2}')
            if st.button('Εμφάνιση', key=19):
                sql_df = cur.execute(
                    "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date BETWEEN ? AND ?",
                    (sum_date1, sum_date2))
                sql_columns = [description[0] for description in sql_df.description]  # Τίτλοι στηλών
                df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

                start_date = pd.to_datetime(sum_dates_input[0])
                end_date = pd.to_datetime(sum_dates_input[1])
                df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

                df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
                st.dataframe(df, hide_index=True)

                dates_outcome_chart = alt.Chart(df_filtered).mark_bar(color='red').encode(x='date', y='outcome')
                st.altair_chart(dates_outcome_chart, use_container_width=True)

    if radio_select_1 == 'Ανα Μήνα':
        sql_df = cur.execute(
            "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date")
        sql_columns = [description[0] for description in sql_df.description]  # Τίτλοι στηλών
        df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        #st.dataframe(df, hide_index=True)
        df['Month'] = df['date'].dt.month
        df['Year'] = df['date'].dt.year

        years = sorted(df['Year'].unique())  # Τράβηξα τα διαθέσιμα έτη απο το Dataframe
        selected_year = st.radio('Eπέλεξε Έτος:', years, horizontal=True)

        df_year = df[df['Year'] == selected_year]
        months = sorted(df_year['Month'].unique())  # Tράβηξα τους μήνες με καταχωρημένα στοιχεία ανα έτος

        if radio_select_2 == 'Έσοδα και Έξοδα':
            radio_select_compare = st.radio('Θέλεις σύγκριση Μηνών;',
                                            ['Όχι', 'Ναί'])
            st.divider()

            if radio_select_compare == 'Όχι':
                #st.dataframe(df_year, hide_index=True)
                selected_month = st.radio('Eπέλεξε Μήνα',months ,key=13)
                df_per_month = df_year[df_year['Month'] == selected_month]

                per_month_income_chart = alt.Chart(df_per_month).mark_bar(color='blue', opacity=1).encode(x='date',
                                                                                      y='income')  # Πρεπει να κάνω δύο διαφορετικά charts για να εμφανίσει έσοδα και έξοδα
                per_month_outcome_chart = alt.Chart(df_per_month).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome')
                per_month_final_chart = alt.layer(per_month_income_chart, per_month_outcome_chart)  # Το layer ενώνει τα charts
                st.altair_chart(per_month_final_chart, use_container_width=True)


            if radio_select_compare == 'Ναί':
                col_comp1, col_comp2 = st.columns(2)

                with col_comp1:
                    selected_month1 = st.radio('Eπέλεξε Πρώτο Μήνα',months ,key=11)

                with col_comp2:
                    selected_month2 = st.radio('Eπέλεξε Δεύτερο Μήνα',months ,key=12)

                df_compare_months = df_year[df_year['Month'].isin([selected_month1, selected_month2])]

                compare_month_income_chart = alt.Chart(df_compare_months).mark_bar(opacity=0.6).encode(x='date',
                                                                                                          y='income', color='Month:N')  # Πρεπει να κάνω δύο διαφορετικά charts για να εμφανίσει έσοδα και έξοδα
                compare_month_outcome_chart = alt.Chart(df_compare_months).mark_bar(opacity=0.3).encode(x='date',
                                                                                                            y='outcome', color='Month:N') # Μετέφερα το color στο encode, ωστε να δινει διαφορετικο χρωμα σε καθε μήνα
                compare_month_final_chart = alt.layer(compare_month_income_chart,
                                                  compare_month_outcome_chart)  # Το layer ενώνει τα charts
                st.altair_chart(compare_month_final_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έσοδα':
            selected_month_income = st.radio('Eπέλεξε Μήνα', months, key=14)
            df_per_month = df_year[df_year['Month'] == selected_month_income]

            month_income_chart = alt.Chart(df_per_month).mark_bar(color='green').encode(x='date', y='income')
            st.altair_chart(month_income_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έξοδα':
            selected_month_outcome = st.radio('Eπέλεξε Μήνα', months, key=15)
            df_per_month = df_year[df_year['Month'] == selected_month_outcome]

            month_outcome_chart = alt.Chart(df_per_month).mark_bar(color='orange').encode(x='date', y='outcome')
            st.altair_chart(month_outcome_chart, use_container_width=True)

    if radio_select_1 == 'Ανα Έτος':
        sql_df = cur.execute(
            "SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date")
        sql_columns = [description[0] for description in sql_df.description]  # Τίτλοι στηλών
        df = pd.DataFrame(sql_df.fetchall(), columns=sql_columns)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df['Month'] = df['date'].dt.month
        df['Year'] = df['date'].dt.year

        years = sorted(df['Year'].unique())  # Τράβηξα τα διαθέσιμα έτη απο το Dataframe
        selected_year = st.radio('Eπέλεξε Έτος:', years, horizontal=True)

        df_year = df[df['Year'] == selected_year]

        if radio_select_2 == 'Έσοδα και Έξοδα':

            per_year_income_chart = alt.Chart(df_year).mark_bar(color='green', opacity=1).encode(x='date', y='income')  # Πρεπει να κάνω δύο διαφορετικά charts για να εμφανίσει έσοδα και έξοδα
            per_year_outcome_chart = alt.Chart(df_year).mark_bar(color='red', opacity=0.5).encode(x='date', y='outcome')
            per_year_final_chart = alt.layer(per_year_income_chart, per_year_outcome_chart)  # Το layer ενώνει τα charts
            st.altair_chart(per_year_final_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έσοδα':

            year_income_chart = alt.Chart(df_year).mark_bar(color='green').encode(x='date', y='income')
            st.altair_chart(year_income_chart, use_container_width=True)

        if radio_select_2 == 'Μόνο Έξοδα':

            year_outcome_chart = alt.Chart(df_year).mark_bar(color='red').encode(x='date', y='outcome')
            st.altair_chart(year_outcome_chart, use_container_width=True)


if 'income_outcome.db' in conn.execute('PRAGMA database_list').fetchone()[2]:
    conn.close()


