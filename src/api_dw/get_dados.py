import os
import psycopg2
from datetime import date

#import src.api_dw.tradutor as tradutor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            database = os.getenv("DW_NAME"),
            user = os.getenv("DW_USER"),
            host = os.getenv("DW_HOST"),
            password = os.getenv("DW_PASS"),
            port = os.getenv("DW_PORT"),
            client_encoding='utf8'
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    return conn



def close_connection(conn):
    if conn:
        conn.close()
        print("Conexão com o banco de dados encerrada.")
    else:
        print("Nenhuma conexão ativa para encerrar.")


def le_query(arquivo):
    print(f"Lendo arquivo SQL: {arquivo}")
    caminho = os.path.join(os.path.dirname(__file__), "..", "..", arquivo)
    try:
        with open(caminho, "r") as arquivo_sql:
            sql_query = arquivo_sql.read()
    except FileNotFoundError:
        raise FileNotFoundError("Erro: Arquivo SQL não encontrado.")
    return sql_query



def dados_estoque(page, size, loja_id):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/estoque_lojas.sql")
        if loja_id is not None:
            query = query.replace("    --and lojas.cod_portal =", f"   and lojas.cod_portal = 'L{loja_id}'")
        query = query.replace("--LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")
        
        cursor.execute(query)
        print("Query executada com sucesso.")
        result = cursor.fetchall()
        if result:
            #print("Dados retornados:", result)
            return result
    except Exception as e:
        print(f"Erro ao buscar dados de estoque: {e}")
    finally:
        cursor.close()
        conn.close()



def dados_img(ref, cor):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/img_produtos.sql")
        query = query.replace("--    and img_prd.referencia = ", f"   and img_prd.referencia = '{ref}' ")
        query = query.replace("--    and img_prd.cor = ", f"   and img_prd.cor = '{cor}' ")

        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            #print("Dados retornados:", result)
            #result = tradutor.tradutor_nome_colunas(df=result, tabela="imagens")
            return result
        else:
            print("Dados não encontrados.")
            return None
    except Exception as e:
        print(f"Erro ao buscar dados de imagens: {e}")
    finally:
        cursor.close()
        conn.close()



def dados_movimentos(loja_id, start_date, end_date, page, size):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/movimentos_lojas.sql")
        hoje = date.today()
        if start_date is not None:
            if end_date is None:
                query = query.replace("   --and mov.data_lancamento between",
                    f"   and mov.data_lancamento between to_date('{start_date}','YYYY-MM-DD') and to_date('{hoje}','YYYY-MM-DD')")
            else:
                query = query.replace("   --and mov.data_lancamento between",
                    f"   and mov.data_lancamento between to_date('{start_date}','YYYY-MM-DD') and to_date('{end_date}','YYYY-MM-DD')")
        
        if loja_id is not None:
            query = query.replace("    --and lojas.cod_portal =", f"   and lojas.cod_portal = 'L{loja_id}'")
        
        query = query.replace("LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return result
    except Exception as e:
        print(f"Erro ao buscar dados de estoque: {e}")
    finally:
        cursor.close()
        conn.close()



def dados_lojas(loja_id):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/lojas.sql")
        
        if loja_id is not None:
            query = query.replace("    --and lojas.cod_portal =", f"   and lojas.cod_portal = 'L{loja_id}'")
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return result
    except Exception as e:
        print(f"Erro ao buscar dados de estoque: {e}")
    finally:
        cursor.close()
        conn.close()



def dados_produtos(sku, is_active, page, size):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/produtos.sql")
        if sku is not None:
            query = query.replace("    --and prd.sku =", f"   and prd.sku = '{sku}'")
        if is_active is not None:
            query = query.replace("    --and prd.ativo =", f"   and prd.ativo = {str(is_active).upper()}")
        query = query.replace("--LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")
        
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return result
    except Exception as e:
        print(f"Erro ao buscar dados de estoque: {e}")
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    dados = dados_estoque()
    print(dados)