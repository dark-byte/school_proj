import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="adrishmitra420",
    database="menu"
)

cur = mydb.cursor()


        
def main(bill):
    print('''
    
██████╗░░█████╗░██╗░░░██╗██╗███████╗███╗░░░███╗
██╔══██╗██╔══██╗╚██╗░██╔╝╚█║██╔════╝████╗░████║
██████╔╝███████║░╚████╔╝░░╚╝█████╗░░██╔████╔██║
██╔═══╝░██╔══██║░░╚██╔╝░░░░░██╔══╝░░██║╚██╔╝██║
██║░░░░░██║░░██║░░░██║░░░░░░███████╗██║░╚═╝░██║
╚═╝░░░░░╚═╝░░╚═╝░░░╚═╝░░░░░░╚══════╝╚═╝░░░░░╚═╝

    D I G I T A L       W A L L E T

    ''')

    while True:

        cmd = input("1.Sign in \n2.Create Account: ")
        if(cmd == '1'):
            id = input("\nEnter you ID: ")
            pswrd = input("Enter Password: ")
            login(id, pswrd, bill)
            break

        elif cmd == '2':
            while True:
                print("\nCREATE NEW ACCOUNT \n")
                fname = input("First Name: ")
                lname = input("Last Name: ")
                id = input("Enter ID: ")
                pswrd = input("Password: ")
                cpswrd = input("Confirm Password: ")

                #Checking if ID exists already:
                cur.execute('SELECT EXISTS (SELECT * from payem where id = %s)',(id,))
                is_id = cur.fetchall()

                if(not is_id):
                    print("\nID is taken\n")
                else:    
                    while True:
                        if(cpswrd == pswrd and fname and lname and id and pswrd):
                            amt = float(input("Innitial deposit (must be more than $20): "))
                            if(amt > 20):
                                createAcc(fname, lname, id, pswrd, amt, bill)
                                break
                            else: print("\nError!\n")
        else: print("\nERROR!\n")




def login(id, pswrd, bill):
    #Checking if Account Exists: 
    sql = 'SELECT EXISTS (SELECT * FROM payem WHERE ID = %s)'
    cur.execute(sql, (id,))
    res = cur.fetchall()
    if(res):
        cur.execute('SELECT password FROM payem WHERE ID = %s', (id,))
        x = cur.fetchall()[0][0]
        print(x, type(x))
        if(x == pswrd):
            print("\nLogin Succesfull! \n")
            pay(bill, id)
        else:
            print("\nPasswords don't match.\n")
            main(bill)
    else: 
        print("\nAccount doesn't exist. \n")
        main(bill)


def createAcc(fname, lname, id, pswrd, amt, bill):
    try:
        sql = 'INSERT INTO payem values (%s, %s, %s, %s, %s)'
        cur.execute(sql, (fname, lname, amt, id, pswrd, ))
        print("\nAccount created succesfully!\n")
        pay(bill, id)
    except:
        print("\nError! \n")
        main(bill)
    



def pay( amt, id):
    cur.execute("SELECT bal FROM payem WHERE id = %s", (id,))
    if(amt < cur.fetchall()[0][0]):
        try:
            sql = 'UPDATE payem SET bal = bal - %s WHERE id = %s'
            cur.execute(sql, (amt, id,))
            print("\nPayment Succesful. Thanks for using PAY'EM ! ")
            exit()
        except:
            print("\nUnknown error occured.\n")
            main(amt)

    else:
        print("Not enough balance in wallet.")
        while True:
            inp = input("1. Add money to wallet \n2. Quit program ")
            if inp =='1':
                add_amt = float(input("Add amount: "))
                cur.execute("UPDATE payem SET bal = bal + %s WHERE id = %s", (add_amt, id))
                pay(amt, id)
            elif inp =='2':
                exit()
            else:
                print("\nWrong Input!\n")

    mydb.commit()
