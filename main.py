from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import copy
import json

app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       port = 8889,
                       password='root',
                       db='project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

app.secret_key = 'database project'

'''
The following specifies index and login pages for customer and staff
'''
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/customer_login')
def customer_login():
    session.clear()
    return render_template('customer_login.html')

@app.route('/staff_login')
def staff_login():
    session.clear()
    return render_template('staff_login.html')

@app.route('/customer_register')
def customer_register():
    session.clear()
    return render_template('customer_register.html')

@app.route('/staff_register')
def staff_register():
    session.clear()
    return render_template('staff_register.html')

'''
Authentication for logins and registers
'''

@app.route('/customer_login_auth', methods=['GET', 'POST'])
def customer_login_auth():
    email = request.form['email']
    password = request.form['password']
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s and customer_password = %s'
    cursor.execute(query, (email, password))
    data = cursor.fetchone()
    cursor.close()
    if (data):
        session['username'] = email
        return redirect(url_for('customer_homepage'))
    else:
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)

@app.route('/staff_login_auth', methods=['GET', 'POST'])
def staff_login_auth():
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username = %s and staff_password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    if (data):
        session['username'] = username
        return redirect(url_for('staff_homepage'))
    else:
        error = 'Invalid login or username'
        return render_template('staff_login.html', error=error)

@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    street = request.form['street']
    building_number = request.form['building_number']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    passport_number = request.form['passport_number']
    exp_month = request.form['exp_month']
    exp_day = request.form['exp_day']
    exp_year = request.form['exp_year']
    passport_country = request.form['passport_country']
    birth_day = request.form['birth_day']
    birth_month = request.form['birth_month']
    birth_year = request.form['birth_year']
    exp_year_match = bool(re.match("[0-9][0-9][0-9][0-9]", exp_year))
    birth_year_match = bool(re.match("[0-9][0-9][0-9][0-9]", birth_year))

    if '@' not in email:
        return render_template('customer_register.html', error='An email address is required!')

    if not exp_year_match or not birth_year_match:
        return render_template('customer_register.html', error='Wrong year format!')

    passport_exp = str(exp_year) + '-' + str(exp_month) + '-' + str(exp_day)
    date_of_birth = str(birth_year) + '-' + str(birth_month) + '-' + str(birth_day)

    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    data = cursor.fetchone()
    if(data):
	    return render_template('customer_register.html', error = 'Customer already exists!')
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, password, building_number, street, city, state, phone, passport_number, passport_exp, passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        session['username'] = email
        return redirect(url_for('customer_homepage'))

