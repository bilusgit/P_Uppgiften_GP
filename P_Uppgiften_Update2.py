from tkinter import *
import random

class InternaFunktioner:
    def __init__(self):  #normal beteckning för variabler som används i flera funktioner i en class
        self.trial = 0 #endast en variablel defineras här

#Addedar ett för varje försök att dra två kort
    def trial_counter(self):
        self.trial = self.trial + 1
        return self.trial

    # Från filen memo.txt importerar vi words
    def words(self):
        with open('memo', 'r', encoding='utf-8') as file:
            return file.read().split()

    # List of the imported words but they will be shuffled
    def generate_shuffled_words(self, antal_rutor):
        copies = []
        for i in range(int(antal_rutor / 2)):  # antal_rutor/2 ger double därför behövs int före
            rand_int = random.randint(0, len(self.words()) - 1)
            copies.append(self.words()[rand_int])  # Store random words in the list 'copies' from the file "memo.txt"
        copies = 2 * copies  # Since the game uses two of each word, we multiply this list by two to get
        shuffled_list = []
        # This is a way of shuffling a list
        for k in range(antal_rutor):
            temp_var = random.randint(0, len(copies) - 1)  # Generate a random intiger within a particular range
            shuffled_list.append(copies[temp_var])  # append a random word within the list to shuffled_list
            copies.pop(temp_var)
        return shuffled_list

    """
    returns how many cards will be placed. 16 cards corresponds to an easy game 
    while 36 cards corresponds to a hard game mode
    """
    def diff_level(self, boolean):
        if boolean:
            return 36, [0, 0]  # Returnerar ett plan med 36 rutor
        else:
            return 16, [75, 50]  # Returnerar ett plan med 16 rutor som centreras i mitten [75,50]



class Visuals:
    def __init__(self, interna_funktioner):
        self.interna_funktioner = interna_funktioner #klassen interna funktioner sparas för användning i den här klassen
        self.is_it_first = True
        self.shuffled_words = None
        self.buttons = []
        self.revealed_cards = []
        self.disabled_buttons = []
        self.window = None
        self.SIZE = 600  #600x600 pixlar

    #trial_disp (trial display) är en funktion som visar vilekn tur det är på windown
    def trial_disp(self):
        trial = self.interna_funktioner.trial_counter()  #turn() adderar ett till antalet försök
        print("trial: ", trial)
        label = Label(self.window, bg="lightblue", text="trial: " + str(trial))  # label containing trial number
        label.place(x=20, y=20)  # placed in the top left corner
        return trial
#notera att trial är nu en temporär variabel inom denna funktion, det är turn() som ändrar på vilekn tur det är


    # this function disables all buttons if the parameter=True or enables all buttons if the parameter=False
    def enable_buttons(self):
        for btn in self.buttons:
            # This enables the buttons functionality again
            btn.unbind("<Button-1>")

    # Function for "hiding" the text by setting text to ""
    def hide_cards(self, first_index, second_index):    #self måste vara första parametern
        self.buttons[first_index].config(text="")
        self.buttons[second_index].config(text="")

#följande kod bestämmer vad som händer om du trycker på ett kort när som helst och med alla krav som helst
    def button_command(self, button_index):
        if len(self.revealed_cards) == 2:
            """If two cards are already revealed, do nothing
            This is very crucial for avoiding bugs during the time period two cards are being shown"""
            return

        # If the player has selected no cards before, or if the player has not selected the same card twice the following code will run
        # If the player select one card twicenothing will happen since the code will not run, nor will the following
        if self.is_it_first == True or self.revealed_cards[0] != button_index: #kort som har valts är inte samma som kort som väljs
            text = self.shuffled_words[button_index]
            self.buttons[button_index].config(text=text)
            self.revealed_cards.append(button_index)
            self.is_it_first = False
