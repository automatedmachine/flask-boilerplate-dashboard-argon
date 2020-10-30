# -*- encoding: utf-8 -*-
from app import db
from app.home import blueprint
from app.home.forms import ClientForm, SessionForm
from app.home.models import Clients, Sessions
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import desc

@blueprint.route('/index')
@login_required
def index():
    return clients()
    #return render_template('index.html', segment='index')

@blueprint.route('clients/<id>', methods=['DELETE'])
@login_required
def delete_client(id):
    client = Clients.query.options(joinedload('sessions')).get(id)
    for session in client.sessions:
        db.session.delete(session)
    db.session.delete(client)
    db.session.commit()
    return('Operation Complete')

@blueprint.route('/clients', methods=['GET', 'POST'])
@blueprint.route('/debug', methods=['GET', 'POST'])
@login_required
def clients():    
    if request.method == 'POST':
      clients = Clients(**request.form)
      if clients.id == '':
        clients.id = None
        clients.user_id = current_user.id
        db.session.add(clients)
        db.session.commit()
      else:
        exist_client = Clients.query.get(clients.id)
        exist_client.update(**clients.values())
        db.session.commit()

    form = ClientForm(request.form)
    data = Clients.query.filter_by(user_id=current_user.id).all()
    data = [row.values() for row in data]
    columns = Clients.table_columns()

    return render_template('table.html',
    data=data,
    columns=columns,
    title='Client',
    form = form)

@blueprint.route('/sessions', methods=['GET', 'POST'])
@login_required
def debug():
    if request.method == 'POST':
      sessions = Sessions(**request.form)
      sessions.date = datetime.strptime(sessions.date,'%Y-%m-%d')
      if sessions.id == '':
        sessions.id = None
        sessions.user_id = current_user.id
        db.session.add(sessions)
        db.session.commit()
      else:
        exist_session = Sessions.query.get(sessions.id)
        exist_session.update(**sessions.values())
        db.session.commit()

    form = SessionForm(request.form)
    form.client_id.choices = GetClientList()
    query = Sessions.query.filter_by(user_id=current_user.id).join('clients').order_by(desc(Sessions.date)).all()

    data = []
    for session in query:
        c = session.clients.values()
        s = session.values()
        s['duration'] = float(s['duration'])
        s['date'] = str(s['date'])
        row = {**c, **s}
        data.append(row)

    columns = Sessions.table_columns()


    return render_template('table.html',
    data=data,
    columns=columns,
    title='Session',
    form = form)

@blueprint.route('sessions/<id>', methods=['DELETE'])
@login_required
def delete_session(id):
    session = Sessions.query.get(id)
    db.session.delete(session)
    db.session.commit()
    return('Operation Complete')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

# Helper - Get Client list for Session Form
def GetClientList():
    clients = Clients.query.filter_by(user_id=current_user.id).all()
    clients = [(client.id, client.first_name + ' ' + client.last_name) for client in clients]
    return(clients)