@app.route('/staff_register_auth', methods=['GET', 'POST'])
def staff_register_auth():
    username = request.form['username']
    password = request.form['password']
    airline = request.form['airline']
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    birth_day = request.form['day']
    birth_month = request.form['month']
    birth_year = request.form['year']

    if '@' in password:
        return render_template('staff_register.html', error='Username cannot be an email address!')

    birth_year_match= bool(re.match("[0-9][0-9][0-9][0-9]", birth_year))
    if not birth_year_match:
        return render_template('staff_register.html', error='Wrong year format!')

    date_of_birth = str(birth_year) + '-' + str(birth_month) + '-' + str(birth_day)

    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    if(data):
        return render_template('staff_register.html', error = 'Staff already exists!')
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, airline, password, f_name, l_name, date_of_birth))
        conn.commit()
        cursor.close()
        session['username'] = username
        return redirect(url_for('staff_homepage'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/customer_homepage')
def customer_homepage():
    check_if_not_logged_in()
    email = session['username']
    if '@' not in email:
        return redirect(url_for('customer_login'))
    cursor = conn.cursor()
    cursor.execute('select customer_name from customer where email = %s', (email))
    name = cursor.fetchone()
    cursor.close()
    return render_template('customer_homepage.html', username=name['customer_name'])

@app.route('/staff_homepage')
def staff_homepage():
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    cursor = conn.cursor()
    cursor.execute('select airline_name, first_name, last_name from airline_staff where username = %s', (username))
    data = cursor.fetchone()
    cursor.close()
    return render_template('staff_homepage.html', airline=data['airline_name'], f_name=data['first_name'], l_name=data['last_name'])

@app.route('/customer_view_flights')
def customer_view_flight():
    check_if_not_logged_in()
    email = session['username']
    if '@' not in email:
        return redirect(url_for('customer_login'))
    cursor = conn.cursor()
    date = datetime.now().date()
    time = datetime.now().time()
    future_query = 'select T.airline_name as t_airline_name, T.flight_number as t_flight_number, ' \
                   'T.departure_date as t_departure_date, T.departure_time as t_departure_time, ' \
                   'D.airport_name as d_airport_name, arrival_date, ' \
                   'arrival_time, A.airport_name as a_airport_name, flight_status ' \
                 'from ticket as T, flight as F, airport as D, airport as A ' \
                 'where T.airline_name = F.airline_name and T.flight_number = F.flight_number ' \
                 'and T.departure_date = F.departure_date and T.departure_time = F.departure_time ' \
                 'and F.departure_airport = D.code and F.arrival_airport = A.code and T.customer_email = %s ' \
                 'and ((T.departure_date > %s) or (T.departure_date = %s and T.departure_time >= %s))'
    past_query = 'select T.airline_name as t_airline_name, T.flight_number as t_flight_number, ' \
                   'T.departure_date as t_departure_date, T.departure_time as t_departure_time, ' \
                   'D.airport_name as d_airport_name, arrival_date, ' \
                   'arrival_time, A.airport_name as a_airport_name, flight_status ' \
                 'from ticket as T, flight as F, airport as D, airport as A ' \
                 'where T.airline_name = F.airline_name and T.flight_number = F.flight_number ' \
                 'and T.departure_date = F.departure_date and T.departure_time = F.departure_time ' \
                 'and F.departure_airport = D.code and F.arrival_airport = A.code and T.customer_email = %s ' \
                 'and ((T.departure_date < %s) or (T.departure_date = %s and T.departure_time <= %s))'
    cursor.execute(future_query, (email, str(date), str(date), str(time)[:8]))
    future_data = cursor.fetchall()
    cursor.execute(past_query, (email, str(date), str(date), str(time)[:8]))
    past_data = cursor.fetchall()
    print(past_data)
    cursor.execute(past_query, (email, str(date), str(date), str(time)[:8]))
    spending_data = []
    rounded_date = copy.deepcopy(date) - relativedelta(days=date.day)
    for i in range(6):
        temp_month = rounded_date - relativedelta(months=i)
        next_month = rounded_date - relativedelta(months=(i-1))
        spending_query = "select sum(sold_price) from ticket where customer_email = %s " \
                         "and purchase_date >= %s and purchase_date < %s"
        cursor.execute(spending_query, (email, str(temp_month), str(next_month)))
        amount = cursor.fetchone()
        spending_data.append({'month':str(temp_month)[5:7], 'amount':amount if amount['sum(sold_price)'] else {'sum(sold_price)': 0}})
    cursor.close()
    return render_template('customer_view_flights.html', future=future_data, past=past_data, spending=spending_data)


@app.route('/rating_form', methods=['GET', 'POST'])
def rating_form():
    check_if_not_logged_in()
    data = {'airline_name': request.form['airline_name'], 'flight_number': request.form['flight_number'],
            'departure_date': request.form['departure_date'], 'departure_time': request.form['departure_time']}
    return render_template('customer_rating.html', data = data)

@app.route('/submit_rating', methods=['GET', 'POST'])
def submit_rating():
    email = session['username']
    if '@' not in email:
        return redirect(url_for('customer_login'))
    flight_info = {'airline_name': request.form['airline_name'], 'flight_number': request.form['flight_number'],
            'departure_date': request.form['departure_date'], 'departure_time': request.form['departure_time']}
    rating = request.form['rating']
    comment = request.form['comment']
    cursor = conn.cursor()
    check_query = "select * from rating where customer_email = %s and airline_name = %s " \
                  "and flight_number = %s and departure_date = %s and departure_time = %s"
    cursor.execute(check_query, (email, flight_info['airline_name'], flight_info['flight_number'], flight_info['departure_date'], flight_info['departure_time']))
    data = cursor.fetchall()
    if(data):
        return render_template('customer_rating.html', data = flight_info, error = 'You already rated for this flight!' )

    insert_query = 'insert into rating values(%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(insert_query, (email, flight_info['airline_name'], flight_info['flight_number'], flight_info['departure_date'], flight_info['departure_time'], rating, comment))
    conn.commit()
    cursor.close()
    return redirect(url_for('customer_view_flight'))

@app.route('/search_flights/<criteria>')
def search_flights(criteria):
    is_login = False
    one_way = True
    email = '_'
    if session.get('username') is not None:
        is_login= True
        email = session['username']
        if '@' not in email:
            return redirect(url_for('customer_login'))
    date = str(datetime.now().date())
    time = str(datetime.now().time())[:8]
    cursor = conn.cursor()
    query = 'select airline_name, flight_number, departure_date, departure_time, D.airport_name as d_airport_name, D.city as d_city, ' \
            'arrival_date, arrival_time, A.airport_name as a_airport_name, A.city as a_city, flight_status from flight as F, airport as D, airport as A ' \
            'where F.departure_airport = D.code and F.arrival_airport = A.code and (departure_date > %s or (departure_date = %s and departure_time >= %s))'
    cursor.execute(query, (date, date, time))
    departure_data= cursor.fetchall()
    return_data = departure_data
    if criteria != '_':
        criteria = criteria.replace("\'", "\"")
        criteria = json.loads(criteria)
        one_way = True if criteria['one_way'] == '1' else False

        if not one_way and criteria['arrival_input'] == '':
            error = 'You need to specify a destination before searching for round-trip!'
            return render_template('search_flights.html', is_login=is_login, login=email, one_way=True,
                                   departure_data=departure_data, return_data=return_data, error=error)

        if criteria['departure_input'] != '':
            new_departure_data = []
            for line in departure_data:
                if line['d_'+criteria['departure_select']] == criteria['departure_input']:
                    new_departure_data.append(line)
            departure_data = new_departure_data
            if not one_way:
                new_return_data = []
                for line in return_data:
                    if line['a_'+criteria['arrival_select']] == criteria['departure_input']:
                        new_return_data.append(line)
                return_data = new_return_data
        if criteria['arrival_input'] != '':
            new_departure_data = []
            for line in departure_data:
                if line['a_'+criteria['arrival_select']] == criteria['arrival_input']:
                    new_departure_data.append(line)
            departure_data = new_departure_data
            if not one_way:
                new_return_data = []
                for line in return_data:
                    if line['d_'+criteria['arrival_select']] == criteria['arrival_input']:
                        new_return_data.append(line)
                return_data = new_return_data
        if criteria['dep_year'] != '':
            dep_date = criteria['dep_year'] + '-' + criteria['dep_month'] + '-' + criteria['dep_day']
            new_departure_data = []
            for line in departure_data:
                if str(line['departure_date']) == dep_date:
                    new_departure_data.append(line)
            departure_data = new_departure_data
        if criteria['ret_year'] != '':
            ret_date = criteria['ret_year'] + '-' + criteria['ret_month'] + '-' + criteria['ret_day']
            if not one_way:
                new_return_data = []
                for line in return_data:
                    print(ret_date)
                    if str(line['departure_date']) == str(ret_date):
                        new_return_data.append(line)
                return_data = new_return_data

    return render_template('search_flights.html', is_login = is_login, login=email, one_way=one_way,
                           departure_data=departure_data, return_data=return_data)

@app.route('/refresh_search_flights', methods=['GET', 'POST'])
def refresh_search_flights():
    criteria = {}
    criteria['departure_select'] = request.form['departure']
    criteria['departure_input']= request.form['departure_input']
    criteria['arrival_select'] = request.form['arrival']
    criteria['arrival_input'] = request.form['arrival_input']
    criteria['dep_month'] = request.form['dep_month']
    criteria['dep_day'] = request.form['dep_day']
    criteria['dep_year'] = request.form['dep_year']
    criteria['ret_month'] = request.form['ret_month']
    criteria['ret_day'] = request.form['ret_day']
    criteria['ret_year'] = request.form['ret_year']
    criteria['one_way'] = request.form['one_way_round_trip']
    return redirect(url_for('search_flights', criteria = criteria))

@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
    check_if_not_logged_in()
    email = session['username']
    if '@' not in email:
        return redirect(url_for('customer_login'))
    flight_data = {'airline_name': request.form['airline_name'], 'flight_number': request.form['flight_number'], 'departure_date': request.form['departure_date'],
                   'departure_time': request.form['departure_time']}
    flight_query = 'select * ' \
                   'from flight as F, airplane as A ' \
                   'where F.airline_name = A.airline_name and F.airplane_ID = A.airplane_ID and F.airline_name = %s ' \
                   'and F.flight_number = %s and F.departure_date = %s and F.departure_time = %s '
    occupancy_query = 'select count(ID) ' \
                   'from ticket ' \
                   'where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s '
    previously_purchased_query = 'select * from ticket where airline_name = %s and flight_number = %s and departure_date = %s and ' \
                              'departure_time = %s and customer_email = %s'
    cursor = conn.cursor()
    cursor.execute(flight_query, (flight_data['airline_name'], flight_data['flight_number'], flight_data['departure_date'], flight_data['departure_time']))
    data = cursor.fetchone()
    cursor.execute(occupancy_query, (flight_data['airline_name'], flight_data['flight_number'], flight_data['departure_date'], flight_data['departure_time']))
    occupancy = cursor.fetchone()['count(ID)']
    price = float(data['base_price']) * 1.25 if occupancy > 0.75 * float(data['num_seats']) else data['base_price']
    cursor.execute(previously_purchased_query, (flight_data['airline_name'], flight_data['flight_number'], flight_data['departure_date'], flight_data['departure_time'], email))
    previously_purchased = cursor.fetchone()
    cursor.close()
    if occupancy == data['num_seats']:
        return render_template("purchase_ticket.html", error='Sorry, the flight is fully booked!')
    elif previously_purchased:
        return render_template("purchase_ticket.html", error='You have previously booked the flight!')
    else:
        return render_template("purchase_ticket.html", data=data, price=price, occupancy=occupancy)

@app.route('/purchase_ticket_submit', methods=['GET', 'POST'])
def purchase_ticket_submit():
    email = session['username']
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    sold_price = request.form['sold_price']
    card_type = request.form['card_type']
    card_number = request.form['card_number']
    name_on_card = request.form['name_on_card']
    exp_day = request.form['exp_day']
    exp_month = request.form['exp_month']
    exp_year = request.form['exp_year']
    exp = str(exp_year) + '-' + str(exp_month) + '-' + str(exp_day)
    date = str(datetime.now().date())
    time = str(datetime.now().time())[:8]
    cursor = conn.cursor()
    ticket_count_query = 'select count(ID) from ticket'
    cursor.execute(ticket_count_query)
    ticket_count = cursor.fetchone()['count(ID)']
    insert_query = 'insert into ticket values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    cursor.execute(insert_query, (int(ticket_count) + 1, airline_name, flight_number, departure_date, departure_time, email,
                                  sold_price, card_type, card_number, name_on_card, exp, date, time))
    conn.commit()
    cursor.close()
    return redirect(url_for('search_flights', criteria = '_'))



