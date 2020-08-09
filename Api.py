from flask import Flask, request, Response
from flask_restx import Api, Resource, fields
import pandas as pd
from Transform import Transform
from Dbase import Dbase
import sqlite3
from flask import jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
api = Api(app, title='Case Itaú API', description='Kaique Pedronio Novi')
api = api.namespace('', description='Operações Residencias e Média de preços')


@api.route('/residencias')
class GetResidencias(Resource):
    @api.param('neighbourhood_group')
    def get(self):
        conn = sqlite3.connect('CaseItau.sqlite3')
        cursor = conn.cursor()

        neighbourhood_group = request.args.get('neighbourhood_group')

        df = pd.read_sql_query("SELECT * FROM residencias WHERE neighbourhood_group =?", conn,
                               params=[neighbourhood_group])
        conn.commit()
        conn.close()

        return Response(df.to_json(orient="records"), mimetype='application/json')

    like = api.model('Residencias', {'id': fields.Integer('ID da residencia'), 'like': fields.Boolean('Like booleano')})

    @api.expect(like)
    def post(self):
        json_data = request.get_json(force=True)

        conn = sqlite3.connect('CaseItau.sqlite3')
        cursor = conn.cursor()

        id = json_data['id']
        like = json_data['like']

        cursor.execute("INSERT INTO residencias_like VALUES(?,?)", (id, like))
        conn.commit()
        conn.close()

        return jsonify(id=id, like=like)


@api.route('/preco-medio')
@api.param('neighbourhood_group')
class GetPrecoMedio(Resource):
    def get(self):
        conn = sqlite3.connect('CaseItau.sqlite3')
        cursor = conn.cursor()

        neighbourhood_group = request.args.get('neighbourhood_group')

        df = pd.read_sql_query("SELECT * FROM media_preco WHERE neighbourhood_group =?", conn,
                               params=[neighbourhood_group])
        conn.commit()
        conn.close()

        return Response(df.to_json(orient="records"), mimetype='application/json')


if __name__ == '__main__':

    pathresidenci_git, pathmediapreco_git = Transform(r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau"
                                                      r"/master/bases/airbnb_ny_2019.csv",
                                                      r"https://raw.githubusercontent.com/KaiquePedronio/CaseItau/master"
                                                      r"/bases/mapeamento_vizinhanca.csv").transform()

    conn, cursor = Dbase(pathresidenci_git, pathmediapreco_git).Main()

    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
