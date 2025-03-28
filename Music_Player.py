# Importing necessary modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pygame
import time
from mutagen.mp3 import MP3
import threading
from PIL import Image
import random

# File paths for storing data
name_list='C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\name.txt'
Database='C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Song_DB\\Song_DB.txt'
Playlist='C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Play_list.txt'

# Initialization of variables
movement_time = 0
movement = True
rand=False
Play = False
pause = False
num_of_loop = 0
time_of_loop = 0
time_in_int = 0
leading_zeroes = 0
finish = False
count = 0
Text_original = ''
stop = False
Text = 'C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Song_DB\\' + Text_original + '.mp3'


UserID='guest'
pygame.mixer.init()

# Function to display the main page of the music player
def mainpage():
    #GUI setup
    main_window = Tk()

    canvas = Canvas(main_window, width=500, height=300)
    canvas.grid(row=0, column=0)
    canvas.create_text(250, 100, font=('Calibri', 30), text='Welcome to my music player')
    canvas.create_text(250, 200, font=('Calibri', 15), text='Please login or register an account to start')

    Button(main_window, text='Login', font=('Calibri, 15'),  command=lambda: [main_window.destroy(), Enter_ID('login')]).grid(row=1, column=0, pady=5)
    Button(main_window, text='Register', font=('Calibri, 15'), command=lambda: [main_window.destroy(), Enter_ID('register')]).grid(row=2, column=0, pady=5)
    Button(main_window, text='Login as guest', command=lambda: [main_window.destroy(), Enter_ID('guest')], font=('Calibri, 15')).grid(row=3, column=0, pady=5)

    main_window.mainloop()

# Function to handle actions such as navigation or closing windows
def Action(window, Act='back'):
    if Act=='forward':
        window.destroy()
        music_page()
    elif Act=='close':
        window.destroy()
        messagebox.showinfo(title='Thanks', message='Thanks for using the music player. Please visit again')
        messagebox.showinfo(title='Success', message='Logout successful')
        return
    else:
        window.destroy()
        mainpage()

