from flask import Blueprint
testRoute = Blueprint('testRoute', __name__)

@testRoute.route('/manu1')  #  路由拿掉剛才標上的生產
def testroute():
    return '<h1>You win!</h1>'

@testRoute.route('/manu2')  #  路由拿掉剛才標上的生產
def testroute2():
    return '<h1>You win2!</h1>'

@testRoute.route('/manu3')  #  路由拿掉剛才標上的生產
def testroute3():
    return '<h1>You win3!</h1>'