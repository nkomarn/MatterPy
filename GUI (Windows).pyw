#!/usr/bin/env python3
# Matter: A Discord Rich Presense Tool
# Created by TechToolbox
# python-discord-rpc API port by suclearnub
# Version 1.0

# Import dependencies
from threading import Thread
import configparser
import rpc
import time
import os

# Import TKinter GUI Library
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import tkinter

# Set toggle boolean to False on startup
bool = False
activity = None
start_time = time.time()

# Connects to Discord (using python-discord-rpc by suclearnub)
def richPresenece():
    try:
        if (not len(largeIconHoverText.get()) < 2) and (not len(smallIconHoverText.get()) < 2):
            # Config for RPC connection 
            rpc_obj = rpc.DiscordIpcClient.for_platform(appIDFieldText.get())
            
            print("RPC connection successful.")

            # Set button to display disable sprite
            stateButton.config(image=disableImage, borderwidth=0, background="#23272A")

            # Define time varibles used for timer
            time.sleep(5)
            global activity

            while True:
                rpc_obj.set_activity(updateTimer(activity))
                # Refresh every 15 sec as per Discord API spec
                time.sleep(15)
        else:
            raise Exception
    except:
        # If not all fields are filled, catch exception generated and display error on button
        stateButton.config(image=missingFieldsImage, borderwidth=0, background="#23272A")

        # Reset toggle value
        global bool
        bool = False  

# Returns the correct activity data based on whether timer is desired or not
def updateTimer(activity):
        if (timerToggleValue.get() == 0):
            activity = {
                    "state": bottomTextFieldText.get(),
                    "details": topTextFieldText.get(),
                    "assets": {
                        "small_text": smallIconHoverText.get(),
                        "small_image": smallIconName.get(),
                        "large_text": largeIconHoverText.get(),
                        "large_image": largeIconName.get()
                    }
                }
            return activity
        else:
            activity = {
                    "state": bottomTextFieldText.get(),
                    "details": topTextFieldText.get(),
                    "timestamps": {
                        "start": start_time
                    },
                    "assets": {
                        "small_text": smallIconHoverText.get(),
                        "small_image": smallIconName.get(),
                        "large_text": largeIconHoverText.get(),
                        "large_image": largeIconName.get()
                    }
                }
            return activity


def load():
    try:
        # Open file dialog and prompt for config file
        filename = askopenfilename()
        
        # Read file and get contents
        config = configparser.ConfigParser()
        config.readfp(open(filename))
        applicationID = config.get('Configuration', 'application-id')
        topText = config.get('Configuration', 'top-text')
        bottomText = config.get('Configuration', 'bottom-text')
        largeIcon = config.get('Configuration', 'large-icon')
        smallIcon = config.get('Configuration', 'small-icon')
        largeIconHover = config.get('Configuration', 'large-icon-hover')
        smallIconHover = config.get('Configuration', 'small-icon-hover')
        timer = config.get('Configuration', 'timer')

        # Set entry field values based on configuration file
        appIDFieldText.set(applicationID)
        topTextFieldText.set(topText)
        bottomTextFieldText.set(bottomText)
        largeIconName.set(largeIcon)
        smallIconName.set(smallIcon)
        largeIconHoverText.set(largeIconHover)
        smallIconHoverText.set(smallIconHover)
        timerToggleValue.set(timer)
        
        # Set button to normal image in case previous attempt failed
        loadButton.config(image=loadProfileImage, borderwidth=0, highlightthickness=0, background="#23272A", command=load)
    except:
        # Change select button to error button
        loadButton.config(image=loadErrorImage, borderwidth=0, highlightthickness=0, background="#23272A", command=load)

def save():
    try:
        # Creates new config based on entry stringvar values
        config = configparser.ConfigParser()
        config.add_section('Configuration')
        config.set('Configuration', 'application-id', appIDFieldText.get())
        config.set('Configuration', 'top-text', topTextFieldText.get())
        config.set('Configuration', 'bottom-text', bottomTextFieldText.get())
        config.set('Configuration', 'large-icon', largeIconName.get())
        config.set('Configuration', 'small-icon', smallIconName.get())
        config.set('Configuration', 'large-icon-hover', largeIconHoverText.get())
        config.set('Configuration', 'small-icon-hover', smallIconHoverText.get())
        config.set('Configuration', 'timer', str(timerToggleValue.get()))

        # Asks user for file path and name
        fileLocation = asksaveasfilename(defaultextension=".txt")

        with open(fileLocation, 'w') as configfile:
            config.write(configfile)

        # Change button back to normal sprite in case error is displaying
        saveButton.config(image=saveProfileImage, borderwidth=0, background="#23272A", highlightthickness=0, command=save)
    except:
        # Chnage button image to failure image
        saveButton.config(image=saveErrorImage, borderwidth=0, background="#23272A", highlightthickness=0, command=save)

