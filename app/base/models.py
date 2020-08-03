# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Float, ForeignKey
from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    funds =  Column(Float, default=0.0)
    reputation = Column(Float, default=0.0  )


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None



class Contracts_final(db.Model, UserMixin):
    __tablename__ = 'Contracts_final'

    id = Column(Integer, primary_key=True)
    contractee = Column(String)
    contract_title =  Column(String)
    discord = Column(String)
    refund = Column(String)
    trader = Column(String)
    payment_options = Column(String)
    payment_amount = Column(Float)
    contract_details = Column(String)
    contracter = Column(String)
    pending = Column(String)
    contract_stat = db.relationship('C_status', backref='contract', uselist=False)
    def __init__(self, contractee, contract_title, discord, refund, trader, payment_options, 
    payment_amount, contract_details, contracter, pending):

        self.contractee                 =  contractee 
        self.contract_title    =  contract_title
        self.discord    = discord
        self.refund    = refund
        self.trader    =  trader
        self.payment_options   = payment_options 
        self.payment_amount = payment_amount
        self.contract_details = contract_details
        self.contracter = contracter
        self.pending = pending


class C_status(db.Model, UserMixin):
    __tablename__ = 'C_status'

    id = Column(Integer, primary_key=True)
    c_id     = Column(Integer, ForeignKey('Contracts_final.id'), nullable=False)
    update   = Column(String)
    status   = Column(String)
    user_one = Column(Integer) 
    user_two = Column(Integer)
    complete = Column(Integer)
    cancel   = Column(Integer)  
    dispute  = Column(Integer)

    def __init__(self, c_id, update, status, user_one, user_two, complete, cancel, dispute): 
        self.c_id    = c_id    
        self.update  = update  
        self.status  = status  
        self.user_one= user_one
        self.user_two= user_two
        self.complete= complete
        self.cancel  = cancel  
        self.dispute = dispute 


class Contracts(db.Model, UserMixin):
    __tablename__ = 'Contract'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    contract_title =  Column(String)
    discord = Column(String)
    refund = Column(String)
    trader = Column(String)
    payment_options = Column(String)
    payment_amount = Column(Float)
    contract_details = Column(String)
    contracter = Column(String)



    def __init__(self, username, contract_title, discord, refund, trader, payment_options, 
    payment_amount, contract_details, contracter):

        self.username                 =  username 
        self.contract_title    =  contract_title
        self.discord    = discord
        self.refund    = refund
        self.trader    =  trader
        self.payment_options   = payment_options 
        self.payment_amount = payment_amount
        self.contract_details = contract_details
        self.contracter = contracter
        
class Contract_status(db.Model, UserMixin):
    __tablename__ = 'Contract_status'

    id               = Column(Integer, primary_key=True)
    
    contract_title    = Column(String)
    contracter           =      Column(String)
    contractee           =      Column(String)
    update              =         Column(String)
    status              =          Column(String)


    def __init__(self, contract_title, contracter, contractee, update, status): 

      
       self.contract_title = contract_title 
       self.contracter     = contracter     
       self.contractee     = contractee     
       self.update         = update         
       self.status         = status             

# ###Currently
# class Contract_log(db.Model, UserMixin):
#     __tablename__ = 'Contract_log'

#     id = Column(Integer, primary_key=True)
#     contract_status_id = Column(Integer, ForeignKey('parent.id'))