@app.route('/staff_view_flights/<criteria>', methods=['GET', 'POST'])
def staff_view_flights(criteria):
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    date = datetime.now().date()
    time = str(datetime.now().time())[:8]
    cursor = conn.cursor()
    data_query = 'select airline_name, flight_number, departure_date, departure_time, D.airport_name as d_airport_name, D.city as d_city, ' \
            'arrival_date, arrival_time, A.airport_name as a_airport_name, A.city as a_city, flight_status from flight as F, airport as D, airport as A ' \
            'where F.departure_airport = D.code and F.arrival_airport = A.code and airline_name = %s ' \
            'order by departure_date desc'
    airline_name = get_airline_name(username)
    cursor.execute(data_query, (airline_name))
    data = cursor.fetchall()
    if criteria != '_':
        criteria = json.loads(criteria.replace("\'", "\""))

        if criteria['departure_input'] != '':
            new_data = []
            for line in data:
                if line['d_'+criteria['departure_select']] == criteria['departure_input']:
                    new_data.append(line)
            data = new_data
        if criteria['arrival_input'] != '':
            new_data = []
            for line in data:
                if line['a_'+criteria['arrival_select']] == criteria['arrival_input']:
                    new_data.append(line)
            data = new_data
        if criteria['start_year'] != '':
            start_date = criteria['start_year'] + '-' + criteria['start_month'] + '-' + criteria['start_day']
            new_data = []
            for line in data:
                if str(line['departure_date']) >= start_date:
                    new_data.append(line)
            data = new_data
        if criteria['end_year'] != '':
            end_date = criteria['end_year'] + '-' + criteria['end_month'] + '-' + criteria['end_day']
            new_data = []
            for line in data:
                if str(line['departure_date']) <= end_date:
                    new_data.append(line)
            data = new_data
    else:
        new_data = []
        print(data)
        for line in data:
            if date < line['departure_date'] < (date + relativedelta(months=1)):
                new_data.append(line)
        data = new_data

    return render_template('staff_view_flights.html', data=data)

