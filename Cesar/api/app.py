# =====================================================================
# Beta da Versão com imagens e reorganizada pra integrar com a versão do André
# =====================================================================
# --- 1. Imports e Configuração Inicial ---
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, date
from werkzeug.utils import secure_filename
import uuid

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CORS(app)
ITEMS_PER_PAGE = 20



# --- 2. Funções Auxiliares ---
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME')
    )

def format_date(date_obj):
    if not date_obj or str(date_obj) == '0001-01-01': return None
    if isinstance(date_obj, (datetime, date)): return date_obj.strftime('%Y-%m-%d')
    return str(date_obj)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rota para Servir Arquivos de Imagem ---
@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#filtros geograficos
@app.route('/api/filtros_geograficos', methods=['GET'])
def get_filtros_geograficos():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT DISTINCT PAIS, ESTADO, CIDADE
            FROM (
                SELECT PAIS, ESTADO, CIDADE FROM templo
                UNION
                SELECT PAIS_ORIGEM_PERSONALIDADE AS PAIS, ESTADO_ORIGEM AS ESTADO, CIDADE_ORIGEM AS CIDADE FROM personalidade
                UNION
                SELECT PAIS_SEDE AS PAIS, ESTADO_SEDE AS ESTADO, CIDADE_SEDE AS CIDADE FROM associacao
            ) AS geografia
            WHERE PAIS IS NOT NULL OR ESTADO IS NOT NULL OR CIDADE IS NOT NULL
        """)
        rows = cursor.fetchall()
        conn.close()

        paises = sorted(set(r['PAIS'] for r in rows if r['PAIS']))
        estados = sorted(set(r['ESTADO'] for r in rows if r['ESTADO']))
        cidades = sorted(set(r['CIDADE'] for r in rows if r['CIDADE']))

        return jsonify({
            "paises": paises,
            "estados": estados,
            "cidades": cidades
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#O Route das pesquisas (tem de todos aí dentro)
@app.route('/api/search', methods=['GET'])
def global_search():
    conn = None
    cursor = None
    try:
        search_term = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        offset = (page - 1) * ITEMS_PER_PAGE
        
        if not search_term:
            return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Busca em templos
        cursor.execute("""
            SELECT 'templo' AS type, ID_TEMPLO AS id, NOME AS name, 
                   PAIS AS country, ESCOLA AS school,
                   DATA_ABERTURA, DATA_FECHAMENTO
            FROM templo 
            WHERE NOME LIKE %s OR PAIS LIKE %s OR ESCOLA LIKE %s
            LIMIT %s OFFSET %s
        """, [f"%{search_term}%"]*3 + [ITEMS_PER_PAGE, offset])
        templos = cursor.fetchall()
        for t in templos:
            t['DATA_ABERTURA'] = format_date(t.get('DATA_ABERTURA'))
            t['DATA_FECHAMENTO'] = format_date(t.get('DATA_FECHAMENTO'))

        # Busca em personalidades
        cursor.execute("""
            SELECT 'personalidade' AS type, ID_PERSONALIDADE AS id, 
                   NOME_PERSONALIDADE AS name, PAIS_ORIGEM_PERSONALIDADE AS country,
                   DATA_NASCIMENTO, DATA_MORTE
            FROM personalidade 
            WHERE NOME_PERSONALIDADE LIKE %s OR PAIS_ORIGEM_PERSONALIDADE LIKE %s
            LIMIT %s OFFSET %s
        """, [f"%{search_term}%"]*2 + [ITEMS_PER_PAGE, offset])
        personalidades = cursor.fetchall()
        for p in personalidades:
            p['DATA_NASCIMENTO'] = format_date(p.get('DATA_NASCIMENTO'))
            p['DATA_MORTE'] = format_date(p.get('DATA_MORTE'))

        # Busca em associações
        cursor.execute("""
            SELECT 'associacao' AS type, ID_ASSOCIACAO AS id, 
                   NOME_ASSOCIACAO AS name, PAIS_ATUACAO AS country,
                   DATA_ABERTURA_ASSOCIACAO, DATA_FECHAMENTO_ASSOCIACAO
            FROM associacao 
            WHERE NOME_ASSOCIACAO LIKE %s OR PAIS_ATUACAO LIKE %s
            LIMIT %s OFFSET %s
        """, [f"%{search_term}%"]*2 + [ITEMS_PER_PAGE, offset])
        associacoes = cursor.fetchall()
        for a in associacoes:
            a['DATA_ABERTURA_ASSOCIACAO'] = format_date(a.get('DATA_ABERTURA_ASSOCIACAO'))
            a['DATA_FECHAMENTO_ASSOCIACAO'] = format_date(a.get('DATA_FECHAMENTO_ASSOCIACAO'))

        results = templos + personalidades + associacoes

        return jsonify({
            "results": results,
            "page": page,
            "per_page": ITEMS_PER_PAGE,
            "total_results": len(results)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()



@app.route('/api/stats/uploads', methods=['GET'])
def get_upload_stats():
    stats = {}
    try:
        total_size_uploads = 0
        file_count = 0
        folder_path = app.config['UPLOAD_FOLDER']
        
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                path = os.path.join(folder_path, filename)
                if os.path.isfile(path):
                    total_size_uploads += os.path.getsize(path)
                    file_count += 1
        
        if total_size_uploads >= 1024**3:
            stats['total_size_str'] = f"{total_size_uploads / (1024**3):.2f} GB"
        elif total_size_uploads >= 1024**2:
            stats['total_size_str'] = f"{total_size_uploads / (1024**2):.2f} MB"
        elif total_size_uploads >= 1024:
            stats['total_size_str'] = f"{total_size_uploads / 1024:.2f} KB"
        else:
            stats['total_size_str'] = f"{total_size_uploads} Bytes"
        
        stats['file_count'] = file_count
        stats['total_size_bytes'] = total_size_uploads
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats/database', methods=['GET'])
def get_database_stats():
    stats = {}
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        db_name = os.getenv('DB_NAME')
        cursor.execute("""
            SELECT SUM(data_length + index_length) AS size_bytes
            FROM information_schema.TABLES
            WHERE table_schema = %s
        """, (db_name,))
        
        result = cursor.fetchone()
        total_size_db = result['size_bytes'] if result and result['size_bytes'] else 0

        if total_size_db >= 1024**3:
            stats['db_size_str'] = f"{total_size_db / (1024**3):.2f} GB"
        elif total_size_db >= 1024**2:
            stats['db_size_str'] = f"{total_size_db / (1024**2):.2f} MB"
        elif total_size_db >= 1024:
            stats['db_size_str'] = f"{total_size_db / 1024:.2f} KB"
        else:
            stats['db_size_str'] = f"{total_size_db} Bytes"
            
        stats['db_size_bytes'] = int(total_size_db) # Garante que seja um inteiro
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- 3. Rotas de Autenticação e Usuários (A parte da administração e moderação)-----------------------------------------------

#Fazer o login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    nome, senha = data.get('nome'), data.get('senha')
    if not nome or not senha:
        return jsonify({"error": "Nome e senha são obrigatórios."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE NOME = %s", (nome,))
        usuario = cursor.fetchone()
        if not usuario or usuario['SENHA'] != senha:
            return jsonify({"error": "Credenciais inválidas."}), 401
        return jsonify({
            "id": usuario["ID_USUARIO"], "nome": usuario["NOME"], "tipo": usuario["TIPO_CONTA"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


#criação de novo usuario via conta de Admin, sempre cria moderadores
@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    nome = data.get("nome")
    senha = data.get("senha")
    tipo = data.get("tipo", "moderador")  # o padrão é moderador

    if not nome or not senha or tipo not in ("admin", "moderador"):
        return jsonify({"error": "Campos obrigatórios ausentes ou tipo inválido."}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # Verificar se já existe um usuário com esse nome
        cursor.execute("SELECT * FROM usuario WHERE NOME = %s", (nome,))
        if cursor.fetchone():
            return jsonify({"error": "Nome de usuário já existe."}), 409

        # Inserir usuário com senha em texto plano
        cursor.execute(
            "INSERT INTO usuario (NOME, SENHA, TIPO_CONTA) VALUES (%s, %s, %s)",
            (nome, senha, tipo)
        )
        conn.commit()

        return jsonify({"message": "Usuário criado com sucesso."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


#lista os moderadores pro Admin
@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    tipo = request.args.get('tipo', 'moderador')

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT ID_USUARIO, NOME, TIPO_CONTA FROM usuario WHERE TIPO_CONTA = %s", (tipo,))
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


#deleta um moderador
@app.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuario WHERE ID_USUARIO = %s AND TIPO_CONTA = 'moderador'", (id_usuario,))
        conn.commit()
        return jsonify({"message": "Moderador apagado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


#editar os dados de um moderador
@app.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    data = request.json
    nome = data.get('nome')
    senha = data.get('senha')

    if not nome and not senha:
        return jsonify({"error": "Nada para atualizar."}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        if nome:
            cursor.execute("UPDATE usuario SET NOME = %s WHERE ID_USUARIO = %s AND TIPO_CONTA = 'moderador'", (nome, id_usuario))
        if senha:
            cursor.execute("UPDATE usuario SET SENHA = %s WHERE ID_USUARIO = %s AND TIPO_CONTA = 'moderador'", (senha, id_usuario))
        conn.commit()
        return jsonify({"message": "Moderador atualizado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# --- 4. Rotas de Entidades (Templos, Personalidades, etc.) -----------------------------------------------

# 4.1 ROTAS PARA TEMPLOS -------------------------------------------------------------------------------------
@app.route('/api/templos', methods=['GET'])
def get_templos():
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        
        # --- LÓGICA ADICIONADA ---
        id_param = request.args.get('id')
        if id_param:
            cursor.execute("SELECT * FROM templo WHERE ID_TEMPLO = %s", (id_param,))
            templo = cursor.fetchone()
            if templo:
                templo['DATA_ABERTURA_TEMPLO'] = format_date(templo.get('DATA_ABERTURA_TEMPLO'))
                templo['DATA_FECHAMENTO_TEMPLO'] = format_date(templo.get('DATA_FECHAMENTO_TEMPLO'))
            return jsonify({"data": [templo] if templo else []})
        # --- FIM DA LÓGICA ADICIONADA ---

        if request.args.get('all') == 'true':
            cursor.execute("SELECT * FROM templo ORDER BY NOME")
        else:
            page = int(request.args.get('page', 1))
            offset = (page - 1) * ITEMS_PER_PAGE
            cursor.execute("SELECT * FROM templo ORDER BY NOME LIMIT %s OFFSET %s", (ITEMS_PER_PAGE, offset))
        
        templos = cursor.fetchall()
        for templo in templos:
            templo['DATA_ABERTURA_TEMPLO'] = format_date(templo.get('DATA_ABERTURA_TEMPLO'))
            templo['DATA_FECHAMENTO_TEMPLO'] = format_date(templo.get('DATA_FECHAMENTO_TEMPLO'))
        return jsonify({"data": templos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/templos', methods=['POST'])
def criar_templo():
    data = request.json
    campos_obrigatorios = ['NOME', 'VEICULO', 'PAIS', 'ESCOLA']
    if not all(campo in data and data[campo] for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios (Nome, Veículo, País, Escola) não podem estar em branco."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        # Query ATUALIZADA para incluir a nova coluna de imagem
        query = """
            INSERT INTO templo 
            (NOME, PAIS, ESTADO, MUNICIPIO, CODIGO_POSTAL, ESCOLA, VEICULO, PUBLICO_ALVO, 
            DATA_ABERTURA_TEMPLO, DATA_FECHAMENTO_TEMPLO, CAMPO_INFO_TEMPLO, IMAGEM_PERFIL_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Valores ATUALIZADOS para corresponder à nova query
        valores = (
            data.get('NOME'), data.get('PAIS'), data.get('ESTADO'), data.get('MUNICIPIO'), data.get('CODIGO_POSTAL'),
            data.get('ESCOLA'), data.get('VEICULO'), data.get('PUBLICO_ALVO'), data.get('DATA_ABERTURA_TEMPLO') or None,
            data.get('DATA_FECHAMENTO_TEMPLO') or None, data.get('CAMPO_INFO_TEMPLO'), None # 'None' para a nova IMAGEM_PERFIL_URL
        )
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Templo criado com sucesso.", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/templos/<int:id_templo>', methods=['PUT'])
def atualizar_templo(id_templo):
    data = request.json
    campos_validos = ['NOME', 'PAIS', 'ESTADO', 'MUNICIPIO', 'CODIGO_POSTAL', 'ESCOLA', 'VEICULO', 'PUBLICO_ALVO', 'DATA_ABERTURA_TEMPLO', 'DATA_FECHAMENTO_TEMPLO', 'CAMPO_INFO_TEMPLO']
    campos, valores = [], []
    for campo in campos_validos:
        if campo in data:
            valor = data[campo]
            if "DATA" in campo and not valor: valor = None
            campos.append(f"`{campo}` = %s")
            valores.append(valor)
    if not campos: return jsonify({"error": "Nada para atualizar."}), 400
    valores.append(id_templo)
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        query = f"UPDATE templo SET {', '.join(campos)} WHERE ID_TEMPLO = %s"
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Templo atualizado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/templos/<int:id_templo>', methods=['DELETE'])
def deletar_templo(id_templo):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # ATUALIZAÇÃO: Apagar arquivos de imagem do servidor antes de deletar do banco
        cursor.execute("SELECT IMAGEM_PERFIL_URL FROM templo WHERE ID_TEMPLO = %s", (id_templo,))
        perfil = cursor.fetchone()
        if perfil and perfil.get('IMAGEM_PERFIL_URL') and os.path.exists(perfil['IMAGEM_PERFIL_URL'].strip('/')):
            os.remove(perfil['IMAGEM_PERFIL_URL'].strip('/'))

        cursor.execute("SELECT URL_IMAGEM FROM imagem_templo WHERE ID_TEMPLO_FK = %s", (id_templo,))
        carrossel = cursor.fetchall()
        for img in carrossel:
            if img.get('URL_IMAGEM') and os.path.exists(img['URL_IMAGEM'].strip('/')):
                os.remove(img['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM templo WHERE ID_TEMPLO = %s", (id_templo,))
        conn.commit()
        return jsonify({"message": "Templo e imagens associadas foram apagados com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4.2 ROTAS PARA PERSONALIDADES -------------------------------------------------------------------------------------

#Rota pra buscar personalidades
@app.route('/api/personalidades', methods=['GET'])
def get_personalidades():
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        id_param = request.args.get('id')
        if id_param:
            cursor.execute("SELECT * FROM personalidade WHERE ID_PERSONALIDADE = %s", (id_param,))
            row = cursor.fetchone()
            if not row:
                return jsonify({"data": []})
            row['DATA_NASCIMENTO'] = format_date(row.get('DATA_NASCIMENTO'))
            row['DATA_MORTE'] = format_date(row.get('DATA_MORTE'))
            return jsonify({"data": [row]})
        elif request.args.get('all') == 'true':
            cursor.execute("SELECT * FROM personalidade")
            personalidades = cursor.fetchall()
            for p in personalidades:
                p['DATA_NASCIMENTO'] = format_date(p.get('DATA_NASCIMENTO'))
                p['DATA_MORTE'] = format_date(p.get('DATA_MORTE'))
            return jsonify({"data": personalidades})
        else:
            page = int(request.args.get('page', 1))
            offset = (page - 1) * ITEMS_PER_PAGE
            cursor.execute("SELECT * FROM personalidade LIMIT %s OFFSET %s", (ITEMS_PER_PAGE, offset))
            personalidades = cursor.fetchall()
            for p in personalidades:
                p['DATA_NASCIMENTO'] = format_date(p.get('DATA_NASCIMENTO'))
                p['DATA_MORTE'] = format_date(p.get('DATA_MORTE'))
            return jsonify({
                "data": personalidades,
                "page": page,
                "per_page": ITEMS_PER_PAGE
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# Rota para CRIAR uma nova Personalidade
@app.route('/api/personalidades', methods=['POST'])
def criar_personalidade():
    data = request.json
    campos_obrigatorios = ['NOME_PERSONALIDADE', 'NIVEL', 'RACA']
    if not all(campo in data and data[campo] for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios (Nome, Nível, Raça) não podem estar em branco."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO personalidade 
            (NOME_PERSONALIDADE, PAIS_ORIGEM_PERSONALIDADE, NIVEL, GENERO, RACA, 
            DATA_NASCIMENTO, DATA_MORTE, CAMPO_INFO_PERSONALIDADE, IMAGEM_PERFIL_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data.get('NOME_PERSONALIDADE'), data.get('PAIS_ORIGEM_PERSONALIDADE'), data.get('NIVEL'),
            data.get('GENERO'), data.get('RACA'), data.get('DATA_NASCIMENTO') or None,
            data.get('DATA_MORTE') or None, data.get('CAMPO_INFO_PERSONALIDADE'), None
        )
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Personalidade criada com sucesso.", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/personalidades/<int:id_personalidade>', methods=['PUT'])
def atualizar_personalidade(id_personalidade):
    data = request.json
    campos = []
    valores = []
    
    # [cite_start]Lista de colunas que podem ser atualizadas na tabela PERSONALIDADE [cite: 1]
    campos_validos = [
        'NOME_PERSONALIDADE', 'PAIS_ORIGEM_PERSONALIDADE', 'NIVEL', 'GENERO', 
        'RACA', 'DATA_NASCIMENTO', 'DATA_MORTE', 'CAMPO_INFO_PERSONALIDADE'
    ]
    
    for campo in campos_validos:
        if campo in data:
            valor = data[campo]
            # Trata campos de data vazios como nulos no banco
            if "DATA" in campo and not valor:
                valor = None
            campos.append(f"`{campo}` = %s")
            valores.append(valor)

    if not campos:
        return jsonify({"error": "Nada para atualizar."}), 400

    valores.append(id_personalidade)
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = f"UPDATE PERSONALIDADE SET {', '.join(campos)} WHERE ID_PERSONALIDADE = %s"
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Personalidade atualizada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para APAGAR uma personalidade existente
@app.route('/api/personalidades/<int:id_personalidade>', methods=['DELETE'])
def deletar_personalidade(id_personalidade):
    # ATUALIZAÇÃO: Lógica para apagar arquivos de imagem
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT IMAGEM_PERFIL_URL FROM personalidade WHERE ID_PERSONALIDADE = %s", (id_personalidade,))
        perfil = cursor.fetchone()
        if perfil and perfil.get('IMAGEM_PERFIL_URL') and os.path.exists(perfil['IMAGEM_PERFIL_URL'].strip('/')):
            os.remove(perfil['IMAGEM_PERFIL_URL'].strip('/'))
        cursor.execute("SELECT URL_IMAGEM FROM imagem_personalidade WHERE ID_PERSONALIDADE_FK = %s", (id_personalidade,))
        carrossel = cursor.fetchall()
        for img in carrossel:
            if img.get('URL_IMAGEM') and os.path.exists(img['URL_IMAGEM'].strip('/')):
                os.remove(img['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM personalidade WHERE ID_PERSONALIDADE = %s", (id_personalidade,))
        conn.commit()
        return jsonify({"message": "Personalidade e imagens associadas foram apagadas com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# 4.3 ROTAS PARA ASSOCIAÇÕES -------------------------------------------------------------------------------------
#Buscar Associação
@app.route('/api/associacoes', methods=['GET'])
def get_associacoes():
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        id_param = request.args.get('id')
        if id_param:
            cursor.execute("SELECT * FROM associacao WHERE ID_ASSOCIACAO = %s", (id_param,))
            row = cursor.fetchone()
            
            # --- CORREÇÃO AQUI ---
            # Adicionando a formatação de data que estava faltando para a busca de um único item
            if row:
                row['DATA_ABERTURA_ASSOCIACAO'] = format_date(row.get('DATA_ABERTURA_ASSOCIACAO'))
                row['DATA_FECHAMENTO_ASSOCIACAO'] = format_date(row.get('DATA_FECHAMENTO_ASSOCIACAO'))
            # --- FIM DA CORREÇÃO ---

            return jsonify({"data": [row] if row else []})
        
        # O resto da função para buscar todos os itens já estava correto
        if request.args.get('all') == 'true':
            cursor.execute("SELECT * FROM associacao ORDER BY NOME_ASSOCIACAO")
        else:
            page = int(request.args.get('page', 1))
            offset = (page - 1) * ITEMS_PER_PAGE
            cursor.execute("SELECT * FROM associacao ORDER BY NOME_ASSOCIACAO LIMIT %s OFFSET %s", (ITEMS_PER_PAGE, offset))
            
        associacoes = cursor.fetchall()
        for a in associacoes:
            a['DATA_ABERTURA_ASSOCIACAO'] = format_date(a.get('DATA_ABERTURA_ASSOCIACAO'))
            a['DATA_FECHAMENTO_ASSOCIACAO'] = format_date(a.get('DATA_FECHAMENTO_ASSOCIACAO'))
        return jsonify({"data": associacoes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

#Criar Associação
@app.route('/api/associacoes', methods=['POST'])
def criar_associacao():
    data = request.json
    campos_obrigatorios = ['NOME_ASSOCIACAO', 'GRAU', 'PAIS_ATUACAO']
    if not all(campo in data and data[campo] for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios (Nome, Grau, País de Atuação) não podem estar em branco."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO associacao 
            (NOME_ASSOCIACAO, GRAU, PAIS_ATUACAO, SEDE_ASSOCIACAO, 
            DATA_ABERTURA_ASSOCIACAO, DATA_FECHAMENTO_ASSOCIACAO, CAMPO_INFO_ASSOCIACAO, IMAGEM_PERFIL_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data.get('NOME_ASSOCIACAO'), data.get('GRAU'), data.get('PAIS_ATUACAO'),
            data.get('SEDE_ASSOCIACAO'), data.get('DATA_ABERTURA_ASSOCIACAO') or None,
            data.get('DATA_FECHAMENTO_ASSOCIACAO') or None, data.get('CAMPO_INFO_ASSOCIACAO'), None
        )
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Associação criada com sucesso.", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# Rota para ATUALIZAR uma associação existente
@app.route('/api/associacoes/<int:id_associacao>', methods=['PUT'])
def atualizar_associacao(id_associacao):
    data = request.json
    campos = []
    valores = []
    
    # [cite_start]Lista de colunas que podem ser atualizadas na tabela ASSOCIACAO [cite: 1]
    campos_validos = [
        'NOME_ASSOCIACAO', 'GRAU', 'PAIS_ATUACAO', 'SEDE_ASSOCIACAO', 
        'DATA_ABERTURA_ASSOCIACAO', 'DATA_FECHAMENTO_ASSOCIACAO', 'CAMPO_INFO_ASSOCIACAO'
    ]
    
    for campo in campos_validos:
        if campo in data:
            valor = data[campo]
            if "DATA" in campo and not valor:
                valor = None
            campos.append(f"`{campo}` = %s")
            valores.append(valor)

    if not campos:
        return jsonify({"error": "Nada para atualizar."}), 400

    valores.append(id_associacao)
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = f"UPDATE ASSOCIACAO SET {', '.join(campos)} WHERE ID_ASSOCIACAO = %s"
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Associação atualizada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para APAGAR uma associação existente
@app.route('/api/associacoes/<int:id_associacao>', methods=['DELETE'])
def deletar_associacao(id_associacao):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Apaga relações primeiro
        cursor.execute("DELETE FROM TEMPLO_ASSOCIACAO WHERE ID_ASSOCIACAO = %s", (id_associacao,))
        cursor.execute("DELETE FROM PERSONALIDADE_ASSOCIACAO WHERE ID_ASSOCIACAO = %s", (id_associacao,)) 

        # Apaga a associação principal
        cursor.execute("DELETE FROM ASSOCIACAO WHERE ID_ASSOCIACAO = %s", (id_associacao,))
        conn.commit()
        return jsonify({"message": "Associação apagada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()




# 4.4 ROTAS PARA PRODUTOS -------------------------------------------------------------------------------------

#Buscar Produto
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # --- LÓGICA ADICIONADA ---
        id_param = request.args.get('id')
        if id_param:
            cursor.execute("SELECT * FROM produto WHERE ID_PRODUTO = %s", (id_param,))
            produto = cursor.fetchone()
            if produto:
                produto['DATA_LANCAMENTO'] = format_date(produto.get('DATA_LANCAMENTO'))
            return jsonify({"data": [produto] if produto else []})
        # --- FIM DA LÓGICA ADICIONADA ---

        cursor.execute("SELECT * FROM produto ORDER BY NOME_PRODUTO")
        produtos = cursor.fetchall()
        for produto in produtos:
            if produto.get('DATA_LANCAMENTO'):
                produto['DATA_LANCAMENTO'] = format_date(produto.get('DATA_LANCAMENTO'))
        return jsonify({"data": produtos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

#Criar Produto
@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    campos_obrigatorios = ['NOME_PRODUTO', 'TIPO_PRODUTO']
    if not all(campo in data and data[campo] for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios (Nome, Tipo) não podem estar em branco."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        query = "INSERT INTO produto (NOME_PRODUTO, TIPO_PRODUTO, CAMPO_INFO_PRODUTO, DATA_LANCAMENTO, IMAGEM_PERFIL_URL) VALUES (%s, %s, %s, %s, %s)"
        valores = (
            data.get('NOME_PRODUTO'), 
            data.get('TIPO_PRODUTO'),
            data.get('CAMPO_INFO_PRODUTO'), # <- NOVO CAMPO ADICIONADO
            data.get('DATA_LANCAMENTO') or None, 
            None
        )
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Produto criado com sucesso.", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

#Editar Produto
@app.route('/api/produtos/<int:id_produto>', methods=['PUT'])
def atualizar_produto(id_produto):
    data = request.json
    campos = []
    valores = []
    
    # [cite_start]Lista de colunas que podem ser atualizadas na tabela PRODUTO [cite: 1]
    campos_validos = ['NOME_PRODUTO', 'TIPO_PRODUTO', 'DATA_LANCAMENTO']
    
    for campo in campos_validos:
        if campo in data:
            valor = data[campo]
            if "DATA" in campo and not valor:
                valor = None
            campos.append(f"`{campo}` = %s")
            valores.append(valor)

    if not campos:
        return jsonify({"error": "Nada para atualizar."}), 400

    valores.append(id_produto)
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = f"UPDATE PRODUTO SET {', '.join(campos)} WHERE ID_PRODUTO = %s"
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Produto atualizado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para APAGAR um produto existente
@app.route('/api/produtos/<int:id_produto>', methods=['DELETE'])
def deletar_produto(id_produto):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Apaga relações primeiro
        cursor.execute("DELETE FROM PERSONALIDADE_PRODUTO WHERE ID_PRODUTO = %s", (id_produto,))

        # Apaga o produto principal
        cursor.execute("DELETE FROM PRODUTO WHERE ID_PRODUTO = %s", (id_produto,))
        conn.commit()
        return jsonify({"message": "Produto apagado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# --- 5. Rotas de Relações ---

# 5.1 Buscar relações
@app.route('/api/relations/<string:entity_type>/<int:entity_id>', methods=['GET'])
def get_relations(entity_type, entity_id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        relations = {}
        
        if entity_type == 'templo':
            cursor.execute("SELECT p.*, pt.FUNCAO FROM personalidade p JOIN personalidade_templo pt ON p.ID_PERSONALIDADE = pt.ID_PT_PERSONALIDADE_FK WHERE pt.ID_PT_TEMPLO_FK = %s", [entity_id])
            relations['personalidades'] = cursor.fetchall()
            cursor.execute("SELECT a.* FROM associacao a JOIN templo_associacao ta ON a.ID_ASSOCIACAO = ta.ID_TA_ASSOCIACAO_FK WHERE ta.ID_TA_TEMPLO_FK = %s", [entity_id])
            relations['associacoes'] = cursor.fetchall()
            cursor.execute("SELECT * FROM imagem_templo WHERE ID_TEMPLO_FK = %s", [entity_id])
            relations['imagens_carrossel'] = cursor.fetchall()

        elif entity_type == 'personalidade':
            cursor.execute("SELECT t.*, pt.FUNCAO FROM templo t JOIN personalidade_templo pt ON t.ID_TEMPLO = pt.ID_PT_TEMPLO_FK WHERE pt.ID_PT_PERSONALIDADE_FK = %s", [entity_id])
            relations['templos'] = cursor.fetchall()
            cursor.execute("SELECT a.* FROM associacao a JOIN personalidade_associacao pa ON a.ID_ASSOCIACAO = pa.ID_PA_ASSOCIACAO_FK WHERE pa.ID_PA_PERSONALIDADE_FK = %s", [entity_id])
            relations['associacoes'] = cursor.fetchall()
            cursor.execute("SELECT p.* FROM PRODUTO p JOIN PERSONALIDADE_PRODUTO pp ON p.ID_PRODUTO = pp.ID_PP_PRODUTO_FK WHERE pp.ID_PP_PERSONALIDADE_FK = %s", [entity_id])
            relations['produtos'] = cursor.fetchall()
            cursor.execute("SELECT * FROM imagem_personalidade WHERE ID_PERSONALIDADE_FK = %s", [entity_id])
            relations['imagens_carrossel'] = cursor.fetchall()

        elif entity_type == 'associacao':
            cursor.execute("SELECT t.* FROM templo t JOIN templo_associacao ta ON t.ID_TEMPLO = ta.ID_TA_TEMPLO_FK WHERE ta.ID_TA_ASSOCIACAO_FK = %s", [entity_id])
            relations['templos'] = cursor.fetchall()
            cursor.execute("SELECT p.* FROM personalidade p JOIN personalidade_associacao pa ON p.ID_PERSONALIDADE = pa.ID_PA_PERSONALIDADE_FK WHERE pa.ID_PA_ASSOCIACAO_FK = %s", [entity_id])
            relations['personalidades'] = cursor.fetchall()
            cursor.execute("SELECT * FROM imagem_associacao WHERE ID_ASSOCIACAO_FK = %s", [entity_id])
            relations['imagens_carrossel'] = cursor.fetchall()

        elif entity_type == 'produto':
            cursor.execute("SELECT p.* FROM PERSONALIDADE p JOIN PERSONALIDADE_PRODUTO pp ON p.ID_PERSONALIDADE = pp.ID_PP_PERSONALIDADE_FK WHERE pp.ID_PP_PRODUTO_FK = %s", [entity_id])
            relations['personalidades'] = cursor.fetchall()
            cursor.execute("SELECT * FROM imagem_produto WHERE ID_PRODUTO_FK = %s", [entity_id])
            relations['imagens_carrossel'] = cursor.fetchall()
        
        for key, items in relations.items():
            for item in items:
                for date_field in item:
                    if 'DATA' in date_field:
                        item[date_field] = format_date(item[date_field])
                        
        return jsonify(relations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# 5.2 Conexões do templo
@app.route('/api/relations/templo/<int:templo_id>', methods=['POST'])
def adicionar_conexao_templo(templo_id):
    data = request.json
    tipo = data.get('tipo')
    id_rel = data.get('id_rel')

    if tipo not in ['personalidade', 'associacao'] or not id_rel:
        return jsonify({"error": "Tipo ou id_rel inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        if tipo == 'personalidade':
            funcao_recebida = data.get('funcao')
            
            if funcao_recebida and funcao_recebida.strip():
                valor_final_funcao = funcao_recebida
            else:
                valor_final_funcao = 'Não especificado'
            
            cursor.execute(
                "INSERT INTO personalidade_templo (ID_PT_PERSONALIDADE_FK, ID_PT_TEMPLO_FK, FUNCAO) VALUES (%s, %s, %s)", 
                (id_rel, templo_id, valor_final_funcao)
            )
        else:
            cursor.execute(
                "INSERT INTO templo_associacao (ID_TA_ASSOCIACAO_FK, ID_TA_TEMPLO_FK) VALUES (%s, %s)",
                (id_rel, templo_id)
            )

        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} adicionada com sucesso ao templo."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/relations/templo/<int:templo_id>', methods=['DELETE'])
def remover_conexao_templo(templo_id):
    tipo = request.args.get('tipo')
    id_rel = request.args.get('id_rel')

    if tipo not in ['personalidade', 'associacao'] or not id_rel:
        return jsonify({"error": "Tipo ou id_rel inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        if tipo == 'personalidade':
            cursor.execute("DELETE FROM personalidade_templo WHERE ID_PT_PERSONALIDADE_FK = %s AND ID_PT_TEMPLO_FK = %s", (id_rel, templo_id))
        else:
            cursor.execute("DELETE FROM templo_associacao WHERE ID_TA_ASSOCIACAO_FK = %s AND ID_TA_TEMPLO_FK = %s", (id_rel, templo_id))

        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} removida com sucesso do templo."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5.3 Conexões das Personalidades

@app.route('/api/relations/personalidade/<int:personalidade_id>', methods=['POST'])
def adicionar_conexao_personalidade(personalidade_id):
    data = request.json
    tipo, id_rel = data.get('tipo'), data.get('id_rel')
    if tipo not in ['templo', 'associacao', 'produto'] or not id_rel: return jsonify({"error": "Parâmetros inválidos."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        if tipo == 'templo':
            funcao = data.get('funcao', 'Não especificado').strip() or 'Não especificado'
            cursor.execute("INSERT INTO PERSONALIDADE_TEMPLO (ID_PT_PERSONALIDADE_FK, ID_PT_TEMPLO_FK, FUNCAO) VALUES (%s, %s, %s)", (personalidade_id, id_rel, funcao))
        elif tipo == 'associacao':
            cursor.execute("INSERT INTO PERSONALIDADE_ASSOCIACAO (ID_PA_PERSONALIDADE_FK, ID_PA_ASSOCIACAO_FK) VALUES (%s, %s)", (personalidade_id, id_rel))
        elif tipo == 'produto':
            # CORREÇÃO: Usando a convenção _FK para a tabela de produtos
            cursor.execute("INSERT INTO PERSONALIDADE_PRODUTO (ID_PP_PERSONALIDADE_FK, ID_PP_PRODUTO_FK) VALUES (%s, %s)", (personalidade_id, id_rel))
        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} adicionado(a) com sucesso."})
    except Exception as e:
        if 'Duplicate entry' in str(e): return jsonify({"error": f"Esta relação já existe."}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/relations/personalidade/<int:personalidade_id>', methods=['DELETE'])
def remover_conexao_personalidade(personalidade_id):
    tipo, id_rel = request.args.get('tipo'), request.args.get('id_rel')
    if tipo not in ['templo', 'associacao', 'produto'] or not id_rel: return jsonify({"error": "Parâmetros inválidos."}), 400
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        if tipo == 'templo':
            cursor.execute("DELETE FROM PERSONALIDADE_TEMPLO WHERE ID_PT_PERSONALIDADE_FK = %s AND ID_PT_TEMPLO_FK = %s", (personalidade_id, id_rel))
        elif tipo == 'associacao':
            cursor.execute("DELETE FROM PERSONALIDADE_ASSOCIACAO WHERE ID_PA_PERSONALIDADE_FK = %s AND ID_PA_ASSOCIACAO_FK = %s", (personalidade_id, id_rel))
        elif tipo == 'produto':
            # CORREÇÃO: Usando a convenção _FK para a tabela de produtos
            cursor.execute("DELETE FROM PERSONALIDADE_PRODUTO WHERE ID_PP_PERSONALIDADE_FK = %s AND ID_PP_PRODUTO_FK = %s", (personalidade_id, id_rel))
        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} removido(a) com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 5.4 Conexões das Associações

#Adicionar conexão
@app.route('/api/relations/associacao/<int:associacao_id>', methods=['POST'])
def adicionar_conexao_associacao(associacao_id):
    data = request.json
    tipo = data.get('tipo')
    id_rel = data.get('id_rel')

    if tipo not in ['templo', 'personalidade'] or not id_rel:
        return jsonify({"error": "Parâmetros 'tipo' ou 'id_rel' inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        if tipo == 'templo':
            cursor.execute(
                "INSERT INTO templo_associacao (ID_TA_ASSOCIACAO_FK, ID_TA_TEMPLO_FK) VALUES (%s, %s)", 
                (associacao_id, id_rel)
            )
        elif tipo == 'personalidade':
            # --- CORREÇÃO AQUI ---
            # Query INSERT sem o campo FUNCAO
            cursor.execute(
                "INSERT INTO personalidade_associacao (ID_PA_ASSOCIACAO_FK, ID_PA_PERSONALIDADE_FK) VALUES (%s, %s)",
                (associacao_id, id_rel)
            )
        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} adicionado(a) com sucesso à associação."})
    except Exception as e:
        if 'Duplicate entry' in str(e): return jsonify({"error": "Esta relação já existe."}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Rota para REMOVER uma conexão de uma associação
@app.route('/api/relations/associacao/<int:associacao_id>', methods=['DELETE'])
def remover_conexao_associacao(associacao_id):
    tipo = request.args.get('tipo')
    id_rel = request.args.get('id_rel')
    
    if tipo not in ['templo', 'personalidade'] or not id_rel:
        return jsonify({"error": "Parâmetros 'tipo' ou 'id_rel' inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        if tipo == 'templo':
            cursor.execute("DELETE FROM templo_associacao WHERE ID_TA_ASSOCIACAO_FK = %s AND ID_TA_TEMPLO_FK = %s", (associacao_id, id_rel))
        elif tipo == 'personalidade':
            cursor.execute("DELETE FROM personalidade_associacao WHERE ID_PA_ASSOCIACAO_FK = %s AND ID_PA_PERSONALIDADE_FK = %s", (associacao_id, id_rel))
        
        conn.commit()
        return jsonify({"message": f"{tipo.capitalize()} removido(a) com sucesso da associação."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 5.5 Conexões dos Produtos

# Rota para ADICIONAR uma personalidade a um produto
@app.route('/api/relations/produto/<int:produto_id>', methods=['POST'])
def adicionar_conexao_produto(produto_id):
    data = request.json
    tipo = data.get('tipo')
    id_rel = data.get('id_rel')

    if tipo != 'personalidade' or not id_rel:
        return jsonify({"error": "Parâmetros inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        # Usa os nomes de coluna com _FK que descobrimos serem os corretos
        cursor.execute(
            "INSERT INTO PERSONALIDADE_PRODUTO (ID_PP_PRODUTO_FK, ID_PP_PERSONALIDADE_FK) VALUES (%s, %s)",
            (produto_id, id_rel)
        )
        conn.commit()
        return jsonify({"message": "Personalidade adicionada com sucesso ao produto."})
    except Exception as e:
        if 'Duplicate entry' in str(e): return jsonify({"error": "Esta relação já existe."}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Rota para REMOVER uma personalidade de um produto
@app.route('/api/relations/produto/<int:produto_id>', methods=['DELETE'])
def remover_conexao_produto(produto_id):
    tipo = request.args.get('tipo')
    id_rel = request.args.get('id_rel')

    if tipo != 'personalidade' or not id_rel:
        return jsonify({"error": "Parâmetros inválidos."}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        # Usa os nomes de coluna com _FK que descobrimos serem os corretos
        cursor.execute(
            "DELETE FROM PERSONALIDADE_PRODUTO WHERE ID_PP_PRODUTO_FK = %s AND ID_PP_PERSONALIDADE_FK = %s",
            (produto_id, id_rel)
        )
        conn.commit()
        return jsonify({"message": "Personalidade removida com sucesso do produto."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()   


# --- 6. Editor ------
#O monstro de sete cabeças das edições insanas
@app.route('/api/editor', methods=['GET'])
def get_editor_data():
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM templo LIMIT 10")
        templos = cursor.fetchall()

        cursor.execute("SELECT * FROM personalidade LIMIT 10")
        personalidades = cursor.fetchall()

        cursor.execute("SELECT * FROM associacao LIMIT 10")
        associacoes = cursor.fetchall()

        cursor.execute("SELECT * FROM produto LIMIT 10")
        produtos = cursor.fetchall()

        return jsonify({
            "templos": templos,
            "personalidades": personalidades,
            "associacoes": associacoes,
            "produtos": produtos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- 7. Imagens ------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para fazer upload da IMAGEM DE PERFIL de um templo
@app.route('/api/templos/<int:id_templo>/imagem_perfil', methods=['POST'])
def upload_imagem_perfil_templo(id_templo):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    file = request.files['imagem']
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido."}), 400
    
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1]
    unique_filename = f"templo_{id_templo}_perfil_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)
    
    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE templo SET IMAGEM_PERFIL_URL = %s WHERE ID_TEMPLO = %s", (url_imagem, id_templo))
        conn.commit()
        return jsonify({"message": "Imagem de perfil atualizada.", "url": url_imagem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# Rota para fazer upload de uma IMAGEM DO CARROSSEL de um templo
@app.route('/api/templos/<int:id_templo>/imagens_carrossel', methods=['POST'])
def upload_imagem_carrossel_templo(id_templo):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo enviado."}), 400
    file = request.files['imagem']
    legenda = request.form.get('legenda', '')
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido."}), 400
    
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1]
    unique_filename = f"templo_{id_templo}_carrossel_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)
    
    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO imagem_templo (URL_IMAGEM, LEGENDA, ID_TEMPLO_FK) VALUES (%s, %s, %s)", (url_imagem, legenda, id_templo))
        conn.commit()
        return jsonify({"message": "Imagem adicionada ao carrossel.", "id": cursor.lastrowid, "url": url_imagem, "legenda": legenda}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# Rota para DELETAR uma imagem do carrossel
@app.route('/api/imagens_carrossel/templo/<int:id_imagem>', methods=['DELETE'])
def deletar_imagem_carrossel_templo(id_imagem):
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT URL_IMAGEM FROM imagem_templo WHERE ID_IMAGEM = %s", (id_imagem,))
        result = cursor.fetchone()
        if result and os.path.exists(result['URL_IMAGEM'].strip('/')):
            os.remove(result['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM imagem_templo WHERE ID_IMAGEM = %s", (id_imagem,))
        conn.commit()
        return jsonify({"message": "Imagem do carrossel deletada."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- IMAGENS DE PERSONALIDADE ---
@app.route('/api/personalidades/<int:id_personalidade>/imagem_perfil', methods=['POST'])
def upload_imagem_perfil_personalidade(id_personalidade):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo enviado."}), 400
    file = request.files['imagem']
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido."}), 400
    
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1]
    unique_filename = f"personalidade_{id_personalidade}_perfil_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)
    
    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE personalidade SET IMAGEM_PERFIL_URL = %s WHERE ID_PERSONALIDADE = %s", (url_imagem, id_personalidade))
        conn.commit()
        return jsonify({"message": "Imagem de perfil atualizada.", "url": url_imagem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/personalidades/<int:id_personalidade>/imagens_carrossel', methods=['POST'])
def upload_imagem_carrossel_personalidade(id_personalidade):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo enviado."}), 400
    file = request.files['imagem']
    legenda = request.form.get('legenda', '')
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido."}), 400
    
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1]
    unique_filename = f"personalidade_{id_personalidade}_carrossel_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)
    
    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO imagem_personalidade (URL_IMAGEM, LEGENDA, ID_PERSONALIDADE_FK) VALUES (%s, %s, %s)", (url_imagem, legenda, id_personalidade))
        conn.commit()
        return jsonify({"message": "Imagem adicionada ao carrossel.", "id": cursor.lastrowid, "url": url_imagem, "legenda": legenda}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/imagens_carrossel/personalidade/<int:id_imagem>', methods=['DELETE'])
def deletar_imagem_carrossel_personalidade(id_imagem):
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT URL_IMAGEM FROM imagem_personalidade WHERE ID_IMAGEM = %s", (id_imagem,))
        result = cursor.fetchone()
        if result and os.path.exists(result['URL_IMAGEM'].strip('/')):
            os.remove(result['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM imagem_personalidade WHERE ID_IMAGEM = %s", (id_imagem,))
        conn.commit()
        return jsonify({"message": "Imagem do carrossel deletada."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- IMAGENS DE ASSOCIAÇÃO ---

@app.route('/api/associacoes/<int:id_associacao>/imagem_perfil', methods=['POST'])
def upload_imagem_perfil_associacao(id_associacao):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    file = request.files['imagem']
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido ou não selecionado."}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"associacao_{id_associacao}_perfil_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)

    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE associacao SET IMAGEM_PERFIL_URL = %s WHERE ID_ASSOCIACAO = %s", (url_imagem, id_associacao))
        conn.commit()
        return jsonify({"message": "Imagem de perfil da associação atualizada.", "url": url_imagem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/associacoes/<int:id_associacao>/imagens_carrossel', methods=['POST'])
def upload_imagem_carrossel_associacao(id_associacao):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    file = request.files['imagem']
    legenda = request.form.get('legenda', '')
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido ou não selecionado."}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"associacao_{id_associacao}_carrossel_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)

    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO imagem_associacao (URL_IMAGEM, LEGENDA, ID_ASSOCIACAO_FK) VALUES (%s, %s, %s)", (url_imagem, legenda, id_associacao))
        conn.commit()
        return jsonify({"message": "Imagem adicionada ao carrossel da associação.", "id": cursor.lastrowid, "url": url_imagem, "legenda": legenda}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/imagens_carrossel/associacao/<int:id_imagem>', methods=['DELETE'])
def deletar_imagem_carrossel_associacao(id_imagem):
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT URL_IMAGEM FROM imagem_associacao WHERE ID_IMAGEM = %s", (id_imagem,))
        result = cursor.fetchone()
        if result and result.get('URL_IMAGEM') and os.path.exists(result['URL_IMAGEM'].strip('/')):
            os.remove(result['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM imagem_associacao WHERE ID_IMAGEM = %s", (id_imagem,))
        conn.commit()
        return jsonify({"message": "Imagem do carrossel da associação deletada."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# --- IMAGENS DE PRODUTO ---

@app.route('/api/produtos/<int:id_produto>/imagem_perfil', methods=['POST'])
def upload_imagem_perfil_produto(id_produto):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    file = request.files['imagem']
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido ou não selecionado."}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"produto_{id_produto}_perfil_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)

    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE produto SET IMAGEM_PERFIL_URL = %s WHERE ID_PRODUTO = %s", (url_imagem, id_produto))
        conn.commit()
        return jsonify({"message": "Imagem de perfil do produto atualizada.", "url": url_imagem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/produtos/<int:id_produto>/imagens_carrossel', methods=['POST'])
def upload_imagem_carrossel_produto(id_produto):
    if 'imagem' not in request.files: return jsonify({"error": "Nenhum arquivo de imagem enviado."}), 400
    file = request.files['imagem']
    legenda = request.form.get('legenda', '')
    if file.filename == '' or not allowed_file(file.filename): return jsonify({"error": "Arquivo inválido ou não selecionado."}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"produto_{id_produto}_carrossel_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(path)

    url_imagem = f'/uploads/{unique_filename}'
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO imagem_produto (URL_IMAGEM, LEGENDA, ID_PRODUTO_FK) VALUES (%s, %s, %s)", (url_imagem, legenda, id_produto))
        conn.commit()
        return jsonify({"message": "Imagem adicionada ao carrossel do produto.", "id": cursor.lastrowid, "url": url_imagem, "legenda": legenda}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/api/imagens_carrossel/produto/<int:id_imagem>', methods=['DELETE'])
def deletar_imagem_carrossel_produto(id_imagem):
    conn, cursor = get_db(), None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT URL_IMAGEM FROM imagem_produto WHERE ID_IMAGEM = %s", (id_imagem,))
        result = cursor.fetchone()
        if result and result.get('URL_IMAGEM') and os.path.exists(result['URL_IMAGEM'].strip('/')):
            os.remove(result['URL_IMAGEM'].strip('/'))
        
        cursor.execute("DELETE FROM imagem_produto WHERE ID_IMAGEM = %s", (id_imagem,))
        conn.commit()
        return jsonify({"message": "Imagem do carrossel do produto deletada."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- 8. Bloco de Execução ---
if __name__ == '__main__': 
    app.run(debug=True)