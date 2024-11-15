##### USER TABLE CREATE QUERY
create_user_table = (
    "CREATE TABLE users ("
    "user_id SERIAL PRIMARY KEY, "
    "first_name VARCHAR(100) NOT NULL, "
    "last_name VARCHAR(100), "
    "email VARCHAR(100), "
    "phone VARCHAR(100), "
    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ");"
)

##### ATTENDANCE TABLE CREATE QUERY
create_attendance_table = (
    "CREATE TABLE attendance ("
    "attendance_id SERIAL PRIMARY KEY, "
    "user_id INT NOT NULL, "
    "check_in_time TIMESTAMP NOT NULL, "
    "check_out_time TIMESTAMP, "
    "is_checked_in BOOLEAN DEFAULT TRUE, " 
    "FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE "
    ");"
)

##### INSERT USER QUERY
insert_user_query = (
    "INSERT INTO users (first_name, last_name, email, phone) "
    "VALUES (%s, %s, %s, %s) RETURNING user_id;"
)

##### CHECK-IN QUERY
check_in_query = (
    "INSERT INTO attendance (user_id, check_in_time, is_checked_in) "
    "VALUES (%s, NOW(), TRUE); "
)

##### CHECK-OUT QUERY
check_out_query = (
    "UPDATE attendance "
    "SET check_out_time = NOW(), is_checked_in = FALSE "
    "WHERE user_id = %s AND is_checked_in = TRUE "
)

##### COUNT ACTIVE USER CHECK-IN QUERY
is_user_checked_in = (
    "SELECT COUNT(*) FROM attendance "
    "WHERE user_id = %s AND is_checked_in = TRUE; "
)