@app.route('/refresh_staff_view_flights', methods=['GET', 'POST'])
def refresh_staff_view_flights():
    criteria = {}
    criteria['departure_select'] = request.form['departure']
    criteria['departure_input'] = request.form['departure_input']
    criteria['arrival_select'] = request.form['arrival']
    criteria['arrival_input'] = request.form['arrival_input']
    criteria['start_day'] = request.form['start_day']
    criteria['start_month'] = request.form['start_month']
    criteria['start_year'] = request.form['start_year']
    criteria['end_day'] = request.form['end_day']
    criteria['end_month'] = request.form['end_month']
    criteria['end_year'] = request.form['end_year']
    return redirect(url_for('staff_view_flights', criteria=criteria))


@app.route('/add_flight')
def add_flight():
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    return render_template('add_flight.html')

@app.route('/add_flight_submit', methods=['GET', 'POST'])
def add_flight_submit():
    username = session['username']
    airline_name = get_airline_name(username)
    flight_number = request.form['flight_number']
    airplane_id = request.form['airplane_ID']
    departure_day = request.form['departure_day']
    departure_month = request.form['departure_month']
    departure_year = request.form['departure_year']
    departure_hour = request.form['departure_hour']
    departure_minute = request.form['departure_minute']
    departure_airport_name = request.form['departure_airport_name']
    arrival_airport_name = request.form['arrival_airport_name']
    arrival_day = request.form['arrival_day']
    arrival_month = request.form['arrival_month']
    arrival_year = request.form['arrival_year']
    arrival_hour = request.form['arrival_hour']
    arrival_minute = request.form['arrival_minute']
    base_price = request.form['base_price']
    cursor = conn.cursor()
    check_airport_query = 'select code from airport where airport_name = %s'
    check_airplane_query = 'select * from airplane where airline_name = %s and airplane_id = %s'
    cursor.execute(check_airplane_query, (airline_name, airplane_id))
    airplane_id = cursor.fetchone()
    if not airplane_id:
        return render_template('add_flight.html', error='Airplane does not exist!')
    cursor.execute(check_airport_query, (departure_airport_name))
    departure_airport = cursor.fetchone()
    cursor.execute(check_airport_query, (arrival_airport_name))
    arrival_airport = cursor.fetchone()
    if not departure_airport or not arrival_airport:
        return render_template('add_flight.html', error='Airport does not exist!')
    departure_year_match = bool(re.match("[0-9][0-9][0-9][0-9]", departure_year))
    arrival_year_match = bool(re.match("[0-9][0-9][0-9][0-9]", arrival_year))
    if not departure_year_match or not arrival_year_match:
        return render_template('add_flight.html', error='Wrong year format!')
    departure_minute_match = bool(re.match("[0-9][0-9]", departure_minute))
    arrival_minute_match = bool(re.match("[0-9][0-9]", arrival_minute))
    if not departure_minute_match or not arrival_minute_match:
        return render_template('add_flight.html', error='Wrong minute format!')
    departure_date = str(departure_year) + '-' + str(departure_month) + '-' + str(departure_day)
    arrival_date = str(arrival_year) + '-' + str(arrival_month) + '-' + str(arrival_day)
    departure_time = str(departure_hour) + ':' + str(departure_minute) + ':00'
    arrival_time = str(arrival_hour) + ':' + str(arrival_minute) + ':00'
    check_if_exist_query = 'select * from flight where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s'
    insert_query = 'insert into flight values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(check_if_exist_query, (airline_name, flight_number, departure_date, departure_time))
    if_exist = cursor.fetchone()
    if if_exist:
        return render_template('add_flight.html', error='Flight already exists!')
    print(airline_name, flight_number, departure_date, departure_time, airplane_id['airplane_ID'], departure_airport['code'], arrival_airport['code'],
                                  arrival_date, arrival_time, int(base_price), 'on-time')
    cursor.execute(insert_query, (airline_name, flight_number, departure_date, departure_time, airplane_id['airplane_ID'], departure_airport['code'], arrival_airport['code'],
                                  arrival_date, arrival_time, int(base_price), 'on-time'))
    conn.commit()
    cursor.close()
    return redirect(url_for('staff_view_flights', criteria='_'))


