from os import path
from ConfigParser import ConfigParser
import json

class Dict:
    
    #CLASS VARIABLES
    size = -1
    flag=0
    date=''
    

    def __init__(self):
        self.idList = []
        self.dateList = []
        self.userList = []
        self.userLabel = ['UserName']
    

    def expdict(self, ndict):  # for listing access keys
        for ele in ndict.keys():
            if ele == 'CreateDate':
                Dict.date = ndict[ele].replace(tzinfo=None)
                self.dateList.append(Dict.date)
            if ele == 'AccessKeyId':
                self.idList.append(ndict[ele])
            if ele == 'AccessKeyMetadata':
                nlist = ndict[ele]
                self.explist(nlist)

    def explist(self, nlist):
        for item in nlist:  # for each iam user this loop will run
            self.expdict(item)


    def expdict2(self, ndict2, nkey2):  # for listing users
        for ele in ndict2.keys():
            if ele == nkey2:
                Dict.size += 1
                if Dict.size == len(self.userLabel):
                    Dict.size = 0
                    self.userList.append(ndict2[ele])
                    return
                nlist2 = ndict2[ele]
                self.explist2(nlist2, Dict.size)

    def explist2(self, nlist2, size):
        for item in nlist2:
            self.expdict2(item, self.userLabel[size])


    def expdict3(self, ndict3, profile):
        if Dict.flag == 1:
            Dict.flag = 0
            newid = ndict3['AccessKeyId']
            username=ndict3['UserName']
        for ele in ndict3.keys():
            if ele == 'AccessKey':
                Dict.flag = 1
                self.expdict3(ndict3[ele], profile)
            if ele == 'SecretAccessKey':
                newkey = ndict3[ele]

                person_dict={"Name" : [{username : [{"Access Id" : newid, "Secret Id" :newkey}]}]}
                person_json=json.dumps(person_dict, indent=4,sort_keys=True)
                
                file=open('userdet.json','a')
                file.write(person_json)
                file.write("\n")

                config = ConfigParser()
                config.read([path.join(path.expanduser("~"), '.aws/credentials')])

                preid = config.get(profile, 'aws_access_key_id')
                prekey = config.get(profile, 'aws_secret_access_key')

                print ("FOUND")

                # WRITING TO AWS CONFIG FILE
                if(preid == self.idList[0] or preid == self.idList[1]):
                    print("SAME USER - AWS CONFIG FILE UPDATED")

                    print("UPDATING")

                    awsconfigfile = open(path.join(path.expanduser("~"), '.aws/credentials'), 'r')
                    aws = awsconfigfile.read()
                    pf1 = aws.replace(preid, newid).replace(prekey, newkey)

                    awsconfigfile2 = open(path.join(path.expanduser("~"), '.aws/credentials'), 'w')
                    awsconfigfile2.write(pf1)


obj3=Dict()