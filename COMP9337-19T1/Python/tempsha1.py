import hashlib


#initializing string 
str = "SHA1 Clear text"
  
result = hashlib.sha1(str.encode()) 
  
# printing the equivalent hexadecimal value. 
print("The hexadecimal equivalent of SHA1 is : ") 
print(result.hexdigest()) 
