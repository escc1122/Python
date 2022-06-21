def string_code():
    hello = 'Hello'
    world = 'world'
    hello_world = hello + ' ' + world
    print(hello_world)


def list_code():
    numbers = [10, 20, 30, 40]
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    aList = [10, 'Hello', 3.1415926]
    emptyList = list()
    emptyList = []
    nestedList = [10, 'Hello', 20.5, [30, 40]]
    print(len(numbers))


def dict_code():
    inventory = {'apple': 430, 'banana': 312, 'orange': 525}
    inventory = dict(apple=430, banana=312, orange=525)
    students = {20: '張三', 21: '李四', 22: '王五'}
    # 讀取項目，例如：
    numApples = inventory['apple']  # 利用方括號語法
    numApples = inventory.get('apple')  # 也可利用 .get() 方法
    numLemons = inventory['lemon']  # 使用方括號時，若找不到鍵值程式會當掉，KeyErrors: 'lemons'
    numLemons = inventory.get('lemon')  # 使用 .get() 方法時，若找不到鍵值程式不會當掉，會回覆 None
    # 加入或修改項目，例如：
    inventory['lemon'] = 100  # 利用方括號語法來新增項目或修改值
    inventory.update({'lemon': 100})  # 也可利用 .update() 方法
    inventory.update({'lemon': 100, 'watermelon': 50})  # 使用 .update() 方法時，可一次加入或修改多個項目
    # 刪除項目，例如：
    del inventory['banana']
    # 字典項目數量 (長度)
    numItems = len(inventory)


# https://selflearningsuccess.com/python-tuple/
# 不可改變
def tuple_code():
    number = 1, 2, 3
    print(number)
    number = 1,
    print(number)
    number = (1, 2, 3)
    print(number)
    number = (1,)
    print(number)

    score = ('A+')
    print("no ',' is str " + score)
    print(type(score))


def for_code():
    persons = ['張三', '李四', '王五', '趙六', '劉七', '孫八', '錢九', '畢十']
    for person in persons:
        print(f'Hi {person}，歡迎參加我星期六舉辦的派對')

    for i in range(10):
        print(i)

    for i in range(10, 0, -2):
        print(i)

    tel = {'jack': 4098, 'sape': 4139}
    for k, v in tel.items():
        print(k, v)
    for k in tel.keys():
        print(tel[k])
    for v in tel.values():
        print(v)

    # 一邊修改 copy()
    users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}
    # Strategy:  Iterate over a copy
    for user, status in users.copy().items():
        if status == 'inactive':
            del users[user]


def comprehension_code():
    list_comprehension = [i ** 2 for i in range(10) if i > 5]
    print(list_comprehension)

    persons = ['張三', '李四', '張三', '張三', '張三']
    set_comprehension = {i for i in persons if i == '張三'}
    print(set_comprehension)

    tel_dict = {'jack': 4098, 'sape': 4139}

    dictionary_comprehension = {k: v for k, v in tel_dict.items() if k == 'jack'}
    print(dictionary_comprehension)

    persons = ['張三', '李四']
    tels = [5555, 66666]
    dictionary_comprehension = {k: v for k, v in zip(persons, tels)}
    print(dictionary_comprehension)

    arr1 = [x * y for x in range(3) for y in range(4)]
    print(arr1)
    arr2 = [(x, y) for x in range(3) for y in range(4)]
    print(arr2)
    arr3 = [[x, y] for x in range(3) for y in range(4)]
    print(arr3)


def lambda_code():
    def make_incrementor(n):
        return lambda x: x + n

    f = make_incrementor(42)
    print(f(0))
    print(f(5))

    f = lambda x, y: x + y
    print(f(5, 12))

    filter_before = [x for x in range(0, 10)]
    print('filter before ', filter_before)
    filter_after = filter(lambda x: x > 5, filter_before)
    print('filter after ', list(filter_after))

    map_before = [x for x in range(0, 10)]
    print('map before ', map_before)
    map_after = map(lambda x: x ** 2, map_before)
    print('map after ', list(map_after))

    from functools import reduce
    reduce_before = [x for x in range(0, 10)]
    print('reduce before ', reduce_before)
    reduce_after = reduce(lambda x, y: x + y, reduce_before)
    print('reduce after ', reduce_after)

    sorted_before = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
    print('sorted_ before ', sorted_before)
    sorted_after = sorted(sorted_before, key=lambda pair: pair[1])
    print('sorted_ before ', sorted_after)

    sorted_before.sort(key=lambda pair: pair[1])
    print(sorted_before)


def slice_code():
    s_before = "abcdefg"

    print(s_before[0:len(s_before)])
    print(s_before[0:len(s_before):2])
    print(s_before[3:])
    print(s_before[:3])

    a_before = list(range(10))
    print(a_before[0:len(a_before)])
    print(a_before[0:len(a_before):2])
    print(a_before[3:])
    print(a_before[:3])


# https://docs.python.org/zh-tw/3/tutorial/controlflow.html#for-statements
def parameter_code():
    # *name =>  tuple , **name => dict
    def cheeseshop(kind, *arguments, **keywords):
        print("-- Do you have any", kind, "?")
        print("-- I'm sorry, we're all out of", kind)
        # tuple
        for arg in arguments:
            print(arg)
        print("-" * 40)
        # dict
        for kw in keywords:
            print(kw, ":", keywords[kw])

    cheeseshop("Limburger", "It's very runny, sir.",
               "It's really very, VERY runny, sir.",
               shopkeeper="Michael Palin",
               client="John Cleese",
               sketch="Cheese Shop Sketch")

    print('-' * 40)

    def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
        print("-- This parrot wouldn't", action, end=' ')
        print("if you put", voltage, "volts through it.")
        print("-- Lovely plumage, the", type)
        print("-- It's", state, "!")

    # test
    parrot(1000)  # 1 positional argument
    # parrot(voltage=1000)  # 1 keyword argument
    # parrot(voltage=1000000, action='VOOOOOM')  # 2 keyword arguments
    # parrot(action='VOOOOOM', voltage=1000000)  # 2 keyword arguments
    # parrot('a million', 'bereft of life', 'jump')  # 3 positional arguments
    # parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword


if __name__ == '__main__':
    # string_code()
    # for_code()
    # tuple_code()
    # comprehension_code()
    # lambda_code()
    # slice_code()
    parameter_code()