# Function for handling user login and registration
def Enter_ID(action):
    Show=False
    Entry_window=Tk()
    Entry_window.title('Music Player')
    Entry_window.geometry('500x500')

    #allows users to access the music_player as guests. Their playlist will not be saved
    if action == 'guest':
        Action(Entry_window, 'forward')
    else:
        #designing GUI
        canvas=Canvas(Entry_window, width=500, height=100)
        canvas.grid(row=0, column=0, columnspan=100)
        canvas.create_text(250, 50, text='Welcome to My music player', font=('Calibri, 25'))

        Email_label=Label(Entry_window,text='Email: ', font=('Calibri, 15'))
        Email_label.grid(row=1, column=0)
        Email=Entry(Entry_window, width=25, font=('Calibri, 15'))
        Email.grid(row=1, column=1, columnspan=2)

        Password_label = Label(Entry_window, text='Password: ', font=('Calibri, 15'))
        Password_label.grid(row=2, column=0)
        Password=Entry(Entry_window, width=25, font=('Calibri, 15'), show='*')
        Password.grid(row=2, column=1, columnspan=2)

        #function to by default show the password as * but will turn into words when clicked on
        def show_password():
            nonlocal Show
            if Show == False:
                Password.config(show='')
                Hide.config(text='Hide Password')
                Show=True
            else:
                Password.config(show='*')
                Hide.config(text='Show Password')
                Show=False

        #register accounts for users
        def Register():
            global ID
            ID=0
            Address = Email.get()
            Passcode = Password.get()
            #error and validation check for the format of emails
            for i in range(len(Address)):
                if '@' and '.' not in Address:
                    return messagebox.showerror(title='Invalid Email', message='Please type in a valid email.\nexample@mail.com')
            #check if the email already exists
            with open(name_list,'r') as file:
                lines=file.readlines()
                for j in range(len(lines)):
                    ID+=1
                for line in lines:
                    line=line.strip('\n')
                    line=line.split(', ')
                    Stored_name=line[0]
                    if Address == Stored_name:
                        return messagebox.showerror(title='Account already exists!',
                            message='An account has already been registered using the same email\nPlease login at the mainpage')

            #error and validation check for the password
            if len(Passcode) < 8:
                return messagebox.showerror(title='Invalid Password', message='Password must be at least 8 characters long')
            with open(name_list,'a') as file:
                file.write(Address+', '+Passcode+', '+str(ID)+'\n')
                messagebox.showinfo(title='Success', message='Successfully Registered, please login to continue!')
            with open(Playlist,'a') as file:
                file.write(str(ID)+', \n')
            Action(Entry_window)

        #a function that allows users to login to the music_player
        def login():
            login='failed'
            Address = Email.get()
            Passcode = Password.get()
            with open(name_list,'r') as file:
                lines=file.readlines()
                for line in lines:
                    line=line.strip('\n')
                    line=line.split(', ')
                    Stored_name=line[0]
                    Stored_password = line[1]
                    Stored_ID = line[2]
                    if Address == Stored_name and Passcode == Stored_password:
                        messagebox.showinfo(title='Success', message='Login Successful')
                        login='Success'
                        global UserID
                        UserID = Stored_ID
                        Action(Entry_window, Act='forward')
                    elif Address == Stored_name and Passcode != Stored_password:
                        error='Incorrect Password'
                        break
                    else:
                        error = 'Email Address not found'
                if login=='failed':
                    messagebox.showinfo(title='Denied', message=error)

        #action is the parametered enter for this function. This one function containes three different actions
        if action == 'register':
            Enter = Button(Entry_window, text='Register', command=Register, font=('Calibri, 15'))
            Enter.grid(row=4, column=1)
            Button(Entry_window, text='Back', command=lambda: Action(Entry_window), font=('Calibri, 15')).grid(row=4, column=2)
        elif action == 'login':
            Enter2 = Button(Entry_window, text='Login', command=login, font=('Calibri, 15'))
            Enter2.grid(row=4, column=1)
            Button(Entry_window, text='Back', command=lambda: Action(Entry_window), font=('Calibri, 15')).grid(row=4, column=2)
        elif action == 'guest':
            Button(Entry_window, text='Back', command=lambda: Action(Entry_window), font=('Calibri, 15')).grid(row=5, column=2)

        if Show == False:
            Hide = Button(Entry_window, text='Show password', command=lambda: show_password(), bd=10)
        elif Show == True:
            Hide = Button(Entry_window, text='Hide password', command=lambda: show_password(), bd=10)
        Hide.grid(row=2, column=3, padx=10)

    Entry_window.mainloop()

# Function to handle user logout and saves their playlist
def logout():
    global UserID
    if UserID != 'guest':
        music_list = []
        for i in range(listbox.size()):
            song=listbox.get(i)
            music_list.append(song)
        with open(Playlist,'r') as file:
            lines = file.readlines()
            lines[int(UserID)]=str(UserID) + ', '+str(music_list)+'\n'
        with open(Playlist,'w') as file:
            file.writelines(lines)

