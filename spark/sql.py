import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='768114',
        database='lagou_data'
    )
    cursor = conn.cursor()


    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("数据库中的表：")
    for table in tables:
        print(table[0])

    # 测试
    cursor.execute("SELECT * FROM recomdata LIMIT 5")
    rows = cursor.fetchall()
    print("\n测试读取 recomdata 表的前5条数据：")
    for row in rows:
        print(row)

except mysql.connector.Error as e:
    print(f"数据库连接错误: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()