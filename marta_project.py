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

        self.viewTripHistoryExist = False
        self.manageBreezecardExist = False

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
        regusernameEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationUsername, width=25)
        regusernameEntry.grid(row=2, column=3, padx=1)


        # Email Address Entry
        self.registrationEmailAddress = StringVar()
        regemailAddressEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationEmailAddress,width=25)
        regemailAddressEntry.grid(row=3, column=3, padx=1)

        # Password Entry
        self.registrationPassword = StringVar()
        regpasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationPassword,show = '*',width=25)
        regpasswordEntry.grid(row=4, column=3, padx=1)

        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        regconfirmPasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationConfirmPassword,show = '*',width=25)
        regconfirmPasswordEntry.grid(row=5, column=3, padx=1)

        self.var = StringVar()
        r1 = Radiobutton(newUserRegistrationWindow, text="Option 1", variable=self.var, value="exist")
        r1.grid(row=6, column=1, sticky=W)
        breezebox = Label(newUserRegistrationWindow, text="Card Number")
        breezebox.grid(row=7, column=1, sticky=E)
        self.registrationCardNum = StringVar()
        breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        breezeboxEntry.grid(row=7, column=2, padx=1)

        r2 = Radiobutton(newUserRegistrationWindow, text="Option 2", variable=self.var, value="new")
        r2.grid(row=8, column=1, sticky=W)

        self.var.set("new")

        # Create Button
        newRegisterButton = Button(newUserRegistrationWindow, text="Register", command=self.newRegistrationWindowButtonClicked)
        newRegisterButton.grid(row=8, column=4, sticky=E)


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
            if (len(self.existBreeze) != 16):
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

        self.passengerFunctionalityWindow.protocol("WM_DELETE_WINDOW", self.passenger_on_closing)

    def passenger_on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if (self.viewTripHistoryExist):
                self.cursor.execute("DROP VIEW TripHistory")
            self.loginWindow.destroy()

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
        self.viewTripHistoryWindow.protocol("WM_DELETE_WINDOW", self.dropview)

    def dropview(self):
        self.cursor.execute("DROP VIEW TripHistory")
        self.viewTripHistoryExist = 0
        self.viewTripHistoryWindow.withdraw()

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

        if not self.viewTripHistoryExist:
            self.viewTripHistoryExist = True
            self.cursor.execute("CREATE VIEW TripHistory AS (SELECT startTime, startID, endID, currentFare, bcNum FROM Trip WHERE bcNUM IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", self.passusername)

        self.cursor.execute("SELECT * FROM TripHistory")
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

        self.cursor.execute("DROP VIEW TripHistory")
        self.cursor.execute("CREATE VIEW TripHistory AS (SELECT startTime, startID, endID, currentFare, bcNum FROM Trip WHERE(bcNum IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s)) AND (startTime >= %s) AND (startTime <= %s))", (self.passusername, startDateFormat, endDateFormat))

        self.buildViewTripHistoryWindow(self.viewTripHistoryWindow)
        return True

        #If only endTime was input
        #If both startTime and endTime was input

    def viewTripHistoryResetClicked(self):
        self.cursor.execute("DROP VIEW TripHistory")
        self.cursor.execute("CREATE VIEW TripHistory AS (SELECT startTime, startID, endID, currentFare, bcNum FROM Trip WHERE bcNUM IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", self.passusername)
        self.buildViewTripHistoryWindow(self.viewTripHistoryWindow)
        return True

    def passengerFunctionalityWindowLogOutButtonClicked(self):
        # Click the Log Out Button on Passenger Functionality Window:
        if (self.viewTripHistoryExist):
            self.cursor.execute("DROP VIEW TripHistory")

        self.loginWindow.destroy()


    #=============Administrator Functionality Window========================
    def createAdminFunctionalityWindow(self):
        self.adminFunctionalityWindow = Toplevel()
        self.adminFunctionalityWindow.title("Administrator")

        self.adminFunctionalityWindow.protocol("WM_DELETE_WINDOW", self.administrator_on_closing)

    def administrator_on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if (self.manageBreezecardExist):
                self.cursor.execute("DROP VIEW ManageBreezecard")
            self.loginWindow.destroy()

    # def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
    #     #Add component for adminFunctionalityWindow

    #     #Station Management Button
    #     stationManagementButton = Button(adminFunctionalityWindow, text="Station Management", command = self.stationManagementButtonClicked)
    #     stationManagementButton.grid(row=1, column=3, sticky=W + E)

    #     #Suspend Cards Button
    #     suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
    #     suspendedCardButton.grid(row=3, column=3, sticky=W + E)

    #     #Breezecard Management Button
    #     breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management")
    #     breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

    #     #Passenger Flow Report Button
    #     passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")
    #     passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)



        #---------------------------- ver 3.0 -------------------------------------
    def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
        self.adminusername = self.loginUsername.get()
        #Add component for adminFunctionalityWindow

        #Station Management Button
