from flask import Flask,flash,render_template, request, redirect, url_for
import mysql.connector
from flask import session
import random
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'hello'


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tournament_db'
}

def connect_to_database():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index-2.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Username = request.form['Username']
        CollegeName = request.form['CollegeName']
        Password= request.form['Password']
        email = request.form['email']
        phone = request.form['phone']
        Age = request.form['Age']
        
    
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO user (Username, Password, email, phone, CollegeName, Age) VALUES (%s, %s, %s, %s, %s,%s)"
        cursor.execute(query,(Username, Password, email, phone, CollegeName, Age))
        db_connection.commit()

        cursor.close()
        
        return render_template('newLogin.html',  message='Account created successfully')  # Redirect to homepage after creating account
    else:
        
        return render_template('newSignup.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        user_type = request.form.get('user_type')
        

        connection = connect_to_database()
        cursor = connection.cursor()

        if user_type == 'Customer':
            query = "SELECT * FROM user WHERE Username = %s AND Password = %s"

        else:
            query = "SELECT * FROM admin WHERE Username = %s AND Password = %s"          

       
        
        cursor.execute(query, (Username, Password))
        user = cursor.fetchone()
        
        connection.close()

        
        if user:
            session['main_id'] = user[0]
            
            
            
       
            session['logged_in'] = True
            session['username'] = Username
            session['user_type'] = user_type
            if user_type == 'Admin':
                
                return redirect('/AdminHome')
            if user_type == 'Customer':
                session['Age'] = user[6]
                session['email'] = user[3]
                session['ph'] = user[4]
                session['CollegeName'] = user[5]
                return redirect('/' )
        else:
            return render_template('newLogin.html', message='Invalid username or password.')
    else:
        return render_template('newLogin.html')



@app.route('/AdminHome')
def AdminHome():
    return render_template("AdminHome.html")


@app.route('/Schedule')
def Schedule():
    
    return render_template('Schedule.html')




##Your profile


@app.route('/profile', methods = ['GET'])
def profile():

    return render_template('Profile.html')




##CRUD APPLICATIONS ROUTES
@app.route('/AccCRUD')
def AccCRUD():
    connection = connect_to_database()
    cur = connection.cursor()

    

    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    cur.close()

    return render_template('AccCRUD.html', user=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        Username = request.form['Username']
        email = request.form['email']
        phone = request.form['phone']
        connection = connect_to_database()
        cur = connection.cursor()
        cur.execute("INSERT INTO user (Username, email, phone) VALUES (%s, %s, %s)", (Username, email, phone))
        connection.commit()
        return redirect(url_for('AccCRUD'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM user WHERE id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AccCRUD'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        Username = request.form['Username']
        email = request.form['email']
        phone = request.form['phone']

        connection = connect_to_database()
        cur = connection.cursor()




        cur.execute("""
        UPDATE user SET Username=%s, email=%s, phone=%s
        WHERE ID=%s;
        """, (Username, email, phone, id_data))
        
        connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('AccCRUD'))
    

@app.route('/AdminCricket')
def AdminCricket():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM cricketteams c join user u where c.Captain_ID = u.ID;   ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM cricketplayers; ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminCricket.html', user=data, user1 = data1)

@app.route('/deletecricket/<string:id_data>', methods = ['GET'])
def deletecricket(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM cricketteams WHERE Team_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminCricket'))




@app.route('/AdminFootball')
def AdminFootball():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT f.Team_ID, u.Username,f.Captain_ID, f.Collegename, f.sports FROM footballteams f join user u where f.Captain_ID = u.ID ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM footballteams c join user u where c.Captain_ID = u.ID;    ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminFootball.html', user=data, user1 = data1)


@app.route('/deletefoot/<string:id_data>', methods = ['GET'])
def deletefoot(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM footballteams WHERE Team_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminFootball'))











@app.route('/AdminBasketball')
def AdminBasketball():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM basketballteams c join user u where c.Captain_ID = u.ID;   ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM basketballplayers; ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminBasketball.html', user=data, user1 = data1)

@app.route('/deletebasket/<string:id_data>', methods = ['GET'])
def deletebasket(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM basketballteams WHERE Team_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminBasketball'))





@app.route('/AdminBadminton')
def AdminBadminton():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM badmintonteams c join user u where c.Captain_ID = u.ID;    ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM badmintonplayers; ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminBadminton.html', user=data, user1 = data1)

@app.route('/deletebadminton/<string:id_data>', methods = ['GET'])
def deletebadminton(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM badmintonteams WHERE Team_ID=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminBadminton'))




@app.route('/AdminVolleyball')
def AdminVolleyball():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM volleyballteams c join user u where c.Captain_ID = u.ID;   ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM volleyballplayers; ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminVolleyball.html', user=data, user1 = data1)

@app.route('/deletevolley/<string:id_data>', methods = ['GET'])
def deletevolley(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM volleyballteams WHERE Team_ID=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminVolleyball'))






@app.route('/AdminWeight')
def AdminWeight():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT c.Team_ID, u.Username, c.Captain_ID, c.Collegename, c.sports FROM weightteams c join user u where c.Captain_ID = u.ID;   ")
    data = cur.fetchall()
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Team_ID, Weight_Class FROM weightplayers; ")
    data1 = cur.fetchall()
    cur.close()

    return render_template('AdminWeight.html', user=data, user1 = data1)

@app.route('/deleteweight/<string:id_data>', methods = ['GET'])
def deleteweight(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = connect_to_database()
    cur = connection.cursor()
    cur.execute("DELETE FROM weightteams WHERE Team_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('AdminWeight'))




@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('index'))






##CRICKET REGISTRATIONS

@app.route('/CricketReg')
def CricketReg():
    return render_template('cricket.html')


@app.route('/CricketReg1', methods = ['POST'])
def CricketReg1():
        session['status'] = False
        NumberOfPlayers= int(request.form['NumberOfPlayers'])
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO CricketTeams (Captain_ID, CollegeName, NumberOfPlayers, sports) VALUES (%s, %s, %s, 'Cricket')"
        cursor.execute(query,(CaptainID,CollegeN, NumberOfPlayers))
        db_connection.commit()

        cursor.close()

        return render_template('cricket1.html', CaptainID = CaptainID ,NumberOfPlayers = NumberOfPlayers)


@app.route('/CricketReg2', methods=['POST'])
def CricketReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        Role = request.form.getlist('Role[]')
        CaptainID = session['main_id']
        
        print(Name)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from CricketTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO CricketPlayers(Name, Age, Role,Team_ID, sports) values(%s, %s,'Captain' ,%s, 'Cricket');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO CricketPlayers(Name, Age, Role,Team_ID, sports) values(%s,%s,%s,%s, 'Cricket')"
            values = (Name[i], Age[i], Role[i], team_id)
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("cricketConfirm.html", team_id = team_id, college = College)




@app.route('/MyCricketReg')
def MyCricketReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM cricketteams where Captain_ID = %s", (session['main_id'],))
    
    data = cur.fetchall()
    print(data)
    T_ID = 0
    if data:
        T_ID = data[0][0]
    
    print(T_ID)
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID FROM cricketplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyCricketReg.html', user=data, user1 = data1)




##BASKETBALL REGISTRATIONS
@app.route('/basketballReg')
def basketballReg():
    
    return render_template('basketball.html')

@app.route('/basketballReg1', methods = ['POST'])
def basketballReg1():
        session['status'] = False
        NumberOfPlayers= int(request.form['NumberOfPlayers'])
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO basketballTeams (Captain_ID, CollegeName, NumberOfPlayers, sports) VALUES (%s, %s, %s, 'Basketball')"
        cursor.execute(query,(CaptainID,CollegeN, NumberOfPlayers))
        db_connection.commit()

        cursor.close()

        return render_template('basketball1.html', CaptainID = CaptainID ,NumberOfPlayers = NumberOfPlayers)






@app.route('/basketballReg2', methods=['POST'])
def basketballReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        Role = request.form.getlist('Role[]')
        CaptainID = session['main_id']
        
        print(Name)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from basketballTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO basketballPlayers(Name, Age, Role,Team_ID, sports) values(%s, %s,'Captain' ,%s, 'Basketball');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO basketballPlayers(Name, Age, Role,Team_ID, sports) values(%s,%s,%s,%s, 'basketball')"
            values = (Name[i], Age[i], Role[i], team_id)
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("basketballConfirm.html", team_id = team_id, college = College)

@app.route('/MyBasketballReg')
def MyBasketballReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM basketballteams where Captain_ID = %s", (session['main_id'],))
    data = cur.fetchall()
    T_ID = 0
    if data:
        T_ID = data[0][0]
    

    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM basketballplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyBasketballReg.html', user=data, user1 = data1)






##FOOTBALL REGISTRATIONS
@app.route('/footballReg')
def footballReg():
    
    return render_template('football.html')

@app.route('/footballReg1', methods = ['POST'])
def footballReg1():
        session['status'] = False
        NumberOfPlayers= int(request.form['NumberOfPlayers'])
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO footballTeams (Captain_ID, CollegeName, NumberOfPlayers, sports) VALUES (%s, %s, %s, 'Football')"
        cursor.execute(query,(CaptainID,CollegeN, NumberOfPlayers))
        db_connection.commit()

        cursor.close()

        return render_template('football1.html', CaptainID = CaptainID ,NumberOfPlayers = NumberOfPlayers)





@app.route('/footballReg2', methods=['POST'])
def footballReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        Role = request.form.getlist('Role[]')
        CaptainID = session['main_id']
        
        print(Name)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from footballTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO footballPlayers(Name, Age, Role,Team_ID, sports) values(%s, %s,'Captain' ,%s, 'Football');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO footballPlayers(Name, Age, Role,Team_ID, sports) values(%s,%s,%s,%s, 'Football')"
            values = (Name[i], Age[i], Role[i], team_id)
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("footballConfirm.html", team_id = team_id, college = College)

@app.route('/MyFootballReg')
def MyFootballReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM footballteams where Captain_ID = %s", (session['main_id'],))
    data = cur.fetchall()
    T_ID = 0
    if data:
        T_ID = data[0][0]
     
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM footballplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyFootballReg.html', user=data, user1 = data1)





##BADMINTON REGISTRATIONS
@app.route('/badmintonReg')
def badmintonReg():
    
    return render_template('badminton.html')

@app.route('/badmintonReg1', methods = ['POST'])
def badmintonReg1():
        session['status'] = False
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO badmintonTeams (Captain_ID, CollegeName, NumberOfPlayers, sports) VALUES (%s, %s, 2, 'Badminton')"
        cursor.execute(query,(CaptainID,CollegeN))
        db_connection.commit()

        cursor.close()

        return render_template('badminton1.html', CaptainID = CaptainID ,NumberOfPlayers = 2)





@app.route('/badmintonReg2', methods=['POST'])
def badmintonReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        Role = request.form.getlist('Role[]')
        CaptainID = session['main_id']
        
        print(Name)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from badmintonTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO badmintonPlayers(Name, Age, Role,Team_ID, sports) values(%s, %s,'Captain' ,%s, 'Badminton');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO badmintonPlayers(Name, Age, Role,Team_ID, sports) values(%s,%s,%s,%s, 'Badminton')"
            values = (Name[i], Age[i], Role[i], team_id)
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("badmintonConfirm.html", team_id = team_id, college = College)

@app.route('/MyBadmintonReg')
def MyBadmintonReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM badmintonteams where Captain_ID = %s", (session['main_id'],))
    data = cur.fetchall()
    T_ID = 0
    if data:
        T_ID = data[0][0]
    
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM badmintonplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyBadmintonReg.html', user=data, user1 = data1)





##VOLLEYBALL REGISTRATIONS
@app.route('/volleyballReg')
def volleyballReg():
    
    return render_template('volleyball.html')

@app.route('/volleyballReg1', methods = ['POST'])
def volleyballReg1():
        session['status'] = False
        NumberOfPlayers= int(request.form['NumberOfPlayers'])
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO volleyballTeams (Captain_ID, CollegeName, NumberOfPlayers, sports) VALUES (%s, %s, %s, 'Volleyball')"
        cursor.execute(query,(CaptainID,CollegeN, NumberOfPlayers))
        db_connection.commit()

        cursor.close()

        return render_template('volleyball1.html', CaptainID = CaptainID ,NumberOfPlayers = NumberOfPlayers)




@app.route('/volleyballReg2', methods=['POST'])
def volleyballReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        Role = request.form.getlist('Role[]')
        CaptainID = session['main_id']
        
        print(Name)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from volleyballTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO volleyballPlayers(Name, Age, Role,Team_ID, sports) values(%s, %s,'Captain' ,%s, 'Volleyball');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO volleyballPlayers(Name, Age, Role,Team_ID, sports) values(%s,%s,%s,%s, 'Volleyball')"
            values = (Name[i], Age[i], Role[i], team_id)
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("volleyballConfirm.html", team_id = team_id, college = College)

@app.route('/MyVolleyballReg')
def MyVolleyballReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM volleyballteams where Captain_ID = %s", (session['main_id'],))
    data = cur.fetchall()
    T_ID = 0
    if data:
        T_ID = data[0][0]
    
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Role,Team_ID  FROM volleyballplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyVolleyballReg.html', user=data, user1 = data1)








##BODY BUILDING REGISTRATIONS

@app.route('/weightReg')
def BodyBuildingReg():
    return render_template('weight.html')




@app.route('/weightReg1', methods = ['POST'])
def weightReg1():
        session['status'] = False
        NumberOfPlayers= 5
        CaptainID= session.get('main_id')
        CollegeN = session.get('CollegeName')
        db_connection = connect_to_database()
        cursor = db_connection.cursor()
        query = "INSERT INTO weightTeams (Captain_ID, CollegeName, sports,NumberOfPlayers) VALUES (%s, %s, 'Weight-Lifting',%s )"
        cursor.execute(query,(CaptainID,CollegeN, NumberOfPlayers))
        db_connection.commit()

        cursor.close()

        return render_template('weight1.html', CaptainID = CaptainID ,NumberOfPlayers = NumberOfPlayers)


@app.route('/weightReg2', methods=['POST'])
def weightReg2():
    if request.method == 'POST':
        Name = request.form.getlist('Name[]')
        Age = request.form.getlist('Age[]')
        WeightClass = request.form.getlist('WeightClass[]')
        CaptainID = session['main_id']
        
        print(Name)
        print(Age)
        print(WeightClass)
    
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * from weightTeams where captain_ID = %s;", (CaptainID,))
        data = cursor.fetchall()

        team_id = data[0][0]
        

        College = data[0][2]
        print(data)
        print(team_id)
        
        query = "INSERT INTO weightPlayers(Name, Age, Team_ID, Weight_Class, sports) values(%s, %s ,%s, %s,'Weight-Lifting');"
        # values = (name, Age, a,team_ID)
        cursor.execute(query,(session['username'], session['Age'],team_id, WeightClass[0]))

        for i in range(len(Name)):
            # Insert each passenger's details into the database
            query = "INSERT INTO weightPlayers(Name, Age, Team_ID, Weight_Class, sports) values(%s,%s,%s,%s, 'Weight-Lifting')"
            values = (Name[i], Age[i],  team_id, WeightClass[i+1])
            cursor.execute(query, values)

        session['status'] = True
        connection.commit()
        connection.close()
    return render_template("weightConfirm.html", team_id = team_id, college = College)





@app.route('/MyWeightReg')
def MyWeightReg():
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Team_ID,Captain_ID, Collegename, sports FROM weightteams where Captain_ID = %s", (session['main_id'],))
    
    data = cur.fetchall()
    print(data)
    T_ID = 0
    if data:
        T_ID = data[0][0]
    
    print(T_ID)
    cur.close()

    ##For players
    connection = connect_to_database()
    cur = connection.cursor()

    cur.execute("SELECT Player_ID,Name, Age, Team_ID, Weight_Class FROM weightplayers where Team_ID = %s; ", (T_ID,))
    data1 = cur.fetchall()
    cur.close()

    return render_template('MyWeightReg.html', user=data, user1 = data1)







##CHECKING MY REGISTRATIONS

@app.route('/MyReg')
def MyReg():
    return render_template("YourRegistrations.html")







if __name__ == '__main__':
    app.run(debug=True)
