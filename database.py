from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5432/postgres")