<<<<<<< HEAD
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management",command=self.adminFunctionalityWindowStationManagementButtonClicked)
        stationManagementButton.grid(row=1, column=3, sticky=W + E)
=======
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management")
        stationManagementButton.grid(row=1, column=3, padx = 20, pady = 10, sticky=W + E)
>>>>>>> cddc2e942a67c7fa9447906ffb3b709a68ed9707

        #Suspend Cards Button
        suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
        suspendedCardButton.grid(row=3, column=3, padx = 20, pady = 10, sticky=W + E)

        #Breezecard Management Button
<<<<<<< HEAD
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management",command = self.adminFunctionalityWindowBreezecardManagementButtonClicked)
        breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")

        #Log Out Button        passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)

        logOutAdminButton = Button(adminFunctionalityWindow, text="Log Out") #,command=self.adminFunctionalityWindowLogOutButtonClicked)
        logOutAdminButton.grid(row=9, column=3, sticky=W + E)
    #===============Administrator Functionality - Station Management=========================
    def adminFunctionalityWindowStationManagementButtonClicked(self):
        # Click the Station Management Button on Admin Functionality Window:
        self.createStationManagementWindow()
        self.buildStationManagementWindow(self.stationManagementWindow)

    #Station Management Window
    def createStationManagementWindow(self):
        self.stationManagementWindow = Toplevel()
        self.stationManagementWindow.title("Station Listing")


    # def selectElement(self,event2):
    #     curElement = self.stationListingTree.focus()
    #     print(list(self.stationListingTree.item(curElement)['values'])


    def buildStationManagementWindow(self, stationManagementWindow):
        #Add component for stationManagementWindow
        departureLabel = Label(stationManagementWindow, text = "Station Listing", font = "verdana 20 bold")
        departureLabel.grid(row=1, column=2, sticky= W+E, padx=100,pady=20)


        self.stationListingTree = ttk.Treeview(stationManagementWindow, column=("1", "2", "3", "4"))
        self.stationListingTree['show'] = "headings"
        self.stationListingTree.column("1", width = 150, anchor = "center")
        self.stationListingTree.column("2", width = 150, anchor = "center")
        self.stationListingTree.column("3", width = 150, anchor = "center")
        self.stationListingTree.column("4", width = 150, anchor = "center")

        self.stationListingTree.heading("1", text = "Station Name")
        self.stationListingTree.heading("2", text = "Stop ID")
        self.stationListingTree.heading("3", text = "Fare")
        self.stationListingTree.heading("4", text = "Status")



        self.cursor.execute("SELECT name, stopID, fare, ClosedStatus FROM Station")

        self.selectstationTuple = self.cursor.fetchall()
        self.stationNameList = []
        self.stopIDList = []
        self.fareList = []
        self.statusList = []
        self.statusListEdited = []
        for i in self.selectstationTuple:
            self.stationNameList.append(i[0])
            self.stopIDList.append(i[1])
            self.fareList.append(i[2])
            self.statusList.append(i[3])

        for i in range(len(self.statusList)):
            if self.statusList[i] == 0:
                self.statusListEdited.append("Closed");
            elif self.statusList[i] == 1:
                self.statusListEdited.append("Open");


        # Insert data into the treeview
        for i in range(len(self.selectstationTuple)):
            self.stationListingTree.insert('',i,values=(self.stationNameList[i],self.stopIDList[i],self.fareList[i],self.statusListEdited[i]))
        self.stationListingTree.grid(row=2,column=1, columnspan=4, padx=20, pady=20)




        #Create Create New Station Button
        createNewStationButton = Button(stationManagementWindow, text="Create New Station",command = self.stationManagementWindowCreateNewStationButtonClicked)
        createNewStationButton.grid(row=4, column=1, sticky=W)

        #Create View Station Button
        viewStationButton = Button(stationManagementWindow, text="View Station",command = self.stationManagementWindowViewStationButtonClicked)
        viewStationButton.grid(row=4, column=4, sticky=E)


    def stationManagementWindowCreateNewStationButtonClicked(self):
        # Click the Create New Station Button on Station Management Window:
        self.createCreateNewStationWindow()
        self.buildCreateNewStationWindow(self.createNewStationWindow)

        #self.loginWindow.withdraw()

    #=============New User Registration Window==============
    def createCreateNewStationWindow(self):
        self.createNewStationWindow = Toplevel()
        self.createNewStationWindow.title("Create New Station")


        #---------------------------------------------------------
    def buildCreateNewStationWindow(self, createNewStationWindow):
        #Add component for Create New Station Window
        top_title = Label(createNewStationWindow, text = "Create Station", font = "verdana 10 bold")
        top_title.grid(column=2, sticky= W+E, padx = (0, 95))
        #Station Name Label
        stationNameLabel = Label(createNewStationWindow, text="Station Name")
        stationNameLabel.grid(row=1, column=1, sticky=W, pady=(10,5))

        #StopID Label
        stopIDLabel = Label(createNewStationWindow, text="Stop ID")
        stopIDLabel.grid(row=3, column=1, sticky=W, pady = 5)

        #Entry Fare Label
        entryFareLabel = Label(createNewStationWindow, text="Entry Fare")
        entryFareLabel.grid(row=5, column=1, sticky=W,pady = 5)

        #Station Type Label
        stationTypeLabel = Label(createNewStationWindow, text="Station Type")
        stationTypeLabel.grid(row=7, column=1, sticky=W,pady = 5)

        # nearestIntersection = Label(createNewStationWindow, text="Nearest Intersection")
        # nearestIntersection.grid(row=7, column=2, sticky=W)

        self.typeSelected = StringVar()
        self.typeSelected.set("bus")
        r1 = Radiobutton(createNewStationWindow, text="Bus Station", variable=self.typeSelected, value="bus")
        r1.grid(row=6, column=2, sticky=W)
        self.registerNearInt = StringVar()
        nearSEctionEntry = Entry(createNewStationWindow, textvariable=self.registerNearInt, width=20)
        nearSEctionEntry.grid(row=7, column=2, sticky=W)
        r2 = Radiobutton(createNewStationWindow, text="Train Station", variable=self.typeSelected, value="train")
        r2.grid(row=8, column=2, sticky=W)


        #Description of Open Station Label
        # descriptionOpenStationLabel = Label(createNewStationWindow,text="When checked, passengers can enter at this station.")
        # descriptionOpenStationLabel.grid(row=11,column=1, sticky = W)
        self.var1 = IntVar()
        self.var1.set(1)
        c1 = Checkbutton(createNewStationWindow, text="Open Station", variable=self.var1, onvalue=1, offvalue=0).grid(row=9, column=1, sticky=W)

         # Username Entry
        self.registrationStationName = StringVar()
        stationNameEntry = Entry(createNewStationWindow, textvariable=self.registrationStationName, width=25)
        stationNameEntry.grid(row=1, column=2, sticky = W,pady=(10,5))

        # Email Address Entry
        self.registrationStopID = StringVar()
        stopIDEntry = Entry(createNewStationWindow, textvariable=self.registrationStopID,width=25)
        stopIDEntry.grid(row=3, column=2, sticky= W , pady = 5)

        # Password Entry
        self.registrationFare = StringVar()
        self.registrationFare.set("$")
        fareEntry = Entry(createNewStationWindow, textvariable=self.registrationFare,width=25)
        fareEntry.grid(row=5, column=2, sticky =W, pady = 5)




        #Create Create Station Button
        createStationButton = Button(createNewStationWindow, text="Create Station", command=self.createNewStationWindowCreateStationButtonClicked)
        createStationButton.grid(row=12, column=2, padx=(100,0), sticky=E)


    def createNewStationWindowCreateStationButtonClicked(self):
        # Click the Create Station Button on Create New Station Window:
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        #Clock the button on create new station Window
        self.regStationName = self.registrationStationName.get()
        self.regStopID = self.registrationStopID.get()
        self.regFare = self.registrationFare.get()
        if self.regFare[0] == '$':
            self.regFare = self.regFare[1:]
        self.regNearInt = self.registerNearInt.get()
        self.regType = self.typeSelected.get()
        self.checkboxVar = self.var1.get()
        print (self.checkboxVar)

        # Error message for station input empty
        if not self.regStationName:
            messagebox.showwarning("Station Name input is empty", "Please enter registering station name.")
            return False
        #Error message for stop id input empty
        if not self.regStopID:
            messagebox.showwarning("Stop ID input is empty", "Please enter registering Stop ID.")
            return False
        #Error message for fare input empty
        if not self.regFare:
            messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
            return False
        # Error message that input is not float value
        if not isfloat(self.regFare):
              messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
              return False
        else:
            isFare = (float(self.regFare) <= 50 and float(self.regFare) >= 0)

        # print (isFare)
        # Error message that input is not bween 0.00 and 50.00
        if not isFare:
            messagebox.showwarning("Fare input is not correct","Fare to enter must be between $0.00 and $50.00 \nPlease enter valid station fare.")
            return False


        if self.regType == "bus":
            if not self.regNearInt:
               messagebox.showwarning("Nearest Intersection input is empty", "Please enter valid input.")
               return False

        #Error message for username input already exist in db
        isStation = self.cursor.execute("SELECT * FROM Station WHERE name = %s", self.regStationName)
        if isStation:
            messagebox.showwarning("Station Name already exist", "The station name you entered already exist. \n Try different station.")
            return False

        #Error message for email input already exist in db
        isStopID = self.cursor.execute("SELECT * FROM Station WHERE stopID = %s", self.regStopID)
        if isStopID:
            messagebox.showwarning("stopID already exist", "The stopID you entered already exist. \n Try different stopID.")
            return False

        if (self.regType == "bus"):
            self.cursor.execute("INSERT INTO Station(stopID, name, IsTrain, fare, ClosedStatus) VALUES(%s, %s, False, %s, %s)", (self.regStopID, self.regStationName, self.regFare, self.checkboxVar))
            self.cursor.execute("INSERT INTO Bus(busID, nearestIntersection) VALUES(%s,%s)", (self.regStopID, self.regNearInt))
            messagebox.showwarning("Registration Success", "bus station has successfully registered to database.")
            self.createNewStationWindow.destroy()
            self.db.commit()
            self.buildStationManagementWindow(self.stationManagementWindow)
            return True
        elif (self.regType == "train"):
            self.cursor.execute("INSERT INTO Station(stopID, name, IsTrain, fare, ClosedStatus) VALUES(%s, %s, True, %s, %s)", (self.regStopID, self.regStationName, self.regFare, self.checkboxVar))
            messagebox.showwarning("Registration Success", "train station has successfully registered to database.")
            self.createNewStationWindow.destroy()
            self.db.commit()
            self.buildStationManagementWindow(self.stationManagementWindow)
            return True

    #------------------------- view station -------------------------------

    def stationManagementWindowViewStationButtonClicked(self):
        # Click the View Station Button on Station Management Window:
        curItem = self.stationListingTree.selection()
        if not self.stationListingTree.selection():
            messagebox.showwarning("Nothing Selected", "Please select an entry in the table!")
            return False
        self.createViewStationWindow(curItem)
        self.buildViewStationWindow(self.viewStationWindow, curItem)

    #Create View Station Window
    def createViewStationWindow(self, curItem):
        selectedStation = self.stationListingTree.item(curItem)['values'][0]
        self.viewStationWindow = Toplevel()
        self.viewStationWindow.title("Station Detail - %s" % selectedStation)#####STRING OF STATION NAME

    def buildViewStationWindow(self, viewStationWindow, curItem):
        #Add component for View Station Window
        #Station Detail Name Label
        def change_case(event=None):
            self.updateFareClicked(self.selectedFare)

        def red_text(event=None):
            updatefareLabel.config(fg="red")

        def black_text(event=None):
            updatefareLabel.config(fg="blue")



        self.selectedStation = self.stationListingTree.item(curItem)['values'][0]
        self.selectedStopID = self.stationListingTree.item(curItem)['values'][1]
        self.selectedFare = self.stationListingTree.item(curItem)['values'][2]
        self.selectedStatus = self.stationListingTree.item(curItem)['values'][3]
        if self.selectedStatus == "Open":
            statusBin = 1;
        elif self.selectedStatus == "Closed":
            statusBin = 0;
        print ("selected status: " + str(self.selectedStatus))

        stationDetailNameLabel = Label(viewStationWindow,text=self.selectedStation, font = "Verdana 12 bold") #####STRING OF STATION NAME
        stationDetailNameLabel.grid(row=2,column=1,sticky=W) #####STRING OF STATION NAME


        #Station Detail StopID Label
        stationDetailStopIDLabel = Label(viewStationWindow,text="Stop %s" % self.selectedStopID, fg = "red", font = "Verdana 8 bold") #####STRING OF STATION STOP ID
        stationDetailStopIDLabel.grid(row=2,column=10,sticky=E) #####STRING OF STATION STOP ID

        #Fare Label
        fareLabel = Label(viewStationWindow,text="Fare")
        fareLabel.grid(row=3,column=1,sticky=W)

        self.newFare = StringVar()
        self.newFare.set("$%s" % self.selectedFare)
        fareEntry2 = Entry(viewStationWindow, textvariable=self.newFare, width=30)
        fareEntry2.grid(row=3, column=2, sticky =W, pady = 5)

        updatefareLabel = Label(viewStationWindow, text="Update Fare", fg= "blue", font = "time 8 underline")
        updatefareLabel.bind("<Button-1>",change_case)
        updatefareLabel.bind("<Enter>",red_text)
        updatefareLabel.bind("<Leave>",black_text)

        updatefareLabel.grid(row=3,column=3, sticky=W)


        #Nearest Intersection in Station Detail Label
        nearestIntersectionStationDetailLabel = Label(viewStationWindow, text="Nearest\n  Intersection")
        nearestIntersectionStationDetailLabel.grid(row=5,column=1,sticky=W)

        ###INSERT MESSAGE "Not available for train stations" If Train CODE
        self.isTrainType();
        if (self.selectedType == 1):
            descriptionLabel = Label(viewStationWindow, text="Not available for train stations", font = "Verdana 7 bold")
            descriptionLabel.grid(row=5,column=2,sticky=W, padx=(0,150))
        elif (self.selectedType == 0):
            self.newNearIntSect = StringVar()
            self.cursor.execute("SELECT nearestIntersection FROM Bus WHERE busID = %s", self.selectedStopID)
            self.selectedIntSect = self.cursor.fetchone()
            self.selectedIntSect = self.selectedIntSect[0]
            self.newNearIntSect.set(self.selectedIntSect)
            print (self.selectedIntSect)
            stopIDEntry = Entry(viewStationWindow, textvariable=self.newNearIntSect,width=30)
            stopIDEntry.grid(row=5, column=2, sticky= W , padx=(0,150))






        #Open Station in Station Detail Label
        self.var2 = IntVar()
        self.var2.set(statusBin)
        c1 = Checkbutton(viewStationWindow, text="Open Station", variable=self.var2, onvalue=1, offvalue=0).grid(row=9, column=1, sticky=W)


        #Description of Open Station in Station Detail Label
        descriptionOpenStationStationDetailLabel = Label(viewStationWindow,text="When checked, passengers can enter at this station.")
        descriptionOpenStationStationDetailLabel.grid(row=10,column=1,sticky=W)

    # def change_case(event=None):
    #     def isfloat(value):
    #         try:
    #             float(value)
    #             return True
    #         except ValueError:
    #             return False
    #     print ("in def")
    #     inputFare = self.newFare.get()
    #     if inputFare[0] == '$':
    #         inputFare = inputFare[1:]
    #     if not inputFare:
    #         messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
    #         return False
    #     if not isfloat(self.inputFare):
    #         messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
    #     else:
    #         isFare = (float(self.inputFare) <= 50 and float(self.inputFare) >= 0)
    #     # Error message that input is not bween 0.00 and 50.00
    #     if not isFare:
    #         messagebox.showwarning("Fare input is not correct","Fare to enter must be between $0.00 and $50.00 \nPlease enter valid station fare.")
    #         return False
    def isTrainType(self):
        self.cursor.execute("SELECT IsTrain FROM Station WHERE stopID = %s", self.selectedStopID)
        self.selectedType = self.cursor.fetchone()
        self.selectedType =self.selectedType[0]
        print ("%s station is :" % self.selectedStation + str(self.selectedType))

        return True

    def updateFareClicked(self, selectedFare):
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        print (self.newFare.get())
        inputFare = self.newFare.get()
        oldFare = self.selectedFare
        print (oldFare)

        if not inputFare:
            messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
            return False
        if inputFare[0] == '$':
            inputFare = inputFare[1:]
        if not isfloat(inputFare):
            messagebox.showwarning("Input is not float value", "Please enter valid fare value.")
            return False
        else:
            isFare = (float(inputFare) <= 50 and float(inputFare) >= 0)
        # Error message that input is not bween 0.00 and 50.00
        if float(oldFare) == float(inputFare):
            messagebox.showwarning("Nothing Has Changed", "Nothing has changed.\nPlease enter desire fare.")
            return False

        self.cursor.execute("UPDATE Station SET fare = %s WHERE StopID = %s",  (inputFare, self.selectedStopID))
        self.db.commit()
        messagebox.showwarning("Change Successfully", "Fare information has been updated for %s" % self.selectedStation)
        return True

    def adminFunctionalityWindowBreezecardManagementButtonClicked(self):
        self.createBreezecardMangementWindow()
        self.buildcreateBreezecardMangementWindow(self,createNewStationWindow)

    def createBreezecardMangementWindow(self):
        self.stationManagementWindow = Toplevel()
        self.stationManagementWindow.title("Breeze Card Management")
