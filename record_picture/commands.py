# -*- coding: utf-8 -*-
import click

from record_picture import app, db
from record_picture.models import User, Picture


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    user = User()
    picture = Picture()
    db.session.add(picture)
    db.session.add(user)
    db.session.commit()
    click.echo('Done.')
