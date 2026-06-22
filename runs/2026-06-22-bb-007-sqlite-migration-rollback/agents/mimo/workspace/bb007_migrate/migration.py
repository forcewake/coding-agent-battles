def _has_column(conn, table, column):
    rows = conn.execute(f'PRAGMA table_info({table})').fetchall()
    return any(r[1] == column for r in rows)


def upgrade(conn):
    if not _has_column(conn, 'users', 'email'):
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
    conn.commit()


def downgrade(conn):
    if not _has_column(conn, 'users', 'email'):
        conn.commit()
        return
    conn.execute('CREATE TABLE users_new (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    conn.execute('INSERT INTO users_new (id, name) SELECT id, name FROM users')
    conn.execute('DROP TABLE users')
    conn.execute('ALTER TABLE users_new RENAME TO users')
    conn.commit()
