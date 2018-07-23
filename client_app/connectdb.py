import MySQLdb

def connection():
    conn = MySQLdb.connect(host="surveillance.ciaezgtf2rvc.us-west-2.rds.amazonaws.com",
                           user = "surveillancess",
                           passwd = "rohith201",
                           db = "HOME_SURVEILLANCE",
                          cursorclass = MySQLdb.cursors.SSCursor)
    c = conn.cursor()

    return c, conn