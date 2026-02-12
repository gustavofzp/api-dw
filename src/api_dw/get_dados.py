import os
import math
import psycopg2
import src.api_dw.tradutor as tradutor
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



def _count_from_query(cursor, raw_query):
    # remove placeholder de paginação caso exista
    count_subquery = raw_query.replace("--LIMIT <page> OFFSET <size>", "")
    # garante que subquery não tenha trailing semicolons
    count_subquery = count_subquery.rstrip().rstrip(';')
    count_query = f"SELECT COUNT(*) FROM ({count_subquery}) as t"
    print(f"Executando contagem com query:\n{count_query}")
    cursor.execute(count_query)
    total = cursor.fetchone()[0] or 0
    return total



def _verificar_codigo_loja(loja_id):
    code = loja_id[1:]
    if not loja_id.startswith("L"):
        return("Store_code format incorrect, it should start with 'L'")
    elif len(code) != 3:
        return("Store_code format incorrect, it should have more 3 digits after 'L'")
    elif not code.isdigit():
        return("Store_code format incorrect, it should start with 'L' followed by numeric digits")
    else:
        return None
            



def dados_estoque(page, size, loja_id):
    conn = get_connection()
    if conn is None:
        return "Erro ao conectar com o DW."
    try:
        cursor = conn.cursor()
        query = le_query(arquivo="queries/estoque_lojas.sql")
        
        if loja_id is not None:
            code = loja_id[1:]
            msg = _verificar_codigo_loja(loja_id)
            if msg is not None:
                print(f"Erro: {msg}")
                raise ValueError(msg)
            query = query.replace("    --and loj.cod_portal =", f"   and loj.cod_portal = '{code}'")
        else:
            query = query.replace("    --and loj.cod_portal =", "")

        # calcula total antes de aplicar LIMIT/OFFSET
        total = _count_from_query(cursor, query)
        # calcula total de páginas
        if size <= 0:
            raise ValueError("size must be > 0")
        total_pages = math.ceil(total / size)
        
        # aplica paginação
        query = query.replace("--LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")
        
        cursor.execute(query)
        print("Query executada com sucesso.")
        result = cursor.fetchall()
        # Define headers
        headers = ["store_code","cnpj","sku","product_stock_date","product_stock_quantity"]
        result = tradutor.ensure_records(result, headers)

        if result:
            item = {
                "Method": "stores", 
                "Status": "Success",
                "page": page,
                "pageSize": size,
                "totalItems": total,
                "totalPages": total_pages,
                "Data": result
            }
            return item
    except ValueError:
        print("Erro: Store_code format incorrect, it should start with 'L' followed by digits")
        raise
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
        else:
            query = query.replace("   --and mov.data_lancamento between", "")
        
        if loja_id is not None:
            code = loja_id[1:]
            msg = _verificar_codigo_loja(loja_id)
            if msg is not None:
                print(f"Erro: {msg}")
                raise ValueError(msg)
            query = query.replace("    --and loj.cod_portal =", f"   and loj.cod_portal = '{code}'")
        else:
            query = query.replace("    --and loj.cod_portal =", "")

        # calcula total antes de aplicar LIMIT/OFFSET
        total = _count_from_query(cursor, query)
        # calcula total de páginas
        if size <= 0:
            raise ValueError("size must be > 0")
        total_pages = math.ceil(total / size)
        
        query = query.replace("--LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Define headers
                # Define headers
        headers = ["store_code","cnpj","store_name","transaction_date","sku","color_code","size_code",
                    "is_canceled","canceled_date","movement_description","operation","transaction_type","invoice_series",
                    "invoice_number","seller_code","is_sale","movement_status","quantity","net_amount",
                    "discount_amount","gross_amount"]
        result = tradutor.ensure_records(result, headers)

        if result:
            item = {
                "Method": "store_transactions", 
                "Status": "Success",
                "page": page,
                "pageSize": size,
                "totalItems": total,
                "totalPages": total_pages,
                "Data": result
            }
            return item
        
    except Exception as e:
        print(f"Erro ao buscar transacao: {e}")
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
            code = loja_id[1:]
            msg = _verificar_codigo_loja(loja_id)
            if msg is not None:
                print(f"Erro: {msg}")
                raise ValueError(msg)
            query = query.replace("    --and loj.cod_portal =", f"   and loj.cod_portal = '{code}'")
        else:
            query = query.replace("    --and loj.cod_portal =", "")
        total = _count_from_query(cursor, query)
        
        cursor.execute(query)
        print("Query executada com sucesso.")
        result = cursor.fetchall()
        # Define headers
        headers = ["store_code","cnpj","store_name","store_chain_code","store_chain_name","zip_code","address",
            "city_code","city_name","state","region_code","region_name","store_size","opening_date","is_open_sunday"]
        result = tradutor.ensure_records(result, headers)

        if result:
            item = {
                "Method": "stores", 
                "Status": "Success",
                "totalItems": total,
                "Data": result
            }
            return item
    except ValueError:
        print("Erro: Store_code format incorrect, it should start with 'L' followed by digits")
        raise
    except Exception as e:
        print(f"Erro ao buscar dados de lojas: {e}")
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
            query = query.replace("    --and prod.sku =", f"   and prod.sku = '{sku}'")
        else:
            query = query.replace("    --and prod.sku =", "")
        
        if is_active is not None:
            query = query.replace("    --and prod.ativo =", f"   and prod.item_ativo = {is_active}")
        else:
            query = query.replace("    --and prod.ativo =", "")

        # calcula total antes de aplicar LIMIT/OFFSET
        total = _count_from_query(cursor, query)
        # calcula total de páginas
        if size <= 0:
            raise ValueError("size must be > 0")
        total_pages = math.ceil(total / size)
        
        query = query.replace("--LIMIT <page> OFFSET <size>", f"LIMIT {size} OFFSET {(page-1)*size}")

        cursor.execute(query)
        result = cursor.fetchall()
        # Define headers
        headers = ["sku","erp_product_code","Style_Color_Code","description","style_code","color_code","color_name","size_code",
                    "size_name","product_line_code","product_line_name","category_code","category_name","product_type_code",
                    "product_type_name","collection_code","collection_name","sub_collection_code","sub_collection_name","is_active"]
        result = tradutor.ensure_records(result, headers)

        if result:
            item = {
                "Method": "store_transactions", 
                "Status": "Success",
                "page": page,
                "pageSize": size,
                "totalItems": total,
                "totalPages": total_pages,
                "Data": result
            }
            return item
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    dados = dados_estoque()
    print(dados)