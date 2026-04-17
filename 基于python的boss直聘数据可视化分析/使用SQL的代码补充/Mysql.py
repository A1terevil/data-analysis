import pymysql


class Mysql(object):
    def __init__(self, host="localhost", user="root", passwd="devilmaycry1412", db_name="dbpro"):
        self.conn = pymysql.connect(
            host=host,      # 连接主机, 默认127.0.0.1
            user=user,      # 用户名
            passwd=passwd,  # 密码
            port=3306,      # 端口，默认为3306
            db=db_name,     # 数据库名称
            charset='utf8'  # 字符编码
        )


    def CurPage_Data(self, sql, FirstParm, SecondParm):
        cur = self.conn.cursor()
        limit = " Limit %s,%s" % (FirstParm, SecondParm)
        sqlNew = sql + limit
        cur.execute(sqlNew)
        res = cur.fetchall()
        return res

    def Total_Count(self, sql):
        cur = self.conn.cursor()
        sqlNew = sql.replace('jc.job_name,jc.job_request,jc.job_req_exp,jc.job_req_degree,jc.salary,c.city,'
                             'c.company_name,jc.address,c.company_nature,jc.company_benefits,c.company_size,'
                             'c.industry', 'COUNT(*)')
        cur.execute(sqlNew)
        res = cur.fetchall()
        return res[0]

    def Work_List(self):
        cur = self.conn.cursor()
        cur.execute("Select j.job_title , COUNT(*) AS Qty FROM jc LEFT JOIN j ON jc.job_id = j.job_id GROUP BY "
                    "jc.job_id ORDER BY Qty DESC LIMIT 0,5")
        res = cur.fetchall()
        return res

    def All_DataRequest(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        return res
