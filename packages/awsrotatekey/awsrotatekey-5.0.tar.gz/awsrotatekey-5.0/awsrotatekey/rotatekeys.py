from operations import *
from expdict import *
from includeexclude import *
from checkexpiry import *
import os
import boto3



class Rotate:
    
    
    def rotatekeys(self,file1,file2,profile):

        session=boto3.session.Session(profile_name=profile)

        file=open('userdet.json','w')
        file.close()
        
        validdays = raw_input("Enter no. of valid days: ")
        obj2.listuser(session)
        print obj3.userList
        print ("\n")
        for user in obj3.userList:
            print user
            rep1 = obj4.excludeuser(user, file1)
            rep2 = obj4.includeuser(user, file2)
            if rep1 == 1:
            	print ("USER IS BLACKLISTED")
                print("\n")
            	continue

            if rep2 == 1:
                print ("USER IS WHITELISTED")
                obj2.listkey(user, session)
                print("ORIGINAL KEYS ARE: ", obj3.idList)

                if len(obj3.idList)==0:
                    continue

                elif len(obj3.idList) == 1:
                    obj2.createkey(user,profile,session)
                    
                else:
                    rep3 = obj5.checkexpiry(user,validdays)
                    if rep3 == True:
                        obj2.rotatekey(user,profile,session)
                        #print("THE UPDATED KEYS ARE: ", obj3.idList)
                    else:
                        print("THE KEYS HAVE NOT EXPIRED")
                obj2.updateList(user, session)
                del obj3.idList[:]
                print ("\n")


obj=Rotate()

    
    