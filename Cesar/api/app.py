from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Certifique-se que esta função auxiliar está no seu código, pois ela é essencial
def format_date(date_str):
    """Converte '0001-01-01' em None e mantém as demais datas."""
    if not date_str or str(date_str) == '0001-01-01':
        return None
    # Se já for um objeto de data, formata. Se for string, apenas retorna.
    if hasattr(date_str, 'strftime'):
        return date_str.strftime('%Y-%m-%d')
    return str(date_str)

load_dotenv()
print("--- SERVIDOR COM O CÓDIGO CORRIGIDO INICIADO ---")
app = Flask(__name__)
CORS(app)

ITEMS_PER_PAGE = 20

def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
#nosso sistema pra data quebrada

def format_date(date_str):
    """Converte '0001-01-01' em None e mantém as demais datas."""
    if not date_str or str(date_str) == '0001-01-01':
        return None
    return str(date_str)

def validate_params(params, allowed_params):
    """(Exemplo simples) Retorna somente parâmetros válidos."""
    return {k: v for k, v in params.items() if k in allowed_params}


#Rotas pra infos dos templos
# SUBSTITUA A SUA FUNÇÃO get_templos POR ESTA:

# DEPOIS (com a formatação de data)

@app.route('/api/templos', methods=['GET'])
def get_templos():
    conn = None
    cursor = None
    page = 1
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        if request.args.get('all') == 'true':
            cursor.execute("SELECT * FROM templo ORDER BY NOME")
            templos = cursor.fetchall()
        else:
            page = int(request.args.get('page', 1))
            offset = (page - 1) * ITEMS_PER_PAGE
            cursor.execute("SELECT * FROM templo ORDER BY NOME LIMIT %s OFFSET %s", (ITEMS_PER_PAGE, offset))
            templos = cursor.fetchall()
            
        # --- INÍCIO DA MELHORIA ---
        # Formata as datas para o padrão AAAA-MM-DD
        for templo in templos:
            if templo.get('DATA_ABERTURA_TEMPLO'):
                templo['DATA_ABERTURA_TEMPLO'] = templo['DATA_ABERTURA_TEMPLO'].strftime('%Y-%m-%d')
            if templo.get('DATA_FECHAMENTO_TEMPLO'):
                templo['DATA_FECHAMENTO_TEMPLO'] = templo['DATA_FECHAMENTO_TEMPLO'].strftime('%Y-%m-%d')
        # --- FIM DA MELHORIA ---
        
        return jsonify({
            "data": templos,
            "page": page if request.args.get('all') != 'true' else None,
            "per_page": ITEMS_PER_PAGE
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


#rotas pra produtos
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        # Boa prática: Adicionei um ORDER BY para que os produtos venham em ordem alfabética.
        cursor.execute("SELECT * FROM produto ORDER BY NOME_PRODUTO")
        produtos = cursor.fetchall()

        # --- INÍCIO DA CORREÇÃO ---
        # É necessário formatar o objeto 'date' do Python para uma string (texto)
        # antes de enviá-lo como JSON. O JSON não entende o tipo 'date' diretamente.
        # Este loop percorre cada produto e converte a data de lançamento.
        for produto in produtos:
            if produto.get('DATA_LANCAMENTO'):
                # .strftime('%Y-%m-%d') converte a data para o formato "Ano-Mês-Dia"
                produto['DATA_LANCAMENTO'] = produto['DATA_LANCAMENTO'].strftime('%Y-%m-%d')
        # --- FIM DA CORREÇÃO ---

        return jsonify({"data": produtos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

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

#personalidade
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

# --- ROTAS PARA EDIÇÃO DE PERSONALIDADES ---

# Rota para ATUALIZAR uma personalidade existente
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
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Primeiro, apaga as relações em tabelas intermediárias para evitar erros de chave estrangeira
        cursor.execute("DELETE FROM PERSONALIDADE_TEMPLO WHERE ID_PERSONALIDADE = %s", (id_personalidade,)) 
        cursor.execute("DELETE FROM PERSONALIDADE_ASSOCIACAO WHERE ID_PERSONALIDADE = %s", (id_personalidade,))
        cursor.execute("DELETE FROM PERSONALIDADE_PRODUTO WHERE ID_PERSONALIDADE = %s", (id_personalidade,)) 

        # Agora, apaga a personalidade principal
        cursor.execute("DELETE FROM PERSONALIDADE WHERE ID_PERSONALIDADE = %s", (id_personalidade,)) 
        conn.commit()
        return jsonify({"message": "Personalidade apagada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#associações
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
            if not row:
                return jsonify({"data": []})
            row['DATA_ABERTURA_ASSOCIACAO'] = format_date(row.get('DATA_ABERTURA_ASSOCIACAO'))
            row['DATA_FECHAMENTO_ASSOCIACAO'] = format_date(row.get('DATA_FECHAMENTO_ASSOCIACAO'))
            return jsonify({"data": [row]})
        else:
            page = int(request.args.get('page', 1))
            offset = (page - 1) * ITEMS_PER_PAGE
            cursor.execute("SELECT * FROM associacao LIMIT %s OFFSET %s", (ITEMS_PER_PAGE, offset))
            associacoes = cursor.fetchall()
            for a in associacoes:
                a['DATA_ABERTURA_ASSOCIACAO'] = format_date(a.get('DATA_ABERTURA_ASSOCIACAO'))
                a['DATA_FECHAMENTO_ASSOCIACAO'] = format_date(a.get('DATA_FECHAMENTO_ASSOCIACAO'))
            return jsonify({
                "data": associacoes,
                "page": page,
                "per_page": ITEMS_PER_PAGE
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- ROTAS PARA EDIÇÃO DE ASSOCIAÇÕES ---

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


#Login dos moderadores/Adms
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    nome = data.get('nome')
    senha = data.get('senha')

    if not nome or not senha:
        return jsonify({"error": "Nome e senha são obrigatórios."}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM usuario WHERE NOME = %s", (nome,))
        usuario = cursor.fetchone()

        if not usuario or usuario['SENHA'] != senha:
            return jsonify({"error": "Credenciais inválidas."}), 401

        return jsonify({
            "id": usuario["ID_USUARIO"],
            "nome": usuario["NOME"],
            "tipo": usuario["TIPO_CONTA"]  # "admin" ou "moderador"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()        

#criação de novo usuario via conta de Admin, sempre cria moderadores
@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    nome = data.get("nome")
    senha = data.get("senha")
    tipo = data.get("tipo", "moderador")  # padrão é moderador

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

# SUBSTITUA A SUA FUNÇÃO criar_templo POR ESTA:

@app.route('/api/templos', methods=['POST'])
def criar_templo():
    data = request.json
    
    # Lista de campos COM OS NOMES CORRETOS do banco de dados
    campos_bd = ['NOME', 'PAIS', 'ESTADO', 'ESCOLA', 'DATA_ABERTURA_TEMPLO', 'DATA_FECHAMENTO_TEMPLO', 'CAMPO_INFO_TEMPLO']
    
    # Pega os valores do JSON recebido
    valores = [data.get(c) for c in campos_bd]

    conn = get_db()
    cursor = conn.cursor()
    try:
        # Query INSERT COM OS NOMES CORRETOS das colunas
        query = """
            INSERT INTO templo (NOME, PAIS, ESTADO, ESCOLA, DATA_ABERTURA_TEMPLO, DATA_FECHAMENTO_TEMPLO, CAMPO_INFO_TEMPLO)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Templo criado com sucesso."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/templos/<int:id_templo>', methods=['PUT'])
def atualizar_templo(id_templo):
    data = request.json
    campos = []
    valores = []
    
    campos_validos = ['NOME', 'PAIS', 'ESTADO', 'ESCOLA', 
                      'DATA_ABERTURA_TEMPLO', 'DATA_FECHAMENTO_TEMPLO', 'CAMPO_INFO_TEMPLO']
    
    for campo in campos_validos:
        if campo in data:
            valor = data[campo]
            if "DATA" in campo and not valor:
                valor = None
            campos.append(f"`{campo}` = %s") # Adicionado backticks para segurança
            valores.append(valor)

    if not campos:
        return jsonify({"error": "Nada para atualizar."}), 400

    valores.append(id_templo)
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = f"UPDATE templo SET {', '.join(campos)} WHERE ID_TEMPLO = %s"
        cursor.execute(query, valores)
        conn.commit()
        return jsonify({"message": "Templo atualizado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/templos/<int:id_templo>', methods=['DELETE'])
def deletar_templo(id_templo):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM templo WHERE ID_TEMPLO = %s", (id_templo,))
        conn.commit()
        return jsonify({"message": "Templo deletado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()




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


# =================================================================================
# BLOCO DE CÓDIGO FINAL PARA AS RELAÇÕES
# Corrige o nome das colunas na tabela PERSONALIDADE_PRODUTO
# =================================================================================
from datetime import date # Certifique-se que 'date' de 'datetime' está importado

def format_date(date_str):
    if not date_str or str(date_str) == '0001-01-01': return None
    if hasattr(date_str, 'strftime'): return date_str.strftime('%Y-%m-%d')
    return str(date_str)

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
        elif entity_type == 'personalidade':
            cursor.execute("SELECT t.*, pt.FUNCAO FROM templo t JOIN personalidade_templo pt ON t.ID_TEMPLO = pt.ID_PT_TEMPLO_FK WHERE pt.ID_PT_PERSONALIDADE_FK = %s", [entity_id])
            relations['templos'] = cursor.fetchall()
            cursor.execute("SELECT a.* FROM associacao a JOIN personalidade_associacao pa ON a.ID_ASSOCIACAO = pa.ID_PA_ASSOCIACAO_FK WHERE pa.ID_PA_PERSONALIDADE_FK = %s", [entity_id])
            relations['associacoes'] = cursor.fetchall()
            # CORREÇÃO: Usando a convenção _FK para a tabela de produtos
            cursor.execute("SELECT p.* FROM PRODUTO p JOIN PERSONALIDADE_PRODUTO pp ON p.ID_PRODUTO = pp.ID_PP_PRODUTO_FK WHERE pp.ID_PP_PERSONALIDADE_FK = %s", [entity_id])
            relations['produtos'] = cursor.fetchall()
        elif entity_type == 'associacao':
            # Templos relacionados à Associação (Esta parte estava correta)
            cursor.execute("""
                SELECT t.* FROM templo t
                JOIN templo_associacao ta ON t.ID_TEMPLO = ta.ID_TA_TEMPLO_FK
                WHERE ta.ID_TA_ASSOCIACAO_FK = %s
            """, [entity_id])
            templos = cursor.fetchall()
            for t in templos:
                t['DATA_ABERTURA_TEMPLO'] = format_date(t.get('DATA_ABERTURA_TEMPLO'))
                t['DATA_FECHamento_TEMPLO'] = format_date(t.get('DATA_FECHAMENTO_TEMPLO'))
            relations['templos'] = templos
            # --- CORREÇÃO AQUI ---
            # Personalidades relacionadas à Associação (Removido ", pa.FUNCAO")
            cursor.execute("""
                SELECT p.* FROM personalidade p
                JOIN personalidade_associacao pa ON p.ID_PERSONALIDADE = pa.ID_PA_PERSONALIDADE_FK
                WHERE pa.ID_PA_ASSOCIACAO_FK = %s
            """, [entity_id])
            personalidades = cursor.fetchall()
            for p in personalidades:
                p['DATA_NASCIMENTO'] = format_date(p.get('DATA_NASCIMENTO'))
                p['DATA_MORTE'] = format_date(p.get('DATA_MORTE'))
            relations['personalidades'] = personalidades
        elif entity_type == 'produto':
            # CORREÇÃO: Usando a convenção _FK para a tabela de produtos
            cursor.execute("SELECT p.* FROM PERSONALIDADE p JOIN PERSONALIDADE_PRODUTO pp ON p.ID_PERSONALIDADE = pp.ID_PP_PERSONALIDADE_FK WHERE pp.ID_PP_PRODUTO_FK = %s", [entity_id])
            relations['personalidades'] = cursor.fetchall()
        
        for key, items in relations.items():
            for item in items:
                for date_field in item.keys():
                    if 'DATA' in date_field and isinstance(item[date_field], date):
                        item[date_field] = item[date_field].strftime('%Y-%m-%d')
        return jsonify(relations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

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




# --- ROTAS PARA EDIÇÃO DE PRODUTOS ---------------------------------------------

# Rota para ATUALIZAR um produto existente
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

# =================================================================================
# NOVAS FUNÇÕES para gerenciar relações a partir da página de Associações
# =================================================================================

# Rota para ADICIONAR uma conexão a uma associação
# Função ATUALIZADA - Removido o tratamento do campo "funcao" para personalidade
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

# =================================================================================
# Funções para gerenciar relações a partir da página de Produtos
# (Verifique se já existem no seu app.py)
# =================================================================================

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

if __name__ == '__main__': 
    app.run(debug=True)