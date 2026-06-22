def _columns(conn):
    return [row[1] for row in conn.execute('PRAGMA table_info(users)')]


def upgrade(conn):
    if 'email' not in _columns(conn):
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
        conn.commit()

def downgrade(conn):
    if 'email' not in _columns(conn):
        return

    conn.execute('CREATE TABLE users_new (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    conn.execute('INSERT INTO users_new (id, name) SELECT id, name FROM users')
    conn.execute('DROP TABLE users')
    conn.execute('ALTER TABLE users_new RENAME TO users')
    conn.commit()