@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    status = request.form['status']
    cursor = conn.cursor()
    query = 'update flight ' \
            'set flight_status = %s ' \
            'where airline_name = %s and flight_number = %s and departure_date = %s and departure_time = %s'
    cursor.execute(query, (status, airline_name, flight_number, departure_date, departure_time))
    conn.commit()
    cursor.close()
    return redirect(url_for('staff_view_flights', criteria='_'))

@app.route('/flight_customer_rating', methods=['GET', 'POST'])
def flight_customer_rating():
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    flight_data = {'airline_name': request.form['airline_name'], 'flight_number': request.form['flight_number'],
                   'departure_date': request.form['departure_date'], 'departure_time': request.form['departure_time']}
    cursor = conn.cursor()
    customer_query = 'select customer_name, email, phone_number ' \
                     'from customer as C, ticket as T ' \
                     'where C.email = T.customer_email and T.airline_name = %s and ' \
                     'T.flight_number = %s and T.departure_date = %s and T.departure_time = %s'
    rating_query = 'select customer_name, email, rate, rating_comment ' \
                     'from customer as C, rating as R ' \
                     'where C.email = R.customer_email and R.airline_name = %s and ' \
                     'R.flight_number = %s and R.departure_date = %s and R.departure_time = %s'
    cursor.execute(customer_query, (flight_data['airline_name'], flight_data['flight_number'], flight_data['departure_date'],
                                    flight_data['departure_time']))
    customer_data = cursor.fetchall()
    cursor.execute(rating_query, (flight_data['airline_name'], flight_data['flight_number'], flight_data['departure_date'],
                    flight_data['departure_time']))
    rating_data = cursor.fetchall()
    cursor.close()
    return render_template('flight_customer_rating.html', flight_data=flight_data, customers=customer_data, ratings=rating_data)

