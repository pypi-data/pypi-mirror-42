import datetime  # line:1
import json  # line:2
import uuid  # line:3
import requests  # line:4
from sqlalchemy import *  # line:5
from sqlalchemy.ext.declarative import *  # line:6
from sqlalchemy.orm import *  # line:7

engine = create_engine('sqlite:///.\data.db')  # line:9
Base = declarative_base()  # line:10
Session = sessionmaker(bind=engine)  # line:11
session = Session()  # line:12
path = "http://120.77.248.221:5678/"



class Software(Base):  # line:13
    import datetime  # line:14
    __tablename__ = 'software'  # line:15
    id = Column(Integer, primary_key=True)  # line:16
    key = Column(String(1024))  # line:17
    code = Column(String(1024))  # line:18
    mac = Column(String(1024))  # line:19
    date = Column(DateTime, default=datetime.datetime.now())  # line:20

class s:
    def __init__(self,key,secrets):
        self.key = key
        self.secrets = secrets

    def a(self):  # line:21
        Base.metadata.create_all(engine)  # line:22
        OO0OOO00O0OO0000O = session.query(Software).filter(Software.id == 1).all()  # line:23
        if not OO0OOO00O0OO0000O:  # line:24
            O000O00000OOO00O0 = Software(id=1, key=self.key, code=self.secrets,
                                         mac=uuid.UUID(int=uuid.getnode()).hex[-12:].upper())  # line:25
            session.add(O000O00000OOO00O0)  # line:26
            session.commit()  # line:27
            return  # line:28
        OO0OOO00O0OO0000O[0].code = self.secrets  # line:29
        OO0OOO00O0OO0000O[0].key = self.key  # line:30
        session.commit()  # line:31


    def c(self):  # line:32
        try:  # line:33
            OOOO000OOOO0O00OO = session.query(Software).filter(Software.id == 1).one()  # line:35
            OOOO000OOO000000O = OOOO000OOOO0O00OO.key  # line:36
            OOOOOOO0O0O0OOO0O = OOOO000OOOO0O00OO.code  # line:37
            OO0O00O0OOOO0OO0O = {'key': OOOO000OOO000000O, 'secrets': OOOOOOO0O0O0OOO0O}  # line:38
            OOOOO0OOO00OOO0O0 = path + 'verifySecrets'  # line:39
            O0OO0O0O000O00OOO = requests.post(url=OOOOO0OOO00OOO0O0, data=OO0O00O0OOOO0OO0O)  # line:40
            OOOOOOO0O0O000OOO = json.loads(O0OO0O0O000O00OOO.text)  # line:41
            if OOOOOOO0O0O000OOO["Status Code"] == 404:  # line:42
                print(OOOOOOO0O0O000OOO["des"])  # line:43
                exit()  # line:44
            if OOOOOOO0O0O000OOO["Status Code"] == 200:  # line:45
                O00OO00O0OO000OO0 = OOOOOOO0O0O000OOO["date"]  # line:46
                O0OOO000O00OOO000 = datetime.datetime.strptime(O00OO00O0OO000OO0, '%Y-%M-%d')  # line:47
                OOOO000OOOO0O00OO = session.query(Software).filter(Software.id == 1).all()  # line:48
                OOOO000OOOO0O00OO[0].code = OOOOOOO0O0O0OOO0O  # line:49
                OOOO000OOOO0O00OO[0].key = OOOO000OOO000000O  # line:50
                OOOO000OOOO0O00OO[0].date = O0OOO000O00OOO000  # line:51
                session.commit()  # line:52
                return  # line:53
        except:  # line:54

            print(
                """\u8f6f\u4ef6\u9047\u5230\u9519\u8bef\uff0c\u8bf7\u8054\u7cfb\uff1a:h916232476@gmail.com\nThe software encountered an error, please contact:h916232476@gmail.com""")
            exit()


    def b(self):  # line:57
        ""  # line:58
        try:  # line:59
            O00OO0O00O0O00000 = requests.get("http://123.125.115.110", timeout=2)  # line:60
        except:  # line:61
            print(
                u"""\u8bf7\u786e\u4fdd\u8ba1\u7b97\u673a\u8fde\u63a5\u4e92\u8054\u7f51\u540e\uff0c\u518d\u8fd0\u884c\u8f6f\u4ef6\uff01\nPlease make sure the computer is connected to the Internet before running the software!""")
            exit()  # line:63
        return True  # line:64


    def d(self):  # line:65
        ""  # line:66
        import datetime  # line:67
        OO00OO0OO0O0000OO = session.query(Software).filter(Software.key == self.key,
                                                           Software.code == self.secrets).first()  # line:68
        if OO00OO0OO0O0000OO:  # line:69
            OOOO00O0O0OO0O00O = OO00OO0OO0O0000OO.date  # line:70
            O0000OOO00OO0O000 = datetime.datetime.now()  # line:71
            O00O000O0OOO0OO0O = (
                                        O0000OOO00OO0O000.year * 365 + O0000OOO00OO0O000.month * 30 + O0000OOO00OO0O000.day) - (
                                        OOOO00O0O0OO0O00O.year * 365 + OOOO00O0O0OO0O00O.month * 30 + OOOO00O0O0OO0O00O.day)  # line:72
            if O00O000O0OOO0OO0O > 60:  # line:73
                print(
                    u"\u8f6f\u4ef6\u4f7f\u7528\u65f6\u95f4\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfbh916232476@gmail.com\u91cd\u65b0\u6fc0\u6d3b！")  # line:74
                exit()  # line:75
            return  # line:76
        return  # line:77
    def start(self):
        self.a()
        self.b()
        self.c()
        self.d()



