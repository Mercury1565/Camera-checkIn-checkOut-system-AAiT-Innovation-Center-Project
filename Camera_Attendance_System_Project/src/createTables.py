from db_queries import create_user_table, create_attendance_table
from database import Database

DATABASE_NAME= 'perago'
DATABASE_USER= 'mercury'
DATABASE_PASSWORD= 'herget123'

db = Database(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)
db.create_table(create_user_table)
db.create_table(create_attendance_table)
