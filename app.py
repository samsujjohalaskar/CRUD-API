import json
from flask import Flask, request, jsonify
import gladiator as gl
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password@9674'
app.config['MYSQL_DB'] = 'Ascendo'
 
mysql = MySQL(app)

@app.route('/student', methods = ['GET', 'POST','PUT','DELETE'])
def home():
    if(request.method == 'GET'): 
        args = request.args

        if(args):   
            student_id=args['student_id']
            cursor = mysql.connection.cursor()
            try:
                cursor.execute(''' SELECT * FROM Student WHERE student_id=%s''',(student_id))
                data=cursor.fetchone()
                if(data):
                    field_names = [i[0] for i in cursor.description]

                    # length=len(field_names)
                    dict={}
                    for i in range(len(field_names)):
                        field=field_names[i]
                        dict[field]=data[i]

                    cursor.close() 
                    return jsonify({'data': dict})
            except:
                return jsonify({'data':"NO DATA FOUND"})    

        else:    
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM Student''')
            data=cursor.fetchall()
            cursor.close() 
            return jsonify({'data': data})

    if(request.method=="POST"):
        record = json.loads(request.data)
        student_Name=record["student_Name"]
        created_by=record['created_by']
        valid_data = {
            'student_Name': student_Name,
            'created_by': created_by
        }
       # assigning validations
        field_validations = (
            ('student_Name', gl.required, gl.type_(str),gl.length_min(2)),
            ('created_by', gl.required, gl.length_min(2)), 
        )
        result = gl.validate(field_validations,valid_data)
        if(bool(result)):
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO Student(student_Name,created_by) VALUES(%s,%s)''',(student_Name,created_by))
            mysql.connection.commit()
            cursor.close()
            return f"Done!!"  
        else:
            return f"Validation Error"  

    if(request.method=="PUT"):
        record = json.loads(request.data)
        args = request.args
        student_id=args['student_id']
        student_Name=record["student_Name"]
        updated_by=record['updated_by']
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE Student SET student_Name=%s,updated_by=%s WHERE student_id=%s''',(student_Name,updated_by,student_id))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!" 

    if(request.method=="DELETE"):
        args=request.args
        student_id=args['student_id']
        cursor=mysql.connection.cursor()
        cursor.execute(''' DELETE FROM Student WHERE student_id=%s''',(student_id))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"



if __name__ == '__main__':
  
    app.run(debug = True)  