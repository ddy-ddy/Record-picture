# -*- coding: utf-8 -*-
import click

from record_picture import app, db
from record_picture.models import User, login_password


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    name = 'Yu Duan'
    infos = [
        {"email": "1179730251@qq.com", "password": 123456},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in infos:
        login_info = login_password(email=m['email'], password=m['password'])
        db.session.add(login_info)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
