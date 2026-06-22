def _columns(conn):
    return [r[1] for r in conn.execute('PRAGMA table_info(users)')]


def upgrade(conn):
    # Add a nullable email column; idempotent so running twice is safe.
    if 'email' not in _columns(conn):
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
    conn.commit()


def downgrade(conn):
    # Remove only the email column; preserves id/name rows and is idempotent.
    if 'email' in _columns(conn):
        conn.execute('ALTER TABLE users DROP COLUMN email')
    conn.commit()
