import re
print(re.match(r'^\d{3}\-\d{3,8}$', '010-12345678'))

# test = '用户输入的字符串'
# if re.match(r'正则表达式', test):
#     print('ok')
# else:
#     print('failed')

a = 'a b   c'.split(' ')
print('a = ', a)

b = re.split(r'\s+', 'a b   c')
print('b = ', b)

c = re.split(r'[\s\,]+', 'a,b   c')
print('c = ', c)

d = re.split(r'[\s\,\;]+', 'a,b;c;;d  e')
print('d = ', d)

e = re.match(r'^(\d{3})\-(\d{3,8})$', '010-12345678')
print(e.group(0))
print(e.group(1))
print(e.group(2))

t = '19:05:30'
m = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
print(m.groups())


# someone@gmail.com
# bill.gates@microsoft.com
def is_valid_email(addr):
    return re.match(r'\w+\.?\w+@\w+\.com', addr)


# <Tom Paris> tom@voyager.org => Tom Paris
# bob@example.com => bob
def name_of_email(addr):
    return re.match(r'^\<?(\w+\s*\w+)\>?\s*\w*\@\w+\.\w+$', addr).group(1)
