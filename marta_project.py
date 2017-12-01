from tkinter import *
from PIL import ImageTk, Image
import pymysql
from tkinter import messagebox
from tkinter import ttk, Canvas
from datetime import datetime, timedelta
import decimal
import hashlib
from hashlib import md5
from random import *

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
        #self.newUserRegistrationWindow.mainloop()
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
        isUsername = self.cursor.execute("SELECT * FROM User WHERE username = %s", self.username)
        if not isUsername:
            messagebox.showwarning("Username doesn't exist", "The username you entered does not exist.")
            return False
        #Error message for username and password doesn't match with db
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM User WHERE (username = %s AND password = %s)", (self.username, self.password))
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
        #self.loginWindow.withdraw()

    #=============New User Registration Window==============

    def createNewUserRegistrationWindow(self):
        # Create blank newUserRegistrationWindow
        self.newUserRegistrationWindow = Toplevel()
        self.newUserRegistrationWindow.title("Create a MARTA Account")

    def buildNewUserRegistrationWindow(self,newUserRegistrationWindow):
        # Add components for newUserRegistrationWindow

        # Username Label
        usernameLabel = Label(newUserRegistrationWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W, columnspan=2)

        # Email Address Label
        emailAddressLabel = Label(newUserRegistrationWindow, text="Email Address")
        emailAddressLabel.grid(row=3, column=2, sticky=W, columnspan=2)


        # Password Label
        passwordLabel = Label(newUserRegistrationWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W, columnspan=2)

        # Confirm Password Label
        confirmPasswordLabel = Label(newUserRegistrationWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=5, column=2, sticky=W, columnspan=2)

        # Username Entry
        self.registrationUsername = StringVar()
        regusernameEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationUsername, width=25)
        regusernameEntry.grid(row=2, column=3, padx=1, columnspan=2)


        # Email Address Entry
        self.registrationEmailAddress = StringVar()
        regemailAddressEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationEmailAddress,width=25)
        regemailAddressEntry.grid(row=3, column=3, padx=1, columnspan=2)

        # Password Entry
        self.registrationPassword = StringVar()
        regpasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationPassword,show = '*',width=25)
        regpasswordEntry.grid(row=4, column=3, padx=1, columnspan=2)

        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        regconfirmPasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationConfirmPassword,show = '*',width=25)
        regconfirmPasswordEntry.grid(row=5, column=3, padx=1, columnspan=2)

        self.var = StringVar()
        r1 = Radiobutton(newUserRegistrationWindow, text="Enter Existing Breezecard", variable=self.var, value="exist")
        r1.grid(row=6, column=2, sticky=W, pady=(20, 0))
        breezebox = Label(newUserRegistrationWindow, text="Card Number")
        breezebox.grid(row=7, column=2, sticky=E)
        self.registrationCardNum = StringVar()
        breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        breezeboxEntry.grid(row=7, column=3, padx=1)

        r2 = Radiobutton(newUserRegistrationWindow, text="Create a new Breezecard", variable=self.var, value="new")
        r2.grid(row=8, column=2, sticky=W, pady = (30, 0))

        self.var.set("new")

        # Create Button
        newRegisterButton = Button(newUserRegistrationWindow, text="Create Account", command=self.newRegistrationWindowButtonClicked)
        newRegisterButton.grid(row=9, column=2, sticky=E+W, pady=(50, 10), columnspan=4, padx = 30)


    def newRegistrationWindowButtonClicked(self):
        #Clock the button on Register Window
        #Obtain username, Email Address, Password, confirm password from keypress
        self.regusername = self.registrationUsername.get()
        self.regemail = self.registrationEmailAddress.get()
        self.regpassword = self.registrationPassword.get()
        self.regconfirmpassword = self.registrationConfirmPassword.get()
        self.radiobuttonvalue = self.var.get()

        #TODO: password hashing before input in the db
        # Error message for username input empty
        if not self.regusername:
            messagebox.showwarning("Username input is empty", "Please enter registering username.")
            return False
        #Error message for email input empty
        if not self.regemail:
            messagebox.showwarning("Email input is empty", "Please enter registering email.")
            return False
        #Error message for password input empty
        if not self.regpassword:
            messagebox.showwarning("Password input is empty", "Please enter password.")
            return False

        #Error message for password not longer than 8 characters
        if (len(self.regpassword) < 8):
            messagebox.showwarning("Password input invalid", "Password has to be longer than 8 characters/numbers. \n (password is case sensitive)")
            return False

        #Error message for email not valid
        if not (re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.regemail)):
            messagebox.showwarning("Not a valid email", "Please enter valid E-mail address.")
            return False
        #Error message for username input already exist in db
        isUsername = self.cursor.execute("SELECT * FROM User WHERE username = %s", self.regusername)
        if isUsername:
            messagebox.showwarning("Username already exist", "The username you entered already exist. \n Try different username.")
            return False

        #Error message for email input already exist in db
        isEmail = self.cursor.execute("SELECT * FROM Passenger WHERE email = %s", self.regemail)
        if isEmail:
            messagebox.showwarning("Email already exist", "The email you entered already exist. \n Try different email.")
            return False

        #Error message for password not matching confirmpassword
        if (self.regpassword != self.regconfirmpassword):
            messagebox.showwarning("Password confirmation Error", "Password and Confirm password doesn't match.")
            return False
     
        #For clicking "Use my existing Breezecard"
        if (self.radiobuttonvalue == "exist"):
            self.existBreeze = self.registrationCardNum.get()
            #Error message for Breezecard input empty
            if not self.existBreeze:
                messagebox.showwarning("Exist card input is empty", "Please enter the existing Breezecard Number.")
                return False

            #Error message for Breezecard input invalid (less than 16-digit)
            if (len(self.existBreeze) != 16) and self.existBreeze.isdigit():
                messagebox.showwarning("Breezecard input invalid", "Breezecard number is invalid. \n Breezecard number must be 16-digit long.")
            else:
                #Error message for Breezecard input invalid (input contains other things than number)

                if (self.existBreeze.isdigit() == 0):
                    messagebox.showwarning("Breezecard input invalid", "Breezecard number must be 16-digit numbers. \n Your input contains something other than number.")
                    return False

                #Error message for Breezecard input not exist in db
                isBreezecard = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", self.existBreeze)
                if not isBreezecard:
                    messagebox.showwarning("Breezecard doesn't exist", "Breezecard you put in doesn't not exist in our system.")
                    return False

                self.cursor.execute("SELECT cUsername FROM Breezecard WHERE cardNum = %s", self.existBreeze)
                hasUser = self.cursor.fetchone()[0]
                #1) If Breezecard input doesn't have user -> put it in Breezecard table (update)
                if not hasUser:
                    self.hashpassword = self.computeMD5hash(self.regpassword)
                    self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
                    self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
                    self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s", (self.regusername, self.regpassword))
                    self.db.commit()
                    messagebox.showwarning("Registration Success", "You have successfully registered to MARTA system! Please log in.")
                    self.newUserRegistrationWindow.destroy()
                    return True
                #2) If Breezecard input already have user -> put Breezecard in conflict table and assign passenger with random card
                else:
                    randomBreeze = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
                    currentTime = datetime.now()
                    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
                    self.hashpassword = self.computeMD5hash(self.regpassword)
                    self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
                    self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
                    self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)", (randomBreeze, self.regusername))
                    self.cursor.execute("INSERT INTO Conflict(conUsername, conCardNum, dateTime) VALUES(%s, %s, %s)", (self.regusername, self.existBreeze, currentTime))

                    self.db.commit()
                    messagebox.showwarning("Registration Success", "Your account has been made but the card already has existing user. \n Please contact one of our representatives.")
                    self.newUserRegistrationWindow.destroy()
                    return True



        #For clicking "Create a New Breezecard" - make random 16-digit that doesn't exist in db
        if (self.radiobuttonvalue == "new"):
            self.newBreeze = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
            self.hashpassword = self.computeMD5hash(self.regpassword)
            self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
            self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
            self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)", (self.newBreeze, self.regusername))
            self.db.commit()
            messagebox.showwarning("Registration Sucess", "You have successfully registered to MARTA system! Please log in.")
            self.newUserRegistrationWindow.destroy()
            return True

    #=====================Passenger Functionality Window=======================
    def createPassengerFunctionalityWindow(self):
        self.passengerFunctionalityWindow = Toplevel()
        self.passengerFunctionalityWindow.title("Welcome to Marta")

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.loginWindow.destroy()

        self.passengerFunctionalityWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildPassengerFunctionalityWindow(self, passengerFunctionalityWindow):
        self.passusername = self.loginUsername.get()
        self.cursor.execute("SELECT cardNum FROM Breezecard WHERE cUsername = %s", self.passusername)
        myCards = self.cursor.fetchall()
        self.listmyCards = []
        for card in myCards:
            self.listmyCards.append(card[0])

        #Welcome user label
        welcomeLabel = Label(passengerFunctionalityWindow, text= ("Welcome, " + self.passusername))
        welcomeLabel.grid(row=1, column=5, sticky=E)

        #Breezecard Label
        breezecardLabel = Label(passengerFunctionalityWindow, text="Breezecard: ")
        breezecardLabel.grid(row=2, column=1, sticky=W)

        #Balance Label
        balanceLabel = Label(passengerFunctionalityWindow, text="Balance: ")
        balanceLabel.grid(row=3, column=1, sticky=W)

        #Balance Showing Label
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", self.listmyCards[0])
        balance = self.cursor.fetchone()[0]

        self.balanceVar = StringVar()
        self.balanceVar.set("$ " + str(balance))

        self.balanceShowLabel = Label(passengerFunctionalityWindow, textvariable=self.balanceVar)
        self.balanceShowLabel.grid(row=3, column=2, sticky=W)

        #Breezecard Dropdown Menu
        self.breezecardDropVar = StringVar(passengerFunctionalityWindow)
        self.breezecardDropVar.set(self.listmyCards[0])

        self.breezecardDropDown = OptionMenu(passengerFunctionalityWindow, self.breezecardDropVar, *self.listmyCards, command = self.displayBalance)
        self.breezecardDropDown.grid(row=2, column=2, sticky=W)

        #Manage Cards Button
        manageCardButton = Button(passengerFunctionalityWindow, text="Manage Cards", command=self.passengerManageCardButtonClicked)
        manageCardButton.grid(row=2, column=3, sticky=W+E)

        #Create View Trip History Button
        viewTripHistoryButton = Button(passengerFunctionalityWindow, text="View Trip History", command=self.passengerFunctionalityWindowViewTripHistoryButtonClicked)
        viewTripHistoryButton.grid(row=8, column=1, sticky=W)

        #Log Out Button
        logOutButton = Button(passengerFunctionalityWindow, text="Log Out", command=self.passengerFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=8, column=5, sticky=E)

        #======================================================Start and End Trip=================================================
        #Starts At Label
        startsAtLabel = Label(passengerFunctionalityWindow, text="Starting at: ")
        startsAtLabel.grid(row=4, column=1, sticky=W)

        #Starts At and Ends At Dropdown Menu
        self.cursor.execute("SELECT * FROM Station")
        stations = self.cursor.fetchall()
        self.liststations = []
        self.busstations = []
        self.trainstations = []
        self.dictionarystations = {}
        #index: 0-stopID, 1-name, 2-IsTrain, 3-fare, 4-closedStatus
        for station in stations:
            station_name = station[1]
            if (station[2] == 0):
                station_name = station_name + "(Bus station)"
                station_name = station_name + " - $" + "{0:.2f}".format(station[3])
                self.busstations.append(station_name)
                self.liststations.append(station_name)
            else:
                station_name = station_name + " - $" + "{0:.2f}".format(station[3])
                self.trainstations.append(station_name)
                self.liststations.append(station_name)
            self.dictionarystations[station_name] = station[0]

        self.dictionaryEndStations = {}
        for station in self.liststations:
            if "(Bus station)" in station:
                self.dictionaryEndStations[station] = self.busstations
            else:
                self.dictionaryEndStations[station] = self.trainstations

        self.startsAtDropVar = StringVar(passengerFunctionalityWindow)
        self.endsAtDropVar = StringVar(passengerFunctionalityWindow)

        self.startsAtDropVar.trace("w", self.update_options)

        self.startsAtDropDown = OptionMenu(passengerFunctionalityWindow, self.startsAtDropVar,*self.liststations)
        self.startsAtDropDown.grid(row=4, column=2, sticky=W)

        self.endsAtDropDown = OptionMenu(passengerFunctionalityWindow, self.endsAtDropVar, "")
        self.endsAtDropDown.grid(row=5, column=2, sticky=W)

        self.startsAtDropVar.set(self.liststations[0])

        #Starts At Button
        self.startAtButton = Button(passengerFunctionalityWindow, text="Start Trip", state=NORMAL, command=self.toggle_startbutton)
        self.startAtButton.grid(row=4, column=3, sticky=W+E)

        #Ending At Label
        endingAtLabel = Label(passengerFunctionalityWindow, text="Ending at: ")
        endingAtLabel.grid(row=5, column=1, sticky=W)

        #Ends At Button
        self.endsAtButton = Button(passengerFunctionalityWindow, text="End Trip", command=self.toggle_endbutton)
        self.endsAtButton.grid(row=5, column=3, sticky=W+E)

        ##MANAGE CARDS LINK
        ##END TRIP LINK
    def displayBalance(self, cardNum):
        #DisplayBalance depends on Dropdown menu
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", cardNum)
        balance = self.cursor.fetchone()[0]
        self.balanceVar.set("$ " + str(balance))

    def update_options(self, *args):
        updatedEndList = self.dictionaryEndStations[self.startsAtDropVar.get()]
        self.endsAtDropVar.set(updatedEndList[0])

        menu = self.endsAtDropDown['menu']
        menu.delete(0, 'end')
        for updatedEnd in updatedEndList:
            menu.add_command(label=updatedEnd, command=lambda endingstation=updatedEnd: self.endsAtDropVar.set(endingstation))       

    def toggle_startbutton(self):
        #Press Start Trip
        startID = self.dictionarystations[self.startsAtDropVar.get()]
        breezecardUsed =self.breezecardDropVar.get()

        self.cursor.execute("SELECT IsTrain FROM Station WHERE (fare < (SELECT value FROM Breezecard WHERE cardNum = %s)) AND (stopID = %s)", (breezecardUsed, startID))
        constraintStation = self.cursor.fetchone()
        #Error: Buzzcard doesn't have enough balance
        if not constraintStation:
            messagebox.showwarning("Cannot start trip", "You don't have enough balance on your Breezecard.")
            return False

        #Error: Buzzcard is suspended
        self.cursor.execute("SELECT * FROM Conflict WHERE conCardNum = %s", breezecardUsed)
        constraintBuzzcard = self.cursor.fetchall()
        if constraintBuzzcard:
            messagebox.showwarning("Cannot start trip", "Your buzzcard is suspended. \n Please call/email one of our representatives.")
            return False

        #Error: passenger already is in trip
        for checker in self.listmyCards:
            self.cursor.execute("SELECT startID, endID FROM Trip WHERE bcNum = %s", checker)
            ended = self.cursor.fetchall()
            for end in ended:
                if not end[1]:
                    self.inverse_dictionary = {v: k for k, v in self.dictionarystations.items()}
                    myTripOrigin = self.inverse_dictionary[end[0]]
                    self.startsAtDropVar.set(myTripOrigin)
                    self.startsAtDropDown.config(state=DISABLED)

                    self.startAtButton.config(text="In Progress")
                    self.startAtButton.config(state=DISABLED)
                    messagebox.showwarning("Cannot start trip", "You are already in trip. Please end the trip before starting another.")
                    return False

        #Start Trip
        currentTime = datetime.now()
        currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", breezecardUsed)
        ValueNow = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT fare FROM Station WHERE stopID = %s", startID)
        FareStart = self.cursor.fetchone()[0]
        ValueEnd = ValueNow - FareStart

        self.startAtButton.config(text="In Progress")
        self.startAtButton.config(state=DISABLED)
        self.startsAtDropDown.config(state=DISABLED)

        self.cursor.execute("INSERT INTO Trip(bcNum, startTime, currentFare, startID, endID) VALUES(%s, %s, %s, %s, NULL)",
            (breezecardUsed, currentTime, FareStart, startID))
        self.cursor.execute("UPDATE Breezecard SET value = %s WHERE cardNum = %s", (ValueEnd, breezecardUsed))
        self.db.commit()
        messagebox.showwarning("Trip Success", "You are now in trip!")
        self.displayBalance(breezecardUsed)
        return True

    def toggle_endbutton(self):
        #Press End Trip
        #cards = self.listmyCards
        willendID = self.dictionarystations[self.endsAtDropVar.get()]
        #startID = self.dictionarystations[self.startsAtDropVar.get()]
        #print(cards, willendID, startID)

        self.cursor.execute("SELECT * FROM Trip WHERE (endID IS NULL) AND (bcNum IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", self.passusername)
        notendedTrip = self.cursor.fetchall()
        if not notendedTrip:
            messagebox.showwarning("All trips ended", "You are not in trip right now.")
            return False
        else:
            self.startAtButton.config(text="Start Trip")
            self.startAtButton.config(state=NORMAL)
            self.startsAtDropDown.config(state=NORMAL)
            self.cursor.execute("UPDATE Trip SET endID = %s WHERE (endID IS NULL) AND (bcNum IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", (willendID, self.passusername))
            self.db.commit()
            messagebox.showwarning("Trip Success", "You have arrived to your destiny. \n Thank you for using MARTA")
            return True      

    ##===========================================Passenger Functionality - Manage Cards==================================================
    def passengerManageCardButtonClicked(self):
        # Click button on passnger functionality Window:
        # Invoke createNewManageCardsWindow; Invoke buildNewManageCardsWindow;

        self.createManageCardsWindow()
        self.buildManageCardsWindow(self.manageCardsWindow)
        #self.passengerFunctionalityWindow.withdraw()

    def createManageCardsWindow(self):
        self.manageCardsWindow = Toplevel()
        self.manageCardsWindow.title("Manage Cards")

        def on_closing():
            self.manageCardsWindow.withdraw()
            self.passengerFunctionalityWindow.withdraw()
            self.createPassengerFunctionalityWindow()
            self.buildPassengerFunctionalityWindow(self.passengerFunctionalityWindow)

        self.manageCardsWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildManageCardsWindow(self, manageCardsWindow):
        self.manageCardsTree = ttk.Treeview(manageCardsWindow, column=("cardNum", "value"))
        self.manageCardsTree['show'] = 'headings'

        self.manageCardsTree.column("cardNum", width=150, anchor="center")
        self.manageCardsTree.column("value", width=150, anchor="center")

        self.manageCardsTree.heading("cardNum", text="Card #")
        self.manageCardsTree.heading("value", text="Value")

        self.cursor.execute("SELECT cardNum, value FROM Breezecard WHERE cUsername = %s", self.passusername)
        self.manageCardsTuple = self.cursor.fetchall()
        self.manageCardNum = []
        self.manageCardValue = []
        self.manageCardsTreeIndex = 0
        for entry in self.manageCardsTuple:
            self.manageCardNum.append(entry[0])
            self.manageCardValue.append(entry[1])
            self.manageCardsTree.insert('', self.manageCardsTreeIndex, values=entry)
            self.manageCardsTreeIndex+=1

        #Breezecard Title Label
        breezecardsLabel = Label(manageCardsWindow, text="Breeze Cards", font="Verdana 13 bold ")
        breezecardsLabel.grid(row=0, column=1, sticky= W+E)

        #Table
        self.selectedBreezecard = StringVar()
        self.selectedBreezecard.set("")

        self.manageCardsTree.grid(row=1, column=0, rowspan=8, padx = 20, pady = (10,10))
        self.manageCardsTree.bind("<ButtonRelease-1>", self.selectItem)

        #Adding Breezecard Entry
        self.entryBreezeCard = StringVar()
        breezecardEntry = Entry(manageCardsWindow, textvariable=self.entryBreezeCard, width=20)
        breezecardEntry.grid(row=1, column=1, sticky=W)

        #Breezecard Adding Button
        addCardButton = Button(manageCardsWindow, text="Add Card", command=self.manageCardsWindowAddCardButtonClicked)
        addCardButton.grid(row=1, column=2, sticky=W)

        #Add Value to Selected Card
        self.addValueToSelectedCardLabel = Label(manageCardsWindow, text="Selected Card: ")
        self.addValueToSelectedCardLabel.grid(row=2, column=1, sticky=W+E)

        #Add Selected Card Label
        self.selectedCardLabel = Label(manageCardsWindow, textvariable=self.selectedBreezecard, fg="blue")
        self.selectedCardLabel.grid(row=2, column=2, sticky=W)

        removeButton = Button(manageCardsWindow, text="Remove Selected Card", padx = 20, command=self.removeSelectedCardClicked)
        removeButton.grid(row=3, column=2, sticky=E)

        #Credit Card Label
        self.creditcardLabel = Label(manageCardsWindow, text="Credit Card #: ")
        self.creditcardLabel.grid(row=5, column=1, sticky=W)

        #Credit card Entry
        self.entryCreditCard = StringVar()
        self.creditcardEntry = Entry(manageCardsWindow, textvariable=self.entryCreditCard, width=20)
        self.creditcardEntry.grid(row=5, column=2, sticky=W)

        #Value Label
        self.valueLabel = Label(manageCardsWindow, text="Value: ")
        self.valueLabel.grid(row=6, column=1, sticky=W)

        #Value Entry
        self.entryValue = StringVar()
        self.valueEntry = Entry(manageCardsWindow, textvariable=self.entryValue, width=20)
        self.valueEntry.grid(row=6, column=2, sticky=W)

        #Add Value Button
        self.addValueButton = Button(manageCardsWindow, text="Add Value to Selected Card", command=self.manageCardsWindowAddValueButtonClicked)
        self.addValueButton.grid(row=7, column=2, sticky=W+E)


