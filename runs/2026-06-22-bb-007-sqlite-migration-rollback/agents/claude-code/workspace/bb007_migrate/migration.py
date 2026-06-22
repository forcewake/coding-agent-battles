def upgrade(conn):
    cols = {r[1] for r in conn.execute('PRAGMA table_info(users)')}
    if 'email' not in cols:
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
        conn.commit()

def downgrade(conn):
    conn.execute('ALTER TABLE users DROP COLUMN email')
    conn.commit()
