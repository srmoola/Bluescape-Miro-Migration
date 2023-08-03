from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import MigrationMasterScript_Generic_Working

app = Flask(__name__)
CORS(app)
api = Api(app)


class MainLink(Resource):
    @cross_origin()
    def options(self):
        return {"Allow": "POST, GET"}, 200

    def post(self):
        data = request.get_json()
        bluescape_id = data.get("bluescape")
        miro_id = data.get("miro")

        MigrationMasterScript_Generic_Working.MigrationMaster(bluescape_id, miro_id)

        return {"status": "Migration Completed"}, 200

    def get(self):
        return {"Server Status": "Up and Running!"}


api.add_resource(MainLink, "/")

if __name__ == "__main__":
    app.run()
