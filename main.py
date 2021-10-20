from flask import Flask,jsonify,request,redirect
from flask import render_template
import pymysql

from anytree import Node, RenderTree


app = Flask(__name__)

conn=pymysql.connect(host='localhost',
                             user='root',
                             password='1234qweasd',
                             database='mydb',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route("/anakbudi")
def anakBudi():
    cursor=conn.cursor()
    sql="select nama,kelamin from keluarga where anakdari=1 "
    data=cursor.execute(sql)
    data=cursor.fetchall()
    return jsonify(data)

@app.route("/cucubudi")
def cucuBudi():
    cursor=conn.cursor()
    sql="""SELECT cucu.nama,cucu.kelamin FROM 
keluarga kakek 
JOIN keluarga ortu ON ortu.anakdari = kakek.id 
JOIN keluarga cucu ON cucu.anakdari=ortu.id """
    data=cursor.execute(sql)
    data=cursor.fetchall()
    return jsonify(data)


@app.route("/cucuperempuanbudi")
def cucuPerempuanBudi():
    cursor=conn.cursor()
    sql="""SELECT cucu.nama,cucu.kelamin FROM 
keluarga kakek 
JOIN keluarga ortu ON ortu.anakdari = kakek.id 
JOIN keluarga cucu ON cucu.anakdari=ortu.id where cucu.kelamin="Perempuan"  """
    data=cursor.execute(sql)
    data=cursor.fetchall()
    return jsonify(data)

@app.route("/bibifarah")
def bibiFarah():
    cursor=conn.cursor()
    sql="""select distinct b.nama,b.kelamin 
from keluarga kk 
JOIN keluarga a ON a.id=kk.anakdari
Join keluarga b ON b.anakdari=a.anakdari where b.id!=(select anakdari from keluarga where nama="Farah") and b.kelamin="Perempuan"  """
    data=cursor.execute(sql)
    data=cursor.fetchall()
    return jsonify(data)

@app.route("/sepupulakifarah")
def sepupuLakiFarah():
    cursor=conn.cursor()
    sql="""select distinct c.nama,c.kelamin 
from keluarga kk 
JOIN keluarga a ON a.id=kk.anakdari
Join keluarga b ON b.anakdari=a.anakdari
join keluarga c ON c.anakdari=b.id where b.id!=(select anakdari from keluarga where nama="Hani") and c.kelamin="Laki-laki"  """
    data=cursor.execute(sql)
    data=cursor.fetchall()
    return jsonify(data)

def querydict(id,data):
    for i in data:
        if i['id']==id:
            return i['nama']

@app.route("/crud",methods=['GET','POST'])
def crud():
    cursor=conn.cursor()
    if request.method=='GET':
        rootsql="select * from keluarga where anakdari is null"
        sql="select * from keluarga"
        data=cursor.execute(sql)
        data=cursor.fetchall()
        tree={}
        strTree=''
        for i,v in enumerate(data):
            if (v['anakdari']==None):
                tree[v['nama']]=(Node(v['nama']))
            else:
                tree[v['nama']]=(Node(v['nama'],parent=tree[querydict(v['anakdari'],data)]))
        
        for pre, fill, node in RenderTree(tree['Budi']):
            strTree+=("%s%s<br>" % (pre, node.name)).replace(' ',"&ensp;")

        return render_template("index.html",data=data,strTree=strTree)
    elif request.method == 'POST':
        nama=request.form['nama']
        kelamin=request.form['kelamin']
        orangTua=request.form['orangTua']
        sql="""INSERT INTO keluarga (nama,kelamin,anakdari)
        VALUES ('%s','%s',%s) """%(nama,kelamin,orangTua)
        cursor.execute(sql)
        conn.commit()
        return redirect("./crud")
@app.route("/delete")
def delete():
    cursor=conn.cursor()
    id=request.args['id']
    sql=""" DELETE FROM keluarga WHERE id=%s"""%(id)
    cursor.execute(sql)
    conn.commit()

    return redirect("./crud")

@app.route("/edit",methods=['GET','POST'])
def edit():
    cursor=conn.cursor()
    if request.method=="POST":
        id=request.args['id']
        nama=request.form['nama']
        kelamin=request.form['kelamin']
        orangTua=request.form['orangTua']
        sql="""UPDATE keluarga 
SET nama='%s',kelamin='%s',anakdari=%s
WHERE id=%s
        """%(nama,kelamin,orangTua,id)

        cursor.execute(sql)

        return redirect("./crud")
    id=request.args['id']
    sql1=""" SELECT * FROM keluarga WHERE id=%s"""%(id)
    sql2="select * from keluarga"
    data=cursor.execute(sql1)
    data=cursor.fetchone()
    keluarga=cursor.execute(sql2)
    keluarga=cursor.fetchall()
    
    return render_template("edit.html",data=data,keluarga=keluarga)


if __name__=="__main__":
    app.run()