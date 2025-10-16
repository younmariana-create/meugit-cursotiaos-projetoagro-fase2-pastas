
import csv
import json
from datetime import date, datetime
import oracledb
import os


DB_USER = "RM568548"
DB_PASSWORD = "280106"
DB_DSN = "oracle.fiap.com.br/orcl" 


SETORES = {
    1: "Cana-de-açúcar",
    2: "Laranja"
}

CSV_FILE = "leituras.csv"
JSON_FILE = "leituras.json"
TXT_FILE = "resumo.txt"


def proximo_id():
    if not os.path.exists(CSV_FILE):
        return 1
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            if not rows:
                return 1
            last = rows[-1]
            return int(last.get("id", 0)) + 1
    except Exception:
        return 1


def coletar_leitura():
    print("\nSetores disponíveis:")
    for k, v in SETORES.items():
        print(f"{k} - {v}")
    escolha = input("Escolha o número do setor (ou Enter para voltar): ").strip()
    if escolha == "":
        return None
    try:
        escolha = int(escolha)
        if escolha not in SETORES:
            print("⚠️ Setor inválido.")
            return None
    except ValueError:
        print("⚠️ Entrada inválida.")
        return None

    setor = SETORES[escolha]
    try:
        umidade = float(input(f"Umidade do solo (%) no setor '{setor}': ").strip())
    except ValueError:
        print("⚠️ Umidade inválida. Use apenas números.")
        return None

    irrigado = "Sim" if umidade < 50 else "Nao"
    id_leitura = proximo_id()
    data_iso = date.today().isoformat() 

    leitura = {
        "id": id_leitura,
        "setor": setor,
        "umidade": umidade,
        "irrigado": irrigado,
        "data": data_iso
    }
    print(f"✅ Registrado: ID={id_leitura} | Setor={setor} | Umidade={umidade}% | Irrigado={irrigado}")
    return leitura


def salvar_csv_append(leitura):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "setor", "umidade", "irrigado", "data"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(leitura)


def exportar_arquivos(leituras):
    
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "setor", "umidade", "irrigado", "data"])
        writer.writeheader()
        writer.writerows(leituras)
    
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(leituras, f, ensure_ascii=False, indent=4)
    
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("Resumo das Leituras de Irrigação\n")
        f.write("---------------------------------\n")
        for l in leituras:
            f.write(f"ID: {l['id']} | Setor: {l['setor']} | Umidade: {l['umidade']}% | "
                    f"Irrigado: {l['irrigado']} | Data: {l['data']}\n")
    print("📁 Arquivos exportados: leituras.csv, leituras.json, resumo.txt")


def ler_historico():
    if not os.path.exists(CSV_FILE):
        print("⛔ Não há histórico (arquivo CSV não encontrado).")
        return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
        for r in rows:
            try:
                r["id"] = int(r["id"])
                r["umidade"] = float(r["umidade"])
            except Exception:
                pass
        return rows


def enviar_para_oracle(leituras):

  
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = conn.cursor()
        print("🔗 Conectado ao Oracle com sucesso!")

        with open("leituras.json", "r") as jsonfile:
            leituras = json.load(jsonfile)

        for l in leituras:
            try:
                cursor.execute("""
                    INSERT INTO LEITURA_IRRIGACAO (ID, TALHAO, UMIDADE, IRRIGADO, DATA_LEITURA)
                    VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'))
                """, (l["id"], l["setor"], l["umidade"], l["irrigado"], l["data"]))
            except oracledb.IntegrityError:
                print(f"⚠️ ID {l['id']} já existe — ignorado.")
            except Exception as e:
                print(f"⚠️ Erro ao inserir ID {l['id']}: {e}")

        conn.commit()
        print("📤 Todas as leituras foram enviadas ao Oracle (ou ignoradas se já existiam).")

    except Exception as e:
        print(f"❌ Erro geral ao conectar ou inserir no Oracle: {e}")
    finally:
        try:
            conn.close()
            print("🔒 Conexão Oracle encerrada.")
        except:
            pass



def menu():
    while True:
        print("\n=== MENU ===")
        print("1 - Registrar nova leitura")
        print("2 - Ver histórico (CSV)")
        print("3 - Exportar arquivos (CSV, JSON, TXT) com todo histórico")
        print("4 - Enviar todo histórico para Oracle")
        print("0 - Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            leitura = coletar_leitura()
            if leitura:
                salvar_csv_append(leitura)
                print("✅ Leitura salva localmente (CSV).")
        elif op == "2":
            hist = ler_historico()
            if hist:
                print("\n--- Histórico de leituras ---")
                for r in hist:
                    print(f"ID:{r['id']} | {r['setor']} | Umid:{r['umidade']}% | Irrigado:{r['irrigado']} | Data:{r['data']}")
        elif op == "3":
            hist = ler_historico()
            if hist:
                exportar_arquivos(hist)
        elif op == "4":
            hist = ler_historico()
            if hist:
                enviar_para_oracle(hist)
        elif op == "0":
            print("Saindo.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
