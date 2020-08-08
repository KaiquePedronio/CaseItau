import pandas as pd
import os
import shutil
import sys
import platform
from pathlib import Path
import numpy as np
import requests
import io

pd.set_option('display.width', 320)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)


class Transform:

    def __init__(self, fileairbnb, filemapeamento):
        self.fileairbnb = fileairbnb
        self.filemapeamento = filemapeamento
        self.platform = platform.system()

    def transform(self):
        pathtoread, pathtosave = self.platform_path()
        self.create_path(pathtoread, pathtosave)

        self.movefile(pathtoread)

        df_airbnb, df_mapeamento = self.read()

        df_residencia, pathresidenci_git = self.treatment_residencia(df_airbnb, df_mapeamento, pathtosave)

        pathmediapreco_git = self.treatment_mediapreco(pathtosave, df_residencia)

        return pathresidenci_git, pathmediapreco_git

    def platform_path(self):
        pathtoread = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases')
        pathtosave = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases_tratadas')

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


    def read(self):

        download_airbnb = requests.get(self.fileairbnb).content
        download_mapeamento = requests.get(self.filemapeamento).content

        df_airbnb = pd.read_csv(io.StringIO(download_airbnb.decode('utf-8')), sep=",")
        df_mapeamento = pd.read_csv(io.StringIO(download_mapeamento.decode('utf-8')), sep=";")


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

        pathresidenci_git =r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases_tratadas/residencias.csv"

        return df_residencia, pathresidenci_git

    def treatment_mediapreco(self, pathtosave, df_residencia):
        df_mediapreco = df_residencia[['neighbourhood_group', 'room_type', 'price']]

        df_mediapreco = df_mediapreco.groupby(['neighbourhood_group', 'room_type']).mean().reset_index()

        pathmediapreco = os.path.join(pathtosave, 'media_preco.csv')

        if 'media_preco.csv' in os.listdir(pathtosave):
            os.remove(pathmediapreco)

        df_mediapreco.to_csv(pathmediapreco, index=False, header=True)

        pathmediapreco_git = r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases_tratadas/media_preco.csv"

        return pathmediapreco_git


#if __name__ == '__main__':
#    Transform(r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases/airbnb_ny_2019.csv",
#              r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master/bases/mapeamento_vizinhanca.csv").transform()
