import re

# Вхідні дані
x = """
Код до 
//BEGIN 
тимчасовий код 
//END 
код після"""
regex = "//BEGIN.*//END"
y = "[ЗАМІНЕНО]"

# Заміна першого фрагмента, який відповідає regex
result = re.sub(regex, y, x, count=1, flags=re.DOTALL)

# Виведення результату
print("Результат:", result)
