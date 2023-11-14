from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql


app = Flask(__name__)
app.secret_key = "meublogjp"


usuario = "samantha2303"
senha = "samanthasenai"
login = False


#FUNÇÃO SESSÃO
def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False


#CONEXÃO COM O BANCO DE DADOS
def conecta_database():
    conexao = sql.connect("db_blog.db")
    conexao.row_factory = sql.Row
    return conexao


#INICIAR O BANCO DE DADOS
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()


#ROTA DA PÁGINA INICIAL
@app.route('/')
def index():
    global login
    iniciar_db() #chamando o BD
    conexao = conecta_database()
    posts = conexao.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conexao.close()
    if verifica_sessao():
        login = True
    else:
        login = False
    return render_template("home.html", posts=posts,login=login)
   
#ROTA PARA ABRIR O FORMULÁRIO DE CADASTRO
@app.route("/novopost")
def novopost():
    global login
    if verifica_sessao():
        return render_template("novopost.html")
    else:
        return render_template("login.html")




#ROTA PARA RECEBER A POSTAGEM DO FORMULÁRIO
@app.route("/cadpost", methods=['POST'])
def cadpost():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    conexao = conecta_database()
    conexao.execute('INSERT INTO posts (titulo,conteudo) VALUES (?,?)',(titulo,conteudo))
    conexao.commit()
    conexao.close()
    return redirect('/')


#ROTA DE EXCLUSÃO
@app.route("/excluir/<id>")
def excluir(id):
    #id = int(id)
    conexao = conecta_database()
    conexao.execute('DELETE FROM posts WHERE id = ?',(id,))
    conexao.commit()
    conexao.close()
    return redirect('/')


#ROTA DA PÁGINA LOGIN
@app.route("/login")
def login():
    return render_template("login.html")


#ROTA PARA VERIFICAR O ACESSO O ADMIN
@app.route("/acesso", methods=['POST'])
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]


    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/') #homepage
    else:
        return render_template("login.html",msg="Usuário/Senha estão errados!")
   


#código do LOGOUT
@app.route("/logout")
def logout():
    global login
    login = False
    session.clear()
    return redirect('/')

@app.route("/editar/<id>")
def editar(id):
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        posts = conexao.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchall()
        conexao.close()
        return render_template("editar.html",posts=posts)
    
# rota da edição
@app.route("/editpost", methods=['POST'])
def editpost():
    id = request.form['id']
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    conexao = conecta_database()
    conexao.execute('UPDATE posts SET titulo = ?, conteudo = ? WHERE id = ?',(titulo,conteudo,id,))
    conexao.commit() #Confirma a alteração no BD
    conexao.close()
    return redirect('/')



#FINAL DO CÓDIGO - EXECUTANDO O SERVIDOR
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)





#FINAL DO CÓDIGO - EXECUTANDO O SERVIDOR
#app.run(debug=True)
