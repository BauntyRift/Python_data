import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phones TEXT[]
            )
        ''')
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO clients (first_name, last_name, email, phones) VALUES (%s, %s, %s, %s)', (first_name, last_name, email, phones))
    conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('UPDATE clients SET phones = array_append(phones, %s) WHERE id = %s', (phone, client_id))
    conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    update_str = ''
    if first_name:
        update_str += f"first_name = '{first_name}',"
    if last_name:
        update_str += f"last_name = '{last_name}',"
    if email:
        update_str += f"email = '{email}',"
    if phones:
        update_str += f"phones = '{phones}',"

    with conn.cursor() as cur:
        cur.execute(f'UPDATE clients SET {update_str.rstrip(",")} WHERE id = {client_id}')
    conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('UPDATE clients SET phones = array_remove(phones, %s) WHERE id = %s', (phone, client_id))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
    conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM clients WHERE first_name = %s OR last_name = %s OR email = %s OR %s = ANY(phones)', (first_name, last_name, email, phone))
        clients = cur.fetchall()
    return clients



with psycopg2.connect(database="homework_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, "Павел", "Дуров", "Man@example.com", ["723456789", "987654321"])
    add_phone(conn, 1, "756877772")
    change_client(conn, 1, first_name="Неприделах")
    delete_phone(conn, 1, "628454789")
    print(find_client(conn, first_name="Неприделах"))
    
conn.close()