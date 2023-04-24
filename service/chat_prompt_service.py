from mysql.sql_client import SQLClient
from common.log import logger
from common.config import MYSQL_HOST, MYSQL_PORT
import datetime
from entity.ChatPrompt import ChatPrompt

TABLE_NAME = "chat_prompt"


class ChatPromptService:
    def __init__(self):
        self.db = SQLClient(host=MYSQL_HOST, port=MYSQL_PORT, user='root', password='root', database='llm_data')
        self.db.connect()

    def select_data(self, page: int = 1, size: int = 10):
        if page < 1:
            page = 1
        values = (size, (page - 1) * size)
        results, col_list, _ = self.db.execute(
            f"SELECT * FROM {TABLE_NAME} WHERE delete_time IS NULL LIMIT %s OFFSET %s;", values)
        if results:
            entityResult = []
            for row in results:
                entityResult.append(ChatPrompt(**(dict(zip(col_list, row)))))
            return entityResult
        else:
            print("No results found.")

    def select_one(self, id: int):
        if id < 1:
            id = 1
        values = (id)
        results, col_list, _ = self.db.execute("SELECT * FROM zhihu_dataset WHERE id = %s ;", values)
        # if results:
        #     for row in results:
        #         return ZhihuDataset(**(dict(zip(col_list, row))))
        # else:
        #     print("No results found.")

    def update_process_type(self, id: int, answer: str, process_type):
        sql = "UPDATE zhihu_dataset SET process_type = %s, answer = %s WHERE id = %s"
        values = (process_type, answer, id)
        self.db.execute(sql, values)
        print("更新id:%s, process_type:%s" % (id, process_type))

    def del_data(self, ids: list):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        list_ids = ','.join(str(i) for i in ids)
        print(list_ids)
        sql = f"UPDATE {TABLE_NAME} SET delete_time  = %s WHERE id in ({list_ids})"
        self.db.execute(sql, now)
        print("更新ids：" % (ids))

    def insert(self, prompt: str = None, target: str = None):
        if prompt is None and target is None:
            logger.warn("没有问题和答案")
            return
        sql = f"INSERT INTO {TABLE_NAME} (prompt, target ) VALUES (%s, %s) "
        values = (prompt, target)
        self.db.execute(sql, values)

    def __del__(self):
        self.db.close()


if __name__ == '__main__':
    testService = ChatPromptService()
    testResult = testService.insert("aaa", "bbb")
    print(testResult)
# for item in testResult:
#     print(item.id, item.question, item.process_id)
#
# testService.update_process_id(12, 1)
