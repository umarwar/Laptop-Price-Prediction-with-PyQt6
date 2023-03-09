def checkPhone(string):
    flag = 1
    
    for characters in string:
        if characters >= '0' and characters <= '9':
            flag = 0 
        else:
            return False
    if len(string) == 11:
        if flag == 0:
            return True
    else:
        return False