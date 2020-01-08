from flask import request, jsonify, g, session, make_response
import click
from init import app
# from toJosn import JSONHelper
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blueprint.article import article_bp
from blueprint.file import file_bp
from blueprint.user import user_bp
import time
import os

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

def register_blueprint():
    app.register_blueprint(article_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(user_bp)

if __name__ == "__main__":
    register_blueprint()
    app.run(debug=True)
