from flask import Flask, render_template, request, redirect
from random import randint
import sqlite3
app=Flask(__name__)

subject_list=['English','Chinese','Math','LS','M1/M2','X1','X2','X3']

@app.route('/')
def hello():
    return render_template('main.htm')


@app.route('/revision', methods=['POST', 'GET'])
def draw_subject():
    if request.method == 'POST':
        hours=request.form['hours']
        minutes=request.form['minutes']

        conn= sqlite3.connect('revision.db')
        cur = conn.cursor()
        cur.execute('SELECT * from revision')
        conn.commit()
        data_list =[]
        
        for row in cur:
            data_list.append(row)
        
        if len(data_list) ==0:
            data_list = subject_list 
            for subject in subject_list:
                cur.execute('INSERT INTO revision(subject, id) VALUES (?,?)' ,(subject,subject_list.index(subject)+1))
                conn.commit()
        else:
            pass
        
        if len(data_list) ==1:
            result=data_list[0][0]
 
        else:
            result= data_list[randint(0,len(data_list)-1)][0]

        #insert draw subject into test database
        index=int(subject_list.index(result)+1)
        print(index)

        cur.execute('INSERT INTO test(subject, id) VALUES (?,?)' ,(result,index))
        conn.commit()

        #delete draw subject from the subject database
        sql = 'DELETE FROM revision WHERE id=?'
        conn= sqlite3.connect('revision.db')
        cur = conn.cursor()
        cur.execute(sql, (index,))
        conn.commit()
        return render_template('list.html', subject=result, minute=minutes, hour=hours)
    else:
        return render_template('revision.html')


@app.route('/test',methods=['POST','GET'])
def test():
    if request.method == 'POST':
        conn= sqlite3.connect('revision.db')
        cur = conn.cursor()
        finished=request.form['finishedSubject']
        sql = 'DELETE FROM test WHERE id=?'
        finished=finished.split(',')
        print(finished)
        if type(finished) ==list:
            for i in finished:
                index=int(subject_list.index(i)+1)
                cur.execute(sql, (index,))
            conn.commit()
        return redirect('/')
    else:
        conn = sqlite3.connect('revision.db')
        cur =conn.cursor()
        cur.execute('SELECT * from test')
        conn.commit()
        test_list =[]
        for row in cur:
            test_list.append(row[0])
        return render_template('test.htm', tests=test_list, length=len(test_list))


if __name__=="__main__":
    app.run(debug=True)


