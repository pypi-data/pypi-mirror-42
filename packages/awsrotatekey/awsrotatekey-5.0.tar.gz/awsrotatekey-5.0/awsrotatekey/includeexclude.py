
class IE:
    
    def excludeuser(self, user, file1):
        if file1==None:
            return -1
            
       
        
        with open(file1,'r') as file:
            for exuser in file.readlines():
                exuser = exuser.strip()
                if user == exuser:
                    return 1
            return 0


   
    def includeuser(self, user, file2):
        if file2==None:
            return -1
        
        with open(file2,'r') as file:
            for inuser in file.readlines():
                inuser = inuser.strip()
                if user == inuser:
                    return 1
            return 0


obj4=IE()