from flask import Flask, render_template, request, redirect, flash, session, url_for
import pymysql

app = Flask(__name__, template_folder=".")
app.secret_key = "chave-secreta"  # Necessário para sessões

# Conexão com o banco de dados
def get_connection():
    return pymysql.connect(host='localhost', user='root', password='102030', database='rmc_db')

# Lista fixa de cidades 
cidades = [
    {
        'id': 'americana',
        'nome': 'Americana',
        'populacao': '243.891',
        'area': '133,91',
        'idh': '0,819',
        'pib': '11.456.789,00',
        'site': 'https://www.americana.sp.gov.br',
        'descricao': 'Americana surgiu como um bairro de Santa Bárbara d’Oeste e cresceu com a chegada da ferrovia e dos imigrantes norte-americanos após a Guerra Civil dos EUA. Hoje, é uma cidade industrializada, com forte presença cultural e qualidade de vida.'
    },
    {
        'id': 'artur_nogueira',
        'nome': 'Artur Nogueira',
        'populacao': '55.340',
        'area': '178,03',
        'idh': '0,748',
        'pib': '1.234.567,89',
        'site': 'https://www.arturnogueira.sp.gov.br',
        'descricao': 'Artur Nogueira é conhecida como a "Cidade Simpatia", com clima de interior e forte espírito comunitário. Com tradição na agricultura e eventos religiosos, destaca-se também por abrigar o centro universitário Unasp, referência na região.'
    },
    {
        'id': 'campinas',
        'nome': 'Campinas',
        'populacao': '1.223.237',
        'area': '795,70',
        'idh': '0,805',
        'pib': '61.789.654,32',
        'site': 'https://www.campinas.sp.gov.br',
        'descricao': 'Campinas é o coração da RMC e surgiu no século XVIII como parada de bandeirantes. Cresceu com o café, industrializou-se e hoje é um dos maiores polos de tecnologia, ciência e educação do país, com vida urbana intensa e centros de inovação.'
    },
    {
        'id': 'cosmopolis',
        'nome': 'Cosmópolis',
        'populacao': '74.848',
        'area': '154,67',
        'idh': '0,755',
        'pib': '1.789.654,00',
        'site': 'https://www.cosmopolis.sp.gov.br',
        'descricao': 'Cosmópolis tem raízes no ciclo do café e ganhou forma com a chegada da ferrovia no século XIX. Hoje, preserva sua herança cultural, abriga indústrias e áreas rurais produtivas, sendo destaque no turismo rural e religioso.'
    },
    {
        'id': 'engenheiro_coelho',
        'nome': 'Engenheiro Coelho',
        'populacao': '20.807',
        'area': '109,31',
        'idh': '0,755',
        'pib': '789.123,45',
        'site': 'https://www.engenheirocoelho.sp.gov.br',
        'descricao': 'Engenheiro Coelho é um recanto tranquilo do Circuito das Águas Paulista. Com raízes no cultivo de café e cana-de-açúcar, ganhou visibilidade por sediar o Unasp, e hoje atrai visitantes pelas áreas verdes e atmosfera acolhedora.'
    },
    {
        'id': 'holambra',
        'nome': 'Holambra',
        'populacao': '15.656',
        'area': '65,58',
        'idh': '0,783',
        'pib': '456.789,12',
        'site': 'https://www.holambra.sp.gov.br',
        'descricao': 'Holambra, a 134 km de São Paulo, é conhecida como a “Cidade das Flores” e maior produtora de flores da América Latina. Fundada por imigrantes holandeses, preserva suas raízes através da arquitetura, gastronomia e festas típicas. O destaque é a Expoflora, maior evento do setor no continente. A cidade também abriga o maior moinho da América Latina e atrações culturais ligadas à imigração.'
    },
    {
        'id': 'hortolandia',
        'nome': 'Hortolândia',
        'populacao': '234.259',
        'area': '62,416',
        'idh': '0,756',
        'pib': '13.116.393,02',
        'site': 'https://www.hortolandia.sp.gov.br/',
        'descricao': 'Hortolândia tem pouco mais de três décadas como cidade e já se destaca por sua vocação tecnológica e ambiental. Com parques urbanos, empresas de ponta e localização estratégica, é símbolo de crescimento acelerado e sustentável na região.'
    },
    {
        'id': 'indaiatuba',
        'nome': 'Indaiatuba',
        'populacao': '256.223',
        'area': '311,55',
        'idh': '0,788',
        'pib': '14.567.890,00',
        'site': 'https://www.indaiatuba.sp.gov.br',
        'descricao': 'Indaiatuba mescla tradição e modernidade, com raízes rurais e forte influência italiana. É hoje uma das cidades mais bem avaliadas em qualidade de vida no Brasil, com áreas verdes, polo industrial e infraestrutura urbana planejada.'
    },
    {
        'id': 'itatiba',
        'nome': 'Itatiba',
        'populacao': '123.336',
        'area': '322,52',
        'idh': '0,787',
        'pib': '6.123.456,78',
        'site': 'https://www.itatiba.sp.gov.br',
        'descricao': 'Itatiba, a "Princesa da Colina", está localizada a 84 km da capital e integra o Circuito das Frutas, com destaque para a tradicional Festa do Caqui. A cidade oferece turismo rural, histórico-cultural e de negócios, além de atrações como o Zooparque, planetário e belos casarões do século XIX. É também reconhecida como a Capital Brasileira do Móvel Colonial.'
    },
    {
        'id': 'jaguariuna',
        'nome': 'Jaguariúna',
        'populacao': '59.893',
        'area': '141,39',
        'idh': '0,803',
        'pib': '4.567.890,12',
        'site': 'https://www.jaguariuna.sp.gov.br',
        'descricao': 'Jaguariúna cresceu ao redor da ferrovia e preserva esse passado com o charmoso trem turístico. Com vocação tecnológica e eventos culturais como o rodeio e o festival de jazz, é um destino vibrante e multifacetado da RMC.'
    },
    {
        'id': 'monte_mor',
        'nome': 'Monte Mor',
        'populacao': '65.977',
        'area': '241,13',
        'idh': '0,739',
        'pib': '2.345.678,90',
        'site': 'https://www.montemor.sp.gov.br',
        'descricao': 'Monte Mor combina história, desde sua emancipação no século XIX, com dinamismo industrial e agrícola. A cidade tem localização estratégica, áreas verdes e vem crescendo com equilíbrio entre o urbano e o rural.'
    },
    {
        'id': 'morungaba',
        'nome': 'Morungaba',
        'populacao': '13.781',
        'area': '146,75',
        'idh': '0,773',
        'pib': '678.901,23',
        'site': 'https://www.morungaba.sp.gov.br',
        'descricao': 'Morungaba, a 103 km de São Paulo, é uma estância turística com clima agradável, belas paisagens e tradição em doces artesanais sem conservantes. Localizada no Circuito das Frutas, oferece também trilhas, parques ecológicos e culinária com especiarias e licores. Seu ambiente acolhedor e tranquilo atrai turistas em busca de natureza e sabores caseiros.'
    },
    {
        'id': 'nova_odessa',
        'nome': 'Nova Odessa',
        'populacao': '61.198',
        'area': '73,85',
        'idh': '0,789',
        'pib': '2.123.456,78',
        'site': 'https://www.novaodessa.sp.gov.br',
        'descricao': 'Nova Odessa nasceu como colônia para imigrantes europeus e hoje é modelo de urbanismo e sustentabilidade. Com o Jardim Botânico e projetos ecológicos, é referência em preservação ambiental e qualidade de vida.'
    },
    {
        'id': 'paulinia',
        'nome': 'Paulínia',
        'populacao': '112.738',
        'area': '139,32',
        'idh': '0,801',
        'pib': '25.678.912,34',
        'site': 'https://www.paulinia.sp.gov.br',
        'descricao': 'Paulínia ganhou projeção nacional com a instalação da refinaria da Petrobras e tornou-se um dos maiores polos petroquímicos do país. Com teatro moderno e infraestrutura urbana, mistura indústria, cultura e inovação.'
    },
    {
        'id': 'pedreira',
        'nome': 'Pedreira',
        'populacao': '48.463',
        'area': '108,82',
        'idh': '0,774',
        'pib': '1.234.567,89',
        'site': 'https://www.pedreira.sp.gov.br',
        'descricao': 'Pedreira, localizada a 133 km de São Paulo, é conhecida como a "Capital da Porcelana" devido às suas mais de 500 lojas que vendem louças e artesanatos direto da fábrica. Com belas paisagens e cortada pelo Rio Jaguari, é integrante do Circuito das Águas Paulista e tornou-se Município de Interesse Turístico em 2017. A cidade também se destaca pelo turismo cultural e religioso, como o Complexo Turístico do Morro do Cristo. Seu nome vem dos muitos “Pedros” da família fundadora Godoy Moreira.'
    },
    {
        'id': 'santa_barbara_d_oeste',
        'nome': 'Santa Bárbara d’Oeste',
        'populacao': '195.610',
        'area': '271,03',
        'idh': '0,774',
        'pib': '8.765.432,10',
        'site': 'https://www.santabarbara.sp.gov.br',
        'descricao': 'Santa Bárbara d’Oeste preserva a memória dos imigrantes norte-americanos que chegaram após a Guerra Civil dos EUA. Rica em história, é também um importante polo industrial, com tradição cultural e eventos como o Santa Bárbara Rock Fest.'
    },
    {
        'id': 'santo_antonio_de_posse',
        'nome': 'Santo Antônio de Posse',
        'populacao': '24.476',
        'area': '154,89',
        'idh': '0,747',
        'pib': '567.890,12',
        'site': 'https://www.pmdposse.sp.gov.br',
        'descricao': 'Santo Antônio de Posse é um refúgio rural com forte vocação agrícola, especialmente na produção de frutas. Com paisagens tranquilas, festas tradicionais e hospitalidade típica do interior paulista, atrai quem busca contato com a natureza.'
    },
    {
        'id': 'sumare',
        'nome': 'Sumaré',
        'populacao': '289.611',
        'area': '153,47',
        'idh': '0,764',
        'pib': '12.345.678,90',
        'site': 'https://www.sumare.sp.gov.br',
        'descricao': 'Sumaré cresceu com a chegada da ferrovia e a força da industrialização. Hoje é uma cidade populosa com economia diversificada, importante parque fabril e localização privilegiada no eixo entre Campinas e Americana.'
    },
    {
        'id': 'valinhos',
        'nome': 'Valinhos',
        'populacao': '132.984',
        'area': '148,54',
        'idh': '0,819',
        'pib': '7.890.123,45',
        'site': 'https://www.valinhos.sp.gov.br',
        'descricao': 'Valinhos é cercada por plantações de figo e goiaba, frutas que marcam sua identidade agrícola. Com boa infraestrutura urbana, festas tradicionais e clima acolhedor, é um dos destinos mais tranquilos e valorizados da RMC.'
    },
    {
        'id': 'vinhedo',
        'nome': 'Vinhedo',
        'populacao': '81.516',
        'area': '81,60',
        'idh': '0,817',
        'pib': '6.789.012,34',
        'site': 'https://www.vinhedo.sp.gov.br',
        'descricao': 'Vinhedo nasceu entre vinhedos e colinas e mantém viva sua herança italiana. Famosa pela tradicional Festa da Uva, combina charme rural com crescimento urbano, sendo destino certo para quem busca lazer e boa gastronomia.'
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
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    next_page = request.form.get('next')

    if username == USUARIO_ADMIN["username"] and password == USUARIO_ADMIN["password"]:
        session['usuario'] = username
        flash("Login realizado com sucesso!", "success")
        return redirect(next_page or url_for('listar_sugestoes'))
    else:
        flash("Usuário ou senha incorretos!", "danger")
        return render_template('index.html', cidades=cidades, abrir_modal=True)



# Página protegida de sugestões
@app.route('/sugestoes')
def listar_sugestoes():
    if 'usuario' not in session:
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for('index', next='/sugestoes'))

    termo = request.args.get('termo', '')
    conn = get_connection()
    cursor = conn.cursor()

    if termo:
        cursor.execute("SELECT * FROM sugestoes WHERE mensagem LIKE %s ORDER BY data_envio DESC", ('%' + termo + '%',))
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
