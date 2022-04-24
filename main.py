from contextlib import nullcontext
from urllib import response
import game as g
import agent as ag
import matplotlib.pylab as plt
import numpy as np
import tkinter as tk
from tkinter.messagebox import *


def plot_agent_reward(rewards):
    """ Function to plot agent's accumulated reward vs. iteration """
    plt.plot(np.cumsum(rewards))
    plt.title('Agent Cumulative Reward vs. Iteration')
    plt.ylabel('Reward')
    plt.xlabel('Episode')
    plt.show()




class GameLearning:
    def __init__(self):
        self.app = tk.Tk()  # creation de la fenêtre
        self.app.title("WELCOM TO PONG GAME")  # titre de ma fenetre
        window_height = 200
        window_width = 500
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.app.geometry("{}x{}+{}+{}".format(window_width,
                                               window_height, x_cordinate, y_cordinate))
        self.Apropos()
  

    

        # fonction qutter
    
    def Quitter(self):
     if askyesno('Confirmation', 'Êtes-vous sûr de vouloir quitter le jeu ?'):
        self.app.quit()
     else:
        showinfo('Confirmation', 'Continuer!')
# fonction a propos


    def Apropos(self):
        

        lbl_reponse = tk.Label(self.app, text="Choisir Le type De L'adversaire Qui Va Jouer Contre L'agent RL : ")
        lbl_reponse.grid(row=1, column=0, pady=5, padx=5)

        reponse = tk.Entry(self.app)  # On demande ici la saisie dans le champ
        reponse.grid(row=1, column=1, pady=5, padx=5)
        
        def start():
            self.type = reponse.get()
            if self.type == '1':
                self.game = g.Game('agentAI')
            elif self.type == '2':
                self.game = g.Game('human')
            else:
                self.game = g.Game('agentRL')
            self.game.play()

        lbl_choix_1 = tk.Label(
            self.app, text="1 . Agent IA")
        lbl_choix_1.grid(row=3, column=0, pady=0, padx=0)
        lbl_choix_2 = tk.Label(
            self.app, text="2 . Hmain   ")
        lbl_choix_2.grid(row=4, column=0, pady=0, padx=0)
        lbl_choix_3 = tk.Label(
            self.app, text="* . Agent RL")
        lbl_choix_3.grid(row=5, column=0, pady=0, padx=0)

        #Création d'un bouton start
        bouton_start = tk.Button(self.app, text="Start", command=start)
        bouton_start.grid(row=6, column=0, pady=10, padx=0)
        # On affecte le resultat de la saisi dans la variable
        


        #Création d'un bouton Quitter
        bouton_quitter = tk.Button(self.app, text="Quitter", command=self.Quitter)
        bouton_quitter.grid(row=6, column=1, pady=15, padx=5)
        
      



        self.app.mainloop()
        

        

if __name__ == '__main__':
    gl = GameLearning()
    
    
