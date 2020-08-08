import sqlite3
import pandas as pd
import requests
import io


class Dbase:

    def __init__(self, pathresidenci_git, pathmediapreco_git):
        self.pathresidenci_git = pathresidenci_git
        self.pathmediapreco_git = pathmediapreco_git

    def Main(self):
        conn, cursor = self.CreateDatabase()
        self.CreateTables(conn, cursor)
        self.DeleteDatas(conn, cursor)
        self.LoadFilestoTables(conn, cursor)
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

    def DeleteDatas(self, conn, cursor):
        cursor.execute("DELETE FROM residencias")
        cursor.execute("DELETE FROM media_preco")

    def LoadFilestoTables(self, conn, cursor):
        download_airbnb = requests.get(self.pathresidenci_git).content
        download_mapeamento = requests.get(self.pathmediapreco_git).content

        df_residenci = pd.read_csv(io.StringIO(download_airbnb.decode('utf-8')), sep=",")
        df_mapeamento = pd.read_csv(io.StringIO(download_mapeamento.decode('utf-8')), sep=",")

        df_residenci.to_sql('residencias', conn, if_exists='append', index=False)
        df_mapeamento.to_sql('media_preco', conn, if_exists='append', index=False)

        conn.commit()
        cursor.close()
        conn.close()


#if __name__ == '__main__':
#    pathresidenci_git = r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases_tratadas/residencias.csv"
#    pathmediapreco_git = r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases_tratadas/media_preco.csv"
#    Dbase(pathresidenci_git, pathmediapreco_git).Main()
