from datetime import datetime
from flask import redirect
from flask import Flask,render_template, request,url_for
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Tejesh123.'
app.config['MYSQL_DB'] = 'mk'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/add',methods=['GET','POST'])
def index():
    msg=''

    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        myDate = request.form['myDate']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO todo(title,des,myDate) VALUES (%s,%s,%s) ",(title,des,myDate))

        mysql.connection.commit()
        
        cur.close()
        return redirect("/")
        
    return render_template('Add_a_to_do.html',msg=msg)

@app.route("/")

def sqldata():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM todo")
  data = cur.fetchall()
  return render_template('sqldata.html', usr=data)
 
  # (C2) RENDER HTML PAGE
  # return render_template("sql-data.html", usr=users)


@app.route("/update", methods = ['GET', 'POST'])
def update():
    msg=''
    if request.method == 'POST' and 'id' in request.form and 'title' in request.form and 'des' in request.form and 'myDate' in request.form:
            id = request.form.get['id']
            title = request.form.get['title']
            des = request.form.get['des']
            myDate = request.form.get['myDate']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM todo WHERE id = % s', (id, ))
            account = cur.fetchone()
            if account:
                cur.execute('UPDATE todo SET title =% s, des =% s, myDate =% s WHERE id =%s', (title, des, myDate,id ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return redirect("/")  
    elif request.method == 'POST':
            msg = 'Please fill out the form !'
            return redirect("/")  
    return render_template('update.html', msg = msg)
    
    
@app.route("/delete",methods=["POST","GET"])
def delete():
    msg=''
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        getid = request.form['id']
        print(getid)
        cur.execute('DELETE FROM todo WHERE id = {0}'.format(getid))
        mysql.connection.commit()       
        cur.close()
        msg = 'Record deleted successfully' 
        return redirect("/")  
    return render_template('delete.html',msg=msg)
   
   


if __name__ == "__main__":
    app.run(debug=True)