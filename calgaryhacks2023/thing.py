import mysql.connector
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


class Kid:
    def __init__(self, name, age, sex, country, about, tags, image):
        self.name = name
        self.age = age
        self.sex = sex
        self.country = country
        self.about = about
        self.tags = tags
        self.image = image

    def add_tag(self, tag):
        self.tags.append(tag)

    def insert_into_db(self):
        try:
            # connect to the database
            mydb = mysql.connector.connect(
                host="host",
                user="root",
                password="password",
                database="Profiles"
            )

            # create a cursor object
            mycursor = mydb.cursor()

            # generate SQL query to insert child data
            sql = "INSERT INTO Profiles (name, age, sex, country, about, tags, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (self.name, self.age, self.sex, self.country, self.about, str(self.tags), self.image)

            # execute query
            mycursor.execute(sql, val)

            # commit changes to the database
            mydb.commit()

            # close the database connection
            mydb.close()
        except Exception as e:
            print(f"Error: {e}")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        country = request.form['country']
        about = request.form['about']
        tags = request.form['tags']
        image = request.form['image']
        
        tags_as_list = tags.split()

        # create a Kid object
        new_kid = Kid(name, age, gender, country, about, tags_as_list, image)
        print(new_kid.name)
        # add the Kid to the database
        new_kid.insert_into_db()
        return render_template("Form.html")
        
    else:
        try:
            # connect to the database
            mydb = mysql.connector.connect(
                host="host",
                user="user",
                password="password",
                database="Profiles"
            )

            # create a cursor object
            mycursor = mydb.cursor()

            # execute SQL query to fetch all kid data
            mycursor.execute("SELECT * FROM Profiles")

            # get all rows from the result
            result = mycursor.fetchall()

            # create a list of Kid objects from the result
            kids = []
            for row in result:
                name, age, sex, country, about, tags, image = row
                tags = tags.split(", ")
                new_kid = Kid(name, age, sex, country, about, tags, image)
                kids.append(new_kid)

            # close the database connection
            mydb.close()
        except Exception as e:
                print(f"Error: {e}")

        return render_template('kid.html', kids=kids)
        

if __name__ == '__main__':
    app.run(debug=True)
    
