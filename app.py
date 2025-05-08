from flask import Flask, render_template, request, redirect, flash, session
import pymysql

app = Flask(__name__, template_folder=".")
app.secret_key = "chave-secreta"  # Necessário para sessões

# Conexão com o banco de dados
def get_connection():
    return pymysql.connect(host='localhost', user='root', password='102030', database='rmc_db')

# Lista fixa de cidades (substituindo o banco de dados para essa informação)
cidades = [
    {
        'id': 'americana',
        'nome': 'Americana',
        'populacao': '243.891',
        'area': '133,91',
        'idh': '0,819',
        'pib': '11.456.789,00',
        'site': 'https://www.americana.sp.gov.br',
        'descricao': 'Americana é conhecida por seu polo têxtil e localização estratégica no interior paulista.'
    },
    {
        'id': 'artur_nogueira',
        'nome': 'Artur Nogueira',
        'populacao': '55.340',
        'area': '178,03',
        'idh': '0,748',
        'pib': '1.234.567,89',
        'site': 'https://www.arturnogueira.sp.gov.br',
        'descricao': 'Artur Nogueira é um município com forte influência agrícola e eventos culturais regionais.'
    },
    {
        'id': 'campinas',
        'nome': 'Campinas',
        'populacao': '1.223.237',
        'area': '795,70',
        'idh': '0,805',
        'pib': '61.789.654,32',
        'site': 'https://www.campinas.sp.gov.br',
        'descricao': 'Campinas é o centro econômico e tecnológico da região, com destaque para universidades e empresas de inovação.'
    },
    {
        'id': 'cosmopolis',
        'nome': 'Cosmópolis',
        'populacao': '74.848',
        'area': '154,67',
        'idh': '0,755',
        'pib': '1.789.654,00',
        'site': 'https://www.cosmopolis.sp.gov.br',
        'descricao': 'Cosmópolis se destaca pelo setor industrial e sua história ligada à imigração europeia.'
    },
    {
        'id': 'engenheiro_coelho',
        'nome': 'Engenheiro Coelho',
        'populacao': '20.807',
        'area': '109,31',
        'idh': '0,755',
        'pib': '789.123,45',
        'site': 'https://www.engenheirocoelho.sp.gov.br',
        'descricao': 'Município tranquilo com destaque para o setor educacional e atividades agrícolas.'
    },
    {
        'id': 'holambra',
        'nome': 'Holambra',
        'populacao': '15.656',
        'area': '65,58',
        'idh': '0,783',
        'pib': '456.789,12',
        'site': 'https://www.holambra.sp.gov.br',
        'descricao': 'Conhecida como a cidade das flores, Holambra tem forte influência da cultura holandesa.'
    },
    {
        'id': 'hortolandia',
        'nome': 'Hortolândia',
        'populacao': '234.259',
        'area': '62,416',
        'idh': '0,756',
        'pib': '13.116.393,02',
        'site': 'https://www.hortolandia.sp.gov.br/',
        'descricao': 'Hortolândia é um importante polo tecnológico e industrial da região de Campinas.'
    },
    {
        'id': 'indaiatuba',
        'nome': 'Indaiatuba',
        'populacao': '256.223',
        'area': '311,55',
        'idh': '0,788',
        'pib': '14.567.890,00',
        'site': 'https://www.indaiatuba.sp.gov.br',
        'descricao': 'Indaiatuba é conhecida pela qualidade de vida, infraestrutura e indústrias de ponta.'
    },
    {
        'id': 'itatiba',
        'nome': 'Itatiba',
        'populacao': '123.336',
        'area': '322,52',
        'idh': '0,787',
        'pib': '6.123.456,78',
        'site': 'https://www.itatiba.sp.gov.br',
        'descricao': 'Itatiba é uma cidade com forte presença industrial e áreas verdes preservadas.'
    },
    {
        'id': 'jaguariuna',
        'nome': 'Jaguariúna',
        'populacao': '59.893',
        'area': '141,39',
        'idh': '0,803',
        'pib': '4.567.890,12',
        'site': 'https://www.jaguariuna.sp.gov.br',
        'descricao': 'Jaguariúna destaca-se pela área de tecnologia, turismo rural e eventos musicais.'
    },
    {
        'id': 'monte_mor',
        'nome': 'Monte Mor',
        'populacao': '65.977',
        'area': '241,13',
        'idh': '0,739',
        'pib': '2.345.678,90',
        'site': 'https://www.montemor.sp.gov.br',
        'descricao': 'Monte Mor é um município com crescente expansão urbana e localização estratégica.'
    },
    {
        'id': 'morungaba',
        'nome': 'Morungaba',
        'populacao': '13.781',
        'area': '146,75',
        'idh': '0,773',
        'pib': '678.901,23',
        'site': 'https://www.morungaba.sp.gov.br',
        'descricao': 'Morungaba é uma estância climática cercada de natureza, ideal para turismo ecológico.'
    },
    {
        'id': 'nova_odessa',
        'nome': 'Nova Odessa',
        'populacao': '61.198',
        'area': '73,85',
        'idh': '0,789',
        'pib': '2.123.456,78',
        'site': 'https://www.novaodessa.sp.gov.br',
        'descricao': 'Nova Odessa possui forte setor de serviços e boa qualidade de vida.'
    },
    {
        'id': 'paulinia',
        'nome': 'Paulínia',
        'populacao': '112.738',
        'area': '139,32',
        'idh': '0,801',
        'pib': '25.678.912,34',
        'site': 'https://www.paulinia.sp.gov.br',
        'descricao': 'Paulínia abriga o maior polo petroquímico da América Latina e possui economia robusta.'
    },
    {
        'id': 'pedreira',
        'nome': 'Pedreira',
        'populacao': '48.463',
        'area': '108,82',
        'idh': '0,774',
        'pib': '1.234.567,89',
        'site': 'https://www.pedreira.sp.gov.br',
        'descricao': 'Pedreira é famosa por suas lojas de porcelana e artesanato, sendo um atrativo turístico.'
    },
    {
        'id': 'santa_barbara_d_oeste',
        'nome': 'Santa Bárbara d’Oeste',
        'populacao': '195.610',
        'area': '271,03',
        'idh': '0,774',
        'pib': '8.765.432,10',
        'site': 'https://www.santabarbara.sp.gov.br',
        'descricao': 'Cidade com rica história industrial e tradicional Festa Confederada.'
    },
    {
        'id': 'santo_antonio_de_posse',
        'nome': 'Santo Antônio de Posse',
        'populacao': '24.476',
        'area': '154,89',
        'idh': '0,747',
        'pib': '567.890,12',
        'site': 'https://www.pmdposse.sp.gov.br',
        'descricao': 'Cidade de pequeno porte com economia baseada na agropecuária e pequenas indústrias.'
    },
    {
        'id': 'sumare',
        'nome': 'Sumaré',
        'populacao': '289.611',
        'area': '153,47',
        'idh': '0,764',
        'pib': '12.345.678,90',
        'site': 'https://www.sumare.sp.gov.br',
        'descricao': 'Sumaré é um importante polo industrial e residencial na RMC.'
    },
    {
        'id': 'valinhos',
        'nome': 'Valinhos',
        'populacao': '132.984',
        'area': '148,54',
        'idh': '0,819',
        'pib': '7.890.123,45',
        'site': 'https://www.valinhos.sp.gov.br',
        'descricao': 'Conhecida pela Festa do Figo, Valinhos combina agricultura com setor imobiliário forte.'
    },
    {
        'id': 'vinhedo',
        'nome': 'Vinhedo',
        'populacao': '81.516',
        'area': '81,60',
        'idh': '0,817',
        'pib': '6.789.012,34',
        'site': 'https://www.vinhedo.sp.gov.br',
        'descricao': 'Vinhedo oferece excelente qualidade de vida, com infraestrutura moderna e natureza.'
    },
]


