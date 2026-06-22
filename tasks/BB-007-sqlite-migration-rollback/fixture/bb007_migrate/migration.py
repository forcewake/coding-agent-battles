def upgrade(conn):
    conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
    conn.commit()

def downgrade(conn):
    # BUG: destructive rollback loses data.
    conn.execute('DROP TABLE users')
    conn.commit()
