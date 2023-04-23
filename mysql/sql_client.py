import pymysql


class SQLClient:
    def __init__(self, host, user, password, database, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            # 列名详细信息
            col_desc = self.cursor.description
            # 列名名称
            col_list = []
            if col_desc:
                for i in range(len(col_desc)):
                    col_list.append(col_desc[i][0])
            return self.cursor.fetchall(), col_list, col_desc
        except pymysql.Error as e:
            print(f"Error executing SQL: {e}")
            return None
