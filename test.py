import string
import random


def random_seril(count):
    
    all_char = string.ascii_letters + string.digits
    
    char_count= len(all_char)
    selil_list = []
     
    while count > 0: 
    
       random_num = random.randint(0 , char_count-1) 
       
       random_char = all_char[random_num]
       
       selil_list.append(random_char)
       
       count-=1
    print("".join(selil_list))


random_seril(30)    