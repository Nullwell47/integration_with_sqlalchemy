from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

# Definição da classe User
class User(Base):
    __tablename__ = "user_account"
    # Atributos da tabela 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    # Relacionamento com a tabela 'adress'
    adress = relationship(
        "Adress", back_populates="user", cascade="all, delete-orphan"
    )

    # Método para representação textual do objeto User
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"

# Definição da classe Adress
class Adress(Base):
    __tablename__ = "adress"
    id = Column(Integer, primary_key=True)
    email_adress = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # Relacionamento com a tabela 'user_account'
    user = relationship("User", back_populates="adress")

    # Método para representação textual do objeto Adress
    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_adress})"
    
# Exibindo os nomes das tabelas criadas
print(User.__tablename__)
print(Adress.__tablename__)

# Criação de um mecanismo de banco de dados em memória
engine = create_engine("sqlite://")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Verifica se a tabela 'user_account' existe no banco de dados
inspect_engine = inspect(engine)
print(inspect_engine.has_table("user_account"))

# Exibindo os nomes das tabelas existentes no banco de dados
print(inspect_engine.get_table_names())
print(inspect_engine.default_schema_name)

# Início da sessão para interagir com o banco de dados
with Session(engine) as session:
    # Criando instâncias de User e Adress
    noel = User(
        name='noel',
        fullname='papai noel',
        adress=[Adress(email_adress='papainoel@email.com')]
    )

    coelho = User(
        name='coelho',
        fullname='coelho da pascoa',
        adress=[Adress(email_adress='coelhopascoa@email.com'),
                Adress(email_adress='pascoacoelho@email.or')]
    )
        
    patrick = User(
    name='patrick',
    fullname='patrick estrela'
    )
    
    # Adicionando os objetos criados à sessão para persistência no banco de dados
    session.add_all([noel, coelho, patrick])

    # Confirmar as mudanças realizadas na sessão (commit)
    session.commit()

# Selecionando usuários com determinados nomes ('noel', 'coelho', 'patrick')
stmt = select(User).where(User.name.in_(['noel','coelho','patrick']))
print('\nRecuperando usuários a partir de condição de filtragem: ')
for user in session.scalars(stmt):
    print(user)

# Selecionando endereços de e-mail associados ao usuário com ID 2 ('coelho')
stmt_address = select(Adress).where(Adress.user_id.in_([2]))
print('\nRecuperando os endereços de e-mail de coelho: ')
for adress in session.scalars(stmt_address):
    print(adress)

# Criando uma declaração para selecionar todos os usuários ordenados pelo nome completo em ordem decrescente
stmt_order = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

# Criando uma declaração para selecionar o nome completo do usuário e o endereço de e-mail usando join entre User e Address
stmt_join = select(User.fullname, Adress.email_adress).join_from(Adress, User)
for result in session.scalars(stmt_join):
    print(result)

# print(select(User.fullname, Adress.email_adress).join_from(Adress, User))

# Conexão ao banco de dados usando engine.connect() e execução da declaração stmt_join
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

# Criando uma declaração para contar o número total de instâncias na tabela User
stmt_count = select(func.count('*')).select_from(User)
print("\nTotal de instâncias em User")
for result in session.scalars(stmt_count):
    print(result)
