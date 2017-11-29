from tkinter import *
from PIL import ImageTk, Image
import pymysql
from tkinter import messagebox
from tkinter import ttk, Canvas
from datetime import datetime, timedelta
import decimal
import hashlib
from hashlib import md5

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

    #=================================LOGIN WINDOW========================================
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

        #Image
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

    #password hashing
    def computeMD5hash(self, str):
        m = hashlib.md5()
        m.update((str.encode('utf-8')))
        c = m.hexdigest()
        return c


    def loginWindowLoginButtonClicked(self):
        # Click the button on Login Window:
        # Obtain the username and password from keypress;
        self.username = self.loginUsername.get()
        self.password = self.loginPassword.get()

        #compute password hashing
        self.password = self.computeMD5hash(self.password)


        # Error message for Username input empty
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        # Error message for password input empty
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        #Error message for username input doesn't exist in db
        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if not isUsername:
            messagebox.showwarning("Username doesn't exist", "The username you entered does not exist.")
            return False
        #Error message for username and password doesn't match with db
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM User WHERE (Username = %s AND Password = %s)", (self.username, self.password))
        if not usernameAndPasswordMatch:
            messagebox.showwarning("Username and password don\'t match",
                                   "Sorry, the username and password you entered"
                                   + " do not match.")
            return False

        self.cursor.execute("SELECT IsAdmin FROM User WHERE (username = %s AND password = %s)", (self.username, self.password))
        isAdmin = self.cursor.fetchone()[0]
        if (isAdmin == 0):
            self.loginWindow.withdraw()
            self.createPassengerFunctionalityWindow()
            self.buildPassengerFunctionalityWindow(self.passengerFunctionalityWindow)
        else:
            self.loginWindow.withdraw()
            self.createAdminFunctionalityWindow()
            self.buildAdminFunctionalityWindow(self.adminFunctionalityWindow)
        return True

    def loginWindowRegisterButtonClicked(self):
        # Click button on Login Window:
        # Invoke createNewUserRegistrationWindow; Invoke buildNewUserRegistrationWindow;
        # Hide Login Window; Set newUserRegistrationWindow on the top
        self.createNewUserRegistrationWindow()
        self.buildNewUserRegistrationWindow(self.newUserRegistrationWindow)

    #=============New User Registration Window==============

    def createNewUserRegistrationWindow(self):
        # Create blank newUserRegistrationWindow
        self.newUserRegistrationWindow = Tk()
        self.newUserRegistrationWindow.withdraw()
        self.newUserRegistrationWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.newUserRegistrationWindow.winfo_screenwidth() - self.newUserRegistrationWindow.winfo_reqwidth()) / 2
        y = (self.newUserRegistrationWindow.winfo_screenheight() - self.newUserRegistrationWindow.winfo_reqheight()) / 2
        self.newUserRegistrationWindow.geometry("+%d+%d" % (x, y))
        self.newUserRegistrationWindow.deiconify()
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


        var = IntVar()
        r1 = Radiobutton(newUserRegistrationWindow, text="Option 1", variable=var, value=1)
        r1.grid(row=6, column=1, sticky=W)
        breezebox = Label(newUserRegistrationWindow, text="Card Number")
        breezebox.grid(row=7, column=1, sticky=E)
        self.registrationCardNum = StringVar()
        breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        breezeboxEntry.grid(row=7, column=2, padx=1)
        r2 = Radiobutton(newUserRegistrationWindow, text="Option 2", variable=var, value=2)
        r2.grid(row=8, column=1, sticky=W)

        # Create Button
        registerButton = Button(newUserRegistrationWindow, text="Register", command=self.registrationWindowButtonClicked)
        registerButton.grid(row=8, column=4, sticky=E)

    def registrationWindowButtonClicked(self):
        #Clock the button on Register Window
        #Obtain username, Email Address, Password, confirm password from keypress
        self.username = self.registrationUsername.get()
        self.email = self.registrationEmailAddress.get()
        self.password = self.registrationPassword.get()
        self.confirmpassword = self.registrationConfirmPassword.get()

        #TODO: password hashing before input in the db
        # Error message for username input empty
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        #Error message for email input empty
        if not self.email:
            messagebox.showwarning("Email input is empty", "Please enter email.")
            return False
        #Error message for password input empty
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password.")
            return False

        #Error message for email not valid
        #Error message for username input already exist in db
        #Error message for email input already exist in db
        #Error message for password not matching confirmpassword
        
        #For clicking "Use my existing Breezecard"
        #Error message for Breezecard input empty
        #Error message for Breezecard input invalid (less than 16-digit)
        #Error message for Breezecard input not exist in db
        #1) If Breezecard input doesn't have user -> put it in Breezecard table (update)
        #2) If Breezecard input already have user -> delete from Breezecard table and put in Conflict table (suspend)

        #For clicking "Create a New Breezecard" - make random 16-digit that doesn't exist in db

    #=====================Passenger Functionality Window=======================
    def createPassengerFunctionalityWindow(self):
        self.passengerFunctionalityWindow = Tk()
        self.passengerFunctionalityWindow.title("Welcome to Marta")

        self.passengerFunctionalityWindow.withdraw()
        self.passengerFunctionalityWindow.update_idletasks()
        x = (self.passengerFunctionalityWindow.winfo_screenwidth() - self.passengerFunctionalityWindow.winfo_reqwidth()) / 2
        y = (self.passengerFunctionalityWindow.winfo_screenheight() - self.passengerFunctionalityWindow.winfo_reqheight()) / 2
        self.passengerFunctionalityWindow.geometry("+%d+%d" % (x, y))
        self.passengerFunctionalityWindow.deiconify()

    def buildPassengerFunctionalityWindow(self, passengerFunctionalityWindow):
        #Add components for passengerFunctionalityWindow

        #temporary label
        passengerLabel = Label(passengerFunctionalityWindow, text = "passenger")
        passengerLabel.grid(row=2, column=2, sticky=W)

    #=============Administrator Functionality Window========================
    def createAdminFunctionalityWindow(self):
        self.adminFunctionalityWindow = Tk()
        self.adminFunctionalityWindow.title("Administrator")

        self.adminFunctionalityWindow.withdraw()
        self.adminFunctionalityWindow.update_idletasks()
        x = (self.adminFunctionalityWindow.winfo_screenwidth() - self.adminFunctionalityWindow.winfo_reqwidth()) / 2
        y = (self.adminFunctionalityWindow.winfo_screenheight() - self.adminFunctionalityWindow.winfo_reqheight()) / 2
        self.adminFunctionalityWindow.geometry("+%d+%d" % (x, y))
        self.adminFunctionalityWindow.deiconify()

    def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
        #Add component for adminFunctionalityWindow

        #Station Management Button
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management")
        stationManagementButton.grid(row=1, column=3, sticky=W + E)

        #Suspend Cards Button
        suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
        suspendedCardButton.grid(row=3, column=3, sticky=W + E)

        #Breezecard Management Button
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management")
        breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")
        passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)


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