# Usuário administrador (para login)
USUARIO_ADMIN = {
    "username": "admin",
    "password": "1234"  
}

# Página principal
@app.route('/')
def index():
    return render_template('index.html', cidades=cidades)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USUARIO_ADMIN["username"] and password == USUARIO_ADMIN["password"]:
            session['usuario'] = username
            flash("Login realizado com sucesso!", "success")
            return redirect('/sugestoes')
        else:
            flash("Usuário ou senha incorretos!", "danger")
            return render_template('index.html', abrir_modal=True)

    return render_template('index.html')



# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Logout realizado!", "info")
    return redirect('/login')

# Página protegida de sugestões
@app.route('/sugestoes')
def listar_sugestoes():
    if 'usuario' not in session:
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect('/login')

    termo = request.args.get('termo', '')
    conn = get_connection()
    cursor = conn.cursor()

    if termo:
        cursor.execute("SELECT * FROM sugestoes WHERE mensagem LIKE %s", ('%' + termo + '%',))
    else:
        cursor.execute("SELECT * FROM sugestoes ORDER BY data_envio DESC")

    sugestoes = cursor.fetchall()
    conn.close()
    return render_template('sugestoes.html', sugestoes=sugestoes, termo=termo)

# Rota para enviar sugestões
@app.route('/enviar_sugestao', methods=['POST'])
def enviar_sugestao():
    try:
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sugestoes (nome, email, mensagem, data_envio) VALUES (%s, %s, %s, NOW())",
                       (nome, email, mensagem))
        conn.commit()
        conn.close()

        flash("Sugestão enviada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao enviar sugestão: {e}", "danger")

    return redirect('/')

# Rota para excluir sugestões
@app.route('/excluir_sugestao/<int:id>', methods=['POST'])
def excluir_sugestao(id):
    if 'usuario' not in session:
        flash("Você precisa fazer login para excluir sugestões.", "warning")
        return redirect('/login')

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sugestoes WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash("Sugestão excluída com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir sugestão: {e}", "danger")

    return redirect('/sugestoes')

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
