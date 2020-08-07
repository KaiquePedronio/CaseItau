import sqlite3
import pandas as pd


class Dbase:

    def __init__(self, pathresidenci, pathmediapreco):
        self.pathresidenci = pathresidenci
        self.pathmediapreco = pathmediapreco

    def Main(self):
        conn, cursor = self.CreateDatabase()
        self.CreateTables(conn, cursor)
        self.LoadFilestoTables(conn)
        conn.close()

        return conn, cursor

    def CreateDatabase(self):
        conn = sqlite3.connect('CaseItau.sqlite3')
        cursor = conn.cursor()

        return conn, cursor

    def CreateTables(self, conn, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS residencias(
                            id integer ,
                            name varchar(50),
                            host_id integer,
                            host_name varchar(50),
                            neighbourhood varchar(50),
                            latitude varchar(50),
                            longitude varchar(50),
                            room_type varchar(50),
                            price float,
                            minimum_nights integer,
                            number_of_reviews integer,
                            last_review Date,
                            reviews_per_month Float,
                            calculated_host_listings_count integer,
                            availability_365 integer,
                            neighbourhood_group varchar(50));
                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS media_preco(
                            neighbourhood_group varchar(50),
                            room_type varchar(50),
                            price float);
                            """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS residencias_like(
                                    id integer PRIMARY KEY,
                                    like boolean);

                                    """)

    def LoadFilestoTables(self, conn):
        df = pd.read_csv(self.pathresidenci, sep=",", encoding='utf8')
        df.to_sql('residencias', conn, if_exists='append', index=False)

        df = pd.read_csv(self.pathmediapreco, sep=",", encoding='utf8')
        df.to_sql('media_preco', conn, if_exists='append', index=False)

# if __name__ == '__main__':
#     Dbase().Main()
