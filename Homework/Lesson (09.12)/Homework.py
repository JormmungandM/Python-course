import sys


class Fraction: 
    def __init__(self,num:int=0,denum:int=1) -> None: 
        if(denum==0): 
            raise ValueError("Denominator cannot be 0")
        self.num = num 
        self.denum = denum 

    
    def __str__(self)->str: 
        return f"{self.num}/{self.denum}" 
    
    def print(self)->None: 
        print(self) 


def  main()-> None:
    try:
        value = Fraction()
        value.print()
        value = Fraction(3)
        value.print()
        value = Fraction(4,10)
        value.print()

    except ValueError:
        excep = sys.exc_info()[1]
        print(excep.args[0])    
   

if __name__ == "__main__" :
    main()