from src.db_queries import create_user_table, create_attendance_table
from src.database import Database

db = Database()
db.create_table(create_user_table)
db.create_table(create_attendance_table)