def toggle():
    global bool
    bool = not bool

    if bool == True:
        # Create thread to run RPC and not freeze GUI
        rpcThread = Thread(target = richPresenece)
        rpcThread.start()  
    else:
        quit()

def quit():
    os._exit(1)

def closeEvent():
    # Destroy all threads on window close
    quit()

# Set up program window
root = tkinter.Tk()
root.title("Matter: A Discord Rich Presence Tool")
root.config(bg='#23272A')
root.geometry("600x350")
root.resizable(False, False)
root.tk.call('wm', 'iconphoto', root._w, tkinter.PhotoImage(file='resources/logo.png'))
root.protocol("WM_DELETE_WINDOW", closeEvent)

# Load images 
loadProfileImage = tkinter.PhotoImage(file="resources/loadprofile.png")
saveProfileImage = tkinter.PhotoImage(file="resources/saveprofile.png")
appIDImage = tkinter.PhotoImage(file="resources/applicationID.png")
largeImageHoverImage = tkinter.PhotoImage(file="resources/largeImageHover.png")
smallImageHoverImage = tkinter.PhotoImage(file="resources/smallImageHover.png")
profileImage = tkinter.PhotoImage(file="resources/profile.png")
controlsImage = tkinter.PhotoImage(file="resources/controls.png")
enableImage = tkinter.PhotoImage(file="resources/enable.png")
disableImage = tkinter.PhotoImage(file="resources/disable.png")
missingFieldsImage = tkinter.PhotoImage(file="resources/missingFields.png")
playingGameImage = tkinter.PhotoImage(file="resources/playingGame.png")
bannerImage = tkinter.PhotoImage(file="resources/banner.png")
loadErrorImage = tkinter.PhotoImage(file="resources/profileerror.png")
saveErrorImage = tkinter.PhotoImage(file="resources/saveerror.png")

# Create GUI elements
topFrame = tkinter.Frame(root, background="#f1f1f1")
bottomFrame = tkinter.Frame(root, background="#23272A")

topFrame.pack(side="top", fill="both", expand=True)
bottomFrame.pack(side="bottom", fill="both", expand=True)

largeImageFrame = tkinter.Frame(topFrame, background="#f1f1f1")
textInputFrame = tkinter.Frame(topFrame, background="#f1f1f1")

largeImageFrame.pack(side="left", expand=True)
textInputFrame.pack(side="right", expand=True)

bannerImageLabel = tkinter.Label(largeImageFrame, image=bannerImage, borderwidth=0, background="#7289DA")

playingGameLabel = tkinter.Label(textInputFrame, image=playingGameImage, background="#f1f1f1")

topTextFieldText = tkinter.StringVar()
topTextFieldText.set('Top line')
topTextField = tkinter.Entry(textInputFrame, textvariable=topTextFieldText, bg="#eaeaea", foreground="#484848", highlightthickness=0.5, highlightbackground="#adadad")
topTextField.config(borderwidth=0)

bottomTextFieldText = tkinter.StringVar()
bottomTextFieldText.set('Bottom line')
bottomTextField = tkinter.Entry(textInputFrame, textvariable=bottomTextFieldText, bg="#eaeaea", foreground="#484848", highlightthickness=0.5, highlightbackground="#adadad")
bottomTextField.config(borderwidth=0)

largeIconName = tkinter.StringVar()
largeIconName.set('Large icon')
largeIconNameField = tkinter.Entry(textInputFrame, textvariable=largeIconName, bg="#eaeaea", foreground="#484848", highlightthickness=0.5, highlightbackground="#adadad")
largeIconNameField.config(borderwidth=0)

smallIconName = tkinter.StringVar()
smallIconName.set('Small icon')
smallIconNameField = tkinter.Entry(textInputFrame, textvariable=smallIconName, bg="#eaeaea", foreground="#484848", highlightthickness=0.5, highlightbackground="#adadad")
smallIconNameField.config(borderwidth=0)

timerToggleValue = tkinter.IntVar()
timerToggle = tkinter.Checkbutton(textInputFrame, text="Show timer", variable=timerToggleValue, bd=0, highlightthickness=0)