=======
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management", command=self.adminFunctionalityWindowBreezecardManagementButtonClicked)
        breezecardManagementButton.grid(row=5, column=3, padx = 20, pady = 10, sticky=W + E)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")
        passengerFlowReportButton.grid(row=7, column=3, padx = 20, pady = 10, sticky=W + E)

        logoutButton = Button(adminFunctionalityWindow, text = "Log Out", command=self.admin_logout)
        logoutButton.grid(row=9, column=3, padx=40, pady=10, sticky=W + E)

    def admin_logout(self):
        if (self.manageBreezecardExist):
            self.cursor.execute("DROP VIEW ManageBreezecard")

        self.loginWindow.destroy()

    #===============Administrator Functionality - Breeze Card Management=====================
    def adminFunctionalityWindowBreezecardManagementButtonClicked(self):
        # Click Breeze Card Management on Admin Functionality Window:
        # Invoke createBreezecardManagementWindow; Invoke buildBreezecardManagementWindow;
        self.createBreezecardManagementWindow()
        self.buildBreezecardManagementWindow(self.breezecardManagementWindow)

    def createBreezecardManagementWindow(self):
        self.breezecardManagementWindow = Toplevel()
        self.breezecardManagementWindow.title("Breeze Card Management")

        self.breezecardManagementWindow.protocol("WM_DELETE_WINDOW", self.breezecard_manage_closing)

    def breezecard_manage_closing(self):
        self.cursor.execute("DROP VIEW ManageBreezecard")
        self.manageBreezecardExist = 0
        self.breezecardManagementWindow.withdraw()

    def buildBreezecardManagementWindow(self, breezecardManagementWindow):
        #Add component for View Station Window

        #Breeze Cards Label
        breezecardsLabel = Label(breezecardManagementWindow,text="Breeze Cards") ###BOLD IT
        breezecardsLabel.grid(row=1,column=1,sticky=W + E)

        #Search/Filter Label
        searchFilterLabel = Label(breezecardManagementWindow,text="Search/Filter") #####STRING OF STATION STOP ID
        searchFilterLabel.grid(row=3,column=1, pady = 10, sticky=W)

        #Owner Label
        ownerLabel = Label(breezecardManagementWindow,text="Owner")
        ownerLabel.grid(row=5,column=1,sticky=W)

        #Owner Entry
        self.owner = StringVar()
        ownerEntry = Entry(breezecardManagementWindow, textvariable=self.owner,width = 20)
        ownerEntry.grid(row=5,column=2,sticky = W)

        self.showSuspendedCards=IntVar()
        showSuspendedCardsCheckButton = Checkbutton(breezecardManagementWindow,text = "Show Suspended Cards",variable = self.showSuspendedCards)
        showSuspendedCardsCheckButton.grid(row=5,column=4,sticky = W)

        #Card Number Label
        cardNumberLabel = Label(breezecardManagementWindow,text="Card Number")
        cardNumberLabel.grid(row=7,column=1,sticky=W)

        #Card Number Entry
        self.card_num = StringVar()
        cardNumberEntry = Entry(breezecardManagementWindow, textvariable=self.card_num,width = 20)
        cardNumberEntry.grid(row=7,column=2,sticky = W)

        #Reset Button
        resetButton = Button(breezecardManagementWindow, text="Reset", command=self.breezecardManagementWindowResetButtonClicked)
        resetButton.grid(row=7, column=5, sticky=W)

        #Value between Label
        valueBetweenLabel = Label(breezecardManagementWindow,text="Value between")
        valueBetweenLabel.grid(row=9,column=1,sticky=W)

        #Value Between Start Value Entry
        self.startValue = StringVar()
        startValueEntry = Entry(breezecardManagementWindow, textvariable=self.startValue,width = 8)
        startValueEntry.grid(row=9,column=2,sticky = W)

        #and Label
        andLabel = Label(breezecardManagementWindow,text="and")
        andLabel.grid(row=9,column=3,sticky=W)

        #Value Between End Value Entry
        self.endValue = StringVar()
        endValueEntry = Entry(breezecardManagementWindow, textvariable=self.endValue,width = 8)
        endValueEntry.grid(row=9,column=4,sticky = W)

        #Update Filter Button
        updateFilterButton = Button(breezecardManagementWindow, text="Update Filter", command=self.breezecardManagementWindowUpdateFilterButtonClicked)
        updateFilterButton.grid(row=9, column=5, sticky=W)


        #Table
        self.cardNumValueOwnerTree = ttk.Treeview(breezecardManagementWindow,column=("card_num","value","owner"))
        self.cardNumValueOwnerTree['show'] = 'headings'
        self.cardNumValueOwnerTree.column("card_num",width=150,anchor="center")
        self.cardNumValueOwnerTree.column("value",width=70,anchor="center")
        self.cardNumValueOwnerTree.column("owner",width=120,anchor="center")

        self.cardNumValueOwnerTree.heading("card_num",text="Card #")
        self.cardNumValueOwnerTree.heading("value",text="Value")
        self.cardNumValueOwnerTree.heading("owner",text="Owner")

        if not self.manageBreezecardExist:
            self.manageBreezecardExist = True
            self.cursor.execute("CREATE VIEW ManageBreezecard AS (SELECT * FROM Breezecard)")

        self.cursor.execute("SELECT * FROM ManageBreezecard")
        self.breezecardInfoTuple = self.cursor.fetchall()
        self.card_nums = []
        self.values = []
        self.owners = []
        self.cardNumValueOwnerTreeIndex = 0
        for breezecardInfo in self.breezecardInfoTuple:
            #make owner as suspended if the card is in suspended status
            #####IDK HOW TO MAKE SUSPENDED BOLD
            isSuspended = self.cursor.execute("SELECT * FROM Conflict WHERE conCardNum = %s", breezecardInfo[0])
            ownerName = breezecardInfo[2]
            if not isSuspended:
                ownerName = ownerName
            else:
                ownerName = "Suspended"
            self.card_nums.append(breezecardInfo[0])
            self.values.append(breezecardInfo[1])
            self.owners.append(breezecardInfo[2])
            self.cardNumValueOwnerTree.insert('',self.cardNumValueOwnerTreeIndex,values = (breezecardInfo[0], breezecardInfo[1], ownerName))
            self.cardNumValueOwnerTreeIndex+=1

        self.cardNumValueOwnerTree.grid(row=10,column=1, columnspan = 5, padx=20,pady=(10,10))
        self.cardNumValueOwnerTree.bind("<ButtonRelease-1>",self.selectElement)

        #Set Value of Selected Card Button
        setValueOfSelectedCardButton= Button(breezecardManagementWindow, text="Set Value of Selected Card",command=self.breezecardManagementWindowSetValueOfSelectedCardButtonClicked)
        setValueOfSelectedCardButton.grid(row=15, column=2, padx=20,pady=(0,10))

        #Transfer Selected Card Button
        transferSelectedCardButton = Button(breezecardManagementWindow, text="Transfer Selected Card",command=self.breezecardManagementWindowTransferSelectedCardButtonClicked)
        transferSelectedCardButton.grid(row=16, column=2, padx=20,pady=20)

        #Set Value of Selected Card Entry
        self.setValueOfSelectedCard = StringVar()
        setValueOfSelectedCardEntry = Entry(breezecardManagementWindow, textvariable=self.setValueOfSelectedCard,width = 10)
        setValueOfSelectedCardEntry.grid(row=15,column=1,sticky = W)

        #Transfer Selected Card Entry
        self.transferSelectedCard = StringVar()
        transferSelectedCardEntry = Entry(breezecardManagementWindow, textvariable=self.transferSelectedCard,width = 10)
        transferSelectedCardEntry.grid(row=16,column=1,sticky = W)

    def breezecardManagementWindowResetButtonClicked(self):
        #Click the Reset Button  on Breezecard Management Window:
        self.buildBreezecardManagementWindow(self.breezecardManagementWindow)

    def breezecardManagementWindowUpdateFilterButtonClicked(self):
        #Click the Update Filter Button  on Breezecard Management Window:
        #Obtain the owner, card number, start and end values
        ownerFilter = self.owner.get()
        card_numFilter = self.card_num.get()
        startValueFilter = self.startValue.get()
        endValueFilter = self.endValue.get()
        suspendedFilter = self.showSuspendedCards.get() # 0 not selected, 1 selected
        #Update based on owner, card number, suspended status, or value range
        #self.card_nums -> list of all cards

        #INPUT ERROR
        #Error if card number is invalid (not 16-digit)
        #Error if card number is invalid (not digit)
        #Error if value input is invalid (not digit)
        #Error if value input exceeds 1000.00

        if not ownerFilter:
            ownerFilter = "%s" % (self.owners,)
        if not card_numFilter:
            card_numFilter = "%s" % (self.card_nums,)
        if not startValueFilter:
            startValueFilter = 0
        if not endValueFilter:
            endValueFilter = 1000.00

        #ownerFilter = (ownerFilter,)
        print(ownerFilter)
        #if (suspendedFilter == 0):
            #self.cursor.execute("DROP VIEW ManageBreezecard")
            #self.cursor.execute("CREATE VIEW ManageBreezecard AS (SELECT * FROM Breezecard WHERE ")


            #self.cursor.execute("CREATE VIEW ManageBreezecard AS (SELECT * FROM Breezecard)")

    def selectElement(self,event2):
        curElement = self.cardNumValueOwnerTree.focus()
        print(list(self.cardNumValueOwnerTree.item(curElement)['values']))

    def breezecardManagementWindowShowSuspendedCardsChecked(self):
        if self.showSuspendedCards.get() == 0:
            pass
        else:
            suspendedCardInfo = self.cursor.execute("SELECT conCardNum, Breezecard.cUsername AS previousOwner FROM Conflict INNER JOIN Breezecard ON (conCardNum = cardNum)")


    def breezecardManagementWindowSetValueOfSelectedCardButtonClicked(self):
        #Click the Set Value of Selected Card Button  on Breezecard Management Window:
        curElement = self.cardNumValueOwnerTree.selection()
        selectedInformation = self.cardNumValueOwnerTree.item(curElement)['values']
        self.newValue = self.setValueOfSelectedCard.get()

        if self.newValue.isdigit()==0:
            messagebox.showwarning("Invalid Value.","The value should be a number.")
            return False
        #Error: nothing selected
        if not self.cardNumValueOwnerTree.selection():
            messagebox.showwarning("Nothing was selected.","Please select an entry from the table.")
            return False
        if float(self.newValue) > 1000.00:
            messagebox.showwarning("Breeze Card cannot exceed $1000.00.","Please enter a lower value.")
            return False
        if float(self.newValue) < 0.00:
            messagebox.showwarning("Breeze Card cannot be below $0.00.", "Please enter a higher value.")
            return False
        else:
            self.cursor.execute("UPDATE Breezecard SET value = %s WHERE cardNum = %s",(self.newValue,selectedInformation[0]))
            self.db.commit()

    def breezecardManagementWindowTransferSelectedCardButtonClicked(self):
        #Click the Transfer Selected Card Button  on Breezecard Management Window:
        curElement = self.cardNumValueOwnerTree.selection()
        selectedInformation = self.cardNumValueOwnerTree.item(curElement)['values']
        self.newOwner = self.transferSelectedCard.get()
        self.cursor.execute("SELECT username FROM User WHERE username = %s", self.newOwner)
        ownerExists=self.cursor.fetchone()[0]
        #print(ownerExists)
        self.cursor.execute("SELECT IsAdmin FROM User WHERE username = %s", self.newOwner)
        is_admin=self.cursor.fetchone()[0]
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
            self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s", (self.newOwner, selectedInformation[0]))
            self.db.commit()
>>>>>>> cddc2e942a67c7fa9447906ffb3b709a68ed9707


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