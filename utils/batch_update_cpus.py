import sqlite3
import random

n_cpus = 500

db_file = "../../robo/logs/database.db"
db_file = "file:" + db_file + "?mode=" + "rwc"
print("Using DB: {}".format(db_file))

# This will raise an error if it can't connect
conn = sqlite3.connect(db_file, uri=True, check_same_thread=False)

default_stats = '00C0A84400C0A84400C0A84400C0A8440000AF430000AF430000AF430000AF430000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
default_ladderstatswide = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

def generate_session_key() -> bytes:
    new_session_key = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) + '\0'
    new_session_key = new_session_key.encode()

    return new_session_key

def _create_new_user(username: str, encrypted_password: str, session_key: bytes):
    c = conn.cursor()
    insert_command = """INSERT INTO users
                        (account_type, username, password, session_key, stats, ladderstatswide)
                        values(?,?,?,?,?,?);
                        """
    account_type = 2
    stats = default_stats
    ladderstatswide = default_ladderstatswide
    c.execute(insert_command, [account_type, username, encrypted_password, session_key.decode(), stats, ladderstatswide])
    conn.commit()
    c.close()
    print(f"Created new user: {username}")


for i in range(1, n_cpus):
    _create_new_user(f"CPU-{str(i).zfill(3)}", "", generate_session_key())
