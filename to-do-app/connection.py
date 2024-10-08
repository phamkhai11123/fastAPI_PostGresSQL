from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.sql_model import BASE
db_user: str = 'postgres'
db_port: int = 5432
db_host: str = 'localhost'
db_password: str = 'admin'
uri :str = F'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/to-do-app'
engine = create_engine(uri)

BASE.metadata.create_all(bind = engine)

session = sessionmaker(
    bind = engine,
    autoflush = True
)
db_session = session()
try:
    connection = engine.connect()
    connection.close()
    print( 'ping, Connected')
except Exception as e:
    print(f'Error:{str(e)}')