# Function to manage the song database
def song_db(act):
    DB = Tk()

    #function to add songs into their database
    if act == 'add':
        Actual_List = Listbox(DB, selectmode=MULTIPLE, width=50)
        Shown_List = Listbox(DB, selectmode=MULTIPLE, width=50)
        with open(Database, 'r') as Db:
            lines = Db.readlines()
            for line in lines:
                line=line.strip('\n')
                if line == '\n' or line == '':
                    pass
                Actual_List.insert(0, line)
                Shown_List.insert(0, line)
        #insert the songs from the Database into user playlist
        def Selected_songs():
            for i in Shown_List.curselection():
                listbox.insert(END, Shown_List.get(i))

        Label(DB, text='Search: ').grid(row=0, column=0)
        Search_box = Entry(DB)
        Search_box.grid(row=0, column=1, columnspan=2)

        #search function that allows users to search for songs in the database to add to their playlist
        def Search():
            Song=Search_box.get()

            while True:
                if Shown_List.get(0) != '':
                    Shown_List.delete(0)
                else:
                    break

            for index in range(Actual_List.size()):
                if Song.lower() in Actual_List.get(index).lower():
                    Shown_List.insert(END, Actual_List.get(index))

        Search_button = Button(DB, text='Search', font=('Calibri, 10'), command=lambda: [Search()])
        Search_button.grid(row=0, column=3, sticky=E)

        insert = Button(DB, text='Done', font=('Calibri, 15'), command=lambda: [Selected_songs(), DB.destroy()])
        insert.grid(row=2, column=2, sticky=E)

        Shown_List.grid(row=1, column=0, columnspan=3)

    #allows users to remove songs from their playlist
    elif act == 'delete':
        list = Listbox(DB, selectmode=MULTIPLE)
        count = 0
        while True:
            list.insert(0, listbox.get(count))
            count += 1
            if listbox.get(count) == '':
                break
        def delete_song():
            for i in list.curselection():
                count=0
                while True:
                    if listbox.get(count) != '':
                        if listbox.get(count) == list.get(i) or listbox.get(i) == '\n':
                            listbox.delete(count)
                            count=0
                        else:
                            count+=1
                    else:
                        break


        list.grid(row=0, column=0)
        delete = Button(DB, text='Done', command=lambda: [delete_song(), DB.destroy()])
        delete.grid(row=2, column=2)

    DB.mainloop()

# Function to open and close the playlist
def Open_close_list():
    global listbox
    listbox=Listbox(height=20, width=30)
    with open(Playlist,'r') as file:
        lines = file.readlines()
    if UserID != 'guest':
        line=lines[int(UserID)]
        line=line.split(', ',1)

        line=line[1].strip("\n[]")
        line=line.split(', ')
        song_list=[]
        for i in line:
            i=i.strip("''\\n")
            song_list.append(i)
        for j in range(len(song_list)):
            listbox.insert(END, song_list[j])

    Add = Button(text='add song', font=('Calibri, 10'), command=lambda: song_db('add'))
    Delete = Button(text='delete song', font=('Calibri, 10'), command=lambda: song_db('delete'))
    label = Label(text='Your Playlist: ', font=('Calibri, 20'), bg='#fafbf9')

    Open_list = Button(text='▶', font=('Calibri, 18'), command=lambda:
    [listbox.grid(row=2, column=0, columnspan=2, padx=(10,0)), label.grid(row=1, column=0, columnspan=2, sticky=S), Close_list.grid(row=2, column=2),
     Open_list.grid_forget(), Add.grid(row=3, column=0), Delete.grid(row=3, column=1) ])
    Open_list.grid(row=2, column=0)

    Close_list = Button(text='◀', font=('Calibri, 20'), command=lambda:
    [Close_list.grid_forget(), label.grid_forget(), listbox.grid_forget(), Open_list.grid(row=2, column=0),
     Add.grid_forget(), Delete.grid_forget()])

