
from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functions import *

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'strob3ehb6gs'  # Change this!
jwt = JWTManager(app)

@app.route('/', methods = ['GET'])
def home():
    return "Welcome to home page"

@app.route('/admin/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return 'missing password or username', 400

    if(username == "Admin" and password == "Admin"):
        access_token = create_access_token(identity={"username": username})
        return {"access_token": access_token}, 200
    else:
        return "Invalid username or password", 400


@app.route('/admin/getUsers', methods = ['GET'])
@jwt_required()
def getUsers():
    return jsonify(readUsers()), 200

@app.route('/admin/getUser/', defaults = {'username' : None}, methods = ['GET'])
@app.route('/admin/getUser/<username>', methods = ['GET'])
@jwt_required()
def getUser(username):
    if username == None:
        return {}, 400
    user, isPresent = readUser(username)
    if isPresent:
        return user, 200
    return {}, 400


@app.route('/admin/createUsers', methods = ['POST'])
@jwt_required()
def createUsers():
    name = request.json.get('name', None)
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    listOfUrl = request.json.get('listOfUrl', None)
    isActive = request.json.get('isActive', None)
    if not name or not username or not email or not password or not listOfUrl or not isActive:
        return 'Missing parameter', 400
    userObj, isCreated = createUser(name, username, email, password, listOfUrl, isActive)
    if not isCreated:
        return "User already exists", 400
    return "User added", 200
    

@app.route('/admin/updateUser/<username>', methods = ['PUT'])
@jwt_required()
def modifyUser(username):
    if username == None:
        return "Please enter username", 400
    propertyName = request.json.get('propertyName', None)
    value = request.json.get('value', None)
    if not propertyName or not value:
        return "Missing parameter", 400
    isUpdated = updateUser(username, propertyName, value)
    if not isUpdated:
        return "No such user", 400
    return "User updated", 200

@app.route('/admin/deleteUser/', defaults = {'username' : None}, methods = ['GET'])
@app.route('/admin/deleteUser/<username>', methods = ['DELETE'])
@jwt_required()
def deleteUser(username):
    if username == None:
        return "Please enter username", 400
    isDeleted = removeUser(username)
    if not isDeleted:
        return "No such user", 400
    return "User Deleted", 200

@app.route('/admin/prioritizeUrl/', defaults = {'shortURL' : None}, methods = ['GET'])
@app.route('/admin/prioritizeUrl/<shortURL>', methods = ['POST'])
@jwt_required()
def prioritizeUrl(shortURL):
    if shortURL == None:
        return "Please enter Url", 400
    isPrioritized = prioritizeURL(shortURL)
    if not isPrioritized:
        return "No such Url", 400
    return "Url Prioritized successfully", 200
    
@app.route('/admin/deletePrioritizedUrl/', defaults = {'shortURL' : None}, methods = ['GET'])
@app.route('/admin/deletePrioritizedUrl/<shortURL>', methods = ['DELETE'])
@jwt_required()
def deletePrioritizedUrl(shortURL):
    if shortURL == None:
        return "Please enter Url", 400
    isDeleted = removePrioritizedURL(shortURL)
    if not isDeleted:
        return "No such Url", 400
    return "Url Deleted successfully", 200

@app.route('/admin/getPrioritizedUrl/', defaults = {'shortURL' : None}, methods = ['GET'])
@app.route('/admin/getPrioritizedUrl/<shortURL>', methods = ['GET'])
@jwt_required()
def getPrioritizedUrl(shortURL):
    if shortURL == None:
        return {}, 400
    url, isPresent = readPrioritizedURL(shortURL)
    if not isPresent:
        return {}, 400
    return url, 200

@app.route('/admin/getPrioritizedUrls', methods = ['GET'])
@jwt_required()
def getPrioritizedUrls():
    return jsonify(readPrioritizedURLs()), 200


@app.route('/admin/getAdminURLs', methods = ['GET'])
@jwt_required()
def getAdminURLs():
    identity = get_jwt_identity()
    username = identity['username']
    urlList, status = readAdminUrls(username)
    if not status:
        return {}, 400
    return jsonify(urlList), 200
    
@app.route('/admin/addUrl', methods = ['POST'])
@jwt_required()
def addUrl():
    username = request.json.get("username" , None)
    originalURL = request.json.get("OriginalURL" , None)
    shortURL = request.json.get("ShortURL" , None)
    if not username or not originalURL or not shortURL:
        return 'Missing parameter', 400
    isAdded = addURL(username, originalURL, shortURL)
    if not isAdded:
        return "Error", 400
    return "Added", 200

@app.route('/admin/updateUrls/', defaults = {'shortURL' : None}, methods = ['PUT'])
@app.route('/admin/updateUrls/<shortURL>', methods = ['PUT'])
@jwt_required()
def updateUrls(shortURL):
    if shortURL == None:
        return "Please enter Url", 400
    propertyName = request.json.get("propertyName" , None)
    value = request.json.get("value" , None)
    if not propertyName or not value:
        return 'Missing parameter', 400
    isUpdated = updateURL(shortURL, propertyName, value)
    if not isUpdated:
        return "Error", 400
    return "Updated", 200

@app.route('/admin/readAllUrls', methods = ['GET'])
@jwt_required()
def readAllUrls():
    return jsonify(readURLs()), 200

@app.route('/admin/getSpecificUrl/', defaults = {'shortURL' : None}, methods = ['GET'])
@app.route('/admin/getSpecificUrl/<shortURL>', methods = ['GET'])
@jwt_required()
def getSpecificUrl(shortURL):
    if shortURL == None:
        return {}, 400
    url, isPresent = readURL(shortURL)
    if not isPresent:
        return {}, 400
    return url, 200

@app.route('/admin/deleteUrls/', defaults = {'shortURL' : None}, methods = ['DELETE'])
@app.route('/admin/deleteUrls/<shortURL>', methods = ['DELETE'])
@jwt_required()
def deleteUrls(shortURL):
    if shortURL == None:
        return "Please enter Url", 400
    isDeleted = removeURL(shortURL)
    if not isDeleted:
        return "Error", 400
    return "Deleted", 200




@app.route('/admin/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return 'missing password or username', 400

    if(username == "Onkar" and password == "Onkar"):
        access_token = create_access_token(identity={"username": username})
        return {"access_token": access_token}, 200
    else:
        return "Invalid username or password", 400


@app.route('/admin/getUser', methods = ['GET'])
@jwt_required()
def getUser():
    user = get_jwt_identity()
    print(user)
    return user['username']

@app.route('/admin/getUsers', methods = ['GET'])
@jwt_required()
def getUsers():
    users = {}
    idx = 1
    for user in functions.User:
        users[idx] = user['Username']
        idx = idx + 1
    print(len(functions.User))
    return users

@app.route('/admin/getUserByUsername/<string:username>' , methods = ['GET'])
@jwt_required()
def getUserByUsername(username):
    for user in functions.User:
        if user['Username'] == username:
            return user
    return "User not found"


@app.route('/getURLs', methods = ['GET'])
@jwt_required()
def getURL():
    userN = get_jwt_identity()
    username = userN['username']
    user = getUserByUsername(username)
    listOfURLs =  user['listOfURLs']
    urlDict = {}
    index = 1
    for url in listOfURLs:
        urlDict[index] = url['shortURL']
        index += 1
    return urlDict

@jwt_required()
def getPrioritizedURL(shortURL):
    for url in functions.prioritizedURLs:
        if url.shortURL == shortURL:
            return url['longURL']
    return "URL not found"

@app.route('/getLongURL/<string:shortURL>' , methods = ['GET'])
@jwt_required()
def getURLByURL(shortURL):
    url = getPrioritizedURL(shortURL)
    if url:
        return url
    userN = get_jwt_identity()
    username = userN['username']
    user = getUserByUsername(username)
    listOfURLs =  user['listOfURLs']
    for url in listOfURLs:
        if url['shortURL'] == shortURL:
            return url['originalURL']
    return "URL not found"

@app.route('/readURL/<string:shortURL>' , methods = ['GET'])
@jwt_required()
def readURL(shortURL):
    userN = get_jwt_identity()
    username = userN['username']
    user = getUserByUsername(username)
    listOfURLs =  user['listOfURLs']
    for url in listOfURLs:
        if url['shortURL'] == shortURL:
            return url
    return "URL not found"
# @app.route('/getLongURL/<string:shortURL>' , methods = ['GET'])
@jwt_required()
def getLongURL(shortURL):
    userN = get_jwt_identity()
    username = userN['username']
    user = getUserByUsername(username)
    listOfURLs =  user['listOfURLs']
    for url in listOfURLs:
        if url['shortURL'] == shortURL:
            return url
    return "URL not found"



def incrementNumOfClicks(url):
    url.numOfClicks += 1
    if url.numOfClicks > 30:
        url.isPrioritized = True
        functions.prioritizedURLs.append(url)

# @app.route('/updateURL' , methods = ['POST'])
# def updateURL():
#     pass

@app.route('/deleteURL/<string:shortURL>' , methods = ['POST'])
def deleteURL(shortURL):
    url = getLongURL(shortURL)
    url['isActive'] = False
    return "URL sucessfully deleted"


@app.route('/updateURL' , methods = ['POST'])
@jwt_required()
def updateURL():
    property = request.json.get('Property' , None)
    value = request.json.get('Value' , None)
    shortURL = request.json.get('ShortURL' , None)

    userN = get_jwt_identity()
    username = userN['username']
    user = getUserByUsername(username)
    listOfURLs =  user['listOfURLs']

    for url in listOfURLs:
        # print(url['shortURL'])
        # print(shortURL)
        if url['shortURL'] == shortURL:
            url[property] = value
            return 'URL updated successfully'
    return "URL not found"

@app.route('/register' , methods = ['POST'])
def register():
    try:
        username = request.json.get('Username' , None)
        password = request.json.get('Password' , None)
        userDict = {"Username": username , "Password": password , "listOfURLs": []}
        functions.User.append(userDict)
        return "Successfully registered"
        return 
    except:
        return "Oops something went wrong, please try again"

@app.route('/addURL' , methods = ['POST'])
@jwt_required()
def addURL():
    userN = get_jwt_identity()
    username = userN['username']
    originalURL = request.json.get("OriginalURL" , None)
    shortURL = request.json.get("ShortURL" , None)
    urlDict = {"Username": username, "originalURL":originalURL, "shortURL": shortURL , "isActive": True , "isPrioritized": False , "numOfClicks" : 0}
    try:
        functions.URLS.append(urlDict)
        user = getUserByUsername(username)
        user['listOfURLs'].append(urlDict)
        return "Successfully added new URL"
    except:
        return "Oops something went wrong, please try again"




app.run(port=5000, debug=True)
