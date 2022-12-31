x = int(input("Enter x -> "))
while True :
    y = int(input("Enter y -> "))
    if y == x :
        print ("Error: x == y")
    elif y < 0 :
        print ("Error: y < 0") 
    else: 
        print ("Success: x != y and y < 0") 
        break
        
   
