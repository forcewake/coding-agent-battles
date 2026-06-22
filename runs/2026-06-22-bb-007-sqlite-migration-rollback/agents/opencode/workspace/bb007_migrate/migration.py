def _has_column(conn, table, column):
    return any(r[1] == column for r in conn.execute(f'PRAGMA table_info({table})'))


def upgrade(conn):
    if not _has_column(conn, 'users', 'email'):
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
    conn.commit()


def downgrade(conn):
    if _has_column(conn, 'users', 'email'):
        conn.executescript('''
            CREATE TABLE _users_backup (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
            INSERT INTO _users_backup (id, name) SELECT id, name FROM users;
            DROP TABLE users;
            ALTER TABLE _users_backup RENAME TO users;
        ''')
    conn.commit()
