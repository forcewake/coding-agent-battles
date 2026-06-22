import sqlite3
from bb007_migrate import upgrade, downgrade

def cols(conn):
    return [r[1] for r in conn.execute('PRAGMA table_info(users)')]

def seed():
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    conn.executemany('INSERT INTO users (id, name) VALUES (?, ?)', [(1, 'Ada'), (2, 'Linus')])
    conn.commit()
    return conn

def test_upgrade_idempotent_and_preserves_rows():
    conn = seed()
    upgrade(conn); upgrade(conn)
    assert cols(conn) == ['id', 'name', 'email']
    assert conn.execute('SELECT id, name FROM users ORDER BY id').fetchall() == [(1, 'Ada'), (2, 'Linus')]

def test_downgrade_removes_email_preserves_rows():
    conn = seed(); upgrade(conn)
    conn.execute("UPDATE users SET email='ada@example.test' WHERE id=1")
    downgrade(conn)
    assert cols(conn) == ['id', 'name']
    assert conn.execute('SELECT id, name FROM users ORDER BY id').fetchall() == [(1, 'Ada'), (2, 'Linus')]
