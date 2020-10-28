"""
Bank Transacion API
--------------------

* Registration of a user with 6 tokens initially.
* Detect similarity between text1 and text2 then return ratio database for 1 token.
* Admin can refill tokens.

@author Hamza Arain
@version 0.0.1v
@date 29 October 2020

"""


# Import modules
## Api related modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

## database related
from pymongo import MongoClient

## password encryption related 
import bcrypt

# ###########################################################
# ########################  Tool Class ######################
# ###########################################################    

class Tool():
    def JSONOutputMessage(statusCode, output=""):
        """Return status code 200 & output"""
        retMap = {
                'Message': output,
                'Status Code': statusCode
            }
        return jsonify(retMap)


    def verifyPw(username, password):
        """varify password from database"""
        hashed_pw = users.find({
            "Username":username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False

    def UserExist(username):
        """Check the existance of user"""
        if users.find({"Username":username}).count() == 0:
            return False
        else:
            return True

    def verifyCredentials(username, password):
        if not Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username"), True

        correct_pw = Tool.verifyPw(username, password)

        if not correct_pw:
            return Tool.JSONOutputMessage(statusCode=302, output="Incorrect password"), True

        return None, False


    def cashWithUser(username):
        cash = users.find({
            "Username":username
        })[0]["Own"]
        return cash

    def debtWithUser(username):
        debt = users.find({
            "Username":username
        })[0]["Debt"]
        return debt

    def updateAccount(username, balance):
        users.update({
            "Username": username
        },{
            "$set":{
                "Own": balance
            }
        })

    def updateDebt(username, balance):
        users.update({
            "Username": username
        },{
            "$set":{
                "Debt": balance
            }
        })



# ###########################################################
# #######################  API Classes ######################
# ###########################################################    

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid username")

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Own":0,
            "Debt":0
        })

        return Tool.JSONOutputMessage(statusCode=200, output="You successfully signed up for the API")

class Add(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        if money<=0:
            return Tool.JSONOutputMessage(statusCode=304, output="The money amount entered must be greater than 0")

        cash = Tool.cashWithUser(username)
        money-= 1 #Transaction fee
        # Add transaction fee to bank account
        # bank_cash = Tool.cashWithUser("BANK")
        bank_cash = Tool.cashWithUser(username)
        Tool.updateAccount(username, bank_cash+1)

        #Add remaining to user
        Tool.updateAccount(username, cash+money)

        return Tool.JSONOutputMessage(statusCode=200, output="Amount Added Successfully to account")


class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to       = postedData["to"]
        money    = postedData["amount"]


        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = Tool.cashWithUser(username)
        if cash <= 0:
            return Tool.JSONOutputMessage(statusCode=303, output="You are out of money, please Add Cash or take a loan")


        if money<=0:
            return Tool.JSONOutputMessage(statusCode=304, output="The money amount entered must be greater than 0")

        if not Tool.UserExist(to):
            return Tool.JSONOutputMessage(statusCode=301, output="Recieved username is invalid")


        cash_from = Tool.cashWithUser(username)
        cash_to   = Tool.cashWithUser(to)
        bank_cash = Tool.cashWithUser(username)

        Tool.updateAccount(username, bank_cash+1)
        Tool.updateAccount(to, cash_to+money-1)
        Tool.updateAccount(username, cash_from - money)

        return Tool.JSONOutputMessage(statusCode=200, output="Amount added successfully to account")


class Balance(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        retJson = users.find({
            "Username": username
        },{
            "Password": 0, #projection
            "_id":0
        })[0]

        return jsonify(retJson)

class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money    = postedData["amount"]

        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = Tool.cashWithUser(username)
        debt = Tool.debtWithUser(username)
        Tool.updateAccount(username, cash+money)
        Tool.updateDebt(username, debt + money)

        return Tool.JSONOutputMessage(statusCode=200, output="Loan Added to Your Account")


class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money    = postedData["amount"]

        retJson, error = Tool.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        cash = Tool.cashWithUser(username)

        if cash < money:
            return Tool.JSONOutputMessage(statusCode=303, output="Not Enough Cash in your account")

        debt = Tool.debtWithUser(username)
        Tool.updateAccount(username, cash-money)
        Tool.updateDebt(username, debt - money)

        return Tool.JSONOutputMessage(statusCode=200, output="Loan Paid")


# ###########################################################
# ##################### Run Application #####################
# ###########################################################


# Database connection
# # "db" is same as written in web Dockerfile
# # "27017" is default port for MongoDB 
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

# App & API creation
app = Flask(__name__)
api = Api(app)

# API paths
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')


if __name__=="__main__":
    app.run(host='0.0.0.0')
