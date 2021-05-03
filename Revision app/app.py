from flask import Flask, render_template, request, redirect, url_for
from random import randint
import sqlite3
app=Flask(__name__)

subject_list=['English','Chinese','Math','LS','M1-M2','X1','X2','X3']

def get_index(subject):
    return int(subject_list.index(subject)+1)

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
                cur.execute('INSERT INTO revision(subject, id) VALUES (?,?)' ,(subject,get_index(subject)))
                conn.commit()
        else:
            pass
        
        if len(data_list) ==1:
            result=data_list[0][0]
 
        else:
            result= data_list[randint(0,len(data_list)-1)][0]

        #insert draw subject into test database
        index=get_index(result)

        cur.execute('INSERT INTO test(subject, id) VALUES (?,?)' ,(result,index))
        conn.commit()

        #delete draw subject from the subject database
        delete_statement = 'DELETE FROM revision WHERE id=?'
        cur.execute(delete_statement, (index,))
        conn.commit()

        note_statement='SELECT * from notes where id=?'
        cur.execute(note_statement, (index,))
        conn.commit()
        for row in cur:
            note=row[1]

        return redirect(url_for('revising',subject=result, minute=minutes, hours=hours, note=note))
    else:
        return render_template('revision.html')


@app.route('/revising/<subject>/<minute>/<hours>/<note>',methods=['POST','GET'])
def revising(subject, minute, hours, note):
    if request.method == 'POST':
        new_note=request.form['new_note']
        print(new_note)
        conn= sqlite3.connect('revision.db')
        cur = conn.cursor()
        sql_update_query = "Update notes set notes = ? where id = ?"
        cur.execute(sql_update_query, (new_note, get_index(subject)))
        conn.commit()
        return redirect('/revision')
    else:
        return render_template('list.html', subject=subject, minute=minute, hour=hours, notes=note)


@app.route('/test',methods=['POST','GET'])
def test():
    if request.method == 'POST':
        conn= sqlite3.connect('revision.db')
        cur = conn.cursor()
        finished=request.form['finishedSubject']
        sql = 'DELETE FROM test WHERE id=?'
        finished=finished.split(',')
        print(finished)
        for i in finished:
            try:
                index=int(subject_list.index(i)+1)
                cur.execute(sql, (index,))
            except:
                ValueError()
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