@app.route('/airplane_list/<error>')
def airplane_list(error):
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    cursor = conn.cursor()
    auth_query = 'select airline_name from airline_staff where username = %s'
    cursor.execute(auth_query, (username))
    airline_name = cursor.fetchone()['airline_name']
    search_query = 'select * from airplane where airline_name = %s'
    cursor.execute(search_query, (airline_name))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airplane_list.html', data=data, airline_name=airline_name, error = error if error != '_' else None)


@app.route('/add_airplane', methods = ['GET', 'POST'])
def add_airplane():
    airline_name = request.form['airline_name']
    airplane_id = request.form['airplane_id']
    num_seats = request.form['num_seats']
    cursor = conn.cursor()
    check_query = 'select * from airplane where airline_name = %s and airplane_ID = %s'
    cursor.execute(check_query, (airline_name, airplane_id))
    data = cursor.fetchone()
    if data:
        return redirect(url_for('airplane_list', error = 'This airplane already exists'))
    else:
        query = 'insert into airplane values(%s, %s, %s)'
        cursor.execute(query,(airline_name, airplane_id, int(num_seats)))
        conn.commit()
        cursor.close()
        return redirect(url_for('airplane_list', error = '_'))

@app.route('/airport_list/<error>')
def airport_list(error):
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        session.pop()
        return redirect(url_for(staff_login))
    cursor = conn.cursor()
    query = 'select * from airport'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('airport_list.html', data=data, error=error if error != '_' else None)

@app.route('/add_airport',  methods=['GET', 'POST'])
def add_airport():
    code = request.form['code']
    airport_name = request.form['airport_name']
    city = request.form['city']
    cursor = conn.cursor()
    check_query = 'select * from airport where code = %s'
    cursor.execute(check_query, (code))
    data = cursor.fetchone()
    if data:
        return redirect(url_for('airport_list', error='This airport already exists'))
    else:
        query = 'insert into airport values(%s, %s, %s)'
        cursor.execute(query, (code, airport_name, city))
        conn.commit()
        cursor.close()
        return redirect(url_for('airport_list', error='_'))

