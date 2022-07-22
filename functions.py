User = [{"name":"Onkar", "username": "ob", "email":"ob@ss.com", "password":"ob123", "listOfUrl":[], "isActive": True}]
URLS = [{"url":"google.com", "shortURL":"gg.com", "isPrioritized": True, "isActive":True}, {"url":"facebook.com", "shortURL":"fb.com", "isPrioritized": False, "isActive":True}]
prioritizedURLs = [{"url":"google.com", "shortURL":"gg.com", "isPrioritized": True, "isActive":True}]
Admin = [{"name":"AdminUser", "username": "Admin", "email":"admin@gmail.com", "password":"Admin", "listOfUrl":[], "isActive":True}]

def checkUnique(shortUrlId):
    for url in URLS:
        if(url.shortUrlId == shortUrlId):
            return False
    return True

def findUsername(username):
    for user in User:
        if user['username'] == username and user['isActive'] == True:
            return user, True
    return None, False

def findAdminUsername(username):
    for admin in Admin:
        if admin['username'] == username and admin['isActive'] == True:
            return admin, True
    return None, False

def readAdminUrls(username):
    admin, isPresent = findAdminUsername(username)
    if not isPresent:
        return [], False
    urlList = []
    for url in admin['listOfUrl']:
        if url['isActive'] == True:
            urlList.append(url)
    return urlList, True


def createUser(name, username, email, password, listOfUrl, isActive):
    userPresent, isPresent = findUsername(username)
    if isPresent:
        return None, False
    user = {"name":name, "username": username, "email":email, "password":password, "listOfUrl":listOfUrl, "isActive": isActive}
    User.append(user)
    return user, True

def readUser(username):
    user, isPresent = findUsername(username)
    if not isPresent:
        return None, False
    return user, True

def readUsers():
    allUsers = []
    for user in User:
        if user['isActive'] == True:
            allUsers.append(user)
    return allUsers


def updateUser(username, propertyName, value):
    user, isPresent = findUsername(username)
    if not isPresent:
        return False
    user[propertyName] = value
    return True

def removeUser(username):
    user, isPresent = findUsername(username)
    if not isPresent:
        return False
    user['isActive'] = False
    for url in user['listOfUrl']:
        shortURL = url['shortURL']
        removeURL(shortURL)
    return True

def findURL(shortURL):
    for url in URLS:
        if url['shortURL'] == shortURL and url['isActive'] == True:
            return url, True
    return None, False

def findPrioritizedURL(shortURL):
    for url in prioritizedURLs:
        if url['shortURL'] == shortURL and url['isPrioritized'] == True:
            return url, True
    return None, False

def prioritizeURL(shortURL):
    urlPresent, isPresent = findURL(shortURL)
    if not isPresent:
        return False
    url, isPresentInPrioritized = findPrioritizedURL(shortURL)
    if isPresentInPrioritized:
        return False
    urlPresent['isPrioritized'] = True
    prioritizedURLs.append(urlPresent)
    return True

def removePrioritizedURL(shortURL):
    urlPresent, isPresent = findURL(shortURL)
    if not isPresent:
        return False
    url, isPresentInPrioritized = findPrioritizedURL(shortURL)
    if not isPresentInPrioritized:
        return False
    url['isPrioritized'] = False
    return True

def readPrioritizedURL(shortURL):
    urlPresent, isPresent = findURL(shortURL)
    if not isPresent:
        return None, False
    url, isPresentInPrioritized = findPrioritizedURL(shortURL)
    if not isPresentInPrioritized:
        return None, False
    return url, True

def readPrioritizedURLs():
    urlList = []
    for url in prioritizedURLs:
        if url['isPrioritized'] == True:
            urlList.append(url)
    return urlList


def addURL(username, originalURL, shortURL):
    url, isPresent = findURL(shortURL)
    if isPresent:
        return False
    user, status = findUsername(username)
    if not status:
        return False
    url = {"Username": username, "originalURL":originalURL, "shortURL": shortURL , "isActive": True , "isPrioritized": False , "numOfClicks" : 0}
    URLS.append(url)
    user['listOfUrl'].append(url)
    return True

def updateURL(shortURL, propertyName, value):
    url, isPresent = findURL(shortURL)
    if not isPresent:
        return False
    url[propertyName] = value
    return True

def readURLs():
    urlList = []
    for url in URLS:
        if url['isActive'] == True:
            urlList.append(url)
    return urlList

def readURL(shortURL):
    url, isPresent = findURL(shortURL)
    if not isPresent:
        return None, False
    return url, True
    

def removeURL(shortURL):
    url, isPresent = findURL(shortURL)
    if not isPresent:
        return False
    url['isActive'] = False
    return True


# User = [{"Username":"Onkar" , "Password":"Onkar" , "listOfURLs":[{"Username": "Onkar", "originalURL":"https://google.com/" , "shortURL": "abcd.com" , "isActive": True , "isPrioritized": True , "numOfClicks" : 47}]}]
# URLS = [{"Username": "Onkar", "originalURL":"https://google.com/" , "shortURL": "abcd.com/" , "isActive": True , "isPrioritized": True , "numOfClicks" : 47} ]
# prioritizedURLs = []
# Admin = {"username": "Admin", "userID": 1, "email":"admin@gmail.com", "password":"Admin", "listOfUrls":[{"Username": "Onkar", "originalURL":"https://google.com/" , "shortURL": "abcd" , "isActive": True , "isPrioritized": True , "numOfClicks" : 47} ]}
