from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_user: str = 'postgres'
db_port: int = 5432
db_host: str = 'localhost'
db_password: str = 'admin'
uri :str = F'postgresql://{db_user}:{db_password}@{db_host}/user'

engine = create_engine(uri)

Base = declarative_base()

SessionLocal = sessionmaker(bind = engine)

# try:
#     connection = engine.connect()
#     connection.close()
#     print( 'ping, Connected')
# except Exception as e:
#     print(f'Error:{str(e)}') 