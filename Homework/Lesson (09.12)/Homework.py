import sys


class Fraction: 
    def __init__( self, num: int = 0 , denum: int = 1 ) -> None: 
        if( denum == 0 ): 
            raise ValueError( "Denominator cannot be 0" )
        self.num = num 
        self.denum = denum 

    
    def __str__( self )->str: 
        return f"{ self.num } / { self.denum }" 
    
    def reduction( self ):
        temp = 0
        if(self.denum <= self.num):                 # получаем наименьшее делимое
            temp = range(self.denum + 1, 1, -1 )    # делаем на его основе диапазон, от большего к меньшему
        else:                                       
            temp = range(self.num + 1, 1 , -1 )
        for i in temp:
            if(self.num % i == 0 and self.denum % i == 0):      # если оба числа делится без остатка 
                self.num = int(self.num / i)                    # мы делим и преобразуем
                self.denum = int(self.denum / i)
                print(f"reduction: { self.num } / { self.denum }")  # показываем результат
                Fraction.reduction(self)                            # используем рекурсию для повторной проверки чисел. Если больше не получается делить, то работа метода заканчивается.



    def print(self)->None: 
        print(self) 


def  main()-> None:
    try:
        value = Fraction()
        value.print()
        value = Fraction(3)
        value.print()
        value = Fraction(56,36)
        value.print()
        value.reduction()

    except ValueError:
        excep = sys.exc_info()[1]
        print(excep.args[0])    
   

if __name__ == "__main__" :
    main()