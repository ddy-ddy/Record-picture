# -*- coding: utf-8 -*-
import click

from record_picture import app, db
from record_picture.models import User, Picture


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    infos_user = [
        {"login_name": "z1", "password": 123, "profile_name": "duanyu", "email": "1179730251@qq.com",
         "iphone": "13237088151",
         }
    ]

    for m in infos_user:
        hash_password = m['password']
        user = User(login_name=m["login_name"], profile_name=m["profile_name"],
                    email=m["email"], iphone=m["iphone"])
        user.set_password(hash_password)  # 给密码加密
        db.session.add(user)
        picture = Picture()
        db.session.add(Picture)
        db.session.commit()
        click.echo('Done.')
