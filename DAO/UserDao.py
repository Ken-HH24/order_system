from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
# from config import cursor, conn
import DAO.Database as Database

login_manager = LoginManager()


def start_transaction(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            self.conn, self.cursor = Database.getConnect()
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception:
            self.conn.rollback()  # 事务回滚
            return 'an Exception raised.'
        finally:
            Database.closeConnect(self.conn)
    return wrapper


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class UserRepository:
    def __init__(self):
        self.conn = None
        self.cursor = None

    @staticmethod
    def getUserById(userid):
        conn, cursor = Database.getConnect()
        sql = "SELECT userid, username, password FROM user WHERE userid = %s"
        cursor.execute(sql, userid)
        user = cursor.fetchone()
        Database.closeConnect(conn)
        if user is None:
            return None
        else:
            return User(user['userid'], user['username'], user['password'])

    @staticmethod
    def getUserByPassword(username, password):
        conn, cursor = Database.getConnect()
        sql = "SELECT userid, username, password FROM user WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()
        Database.closeConnect(conn)
        if user is None:
            return None
        else:
            return User(user['userid'], user['username'], user['password'])

    @start_transaction
    def updateUsername(self, userid, newname):
        sql = "UPDATE user SET username = %s WHERE userid = %s"
        self.cursor.execute(sql, (newname, userid))
        self.conn.commit()

    @start_transaction
    def updatePassword(self, userid, newpassword):
        sql = "UPDATE user SET password = %s WHERE userid = %s"
        self.cursor.execute(sql, (newpassword, userid))
        self.conn.commit()

    def findRepeatedName(self, username):
        conn, cursor = Database.getConnect()
        cursor.callproc("FIND_REPEATED", (username, 0))
        conn.commit()
        cursor.execute("SELECT @_FIND_REPEATED_1")
        cnt = cursor.fetchone()['@_FIND_REPEATED_1']
        Database.closeConnect(conn)
        return cnt

    @start_transaction
    def insertUser(self, name, phone, username, password):
        sql = "INSERT INTO user(name, phone, username, password) VALUES (%s,%s,%s,%s)"
        self.cursor.execute(sql, (name, phone, username, password))
        self.conn.commit()


@login_manager.user_loader
def load_user(user_id):
    return UserRepository.getUserById(user_id)
