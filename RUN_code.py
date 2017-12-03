from tkinter import *
from PIL import ImageTk, Image
import pymysql
from tkinter import messagebox
from tkinter import ttk, Canvas
from datetime import datetime, timedelta
import decimal
import random

#MARTA v1.3
#By Team 54, CS4400 2017 Fall
class MARTA_Client:
    def __init__(self):
        # Invoke createLoginWindow; Invoke buildLoginWindow, Set loginWindow as mainloop
        #Connect to the database
        self.db = self.connect()
        self.cursor = self.db.cursor()
        # Login Window
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)
        self.loginWindow.mainloop()
        sys.exit()

    ##  =======Login Window=======
    def createLoginWindow(self):
        # Create blank Login Window
        self.loginWindow = Tk()
        self.loginWindow.title("MARTA v1.3.54.1")

        self.loginWindow.withdraw()
        self.loginWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.loginWindow.winfo_screenwidth() - self.loginWindow.winfo_reqwidth()) / 2
        y = (self.loginWindow.winfo_screenheight() - self.loginWindow.winfo_reqheight()) / 2
        self.loginWindow.geometry("+%d+%d" % (x, y))
        self.loginWindow.deiconify()

    def buildLoginWindow(self, loginWindow):
        # Add component for Login Window
        # Login Label
        loginLabel = Label(loginWindow, text="Login", font="Verdana 13 bold ")
        loginLabel.grid(row=1, column=3, sticky=W + E)

        # Username Label
        usernameLabel = Label(loginWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Password Label
        passwordLabel = Label(loginWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # # Image
        image = Image.open("MARTA-logo.jpg")
        image = image.resize((60, 60), Image.ANTIALIAS)
        buzzImage = ImageTk.PhotoImage(image)
        imageLabel = Label(loginWindow, image=buzzImage)
        imageLabel.image = buzzImage
        imageLabel.grid(row=2, column=4, rowspan=3, sticky=E)

        # Username Entry
        self.loginUsername = StringVar()
        usernameEntry = Entry(loginWindow, textvariable=self.loginUsername, width=20)
        usernameEntry.grid(row=2, column=3, sticky=W + E)

        # Password Entry
        self.loginPassword = StringVar()
        passwordEntry = Entry(loginWindow, textvariable=self.loginPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=3, sticky=W + E)

        # Login Buttons
        loginButton = Button(loginWindow, text="Login", command=self.loginWindowLoginButtonClicked)
        loginButton.grid(row=6, column=3)

        # Register Button

        registerButton = Button(loginWindow, text="Register", command=self.loginWindowRegisterButtonClicked)
        registerButton.grid(row=6, column=4, sticky=E)

    def loginWindowLoginButtonClicked(self):
        # Click the button on Login Window:
        # Obtain the username and password from keypress;
        # Invoke;
        # Invoke;
        # Withdraw Login Window;
        self.username = self.loginUsername.get()
        self.password = self.loginPassword.get()
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if not isUsername:
            messagebox.showwarning("Username is not an user\'s username",
                                   "The username you entered is not an user\'s username.")
            return False
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM User WHERE (Username = %s AND Password = %s)", (self.username, self.password))
        if not usernameAndPasswordMatch:
            messagebox.showwarning("Username and password don\'t match",
                                   "Sorry, the username and password you entered"
                                   + " do not match.")
            return False
        # to be modified
        isManagerName = self.cursor.execute("SELECT * FROM Manager WHERE Username = %s", (self.username))
        if isManagerName:
            self.loginWindow.withdraw()
            self.createChooseFunctionalityWindowManager()
            self.buildChooseFunctionalityWindowManager(self.chooseFunctionalityWindowManager)
        else:
            self.loginWindow.withdraw()
            self.createChooseFunctionalityWindow()
            self.buildChooseFunctionalityWindow(self.chooseFunctionalityWindow)
        return True

    def loginWindowRegisterButtonClicked(self):
        # Click button on Login Window:
        # Invoke createNewUserRegistrationWindow; Invoke buildNewUserRegistrationWindow;
        # Hide Login Window; Set newUserRegistrationWindow on the top
        self.createNewUserRegistrationWindow()
        self.buildNewUserRegistrationWindow(self.newUserRegistrationWindow)
        self.loginWindow.withdraw()

#======New User Registration Window==============

    def createNewUserRegistrationWindow(self):
        # Create blank newUserRegistrationWindow
        # self.newUserRegistrationWindow = Tk()
        # self.newUserRegistrationWindow.withdraw()
        # self.newUserRegistrationWindow.update_idletasks()  # Update "requested size" from geometry manager
        # x = (self.newUserRegistrationWindow.winfo_screenwidth() - self.newUserRegistrationWindow.winfo_reqwidth()) / 2
        # y = (self.newUserRegistrationWindow.winfo_screenheight() - self.newUserRegistrationWindow.winfo_reqheight()) / 2
        # self.newUserRegistrationWindow.geometry("+%d+%d" % (x, y))
        # self.newUserRegistrationWindow.deiconify()

        # Create blank newUserRegistrationWindow
        self.newUserRegistrationWindow = Toplevel()

        self.newUserRegistrationWindow.title("Create a MARTA Account")

    def buildNewUserRegistrationWindow(self,newUserRegistrationWindow):
        # Add components for newUserRegistrationWindow

        # Username Label
        usernameLabel = Label(newUserRegistrationWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Email Address Label
        emailAddressLabel = Label(newUserRegistrationWindow, text="Email Address")
        emailAddressLabel.grid(row=3, column=2, sticky=W)


        # Password Label
        passwordLabel = Label(newUserRegistrationWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # Confirm Password Label
        confirmPasswordLabel = Label(newUserRegistrationWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=5, column=2, sticky=W)

        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationUsername, width=25)
        usernameEntry.grid(row=2, column=3, padx=1)


        # Email Address Entry
        self.registrationEmailAddress = StringVar()
        emailAddressEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationEmailAddress,width=25)
        emailAddressEntry.grid(row=3, column=3, padx=1)

        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationPassword,show = '*',width=25)
        passwordEntry.grid(row=4, column=3, padx=1)

        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationConfirmPassword,show = '*',width=25)
        confirmPasswordEntry.grid(row=5, column=3, padx=1)


        self.var = IntVar()
        self.var.set(0)
        list_option = [
        ("Option 1", 0),
        ("Option 2", 1)
        ]
        for ops, num in list_option:
            if num == 0:
                r1 = Radiobutton(newUserRegistrationWindow, text=ops, variable=self.var, value=num, command=self.radioButtonChanging)
                r1.grid(row=6, column=1, sticky=W)
            if num == 1:
                r2 = Radiobutton(newUserRegistrationWindow, text=ops, variable=self.var, value=num, command=self.radioButtonChanging)
                r2.grid(row=8, column=1, sticky=W)
        # r1 = Radiobutton(newUserRegistrationWindow, text="Option 1", variable=self.var, value=0, command=self.radioButtonChanging(0))
        # r1.grid(row=6, column=1, sticky=W)
        breezebox = Label(newUserRegistrationWindow, text="Card Number")
        breezebox.grid(row=7, column=1, sticky=E)
        self.registrationCardNum = StringVar()
        # self.breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        # breezeboxEntry.grid(row=7, column=2, padx=1)
        # r2 = Radiobutton(newUserRegistrationWindow, text="Option 2", variable=self.var, value=1, command=self.radioButtonChanging(1))
        # r2.grid(row=8, column=1, sticky=W)
        self.breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)

        print ("inside func" + str(self.var.get()))
        if self.var.get() == 1:
            self.breezeboxEntry.config(state='disabled')
        # if self.var.get() == 0:
        #     print (self.var.get())
        #     breezeboxEntry = Entry(self.newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        #     # breezeboxEntry.grid(row=7, column=2, padx=1)
        # elif self.var.get() == 1:
        #     print (self.var.get())
        #     breezeboxEntry = Entry(self.newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20,state = 'disabled')

        self.breezeboxEntry.grid(row=7, column=2, padx=1)

        # Create Button
        button1 = Button(newUserRegistrationWindow, text="Register", command=self.newUserRegistrationWindowCreateButtonClicked)
        button1.grid(row=8, column=4, sticky=E)

    def radioButtonChanging(self):
        print ("You selected the option " + str(self.var.get()))
        # self.var.set(value)
        if self.var.get() == 0:
            print (str(self.var.get()) + "in if statement")
            # self.breezeboxEntry = Entry(self.newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
            # breezeboxEntry.grid(row=7, column=2, padx=1)
        elif self.var.get() == 1:
            print (str(self.var.get()) + "in elif statement")
            # self.breezeboxEntry = Entry(self.newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20,state = 'disabled')
            # disableBox(self.breezeboxEntry)
        return False

    def newUserRegistrationWindowCreateButtonClicked(self):
        # Click the Create Button on New User Registration Window:
        # Invoke createChooseFunctionalityWindow; Invoke buildChooseFunctionalityWindow;
        # Destroy New User Registration Window
        print(self.registrationUsername.get())
        self.username = self.registrationUsername.get()
        self.emailAddress = self.registrationEmailAddress.get()
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        self.newBreezeCardNum = self.registrationCardNum.get()
        self.isNewcard = self.var.get()
        print (self.isNewcard)
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not self.emailAddress:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password")
            return False
        if self.isNewcard == 0:
            if not len(newBreezeCardNum) == 16:
                messagebox.showwarning("Confirm Breezecard input is empty", "Please enter breezecard number")
            if not len
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
           messagebox.showwarning("This username has been used.",
                                  "Please input another username.")
           return False
        isEmail = self.cursor.execute("SELECT * FROM Passenger WHERE Email = %s", self.emailAddress)
        if isEmail:
           messagebox.showwarning("This E-mail address has been used.",
                                  "Please input another E-mail address.")
           return False

        if not (self.password == self.confirmPassword):
           messagebox.showwarning("Password does not match the confirm password.",
                                  "Please reconfirm the password.")
           return False

        if self.isNewcard:
            while True:
                nums = [x for x in range(16)]
                random.shuffle(nums)
                nums = str(nums)
                self.newBreezeCardNum = nums;
                isBreezeNum = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", self.newBreezeCardNum)
                print (newBreezeCardNum)
                if not isBreezeNum:
                    break


        messagebox.showinfo("info","Register successfully!")
        self.cursor.execute("INSERT INTO User VALUES (%s, %s, 0)", (self.username, self.password))


        self.cursor.execute("INSERT INTO Passenger VALUES (%s, %s)", (self.username, self.emailAddress))
        self.cursor.execute("INSERT INTO Breezecard VALUES (%s, 0, %s)", (self.newBreezeCardNum, self.username))

        self.createChooseFunctionalityWindow()
        self.buildChooseFunctionalityWindow(self.chooseFunctionalityWindow)
        self.newUserRegistrationWindow.destroy()


    # --------------------Database Connection-----------------
    def connect(self):
        try:
            #TODO: figure out the name of the database
            db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                 db='cs4400_Group_54', user='cs4400_Group_54', passwd='qUYP7usT')
            return db
        except:
            messagebox.showwarning('Error!', 'Cannot connect. Internet Connection Issue or DB not ready.')
            return False
a = MARTA_Client()
a.db.close()