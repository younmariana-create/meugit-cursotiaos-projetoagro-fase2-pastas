🧠 README.md — Sistema Inteligente de Irrigação
🌾 Sistema Inteligente de Irrigação - FarmTech Solutions

Curso: Inteligência Artificial – FIAP
Aluna: Mariana Carvalho Youn
Professora: Sabrina Otoni
Coordenador: André Godoi Chiovato
Startup: FarmTech Solutions


📘 Introdução

Este projeto faz parte do desafio da disciplina de Inteligência Artificial aplicada ao Agronegócio, com foco em monitoramento inteligente de irrigação.
A solução foi desenvolvida em Python e tem como objetivo analisar a umidade do solo em diferentes culturas agrícolas, registrar as leituras e integrar os dados a um banco de dados Oracle.

O sistema oferece persistência em CSV, TXT e JSON, além de permitir o envio automatizado para uma base de dados Oracle Cloud.


🚜 Tema do Agronegócio

O projeto trata da otimização do uso da água em lavouras de Laranja e Cana-de-açúcar, utilizando medições de umidade do solo para indicar quando a irrigação é necessária.
Com isso, o sistema contribui para:
Reduzir o desperdício de água.
Aumentar a eficiência energética.
Automatizar processos de decisão no campo.


🧩 Estrutura de Pastas
projeto_agro/
├── main.py              # Código principal do sistema
├── leituras.csv            # Arquivo gerado com as leituras registradas
├── resumo.txt        # Log textual das leituras realizadas
├── leituras.json       # Registro das leituras em formato JSON
├── README.md            # Documento explicativo do projeto



⚙️ Requisitos e Configuração do Ambiente no terminal

1️⃣ Criar e ativar o ambiente virtual
python -m venv venv

Ativar o ambiente:

Windows (PowerShell):
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate


2️⃣ Instalar dependências
pip install oracledb

(Bibliotecas padrão como csv, json, datetime e os já vêm com o Python.)


3️⃣ Configuração do Oracle
No topo do arquivo main.py, altere as credenciais para o seu login Oracle:
DB_USER = "xxxxxxxxxxx" # seu usuário
DB_PASSWORD = "xxxxxxxx"  # sua senha
DB_DSN = "xxxxxxxxxx" # seu localhost


💻 Como Executar o Programa

No terminal (com o ambiente virtual ativo), execute:

python main.py


Será exibido o menu principal:

=== Sistema Inteligente de Irrigação ===
1️⃣ Inserir nova leitura
2️⃣ Exibir histórico
3️⃣ Exportar dados (CSV, TXT, JSON)
4️⃣ Enviar dados ao Oracle
0️⃣ Sair


🧠 Funcionalidades do Sistema

1️⃣ Inserir nova leitura
O usuário informa:

Nome do setor (ex: Cana-de-açúcar, Laranja)

Umidade do solo (%)

O sistema valida o valor, grava a leitura e indica se há necessidade de irrigação com base na cultura.


2️⃣ Exibir histórico
Mostra todas as leituras salvas, com:
ID da leitura
Data e hora
Nome da cultura
Umidade
Status da irrigação


3️⃣ Exportar dados
Cria automaticamente os arquivos:
dados.csv
historico.txt
historico.json

Todos os formatos contêm as leituras completas, prontos para backup ou integração com outras ferramentas.


4️⃣ Enviar dados ao Oracle
Conecta-se ao banco Oracle (usando oracledb), insere os dados da tabela LEITURA_IRRIGACAO e exibe um resumo:
Leituras inseridas
Leituras já existentes (ignoradas)
Status da conexão


🧾 Estrutura da Tabela Oracle
CREATE TABLE LEITURA_IRRIGACAO (
  ID NUMBER PRIMARY KEY,
  CULTURA VARCHAR2(50),
  UMIDADE NUMBER,
  DATA_LEITURA DATE
);


🔍 Como Verificar os Dados no Oracle SQL Developer

Abra o Oracle SQL Developer.

Conecte-se com seu RM, senha e DSN (oracle.fiap.com.br/orcl).

Abra uma nova aba Worksheet.

Digite:

SELECT * FROM LEITURA_IRRIGACAO;

Clique em Executar (Ctrl + Enter) para visualizar as leituras enviadas.



💡 Inovação
O sistema não apenas coleta dados — ele interpreta a umidade do solo de forma contextualizada, adaptando-se às necessidades específicas de cada cultura agrícola (como laranja e cana-de-açúcar).
Isso permite automação inteligente da irrigação, base essencial para o Agro 4.0.


🧩 Histórico de Lançamentos
Versão	Data	Descrição
1.0	15/10/2025	Versão inicial funcional e estável


🧠 Conclusão
O projeto demonstra a aplicação prática da Inteligência Artificial no Agronegócio, integrando lógica de decisão, armazenamento multiplataforma (CSV, TXT, JSON) e integração com Oracle Cloud.
A solução pode ser expandida futuramente para incluir sensores IoT reais, machine learning preditivo e dashboards interativos.