# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.models import Contracts, Contract_status, C_status, Contracts_final
from flask_login import current_user
from sqlalchemy import or_

@blueprint.route('/index')
@login_required
def index():
    
    contracts = Contracts.query.all()
    filter_user = str(current_user)
    contract_status_list = Contract_status.query.filter(or_(Contract_status.contracter == filter_user, Contract_status.contractee == filter_user))
    #c_status = C_status.query.get(contracts_list.id)
    contracts_list = Contracts.query.filter(or_(Contracts.username == filter_user, Contracts.contracter == filter_user))
    #v2
    
    contracts_final_list = Contracts_final.query.filter(or_(Contracts_final.contractee == filter_user, Contracts_final.contracter == filter_user))

    c_status = C_status.query.all()
    ctr = Contracts_final.query.filter(or_(Contracts_final.contractee == filter_user, Contracts_final.contracter == filter_user)).count()
    print(ctr)
    return render_template('index.html', contracts=contracts, contracts_list=contracts_list, contract_status_list=contract_status_list, contracts_final_list=contracts_final_list, filter_user= filter_user, c_status=c_status, ctr=ctr)

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
