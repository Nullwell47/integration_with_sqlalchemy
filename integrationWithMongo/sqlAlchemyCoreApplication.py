from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

# Criação de um engine para se conectar a um banco de dados SQLite em memória
engine = create_engine("sqlite:///:memory")

# Criação de um objeto de metadados associado a um esquema chamado "teste"
metadata_obj = MetaData(schema="teste")

# Definição da tabela 'user' com colunas 'user_id', 'user_name', 'email_address' e 'nickname'
user = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(40), nullable=False),
    Column("email_address", String(60)),
    Column("nickname", String(50), nullable=False)
)

# Definição da tabela 'user_prefs' com colunas 'pref_id', 'user_id', 'pref_name' e 'pref_value'
# Também adiciona uma chave estrangeira ('user_id') referenciando a coluna 'user_id' na tabela 'user'
user_prefs = Table(
    "user_prefs",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)

# Impressão de informações sobre a tabela 'user_prefs'
print("\nInfo da tabela user_prefs")
print(user_prefs.primary_key)  # Mostra a chave primária da tabela 'user_prefs'
print(user_prefs.constraints)  # Mostra as restrições da tabela 'user_prefs'

# Mostra as tabelas contidas no objeto de metadados 'metadata_obj'
print(metadata_obj.tables)

# Itera sobre as tabelas ordenadas dentro do objeto de metadados 'metadata_obj' e as imprime
for table in metadata_obj.sorted_tables:
    print(table)

# Criação de um novo objeto de metadados associado a um esquema chamado "bank"
metadata_db_obj = MetaData(schema="bank")

# Definição da tabela 'financial_info' com colunas 'id' e 'value'
financial_info = Table(
    "financial_info",
    metadata_db_obj,
    Column("id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),
)

# Impressão de informações sobre a tabela 'financial_info'
print("\nInfo da tabela financial_info")
print(financial_info.primary_key)  # Mostra a chave primária da tabela 'financial_info'
print(financial_info.constraints)  # Mostra as restrições da tabela 'financial_info'