#Ifall två olika och giltiga kort har valts så garanterar förra if satsen att len(revealed_cards =2), då körs:
        if len(self.revealed_cards) == 2:
            self.trial_disp()  # only happens when two cards are shown
            first_index, second_index = self.revealed_cards
            if self.shuffled_words[first_index] != self.shuffled_words[second_index]:
                # disable_or_enable_buttons(True)  # disables all buttons
                # Väntar en sekund för att gömma korten igen ifall de inte matchar
                self.buttons[first_index].after(1000, lambda: self.hide_cards(first_index, second_index))
                self.window.update()  # Crusial for allowing the text to show now that we are using time functions
                self.window.after(1000, self.enable_buttons())  # Enables all buttons after the second two cards are shown
                self.window.update()  # Same thing applies here
            else:
                self.buttons[first_index].config(state=DISABLED)  # remove their action listener
                self.buttons[second_index].config(state=DISABLED)  # remove their action listener
                self.disabled_buttons.append([self.buttons[first_index], self.buttons[second_index]])  # storing all dissabeled buttons
                # print(disabled_buttons)
            self.revealed_cards = []  # There are no revealed cards (excet the mathced ones) after the two cards have been shown
            self.is_it_first = True


    # This function will create all the cards for the game
    def create_buttons(self, antal_rutor):
        temp_array = []
        for i in range(antal_rutor):
            button = Button(
                text="",
                command=lambda counter=i: self.button_command(counter),
                # when button is pressed, it will call on button_command() function
                width=8,
                height=2,
                bg="lightblue",
                fg="black",
                font=("Helvetica", 10),  # Font, size
                # relief="raised",
            )
            temp_array.append(button)  # Store each button in an array to be returned as one
            self.buttons = temp_array
        return temp_array
    # This function will adjust the layout of the cards, hence defining their relative distances


    def layout(self, antal_rutor, centrera):  #"Centrerea" (center) is important for structural appeal
        self.shuffled_words = self.interna_funktioner.generate_shuffled_words(antal_rutor)
        buttons = self.create_buttons(antal_rutor)
        counter = 0
        y = 0
        for i in range(int(antal_rutor ** (1 / 2))):
            x = 0
            for ii in range(int(antal_rutor ** (1 / 2))):
                # adds the cards with a relative distance from each other
                buttons[counter].place(x=50 + centrera[0] + x, y=150 + centrera[1] + y)
                counter += 1
                x += 90
            y += 50


    # (Difficulty buttons) Generates two buttons, one which generates a hard game mode and one that generates an easy game mode
    def diff_buttons(self):
        button_easy = Button(
            text="Easy",
            command=lambda: self.create_layout(True),  # calls
            width=8,
            height=1,
            bg="lightblue",
            fg="black",
            font=("Helvetica", 10),
            relief="raised",
        )
        button_hard = Button(
            text="Hard",
            command=lambda: self.create_layout(False),
            width=8,
            height=1,
            bg="lightblue",
            fg="black",
            font=("Helvetica", 10),
            relief="raised",
        )
        button_easy.place(x=200, y=50)
        button_hard.place(x=400, y=50)
        return button_easy, button_hard

#Tar bort action listener av diff_buttons och sedan genererar själva memory griden med alla kort som knappar
    def create_layout(self, boolean):
        buttons = self.diff_buttons()
        if boolean:
            # Dissable the easy and hard button
            buttons[0].config(state=DISABLED)
            buttons[1].config(state=DISABLED)
            rutor = self.interna_funktioner.diff_level(False)  # amount of cards and centers, rutor = [16, [75,50]]
            self.layout(rutor[0], rutor[1])
        else:
            # Dissable the easy and hard button
            buttons[0].config(state=DISABLED)
            buttons[1].config(state=DISABLED)
            rutor = self.interna_funktioner.diff_level(True)  # rutor = [36, [0,0]]
            self.layout(rutor[0], rutor[1])

    #main function, creates window and calls diff_buttons() asking for game diffficulty
    def main(self):
        self.window = Tk()
        self.window.title("MEMORY!")
        # background color is black, while the window has dimensions of SIZE
        canvas = Canvas(self.window, width=self.SIZE, height=self.SIZE, bg="#000000")
        canvas.pack()
        img = PhotoImage(
            file="painting-mountain-lake-with-mountain-background_188544-9126.png")  # imported image as background
        canvas.create_image((self.SIZE / 2, self.SIZE / 2), image=img, state="normal", anchor="center")
        self.diff_buttons()  # Two buttons for game difficulty, pressing one will generate a game
        mainloop()


if __name__ == '__main__':
    inside = InternaFunktioner()
    outside = Visuals(inside)
    outside.main()
