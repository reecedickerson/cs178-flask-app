import pymysql
import creds

try:
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    cur = conn.cursor()
    cur.execute('DESCRIBE movie')
    print('Columns in movie table:')
    for row in cur.fetchall():
        print(f'  {row[0]}: {row[1]}')
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")