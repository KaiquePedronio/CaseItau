import pandas as pd
import os
import shutil
import sys
import platform
from pathlib import Path
import numpy as np

pd.set_option('display.width', 320)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)


class Transform:

    def __init__(self, fileairbnb, filemapeamento):
        self.fileairbnb = fileairbnb
        self.filemapeamento = filemapeamento
        self.platform = platform.system()
        # self.pathload = ''

    def transform(self):
        pathtoread, pathtosave = self.platform_path()
        self.create_path(pathtoread, pathtosave)
        airbnb, mapeamento = self.movefile(pathtoread)

        df_airbnb, df_mapeamento = self.read(airbnb, mapeamento)
        df_residencia, pathresidenci = self.treatment_residencia(df_airbnb, df_mapeamento, pathtosave)

        pathmediapreco = self.treatment_mediapreco(pathtosave, df_residencia)

        return pathresidenci, pathmediapreco

    def platform_path(self):
        pathtoread = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases')
        pathtosave = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases_tratadas')

        if self.platform == 'Windows':
            pass
        else:
            pathtoread = pathtoread.split(":")[1]
            pathtosave = pathtosave.split(":")[1]

        return pathtoread, pathtosave

    def create_path(self, pathtoread, pathtosave):

        if pathtoread.split(os.sep)[-2] in os.listdir(os.path.split(os.path.dirname(pathtoread))[0]):
            pass
        else:
            os.mkdir(os.path.split(pathtoread)[0])
            os.mkdir(pathtoread)
            os.mkdir(pathtosave)

    def movefile(self, pathtoread):
        try:
            if os.path.split(self.fileairbnb)[0] != pathtoread:
                shutil.move(self.fileairbnb, pathtoread)
        except:
            pass

        try:
            if os.path.split(self.filemapeamento)[0] != pathtoread:
                shutil.move(self.filemapeamento, pathtoread)
        except:
            pass

        airbnb = os.path.join(pathtoread, os.path.split(self.fileairbnb)[1])
        mapeamento = os.path.join(pathtoread, os.path.split(self.filemapeamento)[1])

        return airbnb, mapeamento

    def read(self, airbnb, mapeamento):
        df_airbnb = pd.read_csv(airbnb, sep=',', encoding='utf8')
        df_mapeamento = pd.read_csv(mapeamento, sep=';', encoding='utf8')

        return df_airbnb, df_mapeamento

    def treatment_residencia(self, df_airbnb, df_mapeamento, pathtosave):

        df_airbnb = df_airbnb.drop_duplicates()
        df_mapeamento = df_mapeamento.drop_duplicates()

        df_airbnb = df_airbnb.dropna()
        df_mapeamento = df_mapeamento.dropna()

        df_residencia = pd.merge(df_airbnb, df_mapeamento, how='left', left_on='neighbourhood',
                                 right_on='vizinhanca')
        # df_residencia = df_airbnb.set_index('neighbourhood').join(df_mapeamento.set_index('vizinhanca'))

        df_residencia = df_residencia.drop(columns=['vizinhanca'])

        df_residencia.rename(columns={'vizinhanca_grupo': 'neighbourhood_group'}, inplace=True)

        df_residencia = df_residencia.loc[
            df_residencia['neighbourhood_group'].isin(['Brooklyn', 'Manhattan', 'Queens', 'Staten Island'])]

        pathresidenci = os.path.join(pathtosave, 'residencias.csv')

        if 'residencias.csv' in os.listdir(pathtosave):
            os.remove(pathresidenci)

        df_residencia.to_csv(pathresidenci, index=False, header=True)

        return df_residencia, pathresidenci

    def treatment_mediapreco(self, pathtosave, df_residencia):
        df_mediapreco = df_residencia[['neighbourhood_group', 'room_type', 'price']]

        df_mediapreco = df_mediapreco.groupby(['neighbourhood_group', 'room_type']).mean().reset_index()

        pathmediapreco = os.path.join(pathtosave, 'media_preco.csv')

        if 'media_preco.csv' in os.listdir(pathtosave):
            os.remove(pathmediapreco)

        df_mediapreco.to_csv(pathmediapreco, index=False, header=True)

        return pathmediapreco

# if __name__ == '__main__':
#     Transform(r"C:\Users\kaiqu\Case_Itau\bases\airbnb_ny_2019.csv",
#               r"C:\Users\kaiqu\Case_Itau\bases\mapeamento_vizinhanca.csv").transform()
