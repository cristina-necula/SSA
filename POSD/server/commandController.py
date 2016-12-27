import databaseAccessControl

ERROR_PARSE_COMMAND = 'Error whlie trying to parse command. Please check function name and parameters'
ERROR_EXECUTE_COMMAND = 'Error whlie trying to execute command. Please check function name and parameters'

class CommandController(object):

    def __init__(self):
        self.functionsList = {'creareResursa' : self.creareResursa,
                              'readResursa' : self.readResursa,
                              'writeResource' : self.writeResursa,
                              'changeRights' : self.changeRights,
                              'createRole' : self.createRole,
                              'assignRole' : self.assignRole,
                              'addRights' : self.addRights,
                              'createPermission' : self.createPermission,
                              'addPermissionToRole' : self.addPermissionToRole,
                              'assignPermission' : self.assignPermission,
                              'createConstraint' : self.createConstraint,
                              'revokeRole' : self.revokeRole,
                              'createHierarchy': self.createHierarchy}

    def setDBAccessControl(self, dbAccessControl):
        self.dbAccessControl = dbAccessControl

    def creareResursa(self, username, password, resourceName, resourceType, content=None):
        return self.dbAccessControl.createResource(username, password, resourceName, resourceType, content)

    def readResursa(self, username, password, resourceName):
        return self.dbAccessControl.readResource(username, password, resourceName)

    def writeResursa(self, username, password, resourceName, content):
        return self.dbAccessControl.writeResource(username, password, resourceName, content)

    def changeRights(self, roleName, permissions):
        return self.dbAccessControl.changePermissionsForRole(roleName, permissions)

    def createRole(self, username, password, roleName):
        return self.dbAccessControl.createRole(username, password, roleName)

    def assignRole(self, username, password, user, role):
        return self.dbAccessControl.assignRoleToUser(username, password, user, role)

    def addRights(self, username, password, resourceName, roleName):
        return self.dbAccessControl.addACL(username, password, resourceName, roleName)

    def createConstraint(self, username, password, role1, role2):
        return self.dbAccessControl.createConstraint(username, password, role1, role2)

    def revokeRole(self, username, password, user, role):
        return self.dbAccessControl.revokeRole(username, password, user, role)

    def assignPermission(self, username, password, resource, permission):
        return self.dbAccessControl.assignPermission(username, password, resource, permission)

    def addPermissionToRole(self, username, password, role, permission):
        return self.dbAccessControl.addPermissionToRole(username, password, role, permission)

    def createPermission(self, username, password, name, rights):
        return self.dbAccessControl.createPermission(username, password, name, rights)

    def createHierarchy(self, username, password, role1, role2):
        return self.dbAccessControl.createHierarchy(username, password, role1, role2)

    def parseAndExecute(self, clientInput):
        try:
            command, parameters = clientInput.split("(")
            parameters = parameters.replace(")", "")
            parametersList = []
            for param in parameters.split(","):
                param = param.replace(" ", "")
                parametersList.append(param)
        except ValueError as e:
            return str(e)

        try:
            return self.functionsList[command](*parametersList)
        except (KeyError, TypeError):
            return 'Error in funtion signature. Please check again'