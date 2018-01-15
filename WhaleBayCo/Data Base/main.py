import pymysql as sql

class db_class():

    # def __init__(self):
    #     pass

    def __init__(self, db_='db254688_this_is_serious',
                          username="u254688_ironman",
                          password='test1',
                          host_='mysql1327.cp.hostnet.nl',
                          port_=3306):
        self.connection = sql.connect(host=host_, user=username, passwd=password, db=db_, port=port_)

    def create_test_table(self):
        with self.connection.cursor() as cursor:
            sql_statement = "CREATE TABLE IF NOT EXISTS test_table (colom_een varchar(255), colom_twee varchar(255))"
            cursor.execute(sql_statement)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

database = db_class()
# database.create_connection()
database.create_test_table()

database.close_connection()
