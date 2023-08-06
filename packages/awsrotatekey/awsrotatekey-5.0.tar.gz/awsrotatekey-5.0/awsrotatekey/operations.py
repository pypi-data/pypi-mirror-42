from expdict import *

import boto3

class Operations:
    

    def listuser(self,session):
        iam_client = session.client('iam')
        ndict2 = iam_client.list_users()
        obj3.expdict2(ndict2, 'Users')


    def createkey(self, user, profile, session):
        iam_client = session.client('iam')
        ndict3 = iam_client.create_access_key(UserName=user)
        del obj3.idList[:]
        self.listkey(user,session)
        print("A NEW KEY HAS BEEN ADDED")
        print("THE UPDATED KEYS ARE: ", obj3.idList)
        obj3.expdict3(ndict3, profile)


    def listkey(self, user, session):
        iam_client = session.client('iam')
        ndict = iam_client.list_access_keys(UserName=user)
        obj3.expdict(ndict)


    def deletekey(self, user, index, session):
        iam_client = session.client('iam')
        iam_client.delete_access_key(UserName=user, AccessKeyId=obj3.idList[index])


    def rotatekey(self, user, profile, session):
        if obj3.dateList[0] > obj3.dateList[1]:
            self.deletekey(user, 1,session)
            self.createkey(user,profile,session)
        else:
            self.deletekey(user, 0,session)
            self.createkey(user,profile,session)
        print("SUCCESS")


    def updateList(self, user, session):
        del obj3.idList[:]
        del obj3.dateList[:]
        self.listkey(user,session)
        
obj2=Operations()