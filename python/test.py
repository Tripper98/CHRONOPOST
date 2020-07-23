import os    

l=os.listdir('./python/data/')
li=[x.split('.')[0] for x in l]
print(li)