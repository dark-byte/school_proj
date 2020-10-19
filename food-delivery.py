import mysql.connector
import payem

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="adrishmitra420",
    database="menu"
)
cur = mydb.cursor()

cart = {}

def main():
    cmd = input('''
█▀▀ ▄▀█ ▀█▀ █▀▀ █▀▀ █▀█ █▀█ █ █▀▀ █▀  ▀
█▄▄ █▀█ ░█░ ██▄ █▄█ █▄█ █▀▄ █ ██▄ ▄█  ▄

1.Appetizers
2.Accompaniments
3.Indian style soup
4.Tandoori Delicacies
5.Dinner Specials
6.Chicken Specials
7.Biryani
8.Vegetables Specials
9.Tandoori Breads
10.Desserts and Beverages


Enter No 1-10 to browse categores.
Q to Quit the application >>>''')

    if(cmd.isdigit()):
        if 0 < int(cmd) < 11:
            getCat(int(cmd))

    elif cmd.lower() == 'q':
        exit()

    else:
        print('''
█░█░█ █▀█ █▀█ █▄░█ █▀▀   █ █▄░█ █▀█ █░█ ▀█▀
▀▄▀▄▀ █▀▄ █▄█ █░▀█ █▄█   █ █░▀█ █▀▀ █▄█ ░█░''')

        main()
    


def getCat(no):

    ids = []
    cats = ['Appetizers',
        'Accompaniments',
        'Indian Style Soup',
        'Tandoori Delicacies',
        'Dinner Specials for Two',
        'Chicken Specials',
        'Biryani',
        'Vegetable Specials',
        'Tandoori Breads',
        'Desserts & Beverages']

    cur_cat = (cats[no - 1],)
    sql = "SELECT item, des, price, id FROM table1 WHERE cat = (%s)"
    cur.execute(sql, cur_cat)
    res = cur.fetchall()

    print()
    index = 1
    for i in res:
        print(str(index)+ '. ' + i[0] + " " * (35-len(i[0]))+ i[1] + " " * (90-len(i[1])) + '$'+str(i[2]))
        ids.append(i[3])
        index +=1
    index = index -1
    print()

    while True:
        cmd = input(f"\nEnter B to go back to Categories \n1-{index} to add item to cart \nEnter P to go to proceed to Payment>>> ")
        if cmd.lower() == 'b':
            main()
        elif(cmd.lower() =='p'):
            payOut(cart)
            break
        elif cmd.isdigit():
            if int(cmd)<= index:
                quantity = int(input("Enter quantity: "))
                cart[ids[int(cmd) - 1]] = quantity
        else:
            print("Wrong Input")


def payOut(cart):
    prices  = []
    items = []
    ids = []
    bill = 0
    quantities = list(cart.values())

    for i in list(cart.keys()):
        ids.append((i,))
        cur.execute('SELECT item, price from table1 WHERE id = %s',(i,))
        data = cur.fetchall()[0]
        items.append(data[0])
        prices.append(data[1])
    print()
        
    for i in range(len(items)):
        bill += prices[i] * quantities[i]
        print(items[i] + ' - ' + str(prices[i]* quantities[i]))
    print("Grand Total = " +  str(bill) +'\n')
    
    pay_method = input("Pay Using - \n1. Cash On Delivery \n2. Pay'em - Online wallet >>> ")
    if(pay_method == '1'):
        print(f"""
▀█▀ █░█ ▄▀█ █▄░█ █▄▀ █▀   █▀▀ █▀█ █▀█   █░█ █▀ █ █▄░█ █▀▀   ▄▀█ █▄░█ █▄░█ ░ ░ ░ ░
░█░ █▀█ █▀█ █░▀█ █░█ ▄█   █▀░ █▄█ █▀▄   █▄█ ▄█ █ █░▀█ █▄█   █▀█ █░▀█ █░▀█ ▄ ▄ ▄ ▄

        Please keep ${bill} ready to pay on delivery.
        """)
    elif pay_method =='2':
        payem.main(bill)
    else:
        print("\nW R O N G    I N P U T !\n")


if __name__ == "__main__":
    print('''

    ░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗
    ░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝
    ░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░
    ░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░
    ░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗
    ░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

    ▄▀█ █▄░█ █▄░█ ▄▄ █▀▀ █▀█ █▀█ █▀▄   █▀▄ █▀▀ █░░ █ █░█ █▀▀ █▀█ █▄█
    █▀█ █░▀█ █░▀█ ░░ █▀░ █▄█ █▄█ █▄▀   █▄▀ ██▄ █▄▄ █ ▀▄▀ ██▄ █▀▄ ░█░


                        P R O J E C T   B Y -

            𝙰𝙳𝚁𝙸𝚂𝙷 𝙼𝙸𝚃𝚁𝙰   |   𝙰𝙱𝙷𝙸𝙽𝙰𝚅 𝙹𝙷𝙰   |   𝙰𝚁𝙹𝚄𝙽 𝚂𝙸𝙽𝙶𝙷
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''')
    main()