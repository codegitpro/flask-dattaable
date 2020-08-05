# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, flash, Flask
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import os
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, ContractForm
from app.base.models import User, Contracts, Contract_status, Contracts_final, C_status

from app.base.util import verify_pass




@blueprint.route('/')
def route_default():
   
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration

@blueprint.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    
    #v2
    contract_final = Contracts_final.query.get(entry_id)
    if contract_final is not None:
        contract_final.pending = "declined"
        getContract = C_status.query.get(entry_id)
        getContract.update = "Contract was Declined" 
        getContract.status = "Declined"
        db.session.commit()
        flash("Declined")
    return redirect(url_for('base_blueprint.login'))



@blueprint.route('/approve/<int:entry_id>')
def approve_entry(entry_id):
    
    contract_approve = Contracts_final.query.get(entry_id)

  
    if contract_approve is not None: 
        current_obj = C_status.query.get(entry_id)
        current_obj.pending = "no"
        current_obj.status = "Payment Required"
        current_obj.update = "Awaiting Payment"
        db.session.commit()
        contract_final = Contracts_final.query.get(entry_id)
        user = User.query.filter(User.username == str(current_user)).first()
        if(user.funds >= contract_final.payment_amount):
            current_obj.status = "Ongoing"
            current_obj.update = "Contract Started"
        contract_final.pending = "no"
        db.session.commit()
        print("working")
        flash("Approve")
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/complete/<int:entry_id>')
def complete_entry(entry_id):
    get_contract = Contracts_final.query.get(entry_id)
    user = User.query.filter(User.username == str(current_user)).first()
    c_status = C_status.query.get(entry_id)
    if(get_contract.contractee == user.username):
        c_status.status = "Pending (Contracter needs to accept)"
        c_status.update = "Pending Acceptance (Contracter needs to accept)"
        c_status.user_one = 1
        db.session.commit()
    if(get_contract.contracter == user.username):
        c_status.status = "Pending (Contractee needs to accept)"
        c_status.update = "Pending Acceptance(Contractee needs to accept)"
        c_status.user_two = 1
        db.session.commit()
    if(c_status.user_one == 1 and c_status.user_two == 1): 
        c_status.status = "Contract Finished"
        c_status.update = "Completed"
        
        contracter = get_contract.contracter
        user = User.query.filter(User.username == str(contracter)).first()
        user.reputation = user.reputation + 3.0 
        contractee = get_contract.contractee 
        user = User.query.filter(User.username == str(contractee)).first()
        user.reputation = user.reputation + 3.0 
        db.session.commit()
        flash("Complete")
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/cancel/<int:entry_id>')
def cancel_entry(entry_id):
    get_contract = Contracts_final.query.get(entry_id)
    user = User.query.filter(User.username == str(current_user)).first()
    c_status = C_status.query.get(entry_id)
    if(get_contract.contractee == user.username):
        c_status.status = "Action required"
        c_status.update = "Attempting to cancel"
        c_status.user_one = 1
        db.session.commit()
    if(get_contract.contracter == user.username):
        c_status.status = "Action required"
        c_status.update = "Attempting to cancel"
        c_status.user_two = 1
        db.session.commit()
    if(c_status.user_one == 1 and c_status.user_two == 1): 
        c_status.status = "Cancelled"
        c_status.update = "Declined"
        
        # contracter = get_contract.contracter
        # user = User.query.filter(User.username == str(contracter)).first()
        # user.reputation = user.reputation + 3.0 
        # contractee = get_contract.contractee 
        # user = User.query.filter(User.username == str(contractee)).first()
        # user.reputation = user.reputation + 3.0 
        db.session.commit()
        flash("Cancel")
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/dispute/<int:entry_id>')
def dispute_entry(entry_id):
    get_contract = Contracts_final.query.get(entry_id)
    user = User.query.filter(User.username == str(current_user)).first()
    c_status = C_status.query.get(entry_id)
    if(get_contract.contractee == user.username):
        c_status.status = "Dispute"
        c_status.update = "Dispute via discord"
        c_status.user_one = 1
        db.session.commit()
    if(get_contract.contracter == user.username):
        c_status.status = "Dispute"
        c_status.update = "Dispute via discord"
        c_status.user_two = 1
        db.session.commit()
        flash("Dispute")
    return redirect(url_for('base_blueprint.login', message="Dispute"))


@blueprint.route('/contract', methods=['GET', 'POST'])
def contract():
    
    contractform = ContractForm(request.form)
    if request.method == "POST":
        
        
       if 'contract' in request.form:
        
        # read form data
            username = request.form.get('list_user')
            contract_title =  request.form.get('contract_title')
            discord =  request.form.get('discord')
            refund = request.form.get('refund')
            traders_address = request.form.get('traders_address')
            payment_options = request.form.get('test')
            payment_amount = request.form.get('payment_amount')
            details = request.form.get('details')
            contracter =  str(current_user)
            contract_update = "Pending Acceptance"
            contract_status = "Pending"
            #v2
            contracts_final = Contracts_final(username, contract_title, discord, refund, traders_address, payment_options, payment_amount, details, contracter, "yes")
            db.session.add(contracts_final)
            value = 0
            
            db.session.commit()
            ctr = db.session.query(Contracts_final).count()

            c_status = C_status(ctr, contract_update,contract_status, value, value, value, value, value)    
            db.session.add(c_status)       
            db.session.commit()
            return render_template('ui-forms.html', message="Contract sent!", form=contractform)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    filter_user = str(current_user)
    users = User.query.filter(User.username != filter_user).all()
    return render_template('ui-forms.html', form=contractform,users=users) 

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    
    if 'login' in request.form:
        print('loginrequestform')
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        print('formpassword, userpassword', request.form['password'], user)
        # Check the password
        if user and verify_pass( password, user.password):
            
            login_user(user)
            print('loginsuceess')
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
