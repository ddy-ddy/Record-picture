# -*- coding: utf-8 -*-
import click

from record_picture import app, db
from record_picture.models import User


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    infos = [
        {"login_name": "duanyu", "password": "aAabcdefg123"},
        {"login_name": "z1", "password": "123"}
    ]

    for m in infos:
        hash_password = m['password']
        user = User(login_name=m['login_name'])
        user.set_password(hash_password)  # 给密码加密
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