####IMPLEMENT REMOVE CARD

    def selectItem(self, event):
        # for selection debugging
        selectedItem = self.manageCardsTree.focus()
        selectedItem = list(self.manageCardsTree.item(selectedItem)['values'])[0]
        selectedItem = str(selectedItem)
        if (len(selectedItem) != 16):
            selectedItem = "0" + selectedItem
        self.selectedBreezecard.set(selectedItem)
        # print("selection: ", self.suspendedCardsTree.selection())

    def manageCardsWindowAddCardButtonClicked(self):
        # Click the Add Card Button on Manage Cards Window:
        entryBreezecard = self.entryBreezeCard.get()
        #self.passusername - user

        #Error if entry is empty
        if not entryBreezecard:
            messagebox.showwarning("Breezecard input is empty", "Please enter Breezecard.")
            return False

        #Error if entry is invalid (not 16-digit)
        if (len(entryBreezecard) != 16):
            messagebox.showwarning("Breezecard input invalid", "Breezecard has to be 16-digit number")
            return False

        #Error if entry is invalid (16 digit with something other than number)
        if (entryBreezecard.isdigit() == 0):
            messagebox.showwarning("Breezecard input invalid", "Breezecard number must be 16-digit numbers. \n Your input contains something other than number.")
            return False

        #1) Breezecard doesn't exist in database -> insert into database with value 0.00
        hasBreeze = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", entryBreezecard)
        if not hasBreeze:
            self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES (%s, 0.00, %s)", (entryBreezecard, self.passusername))
            self.db.commit()
            messagebox.showwarning("Add Card Success", "You have successfully added Breezecard to the system.")
            self.buildManageCardsWindow(self.manageCardsWindow)
            return True

        self.cursor.execute("SELECT cUsername FROM Breezecard WHERE cardNUm = %s", entryBreezecard)
        hasUser = self.cursor.fetchone()[0]
        #2) Breezecard exist in database without user -> update to current user
        if not hasUser:
            self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s", (self.passusername, entryBreezecard))
            self.db.commit()
            messagebox.showwarning("Add Card Success", "You have successfully added Breezecard to the system.")
            self.buildManageCardsWindow(self.manageCardsWindow)
            return True

        #3) Breezecard exist in database with user -> update to current user
        else:
            currentTime = datetime.now()
            currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO Conflict(conUsername, conCardNum, dateTime) VALUES (%s, %s, %s)", (self.passusername, entryBreezecard, currentTime))
            self.db.commit()
            messagebox.showwarning("Add Card Failed", "This Breezecard already has a user. \n Please contact one of our representatives.")
            return False

    def removeSelectedCardClicked(self):
        selectedBreezecard = self.selectedBreezecard.get()
        #Error if not selected
        if not selectedBreezecard:
            messagebox.showwarning("No Selected Breezecard", "Please select a Breezecard you want to remove.")
            return False

        self.cursor.execute("SELECT COUNT(*) FROM Breezecard WHERE cUsername = %s", self.passusername)
        numHaveBreezecard = self.cursor.fetchone()[0]
        randomBreezecard = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
        if (numHaveBreezecard <= 1):
            messagebox.showwarning("Remove Card Fail", "You have to have at least one Breezecard in your account.")
            return False
        else:
            self.cursor.execute("UPDATE Breezecard SET cUsername = NULL WHERE cardNum = %s", selectedBreezecard)
            self.db.commit()
            messagebox.showwarning("Remove Card Success", "You have successfully added Breezecard from the system.")
            self.buildManageCardsWindow(self.manageCardsWindow)
            return True

    def manageCardsWindowAddValueButtonClicked(self):
        # Click the Add Value Button on Manage Cards Window:
        breezecard_selected = self.selectedBreezecard.get()
        entryCreditCard = self.entryCreditCard.get()
        entryValue = self.entryValue.get()

        #Error: entryCreditCard empty
        if not entryCreditCard:
            messagebox.showwarning("Credit Card Input Empty", "Please input your credit card information.")
            return False
        #Error: entryValue empty
        if not entryValue:
            messagebox.showwarning("Value Input Empty", "Please input amount of value you want to put in your Breezecard")
            return False
        #Error: breezecard not selected
        if not breezecard_selected:
            messagebox.showwarning("No Selected Breezecard", "Please select a Breezecard you want to remove.")
            return False
        #Error: entryCreditCard not 16 digits long
        if (len(entryCreditCard) != 16):
            messagebox.showwarning("Invalid Credit Card", "The Credit Card is invalid. \nCredit Card input should be 16-digit number.")
            return False
        #Error: entryCreditCard not digit
        if (entryCreditCard.isdigit() == 0):
            messagebox.showwarning("Invalid Credit Card", "The Credit Card is invalid. \nCredit Card input should be 16-digit number.")
            return False
        #Error: entryValue not digit
        if (entryValue.isdigit() == 0):
            messagebox.showwarning("Invalid Value", "The value should be a number.")
            return False

        #Error: currentValue + newValue = 1000 (value exceeded)
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", breezecard_selected)
        card_amount = self.cursor.fetchone()[0]
        if (float(card_amount) + float(entryValue) >= 1000.00):
            messagebox.showwarning("Too Much Value Input", "Breezecard cannot hold value more than $1000.00.")
            return False

        #Add Value to the Card and update the page
        final_value = float(card_amount) + float(entryValue)
        final_value = "{0:.2f}".format(final_value)
        self.cursor.execute("UPDATE Breezecard SET value = %s WHERE cardNum = %s", (final_value, breezecard_selected))
        self.db.commit()
        messagebox.showwarning("Add Value Success", "You have successfully added value to your selected Breezecard.")
        self.buildManageCardsWindow(self.manageCardsWindow)
        return True

    #=======================================Passenger View Trip History========================================
    def passengerFunctionalityWindowViewTripHistoryButtonClicked(self):
        #Click button on passenger functionality Window
        #Invoke createViewTripHistoryWindow; Invoke buildViewTripHistoryWindow;

        self.createViewTripHistoryWindow()
        self.buildViewTripHistoryWindow(self.viewTripHistoryWindow)
        #self.viewTripHistoryWindow.withdraw()

    def createViewTripHistoryWindow(self):
        self.viewTripHistoryWindow = Toplevel()
        self.viewTripHistoryWindow.title("Trip History")

    def buildViewTripHistoryWindow(self, viewTripHistoryWindow):
        #self.passusername -> user

        startTimeLabel = Label(viewTripHistoryWindow, text="Start Time: ")
        startTimeLabel.grid(row=1, column=1, sticky=W)

        self.entryStartTime = StringVar()
        startTimeEntry =Entry(viewTripHistoryWindow, textvariable=self.entryStartTime, width=40)
        startTimeEntry.grid(row=1, column=2, sticky=W)

        endTimeLabel = Label(viewTripHistoryWindow, text="End Time: ")
        endTimeLabel.grid(row=2, column=1, sticky=W)

        self.entryEndTime = StringVar()
        endTimeEntry = Entry(viewTripHistoryWindow, textvariable=self.entryEndTime, width=40)
        endTimeEntry.grid(row=2, column=2, sticky=W)

        updateButton = Button(viewTripHistoryWindow, text="Update", command=self.viewTripHistoryUpdateClicked)
        updateButton.grid(row=2, column=3, sticky=W)

        resetButton = Button(viewTripHistoryWindow, text="Reset", command=self.viewTripHistoryResetClicked)
        resetButton.grid(row=2, column=4, sticky=W)

        self.viewTripHistoryTree = ttk.Treeview(viewTripHistoryWindow, column=("startTime", "startStation", "endStation", "fare", "cardNum"))
        self.viewTripHistoryTree['show'] = 'headings'

        self.viewTripHistoryTree.column("startTime", width=150, anchor="center")
        self.viewTripHistoryTree.column("startStation", width=200, anchor="center")
        self.viewTripHistoryTree.column("endStation", width=200, anchor="center")
        self.viewTripHistoryTree.column("fare", width=100, anchor="center")
        self.viewTripHistoryTree.column("cardNum", width=150, anchor="center")

        self.viewTripHistoryTree.heading("startTime", text="Time")
        self.viewTripHistoryTree.heading("startStation", text="Departure")
        self.viewTripHistoryTree.heading("endStation", text="Arrival")
        self.viewTripHistoryTree.heading("fare", text="Fare Paid")
        self.viewTripHistoryTree.heading("cardNum", text="Card #")

        self.cursor.execute("SELECT startTime, startID, endID, currentFare, bcNum FROM Trip WHERE bcNUM IN ("
            "SELECT cardNum FROM Breezecard WHERE cUsername = %s)", self.passusername)
        self.viewTripHistoryTuple = self.cursor.fetchall()
        self.viewTripHistoryStartTime = []
        self.viewTripHistoryStartStation = []
        self.viewTripHistoryEndStation = []
        self.viewTripHistoryFare = []
        self.viewTripHistoryCardNum = []
        self.viewTripHistoryTreeIndex = 0
        for entry in self.viewTripHistoryTuple:
            self.cursor.execute("SELECT name FROM Station WHERE stopID = %s", entry[1])
            startName = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT name FROM Station WHERE stopID = %s", entry[2])
            endName = self.cursor.fetchone()[0]
            self.viewTripHistoryStartTime.append(entry[0])
            self.viewTripHistoryStartStation.append(entry[1])
            self.viewTripHistoryEndStation.append(entry[2])
            self.viewTripHistoryFare.append(entry[3])
            self.viewTripHistoryCardNum.append(entry[4])
            self.viewTripHistoryTree.insert('', self.viewTripHistoryTreeIndex, values=(entry[0], startName, endName, entry[3], entry[4]))
            self.viewTripHistoryTreeIndex+=1

        #INPUT SQL QUERY

        self.viewTripHistoryTree.grid(row=5, column=1, columnspan=6, padx=20, pady = (10,10))
        self.viewTripHistoryTree.bind("<ButtonRelease-1>", self.selectTrip)


    def selectTrip(self, value):
        pass

    def viewTripHistoryUpdateClicked(self):
        startTime = self.entryStartTime.get()
        endTime = self.entryEndTime.get()

        #If only startTime was input
        if not startTime:
            startTime = "0001-01-01 00:00:00"
            startDateFormat = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        else:
            try:
                startDateFormat = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            except:
                messagebox.showwarning("Input invalid", "The Start Time input is invalid.")
                return False

        if not endTime:
            endTime = "9999-01-01 00:00:00"
            endDateFormat = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        else:
            try:
                endDateFormat = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            except:
                messagebox.showwarning("Input invalid", "The Start Time input is invalid.")
                return False

        print(startDateFormat, endDateFormat)

        #If only endTime was input
        #If both startTime and endTime was input

    def viewTripHistoryResetClicked(self):
        pass

    def passengerFunctionalityWindowLogOutButtonClicked(self):
        # Click the Log Out Button on Passenger Functionality Window:
        pass  

    #=============Administrator Functionality Window========================
    def createAdminFunctionalityWindow(self):
        self.adminFunctionalityWindow = Toplevel()
        self.adminFunctionalityWindow.title("Administrator")

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.loginWindow.destroy()

        self.adminFunctionalityWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
        #Add component for adminFunctionalityWindow



        #Station Management Button
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management")
        stationManagementButton.grid(row=1, column=3, sticky=W + E, padx=40, pady = 20)

        #Suspend Cards Button
        suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards", command=self.adminSuspendedCardsClicked)
        suspendedCardButton.grid(row=3, column=3, sticky=W + E, padx=40, pady = 20)

        #Breezecard Management Button
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management",
                                            command=self.adminFunctionalityWindowBreezecardManagementButtonClicked)
        breezecardManagementButton.grid(row=5, column=3, sticky=W + E, padx=40, pady = 20)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report", command=self.adminPassengerFlowClicked)
        passengerFlowReportButton.grid(row=7, column=3, sticky=W + E, padx=40, pady = 20)


        #logout Button
        logoutButton = Button(adminFunctionalityWindow,
                              text="Log Out",
                              command=self.adminFunctionalityWindowLogOutButtonClicked)
        logoutButton.grid(row=9, column=3, padx=40, pady = (50, 20))

    # def adminFunctionalityWindowLogout(self):
    #     adminFuctionalityW

    def adminFunctionalityWindowLogOutButtonClicked(self):
        # Click the Log Out Button on Admin Functionality Window:
        self.loginWindow.destroy()
        # Login Window
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)




    #=================Admin Suspended Card Window======================================
    def adminSuspendedCardsClicked(self):
        self.createAdminSuspendedCardsWindow()
        self.buildAdminSuspendedCardsWindow(self.adminSuspendedCardsWindow)

    def createAdminSuspendedCardsWindow(self):
        self.adminSuspendedCardsWindow = Toplevel()
        # self.adminSuspendedCardsWindow.event_delete()
        self.adminSuspendedCardsWindow.title("Suspended Cards")

    def buildAdminSuspendedCardsWindow(self, adminSuspendedCardsWindow):
        self.suspended_card_num_asc = True
        self.suspended_date_asc = True
        self.sort_mode = {}
        self.sort_mode['cardnum_asc'] = "ORDER BY conCardNum ASC;"
        self.sort_mode['cardnum_desc'] = "ORDER BY conCardNum DESC;"
        self.sort_mode['date_asc'] = "ORDER BY dateTime ASC;"
        self.sort_mode['date_desc'] = "ORDER BY dateTime DESC;"
        self.current_suspended_card_sort = self.sort_mode['cardnum_asc']
        print(self.sort_mode['cardnum_asc'])


        self.suspendedCardsTree = ttk.Treeview(adminSuspendedCardsWindow, column=("cardNum", "newOwner", "dateSuspended", "prevOwner"))
        self.suspendedCardsTree['show'] = 'headings'
        self.suspendedCardsTree.column("cardNum", width=150, anchor="center")
        self.suspendedCardsTree.column("newOwner", width=70, anchor="center")
        self.suspendedCardsTree.column("dateSuspended", width=140, anchor="center")
        self.suspendedCardsTree.column("prevOwner", width=120, anchor="center")

        self.suspendedCardsTree.heading("cardNum", text="Card # ▲")
        self.suspendedCardsTree.heading("newOwner", text="New Owner")
        self.suspendedCardsTree.heading("dateSuspended", text="Date Suspended ▲▼")
        self.suspendedCardsTree.heading("prevOwner", text="Previous Owner")

        self.cursor.execute("SELECT conCardNum, conUsername AS newOwner, dateTime, Breezecard.cUsername AS previousOwner "
                            "FROM Conflict "
                            "INNER JOIN Breezecard ON ( conCardNum = cardNum ) "
                            + self.current_suspended_card_sort)
        self.suspendedCardsTuple = self.cursor.fetchall()
        self.cardNums = []
        self.newOwners = []
        self.datesSuspended = []
        self.prevOwners = []
        self.suspendedCardsTreeIndex = 0
        for entry in self.suspendedCardsTuple:
            self.cardNums.append(entry[0])
            self.newOwners.append(entry[1])
            self.datesSuspended.append(entry[2])
            self.prevOwners.append(entry[3])
            self.suspendedCardsTree.insert('', self.suspendedCardsTreeIndex, values=entry)
            self.suspendedCardsTreeIndex+=1

        # for i in range(len(self.suspendedCardsTuple)):
        self.suspendedCardsTree.grid(row=1, column=1, padx = 20, pady = (10, 10), sticky=W+E+N+S )
        self.suspendedCardsTree.bind("<ButtonRelease-1>", self.selectItem)
        assignToNewUserButton = Button(adminSuspendedCardsWindow,
                                       text="Assign Selected Card to New Owner",
                                       command=self.assignToNewUserButtonClicked)
        assignToNewUserButton.grid(row=2, column=1, padx = 20, pady = (0, 10))
        assignToPreviousOwnerButton = Button(adminSuspendedCardsWindow,
                                             text="Assign Selected Card to Previous Owner",
                                             command=self.assignToPreviousUserButtonClicked)
        assignToPreviousOwnerButton.grid(row=3, column=1, padx = 20, pady = 20)


        adminSuspendedCardsNote = Label(adminSuspendedCardsWindow, text="Assigning the card to an owner will unblock"
                                                                        " all accounts conflicted on the same BreezeCard")
        adminSuspendedCardsNote.grid(row=4, column = 1, padx = 20, pady = 20)
        print("selection: ", self.suspendedCardsTree.selection())

        self.suspendedCardsTree.selection()

    def assignToNewUserButtonClicked(self):
        curItem = self.suspendedCardsTree.selection()

        # for j in self.suspendedCardsTree.item(curItem)['values']:
        #     print(j)

        if not self.suspendedCardsTree.selection():
            messagebox.showwarning("Nothing Selected", "Please select an entry in the table!")
            return False
        print("self.suspendedCardsTree.item(curItem)['values'][0]) =",
              self.suspendedCardsTree.item(curItem)['values'][0])
        oldSnake = self.suspendedCardsTree.item(curItem)['values'][3]

        selectedInfo = self.suspendedCardsTree.item(curItem)['values']

        self.cursor.execute("UPDATE Breezecard\n"
                            "SET cUsername = %s\n"
                            "WHERE cardNum = %s;", (selectedInfo[1], selectedInfo[0]))
        self.cursor.execute("DELETE FROM Conflict\n"
                                "WHERE conCardNum = %s;", selectedInfo[0])
        self.db.commit()
        for i in self.suspendedCardsTree.get_children():
            self.suspendedCardsTree.delete(i)
        self.cursor.execute(
            "SELECT conCardNum, conUsername AS newOwner, dateTime, Breezecard.cUsername AS previousOwner "
            "FROM Conflict "
            "INNER JOIN Breezecard ON ( conCardNum = cardNum ) "
            + self.current_suspended_card_sort)
        self.suspendedCardsTree.heading('#1', text='Card # ▲')
        self.suspendedCardsTree.heading('#3', text='Date Suspended ▲▼')

        self.suspendedCardsTuple = self.cursor.fetchall()
        self.cardNums = []
        self.newOwners = []
        self.datesSuspended = []
        self.prevOwners = []
        self.suspendedCardsTreeIndex = 0
        for entry in self.suspendedCardsTuple:
            self.cardNums.append(entry[0])
            self.newOwners.append(entry[1])
            self.datesSuspended.append(entry[2])
            self.prevOwners.append(entry[3])
            self.suspendedCardsTree.insert('', self.suspendedCardsTreeIndex, values=entry)
            self.suspendedCardsTreeIndex += 1
        self.cursor.execute("SELECT cardNum FROM Breezecard WHERE cUsername = %s", oldSnake)
        hasCard = self.cursor.fetchone()
        print("hasCard", hasCard)
        print("oldSnake", oldSnake)
        if not hasCard:
            randomBreeze = str(randint(0, 9)) + str(randint(100000000000000, 999999999999999))
            self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", randomBreeze)
            duplicateCard = self.cursor.fetchone()
            while duplicateCard:
                randomBreeze = str(randint(0, 9)) + str(randint(100000000000000, 999999999999999))
                self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", randomBreeze)
                duplicateCard = self.cursor.fetchone()
            self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)",
                                (randomBreeze, oldSnake))
            self.db.commit()



    def assignToPreviousUserButtonClicked(self):
        curItem = self.suspendedCardsTree.selection()

        # for j in self.suspendedCardsTree.item(curItem)['values']:
        #     print(j)

        if not self.suspendedCardsTree.selection():
            messagebox.showwarning("Nothing Selected", "Please select an entry in the table!")
            return False
        print("self.suspendedCardsTree.item(curItem)['values'][0]) =",
              self.suspendedCardsTree.item(curItem)['values'][0])

        selectedInfo = self.suspendedCardsTree.item(curItem)['values']

        self.cursor.execute("DELETE FROM Conflict\n"
                            "WHERE conCardNum = %s;", selectedInfo[0])
        self.db.commit()
        for i in self.suspendedCardsTree.get_children():
            self.suspendedCardsTree.delete(i)
        self.cursor.execute(
            "SELECT conCardNum, conUsername AS newOwner, dateTime, Breezecard.cUsername AS previousOwner "
            "FROM Conflict "
            + self.current_suspended_card_sort)
        self.suspendedCardsTuple = self.cursor.fetchall()
        self.cardNums = []
        self.newOwners = []
        self.datesSuspended = []
        self.prevOwners = []
        self.suspendedCardsTreeIndex = 0
        for entry in self.suspendedCardsTuple:
            self.cardNums.append(entry[0])
            self.newOwners.append(entry[1])
            self.datesSuspended.append(entry[2])
            self.prevOwners.append(entry[3])
            self.suspendedCardsTree.insert('', self.suspendedCardsTreeIndex, values=entry)
            self.suspendedCardsTreeIndex += 1



    def selectItem(self, event):
        # for selection debugging
        region = self.suspendedCardsTree.identify("region", event.x, event.y)
        if region == "heading":
            print("You clicked:", region, event.x, event.y)
            print(self.suspendedCardsTree.identify_column(event.x),
                  type(self.suspendedCardsTree.identify_column(event.x)))
            if (self.suspendedCardsTree.identify_column(event.x) == '#1'):
                self.suspended_card_num_asc = not self.suspended_card_num_asc
                self.sortSuspendedCardsByTupleIndex(self.suspended_card_num_asc , 1)
                if (self.suspended_card_num_asc):
                    self.suspendedCardsTree.heading('#1', text='Card # ▲')
                else:
                    self.suspendedCardsTree.heading('#1', text='Card # ▼')
                self.suspendedCardsTree.heading('#3', text='Date Suspended ▲▼')
            elif (self.suspendedCardsTree.identify_column(event.x) == '#3'):
                self.sortSuspendedCardsByTupleIndex(self.suspended_date_asc, 3)
                if (self.suspended_date_asc):
                    self.suspendedCardsTree.heading('#3', text='Date Suspended ▼')
                else:
                    self.suspendedCardsTree.heading('#3', text='Date Suspended ▲')
                self.suspended_date_asc = not self.suspended_date_asc
                self.suspendedCardsTree.heading('#1', text='Card # ▲▼')

        curItem = self.suspendedCardsTree.focus()
        print(list(self.suspendedCardsTree.item(curItem)['values']))
        # print("selection: ", self.suspendedCardsTree.selection())

    def sortSuspendedCardsByTupleIndex(self, asc, ind):
        for i in self.suspendedCardsTree.get_children():
            self.suspendedCardsTree.delete(i)
        self.suspendedCardsTuple = sorted(self.suspendedCardsTuple, key=lambda x: x[ind], reverse = not asc)
        self.cardNums = []
        self.newOwners = []
        self.datesSuspended = []
        self.prevOwners = []
        self.suspendedCardsTreeIndex = 0
        for entry in self.suspendedCardsTuple:
            self.cardNums.append(entry[0])
            self.newOwners.append(entry[1])
            self.datesSuspended.append(entry[2])
            self.prevOwners.append(entry[3])
            self.suspendedCardsTree.insert('', self.suspendedCardsTreeIndex, values=entry)
            self.suspendedCardsTreeIndex += 1

    # ===============Administrator Functionality - Breeze Card Management=====================
    def adminFunctionalityWindowBreezecardManagementButtonClicked(self):
        # Click Breeze Card Management on Admin Functionality Window:
        # Invoke createBreezecardManagementWindow; Invoke buildBreezecardManagementWindow;
        self.createBreezecardManagementWindow()
        self.buildBreezecardManagementWindow(self.breezecardManagementWindow)

    def createBreezecardManagementWindow(self):
        self.breezecardManagementWindow = Toplevel()
        self.breezecardManagementWindow.title("Breeze Card Management")

    def buildBreezecardManagementWindow(self, breezecardManagementWindow):
        # Add component for View Station Window

        # Breeze Cards Label
        breezecardsLabel = Label(breezecardManagementWindow, text="Breeze Cards")  ###BOLD IT
        breezecardsLabel.grid(row=1, column=1, sticky=W)

        # Search/Filter Label
        searchFilterLabel = Label(breezecardManagementWindow,
                                  text="Search/Filter")  #####STRING OF STATION STOP ID
        searchFilterLabel.grid(row=3, column=2, sticky=W)

        # Owner Label
        ownerLabel = Label(breezecardManagementWindow, text="Owner")
        ownerLabel.grid(row=5, column=2, sticky=W)

        # Owner Entry
        self.owner = StringVar()
        ownerEntry = Entry(breezecardManagementWindow, textvariable=self.owner, width=20)
        ownerEntry.grid(row=5, column=3, sticky=W)

        self.showSuspendedCards = IntVar()
        showSuspendedCardsCheckButton = Checkbutton(breezecardManagementWindow, text="Show Suspended Cards",
                                                    variable=self.showSuspendedCards)
        showSuspendedCardsCheckButton.grid(row=5, column=4, sticky=W)

        # Card Number Label
        cardNumberLabel = Label(breezecardManagementWindow, text="Card Number")
        cardNumberLabel.grid(row=7, column=2, sticky=W)

        # Card Number Entry
        self.card_num = StringVar()
        cardNumberEntry = Entry(breezecardManagementWindow, textvariable=self.card_num, width=20)
        cardNumberEntry.grid(row=7, column=3, sticky=W)

        # Reset Button
        resetButton = Button(breezecardManagementWindow, text="Reset",
                             command=self.breezecardManagementWindowResetButtonClicked)
        resetButton.grid(row=7, column=5, sticky=W)

        # Value between Label
        valueBetweenLabel = Label(breezecardManagementWindow, text="Value between")
        valueBetweenLabel.grid(row=9, column=2, sticky=W)

        # Value Between Start Value Entry
        self.startValue = StringVar()
        startValueEntry = Entry(breezecardManagementWindow, textvariable=self.startValue, width=8)
        startValueEntry.grid(row=9, column=3, sticky=W)

        # and Label
        andLabel = Label(breezecardManagementWindow, text="and")
        andLabel.grid(row=9, column=4, sticky=W)

        # Value Between End Value Entry
        self.endValue = StringVar()
        endValueEntry = Entry(breezecardManagementWindow, textvariable=self.endValue, width=8)
        endValueEntry.grid(row=9, column=5, sticky=W)

        # Update Filter Button
        updateFilterButton = Button(breezecardManagementWindow, text="Update Filter",
                                    command=self.breezecardManagementWindowUpdateFilterButtonClicked)
        updateFilterButton.grid(row=9, column=6, sticky=W)

        self.cardNumValueOwnerTree = ttk.Treeview(breezecardManagementWindow,
                                                  column=("card_num", "value", "owner"))
        self.cardNumValueOwnerTree['show'] = 'headings'
        self.cardNumValueOwnerTree.column("card_num", width=150, anchor="center")
        self.cardNumValueOwnerTree.column("value", width=70, anchor="center")
        self.cardNumValueOwnerTree.column("owner", width=120, anchor="center")

        self.cardNumValueOwnerTree.heading("card_num", text="Card #")
        self.cardNumValueOwnerTree.heading("value", text="Value")
        self.cardNumValueOwnerTree.heading("owner", text="Owner")

        self.cursor.execute("SELECT * FROM Breezecard")
        self.breezecardInfoTuple = self.cursor.fetchall()
        self.card_nums = []
        self.values = []
        self.owners = []
        self.cardNumValueOwnerTreeIndex = 0
        for breezecardInfo in self.breezecardInfoTuple:
            self.card_nums.append(breezecardInfo[0])
            self.values.append(breezecardInfo[1])
            self.owners.append(breezecardInfo[2])
            self.cardNumValueOwnerTree.insert('', self.cardNumValueOwnerTreeIndex, values=breezecardInfo)
            self.cardNumValueOwnerTreeIndex += 1

        self.cardNumValueOwnerTree.grid(row=2, column=1, padx=20, pady=(10, 10))
        self.cardNumValueOwnerTree.bind("<ButtonRelease-1>", self.selectElement)

        # Set Value of Selected Card Button
        setValueOfSelectedCardButton = Button(breezecardManagementWindow, text="Set Value of Selected Card",
                                              command=self.breezecardManagementWindowSetValueOfSelectedCardButtonClicked)
        setValueOfSelectedCardButton.grid(row=15, column=1, padx=20, pady=(0, 10))

        # Transfer Selected Card Button
        transferSelectedCardButton = Button(breezecardManagementWindow, text="Transfer Selected Card",
                                            command=self.breezecardManagementWindowTransferSelectedCardButtonClicked)
        transferSelectedCardButton.grid(row=16, column=1, padx=20, pady=20)

        # Set Value of Selected Card Entry
        self.setValueOfSelectedCard = StringVar()
        setValueOfSelectedCardEntry = Entry(breezecardManagementWindow,
                                            textvariable=self.setValueOfSelectedCard, width=10)
        setValueOfSelectedCardEntry.grid(row=15, column=2, sticky=W)

        # Transfer Selected Card Entry
        self.transferSelectedCard = StringVar()
        transferSelectedCardEntry = Entry(breezecardManagementWindow, textvariable=self.transferSelectedCard,
                                          width=10)
        transferSelectedCardEntry.grid(row=16, column=2, sticky=W)

        ####CHECK IF WORKS!

    def breezecardManagementWindowResetButtonClicked(self):
        # Click the Reset Button  on Breezecard Management Window:
        self.buildBreezecardManagementWindow(self.breezecardManagementWindow)

    def breezecardManagementWindowUpdateFilterButtonClicked(self):
        # Click the Update Filter Button  on Breezecard Management Window:
        # Obtain the owner, card number, start and end values
        self.ownerFilter = self.owner.get()
        self.card_numFilter = self.card_num.get()
        self.startValueFilter = self.startValue.get()
        self.endValueFilter = self.endValue.get()

        # Error message for card number input doesn't exist in db
        isCard_num = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", self.card_numFilter)
        if not isCard_num:
            messagebox.showwarning("Card Number does not exist in the Database.",
                                   "Try again using an existing Card Number.")
            return False

        # Error message for owner input doesn't exist in db
        isOwner = self.cursor.execute("SELECT * FROM Breezecard WHERE cUsername = %s", self.ownerFilter)
        if not isOwner:
            messagebox.showwarning("Owner does not exist in the Database.",
                                   "Try again using an existing Owner.")
            return False
        if float(self.startValueFilter) < 0.00:
            messagebox.showwarning("Value cannot be less than 0.",
                                   "Please put a value greater than 0 but less than 1000.")
            return False
        if float(self.startValueFilter) > 1000.00:
            messagebox.showwarning("Value cannot be greater than 1000.",
                                   "Please put a value less than 1000 but greater than 0.")
            return False
        if float(self.endValueFilter) < 0.00:
            messagebox.showwarning("Value cannot be less than 0.",
                                   "Please put a value greater than 0 but less than 1000.")
            return False
        if float(self.endValueFilter) > 1000.00:
            messagebox.showwarning("Value cannot be greater than 1000.",
                                   "Please put a value less than 1000 but greater than 0.")
            return False
        else:
            self.cursor.execute(
                "SELECT cardNum, value, cUsername WHERE cardNum = %s AND (value >= %s AND value <= %s) AND cUsername = %s",
                (self.card_numFilter, self.startValueFilter, self.endValueFilter, self.ownerFilter))

    def selectElement(self, event2):
        curElement = self.cardNumValueOwnerTree.focus()
        print(list(self.cardNumValueOwnerTree.item(curElement)['values']))

    def breezecardManagementWindowShowSuspendedCardsChecked(self):
        if self.showSuspendedCards.get() == 0:
            pass
        else:
            suspendedCardInfo = self.cursor.execute(
                "SELECT conCardNum, Breezecard.cUsername AS previousOwner FROM Conflict INNER JOIN Breezecard ON (conCardNum = cardNum)")

    def breezecardManagementWindowSetValueOfSelectedCardButtonClicked(self):
        # Click the Set Value of Selected Card Button  on Breezecard Management Window:
        curElement = self.cardNumValueOwnerTree.selection()
        selectedInformation = self.cardNumValueOwnerTree.item(curElement)['values']
        self.newValue = self.setValueOfSelectedCard.get()
        if not self.cardNumValueOwnerTree.selection():
            messagebox.showwarning("Nothing was selected.", "Please select an entry from the table.")
            return False
        if float(self.newValue) > 1000.00:
            messagebox.showwarning("Breeze Card cannot exceed $1000.00.", "Please enter a lower value.")
            return False
        else:
            self.cursor.execute("UPDATE Breezecard SET value = %s WHERE cardNum = %s",
                                (self.newValue, selectedInformation[0]))
            self.db.commit()

    def breezecardManagementWindowTransferSelectedCardButtonClicked(self):
        # Click the Transfer Selected Card Button  on Breezecard Management Window:
        curElement = self.cardNumValueOwnerTree.selection()
        selectedInformation = self.cardNumValueOwnerTree.item(curElement)['values']
        self.newOwner = self.transferSelectedCard.get()
        print(self.newOwner)
        ownerExists = self.cursor.execute("SELECT username FROM User WHERE username = %s", self.newOwner)
        is_admin = self.cursor.execute("SELECT IsAdmin FROM User WHERE username = %s", self.newOwner)
        if not self.cardNumValueOwnerTree.selection():
            messagebox.showwarning("Nothing was selected.", "Please select an entry from the table.")
            return False
        if not ownerExists:
            messagebox.showwarning("Owner does not exist.", "Please choose a currently existing owner.")
            return False
        if is_admin:
            messagebox.showwarning("This is an administrator.", "Please choose a passenger.")
            return False
        else:
            self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s",
                                (self.newOwner, selectedInformation[0]))
            self.db.commit()

    #=====================Passenger FLow Report===============
    def adminPassengerFlowClicked(self):
        self.createPassengerFlowWindow()
        self.buildPassengerFlowWindow(self.passengerFlowWindow)

    def createPassengerFlowWindow(self):
        self.passengerFlowWindow = Toplevel()
        self.passengerFlowWindow.title("Passenger Flow Report")

    def buildPassengerFlowWindow(self, passengerFlowWindow):
        #Add components for the Passenger FLow Report
        self.passengerFlowTableTreeView = ttk.Treeview(passengerFlowWindow, column=("stationName",
                                                                                  "numPassengersIn",
                                                                                  "numPassengersOut",
                                                                                  "flow",
                                                                                  "revenue"))
        self.passengerFlowTableTreeView['show'] = 'headings'

        self.passengerFlowTableTreeView.column("stationName", width=150, anchor="center")
        self.passengerFlowTableTreeView.column("numPassengersIn", width=150, anchor="center")
        self.passengerFlowTableTreeView.column("numPassengersOut", width=150, anchor="center")
        self.passengerFlowTableTreeView.column("flow", width=100, anchor="center")
        self.passengerFlowTableTreeView.column("revenue", width=100, anchor="center")

        self.passengerFlowTableTreeView.heading("stationName", text="Station Name ▲")
        self.passengerFlowTableTreeView.heading("numPassengersIn", text="# Passengers In")
        self.passengerFlowTableTreeView.heading("numPassengersOut", text="# Passengers Out")
        self.passengerFlowTableTreeView.heading("flow", text="Flow")
        self.passengerFlowTableTreeView.heading("revenue", text="Revenue")

        self.passengerFlowTableTreeView.grid(row=3, column=0, sticky=E, padx=10, pady=10, columnspan=7)
        startTimeLabel = Label(passengerFlowWindow,
                                text="Start Time")
        startTimeLabel.grid(row=1, column=0, padx = 10, pady = 10, sticky=W)
        endTimeLabel = Label(passengerFlowWindow,
                              text="End Time")
        endTimeLabel.grid(row=2, column=0, padx = 10, pady = 10, sticky=W)

        startTimeEntry = Entry(passengerFlowWindow)
        startTimeEntry.grid(row=1, column=1, sticky=W+E)

        endTimeEntry = Entry(passengerFlowWindow)
        endTimeEntry.grid(row=2, column=1, sticky=W+E)

        updateButton = Button(passengerFlowWindow,
                              text="Update")
        resetButton = Button(passengerFlowWindow,
                             text="Reset")
        updateButton.grid(row=1, column=2, rowspan=2, sticky=W+E+N+S, padx = (20,10), pady = 20)
        resetButton.grid(row=1, column=3, rowspan=2, sticky=W+E+N+S, padx = (10,20), pady = 20)






    # --------------------Database Connection-----------------
    def connect(self):
        try:
            #TODO: figure out the name of the database
            db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                 db='cs4400_Group_54', user='cs4400_Group_54', passwd='qUYP7usT', autocommit=True)
            return db
        except:
            messagebox.showwarning('Error!', 'Cannot connect. Internet Connection Issue or DB not ready.')
            return False
a = MARTA_Client()
a.db.close()