# Function to manage the music player interface
def music_page():
    global movement_time
    song_length = ''
    #changes the volume of the song
    def Volume(x):
        pygame.mixer.music.set_volume(Slider.get())

    #gets length of the song
    def song_duration():
        nonlocal song_length
        # get currently playing song
        if listbox.get(ACTIVE) == '':
            listbox.activate(0)
        current_song = listbox.get(ACTIVE)
        current_song = 'C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Song_DB\\' + current_song + '.mp3'
        song_mut = MP3(current_song)
        song_length = round(song_mut.info.length, 2)
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        status_bar_end.config(text=converted_song_length)

    #gets current time of the song that has been played
    def get_time():
        nonlocal song_length
        global time_of_loop
        global time_in_int
        global finish
        global Play
        time_in_int_original = round(pygame.mixer.music.get_pos() / 1000, 2)

        if pygame.mixer.music.get_busy():
            finish = False
            if time_in_int>= song_length:
                time_of_loop+=1
                time_in_int = 0
                time_in_int += time_in_int_original - (song_length * time_of_loop)
            elif time_of_loop > 0 or num_of_loop !=0:
                time_in_int = time_in_int_original - (song_length * time_of_loop)
            else:
                time_in_int = time_in_int_original
        elif pause == True:
            pass
        else:
            time_in_int = 0
            time_of_loop = 0
        if time_in_int < 0:
            time_in_int = 0
        if (time_in_int >= song_length or time_in_int < 0) and finish == True:
            time_in_int = 0

        current_time = time.strftime('%M:%S', time.gmtime(time_in_int))

        status_bar_start.config(text= current_time)
        Song_slider.config(from_=0, to=song_length, value=time_in_int)

        #alters the status_bar every second changing the current time in song and the progress bar
        status_bar_start.after(1000, get_time)

    get_length = 0

    #a function to loop the songs
    def loop():
        global num_of_loop
        if num_of_loop == 0:
            num_of_loop = -1
            loop_button.config(bd=6 )
        else:
            num_of_loop = 0
            loop_button.config(bd=2)
        select_song('start')

    #a function thet contains three actions namely starting the song and skipping forwards and backwards
    def select_song(act):
        global pause
        global Play
        nonlocal get_length
        global Text_original
        global finish
        global count, stop, movement, movement_time

        Text_original = listbox.get(ACTIVE)
        for i in range(listbox.size()):
            if Text_original == listbox.get(count):
                break
            else:
                count += 1
        Text_original = str(listbox.get(ACTIVE)).strip("'\n'")

        #skips to the next song
        if act == 'forward':
            if listbox.get(ACTIVE) == listbox.get(END):
                listbox.activate(0)
                count = 0
            else:
                count += 1
                listbox.activate(count)
            select_song('start')
        #goes back to the precious song
        elif act == 'backward':
            if listbox.get(ACTIVE) == listbox.get(0):
                messagebox.showinfo(message="You're at the top of your playlist")
            else:
                if count!=0:
                    count -= 1
                listbox.activate(count)

            select_song('start')
        #plays the current song
        elif act == 'start':
            if listbox.get(ACTIVE) == '':
                listbox.activate(0)
            Text_original = listbox.get(ACTIVE)
            Play=True
            pause = False
            song_duration()
            get_length=0
            global movement_time
            if movement_time == 0:
                animation()
                movement = True
                movement_time+=1
        #pause and unpause the songs
        elif act == 'pause':
            if pause == False:
                pygame.mixer.music.pause()
                stop_animation()
                pause = True
            elif pause == True:
                pygame.mixer.music.unpause()
                pause = False
            Play=True
        #end the songs
        elif act == 'stop':
            pygame.mixer.music.stop()
            Play=False
            stop = True
            #plays the song
        if act == 'start' or act == 'forward' or act == 'backward':
            stop = False
            Play = True
            Text = 'C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Song_DB\\' + Text_original + '.mp3'
            pygame.mixer.music.load(Text)
            pygame.mixer.music.play(loops=num_of_loop)
            #checks if the song is still playing
            def Check_if_busy():
                global finish, stop
                if pygame.mixer.music.get_busy():
                    finish = False
                else:
                    finish = True
                t = threading.Timer(1, Check_if_busy)
                t.start()
                if finish == True:
                    auto_next()
                    t.cancel()
            Check_if_busy()
            if get_length == 0:
                song_duration()
                get_length += 1
            get_time()
        else:
            if not pause:
                animation()
            else:
                stop_animation()

        canvas = Canvas(width=300, height=50, bg='silver')
        x_position = canvas.winfo_reqwidth()/2
        y_position = 25
        #makes the text move accross the screen making it more interesting
        def move_text():
            nonlocal x_position, y_position

            x_position+=10
            canvas.coords(word, x_position, y_position)

            if canvas.bbox(word)[0] >= canvas.winfo_width():
                x_position = -canvas.bbox(word)[2]

            global moving
            moving = music_player.after(200, move_text)

        canvas.grid(row=0, column=0, columnspan=20)
        word = canvas.create_text(x_position, y_position, text=Text_original, font=('Calibri, 15'), justify=RIGHT)

        if Play == True:
            move_text()
        else:
            try:
                music_player.after_cancel(moving)
            except:
                pass

    #auto loops to the next song if current song is finished
    def auto_next():
        global finish, rand, pause, stop
        if finish and not stop and not rand and not pause:
            select_song('forward')
        elif finish and not stop  and rand and not pause:
            shuffle_play()

    #plays the song in random orders
    def shuffle_play():
        global count, rand, Play
        if rand == False:
            rand = True
            shuffle_button.config(bd=10)
        else:
            rand = False
            shuffle_button.config(bd=2)
        new_count = random.randint(0, listbox.size())
        if new_count == count:
            while new_count == count:
                new_count = random.randint(0, listbox.size())
        count = new_count
        listbox.activate(count)
        if Play == False:
            select_song('start')
            Play = True

    #music player GUI design
    music_player = Tk()
    music_player.title('Music Player')
    music_player.config(bg='#fafbf9')
    file = "C:\\Users\\Lenovo\\Desktop\\SCHOOL\\programming and coursework\\Music player\\Dancing cat.gif"
    info = Image.open(file)

    frames = info.n_frames  # number of frames

    photoimage_objects = []
    for i in range(frames):
        obj = PhotoImage(file=file, format=f"gif -index {i}")
        photoimage_objects.append(obj)

    #creates an animation to make the music player more interesting
    def animation(current_frame=0):
        global loop
        image = photoimage_objects[current_frame]

        canvas.create_image(-10, 0, anchor=NW, image = image)
        current_frame += 1

        if current_frame == frames:
            current_frame = 0  # reset the current_frame to 0 when end is reached
        global movement

        if movement == False:
            global movement_time
            music_player.after_cancel(loop)
            movement_time = 0
            movement = True
        else:
            loop = music_player.after(50, lambda: animation(current_frame))

    #stops the animation when songs not playing
    def stop_animation():
        global movement
        movement = False

    #GUI design
    Open_close_list()

    canvas = Canvas(music_player, width=700, height=600)
    canvas.grid(row=0, column=3, columnspan=6, rowspan=5, pady=10, padx=10)

    Play = Button(music_player, text='▶', font=('Calibri', 20), command=lambda: select_song('start'))
    Play.grid(row=6, column=4)

    Pause = Button(music_player, text='⏸', font=('Calibri', 20), command=lambda: select_song('pause'))
    Pause.grid(row=6, column=5)

    Stop=Button(music_player, text='𓂸', font=('Calibri', 20), command=lambda: select_song('stop'))
    Stop.grid(row=6, column=6)

    Next = Button(music_player, text='⏭', font=('Calibri', 20), command=lambda: select_song('forward'))
    Next.grid(row=6, column=7)

    Previous = Button(music_player, text='⏮', font=('Calibri', 20), command=lambda: select_song('backward'))
    Previous.grid(row=6, column=3)

    Exit=Button(music_player, text='Exit', font=('Calibri', 20), command=lambda: [logout(), select_song('stop'),Action(music_player, Act='close')])
    Exit.grid(row=6, column=8)

    Label(music_player, text='🔊', font=('Calibri, 20')).grid(row=1, column=9, pady=(20,0))
    Slider = ttk.Scale(music_player, from_=1, to=0, value=1, orient=VERTICAL,  length=250, command=Volume)
    Slider.grid(row=2, column=9,sticky=W, padx=(5,0))

    status_bar_start=Label(music_player, text='',bd=2, font=('Calibri, 10'))
    status_bar_start.grid(row=5, column=3, pady=10)

    status_bar_end = Label(music_player, text='',bd=2)
    status_bar_end.grid(row=5, column=8, pady=10)

    Song_slider = ttk.Scale(music_player, from_=0, to=1, value=0, orient=HORIZONTAL,
                            length=480)
    Song_slider.grid(row=5, column=4, sticky=W, columnspan=10, pady=10)

    loop_button=Button(music_player, text='🔁',bd=2, font=('Calibri, 20'), command=loop)
    loop_button.grid(row=4, column=3)

    shuffle_button=Button(music_player, text='🔀',bd=2, font=('Calibri, 20'), command=shuffle_play)
    shuffle_button.grid(row=4, column=8)

    music_player.mainloop()

# Initialize the music player
pygame.mixer.init()

# Start the music player interface
mainpage()