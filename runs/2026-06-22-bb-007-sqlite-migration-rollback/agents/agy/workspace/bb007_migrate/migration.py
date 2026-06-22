def upgrade(conn):
    columns = [row[1] for row in conn.execute('PRAGMA table_info(users)').fetchall()]
    if 'email' not in columns:
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
        conn.commit()

def downgrade(conn):
    columns = [row[1] for row in conn.execute('PRAGMA table_info(users)').fetchall()]
    if 'email' in columns:
        conn.execute('ALTER TABLE users DROP COLUMN email')
        conn.commit()