@app.route('/customer_list')
def customer_list():
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        session.pop()
        return redirect(url_for(staff_login))
    cursor = conn.cursor()
    auth_query = 'select airline_name from airline_staff where username = %s'
    cursor.execute(auth_query, (username))
    airline_name = cursor.fetchone()['airline_name']
    last_year = str(datetime.now().date() - relativedelta(years = 1))
    top_customer_query = 'select distinct customer_name, customer_email, sum(sold_price) as spending ' \
                        'from ticket as T, customer as C ' \
                        'where T.customer_email = C.email and airline_name = %s and purchase_date > %s ' \
                        'group by customer_name, customer_email order by sum(sold_price) desc'
    cursor.execute(top_customer_query, (airline_name, last_year))
    top_customer = cursor.fetchone()
    all_customer_query = 'select distinct customer_name, customer_email, sum(sold_price) as spending ' \
                        'from ticket as T, customer as C ' \
                         'where T.customer_email = C.email and T.airline_name = %s ' \
                        'group by customer_name, customer_email order by sum(sold_price) desc'
    cursor.execute(all_customer_query, (airline_name))
    customers = cursor.fetchall()
    return render_template('customer_list.html', airline_name = airline_name, top_customer = top_customer, customers = customers)

@app.route('/customer_detail', methods=['GET', 'POST'])
def customer_detail():
    check_if_not_logged_in()
    if len(session) == 0:
        return redirect(url_for('staff_login'))
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    airline_name = request.form['airline_name']
    customer_email = request.form['customer_email']
    print(customer_email)
    customer_name = request.form['customer_name']
    cursor = conn.cursor()
    query = 'select F.airline_name, F.flight_number, F.departure_date as f_dep_date, F.departure_time as f_dep_time, ' \
            'F.departure_airport as f_dep_airport, F.arrival_airport as f_arr_airport, F.arrival_date as f_arr_date, F.arrival_time as f_arr_time ' \
            'from ticket as T natural join flight as F ' \
            'where T.customer_email = %s and F.airline_name = %s'
    cursor.execute(query, (customer_email, airline_name))
    data = cursor.fetchall()
    cursor.close()
    return render_template('customer_detail.html', data=data, airline_name=airline_name, customer_name=customer_name)

@app.route('/reports')
def reports():
    check_if_not_logged_in()
    username = session['username']
    if '@' in username:
        return redirect(url_for('staff_login'))
    cursor = conn.cursor()
    date = datetime.now().date()
    time = datetime.now().time()
    auth_query = 'select airline_name from airline_staff where username = %s'
    cursor.execute(auth_query, (username))
    airline_name = cursor.fetchone()['airline_name']
    revenue_query = "select sum(sold_price) from ticket where purchase_date >= %s and airline_name = %s"
    ticket_query = "select count(ID) from ticket where purchase_date >= %s and airline_name = %s"
    location_query = 'SELECT distinct A.city from ticket as T, flight as F, airport as A ' \
                     'where T.airline_name = F.airline_name and T.flight_number = F.flight_number ' \
                     'and T.departure_date = F.departure_date and T.departure_time = F.departure_time ' \
                     'and F.arrival_airport = A.code and T.purchase_date > %s ' \
                     'group by A.city order by count(T.ID) desc'
    last_month = date - relativedelta(months=1)
    cursor.execute(revenue_query, (str(last_month), airline_name))
    last_month_revenue = cursor.fetchone()
    cursor.execute(ticket_query, (str(last_month), airline_name))
    last_month_ticket = cursor.fetchone()
    last_year = date - relativedelta(years=1)
    cursor.execute(revenue_query, (str(last_year), airline_name))
    last_year_revenue = cursor.fetchone()
    cursor.execute(ticket_query, (str(last_year), airline_name))
    last_year_ticket = cursor.fetchone()
    cursor.execute(location_query, (str(last_month - relativedelta(months=2))))
    location_rank_month = cursor.fetchall()
    cursor.execute(location_query, (str(last_year)))
    location_rank_year = cursor.fetchall()
    cursor.close()
    if len(location_rank_month) > 3:
        location_rank_month = location_rank_month[:3]
    if len(location_rank_year) > 3:
        location_rank_year = location_rank_year[:3]

    return render_template('reports_page.html', last_month_revenue=last_month_revenue, last_year_revenue=last_year_revenue,
                           last_month_ticket = last_month_ticket, last_year_ticket = last_year_ticket, airline_name=airline_name,
                           location_rank_month = location_rank_month,  location_rank_year = location_rank_year)

def check_if_not_logged_in():
    if len(session) == 0:
        return redirect(url_for('index'))

def get_airline_name(username):
    cursor = conn.cursor()
    cursor.execute('select airline_name from airline_staff where username = %s', (username))
    airline_name = cursor.fetchone()['airline_name']
    cursor.close()
    return airline_name

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug = True)

