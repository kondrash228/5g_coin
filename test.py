from hashlib import sha256
 
x = 5
y = 0  # Мы еще не знаем, чему равен y... рил не знаем 100% не знаем
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
 
print(f'The solution is y = {y}')
