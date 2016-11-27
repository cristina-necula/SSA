import sqlite3

DATABASE = 'accessControlPolicy.db'
READ_PERMISSION = 'r'
CREATE_PERMISSION = 'c'
WRITE_PERMISSION = 'w'

TYPE_FOLDER = 0
TYPE_FILE = 1

ERROR_EXISTS = 'AlreadyExisting'
ERROR_NOT_AUTHORIZED = 'NotAuthorized'
ERROR_NOT_EXISTING = 'NotExisting'
ERROR_USER_NOT_FOUND = 'The specified username and password are incorrect'

ERROR_CREATE_PARENT = 'ParentDirectorNotExisting'
ERROR_WRITE_FOLDER = 'Cannot write in a folder'
OK = 'ok'
ROOT = 'root'

class DatabaseAccessControl():
    def __init__(self):
        self.dbConnection = sqlite3.connect(DATABASE, check_same_thread = False)
        self.cursor = self.dbConnection.cursor()

    # <editor-fold desc="Database initialization and cleanup">

    def createTables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS USER(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                            ' username TEXT, password TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS RESOURCE(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            'name TEXT, content TEXT, type INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ACCESS_POLICY(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            'userID INTEGER, resourceID INTEGER, permissions TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ROLE(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            'name TEXT, permissions TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ACL(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            'resourceID INTEGER, roleID INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS USER_ROLE(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            'userID INTEGER, roleID INTEGER)')
        self.dbConnection.commit()

    def dropTables(self):
        self.cursor.execute('DROP TABLE IF EXISTS USER')
        self.cursor.execute('DROP TABLE IF EXISTS RESOURCE')
        self.cursor.execute('DROP TABLE IF EXISTS ACCESS_POLICY')
        self.cursor.execute('DROP TABLE IF EXISTS ROLE')
        self.cursor.execute('DROP TABLE IF EXISTS ACL')
        self.cursor.execute('DROP TABLE IF EXISTS USER_ROLE')
        self.dbConnection.commit()

    def recreateDefaultDB(self):
        self.dropTables()
        self.createTables()
        self.addUserAndDefaultPermissions("alice", "alice")
        self.addUserAndDefaultPermissions("bob", "bob")
        self.addUserAndDefaultPermissions("root", "root")

    def addUserAndDefaultPermissions(self, username, password):
        self.cursor.execute('SELECT * FROM USER WHERE username=? AND password=?', (username, password))
        user = self.cursor.fetchone()
        if user is None:
            newUser = (username, password)
            newDefaultFolder = ("/" + username, "", TYPE_FOLDER)

            self.cursor.execute('INSERT INTO USER VALUES (NULL,?,?)', newUser)
            userID = self.cursor.lastrowid

            self.cursor.execute('INSERT INTO RESOURCE VALUES (NULL,?,?,?)', newDefaultFolder)
            resourceID = self.cursor.lastrowid

            permissions = CREATE_PERMISSION + READ_PERMISSION + WRITE_PERMISSION
            self.cursor.execute('INSERT INTO ACCESS_POLICY VALUES (NULL,?,?,?)', (userID, resourceID, permissions))

            self.dbConnection.commit()

    # </editor-fold>

    # <editor-fold desc="Create, read and write resource">

    def createResource(self, username, password, resourceName, resourceType, content=None):
        # check if user exists
        user = self.getUser(username, password)
        if user is None:
            return ERROR_USER_NOT_FOUND
        else:
            # get parent resource
            path = resourceName.split("/")
            pathToNewFile = ""
            for i in range(1, len(path) - 1):
                pathToNewFile = pathToNewFile + "/" + path[i]
            parentResource = self.getResourceByName(pathToNewFile)
            # check if parent resource exists
            if parentResource is None:
                return ERROR_CREATE_PARENT
            else:
                # get permissions for parent resource
                permissions = self.getResourcePermissionsForUserFromAP(user, parentResource)
                if permissions is None or permissions == "" or permissions[3].find(CREATE_PERMISSION) == -1:
                    return ERROR_NOT_AUTHORIZED
                else:
                    # check if new resource exists
                    newResource = self.getResourceByName(resourceName)
                    if newResource is None:
                        newResourceID = self.insertResourceToDB(user[0], resourceName, resourceType, content,
                                                                permissions[3])
                        self.updateNewResourcePemissionsForOthers(user, parentResource, newResourceID)
                        return OK
                    else:
                        return ERROR_EXISTS

    def readResource(self, username, password, resourceName):
        # check if user exists
        user = self.getUser(username, password)
        if user is None:
            return ERROR_USER_NOT_FOUND
        else:
            # check if resource exists
            resource = self.getResourceByName(resourceName)
            if resource is None:
                return ERROR_NOT_EXISTING
            else:
                # check if user has permission
                permissions = self.getResourcePermissionsForUserFromACL(user, resource)
                if permissions is None or permissions == "" or permissions.find(READ_PERMISSION) == -1:
                    return ERROR_NOT_AUTHORIZED
                else:
                    if resource[3] == TYPE_FILE:
                        if resource[2] is None:
                            return OK + ", \"\""
                        else:
                            return OK + ", " + str(resource[2])
                    else:
                        return OK + ", \"" + self.getFolderContent(resourceName) + "\""

    def writeResource(self, username, password, resourceName, value):
        # check if user exists
        user = self.getUser(username, password)
        if user is None:
            return ERROR_USER_NOT_FOUND
        else:
            # check if resource exists
            resource = self.getResourceByName(resourceName)
            if resource is None:
                return ERROR_NOT_EXISTING
            else:
                # check if user has permission
                permissions = self.getResourcePermissionsForUserFromACL(user, resource)
                if permissions is None or permissions == "" or permissions.find(WRITE_PERMISSION) == -1:
                    return ERROR_NOT_AUTHORIZED
                else:
                    if resource[3] == TYPE_FILE:
                        return self.updateResourceContent(resource[0], value)
                    else:
                        return ERROR_WRITE_FOLDER

    # </editor-fold>

    # <editor-fold desc="RBAC - ACL methods">

    def createRole(self, username, password, roleName):
        if username != ROOT and password != ROOT:
            return ERROR_NOT_AUTHORIZED
        self.cursor.execute('SELECT * FROM ROLE WHERE name=?', (roleName, ))
        role = self.cursor.fetchone()
        if role is None:
            self.cursor.execute('INSERT INTO ROLE VALUES(NULL,?,?)', (roleName, ""))
            self.dbConnection.commit()
            return OK
        return ERROR_EXISTS

    def changePermissionsForRole(self, roleName, permissions):
        self.cursor.execute('SELECT * FROM ROLE WHERE name=?', (roleName, ))
        role = self.cursor.fetchone()
        if role is None:
            return ERROR_NOT_EXISTING
        self.cursor.execute('UPDATE ROLE set permissions=? WHERE id=? AND name=?',
                            (permissions, role[0], role[1]))
        self.dbConnection.commit()
        return OK

    def assignRoleToUser(self, username, roleName):
        # get user
        self.cursor.execute('SELECT * FROM USER WHERE username=?', (username, ))
        user = self.cursor.fetchone()
        if user is None:
            return ERROR_NOT_EXISTING
        # get role
        self.cursor.execute('SELECT * FROM ROLE WHERE name=?', (roleName, ))
        role = self.cursor.fetchone()
        if role is None:
            return ERROR_NOT_EXISTING
        # check if user already has this role
        self.cursor.execute('SELECT * FROM USER_ROLE WHERE userId=? AND roleID=?', (user[0], role[0]))
        userRole = self.cursor.fetchone()
        if userRole is None:
            self.cursor.execute('INSERT INTO USER_ROLE VALUES(NULL,?,?)', (user[0], role[0]))
            self.dbConnection.commit()
            return OK
        else:
            return ERROR_EXISTS

    def addACL(self, username, password, fileName, roleName):
        # check if user exists
        user = self.getUser(username, password)
        if user is None:
            return ERROR_USER_NOT_FOUND
        else:
            # check if resource exists
            resource = self.getResourceByName(fileName)
            # check if user is owner
            filePermissions = self.getResourcePermissionsForUserFromAP(user, resource)
            if filePermissions is None or filePermissions[3].find(CREATE_PERMISSION) == -1:
                return ERROR_NOT_AUTHORIZED
            else:
                # check if role exists
                self.cursor.execute('SELECT * FROM ROLE WHERE name=?', (roleName,))
                role = self.cursor.fetchone()
                if role is None:
                    return ERROR_NOT_EXISTING
                else:
                    # check if file already has this role asociated
                    self.cursor.execute('SELECT * FROM ACL WHERE resourceId=? AND roleID=?', (resource[0], role[0]))
                    acl = self.cursor.fetchone()
                    if acl is None:
                        self.cursor.execute('INSERT INTO ACL VALUES(NULL,?,?)', (resource[0], role[0]))
                        self.dbConnection.commit()
                        return OK
                    else:
                        return ERROR_EXISTS

    def getResourcePermissionsForUserFromACL(self, user, resource):
        # if user is owner, get default permissions
        filePermissions = self.getResourcePermissionsForUserFromAP(user, resource)
        if filePermissions is not None:
            return filePermissions[3]
        permissions = ""
        # get ACL for resource
        self.cursor.execute('SELECT * FROM ACL WHERE resourceId=?', (resource[0],))
        accessControlList = self.cursor.fetchall()
        if accessControlList is None or len(accessControlList) == 0:
            # find parent with ACL
            parentResource = self.getParentResource(resource[1])
            if parentResource is None:
                return permissions
            else:
                return self.getResourcePermissionsForUserFromACL(user, parentResource)
        else:
            # get user role for resource
            userRoles = []
            for accessControlElement in accessControlList:
                self.cursor.execute('SELECT * FROM USER_ROLE WHERE userID=? AND roleID=?',
                                    (user[0], accessControlElement[2]))
                userRoles.append(self.cursor.fetchone())
            for userRole in userRoles:
                # get permissions for role
                self.cursor.execute('SELECT * FROM ROLE WHERE id=?', (userRole[2],))
                role = self.cursor.fetchone()
                permissions += role[2]
            return permissions

    # </editor-fold>

    # <editor-fold desc="Simple access control policy methods">

    def updatePermissionsForResource(self, owner, resource, permissions):
        # check if others already have permissions on file and update them, else insert new permissions
        self.cursor.execute('SELECT * from ACCESS_POLICY WHERE userID NOT LIKE ? AND resourceID=?',
                            (owner[0], resource[0]))
        resources = self.cursor.fetchall()
        if len(resources) == 0:
            self.cursor.execute('SELECT * from USER WHERE username NOT LIKE ?', (owner[1],))
            otherUsers = self.cursor.fetchall()
            for user in otherUsers:
                self.cursor.execute('INSERT INTO ACCESS_POLICY VALUES(NULL,?,?,?)',
                                    (user[0], resource[0], permissions))
        else:
            for res in resources:
                self.cursor.execute(
                    'UPDATE ACCESS_POLICY set permissions=? WHERE userID=? AND resourceID=?',
                    (permissions, res[1], res[2]))

        # if resource is folder, find resource children and update/insert permissions
        if resource[3] == TYPE_FOLDER:
            self.cursor.execute('SELECT USER.id, RESOURCE.id FROM RESOURCE, USER '
                                'WHERE RESOURCE.name LIKE ? AND USER.id NOT LIKE ?',
                                (resource[1] + "/%", resource[1]))
            children = self.cursor.fetchall()
            for child in children:
                self.cursor.execute('SELECT * from ACCESS_POLICY WHERE userID=? AND resourceID=?',
                                    (child[0], child[1]))
                access = self.cursor.fetchone()
                if access is None:
                    self.cursor.execute('INSERT INTO ACCESS_POLICY VALUES(NULL,?,?,?)',
                                        (child[0], child[1], permissions))
                else:
                    self.cursor.execute(
                        'UPDATE ACCESS_POLICY set permissions=? WHERE userID=? AND resourceID=?',
                        (permissions, child[0], child[1]))
        self.dbConnection.commit()

    def getResourcePermissionsForUserFromAP(self, user, resource):
        userID = user[0]
        resourceID = resource[0]
        self.cursor.execute('SELECT * from ACCESS_POLICY where userID=? and resourceID=?',
                            (userID, resourceID))
        return self.cursor.fetchone()

    def updateNewResourcePemissionsForOthers(self, owner, parentResource, newResourceID):
        self.cursor.execute('SELECT * from ACCESS_POLICY WHERE userID NOT LIKE ? and resourceID=?',
                            (owner[0], parentResource[0]))
        resources = self.cursor.fetchall()
        for resource in resources:
            resourcePermissions = resource[3].replace("c", "")
            self.cursor.execute('INSERT INTO ACCESS_POLICY VALUES(NULL,?,?,?)',
                                (resource[1], newResourceID, resourcePermissions))
        self.dbConnection.commit()

    def changePermissions(self, username, password, resourceName, permissions):
        # check if user exists
        user = self.getUser(username, password)
        if user is None:
            return ERROR_USER_NOT_FOUND
        else:
            # check if resource exists
            resource = self.getResourceByName(resourceName)
            if resource is None:
                return ERROR_NOT_EXISTING
            else:
                # check if user has permission
                filePermissions = self.getResourcePermissionsForUserFromAP(user, resource)
                if filePermissions is None or filePermissions[3].find(CREATE_PERMISSION) == -1:
                    return ERROR_NOT_AUTHORIZED
                else:
                    self.updatePermissionsForResource(user, resource, permissions)
                    return OK

    # </editor-fold>

    # --- HELPERS --- #

    def getParentResource(self, resourceName):
        path = resourceName.split("/")
        pathToNewFile = ""
        for i in range(1, len(path) - 1):
            pathToNewFile = pathToNewFile + "/" + path[i]
        return self.getResourceByName(pathToNewFile)

    def updateResourceContent(self, resourceID, content):
        self.cursor.execute('UPDATE RESOURCE SET content=? WHERE id=?', (content, resourceID))
        self.dbConnection.commit()
        return OK

    def getUser(self, username, password):
        self.cursor.execute('SELECT * FROM USER WHERE username=? AND password=?', (username, password))
        return self.cursor.fetchone()

    def getFolderContent(self, folder):
        self.cursor.execute('SELECT * FROM RESOURCE WHERE name LIKE ?', (folder + "/" + "%",))
        rows = self.cursor.fetchall()
        content = set()
        for i in range(0, len(rows)):
            content.add(str(rows[i][1].split(folder)[1].split('/')[1]))
        return ", ".join(str(res) for res in content)

    def getResourceByName(self, resourceName):
        self.cursor.execute('SELECT * FROM RESOURCE WHERE name=?', (resourceName,))
        return self.cursor.fetchone()

    def insertResourceToDB(self, userID, resourceName, resourceType, resourceContent, permissions):
        self.cursor.execute('INSERT INTO RESOURCE VALUES(NULL,?,?,?)',
                            (resourceName, resourceContent, resourceType))
        resourceID = self.cursor.lastrowid
        if resourceType == TYPE_FILE:
            permissions = permissions.replace(CREATE_PERMISSION, "")
        self.cursor.execute('INSERT INTO ACCESS_POLICY VALUES(NULL,?,?,?)', (userID, resourceID, permissions))
        self.dbConnection.commit()
        return resourceID