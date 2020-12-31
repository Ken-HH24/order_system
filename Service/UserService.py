from DAO.UserDao import UserRepository, login_user

userrep = UserRepository()


class UserService:
    @staticmethod
    def authentication(username, password):
        user = userrep.getUserByPassword(username, password)
        if user is None:
            return False
        else:
            login_user(user)
            return True

    def updateUsername(self, userid, newname):
        userrep.updateUsername(userid, newname)

    def updatePassword(self, userid, newpassword):
        userrep.updatePassword(userid, newpassword)

    def findRepeatedName(self, username):
        cnt = userrep.findRepeatedName(username)
        if cnt > 0:
            return False
        else:
            return True

    def insertUser(self, name, phone, username, password):
        userrep.insertUser(name, phone, username, password)