inputFrame = tkinter.Frame(bottomFrame, background="#23272A")
buttonFrame = tkinter.Frame(bottomFrame, background="#23272A")

inputFrame.pack(side="top", fill="both", expand=True)
buttonFrame.pack(side="top", fill="both", expand=True)

appIDLabel = tkinter.Label(inputFrame, image=appIDImage, background="#23272A")
largeImageHoverLabel = tkinter.Label(inputFrame, image=largeImageHoverImage, text="LARGE IMAGE HOVER", foreground="lightgray", background="#23272A")
smallImageHoverLabel = tkinter.Label(inputFrame, image=smallImageHoverImage, text="SMALL IMAGE HOVER", foreground="lightgray", background="#23272A")

inputFrame.grid_columnconfigure((0,1,2), weight=1)
inputFrame.grid_rowconfigure(2, weight=1)

appIDFieldText = tkinter.StringVar()
appIDEntry = tkinter.Entry(inputFrame, borderwidth=0, highlightthickness=0.5, highlightbackground="#000", background="#2C2F33", foreground="#fff", bd=0, textvariable=appIDFieldText)
largeIconHoverText = tkinter.StringVar()
largeImageEntry = tkinter.Entry(inputFrame, highlightthickness=0.5, highlightbackground="#000", background="#2C2F33", foreground="#fff", bd=0, textvariable=largeIconHoverText)
smallIconHoverText = tkinter.StringVar()
smallImageEntry = tkinter.Entry(inputFrame, borderwidth=0, highlightthickness=0.5, highlightbackground="#000", background="#2C2F33", foreground="#fff", bd=0, textvariable=smallIconHoverText)

profileFrame = tkinter.Frame(buttonFrame, background="#23272A")
controlsFrame = tkinter.Frame(buttonFrame, background="#23272A")

profileFrame.pack(side="left", fill="both", expand=True)
controlsFrame.pack(side="right", fill="both", expand=True)

profileLabel = tkinter.Label(profileFrame, image=profileImage, background="#23272A")
loadButton = tkinter.Button(profileFrame)
loadButton.config(image=loadProfileImage, borderwidth=0, highlightthickness=0, background="#23272A", command=load)
saveButton = tkinter.Button(profileFrame)
saveButton.config(image=saveProfileImage, borderwidth=0, background="#23272A", highlightthickness=0, command=save)

controlsLabel = tkinter.Label(controlsFrame, image=controlsImage, background="#23272A")
stateButton = tkinter.Button(controlsFrame, command=toggle)
stateButton.config(image=enableImage, borderwidth=0, highlightthickness=0, background="#23272A")

# GUI Grid layout
playingGameLabel.grid(row=0, column=1, padx=(4, 0), pady=(0,5), sticky="ew")
topTextField.grid(row=1, column=1, padx=(20, 0), pady=(0,6), sticky="ew")
bottomTextField.grid(row=2, column=1, padx=(20, 0), pady=(0,6), sticky="ew")
largeIconNameField.grid(row=3, column=1, padx=(20, 0), pady=(0,6), sticky="ew")
smallIconNameField.grid(row=4, column=1, padx=(20, 0), pady=(0,6), sticky="ew")
timerToggle.grid(row=5, column=1, padx=(0, 0), pady=(0,0), sticky="ew")

bannerImageLabel.grid(row=0, column=1, padx=(5, 0), sticky="ew")

appIDLabel.grid(row=0, column=0, padx=(18, 0), pady=(20, 5), sticky="w")
largeImageHoverLabel.grid(row=0, column=1, padx=(5, 0), pady=(20, 5), sticky="w")
smallImageHoverLabel.grid(row=0, column=2, padx=(5, 0), pady=(20, 5), sticky="w")
appIDEntry.grid(row=1, column=0, padx=(20, 5), ipadx=6, ipady=6, sticky="ew")
largeImageEntry.grid(row=1, column=1, padx=(5, 5), ipadx=6, ipady=6, sticky="ew")
smallImageEntry.grid(row=1, column=2, padx=(5, 20), ipadx=6, ipady=6, sticky="ew")

profileLabel.grid(row=0, column=1, padx=(20, 0), pady=(0, 5), sticky="w")
loadButton.grid(row=1, column=1, padx=(20, 5), sticky="ew")
saveButton.grid(row=1, column=2, padx=(5, 0), sticky="ew")

controlsLabel.grid(row=0, column=1, padx=(15, 0), pady=(0, 5), sticky="ew")
stateButton.grid(row=1, column=1, padx=(108, 0), sticky="ew")

# Display GUI
root.mainloop()