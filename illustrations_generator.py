import numpy as np
import matplotlib.pyplot as plt
from Estimateur_Cout_Emprunt import (compute_periodic_payment,
                                     compute_interests,
                                     convert_annual_to_periodic)

                                    
if __name__ == "__main__":    
    # Création de la fenêtre de visualisation
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Définition des variables
    alpha = 0
    Ra_b = 0.03
    Ra_e = 0.05085
    N = 24
    B = 10000
    
    
    # Les facteurs qui entrent en jeu dans la variation du patrimoine global
    emprunt = (1-alpha) * B
    apport = alpha * B
    Rp_b = convert_annual_to_periodic(Ra_b)

    # Pertes périodiques
    # Directement relatifs au crédit
    annuites = compute_periodic_payment(emprunt, N, Ra_e)
    montant_interets_periodiques = compute_interests(emprunt, N, Ra_e).ravel() # tableau (N,)
    amortissements_periodiques = annuites - montant_interets_periodiques # tableau (N,)


    # Total                         # revenus périodiques    # remboursement périodique
    patrimoine = apport + emprunt + annuites*np.arange(N+1) - annuites*np.arange(N+1)   
                 
    

    # Référence : patrimoine si le bien n'est pas acheté
    patrimoine_sans_achat = apport * ((1+Rp_b)**np.arange(N+1))\ # apport personnel et ses intérêts
                            + annuites*np.arange(N+1) #revenus périodiques
    
    #!!!!!!!!!!!!!!!!!!! Manque intérêts sur revenus !!!!!!!!!!!!!!!!!!!!!!!!!

    # Différence
    cout_achat = patrimoine_sans_achat[-1]-patrimoine[-1]
    
    # Génération du graphe
    bar_width = 0.2
    
    # Gains
    # Apport personnel
    ax.bar(0-3*bar_width,
           apport,
           bottom=0,
           width=bar_width, align="edge",
           color='chartreuse', label="Apport personnel")

    # Somme empruntée
    ax.bar(0-3*bar_width,
           emprunt,
           bottom=apport,
           width=bar_width, align="edge",
           color='y', label="Somme empruntée")
    
    # Valeur du bien
    ax.bar(0-2*bar_width,
           B,
           bottom=0,
           width=bar_width, align="edge",
           color='yellowgreen', label="Valeur du bien")

    # Revenus périodiques
    ax.bar(np.arange(1, N+1)-2*bar_width,
           annuites,
           bottom=0,
           width=bar_width, align="edge",
           color='forestgreen', label="Revenus")
    
    # Pertes
    # Apport personnel
    ax.bar(0-bar_width,
           apport,
           bottom=0,
           width=bar_width, align="edge",
           color='firebrick', label="Apport personnel")

    # Somme empruntée
    ax.bar(0-bar_width,
           emprunt,
           bottom=apport,
           width=bar_width, align="edge",
           color='lightcoral', label="Somme empruntée")

    # Amortissements périodiques
    ax.bar(np.arange(1, N+1)-bar_width,
           amortissements_periodiques,
           bottom=0,
           width=bar_width, align="edge",
           color='lightsalmon', label="Amortissement")

    # Paiement périodique des intérêts
    ax.bar(np.arange(1, N+1)-bar_width,
           montant_interets_periodiques,
           bottom=amortissements_periodiques,
           width=bar_width, align="edge",
           color='orangered', label="Intérêts")

    # Bilans
    # Situation avec achat
    ax.bar(np.arange(N+1),
           patrimoine,
           bottom=0,
           width=bar_width, align="edge",
           color='royalblue', label="Patrimoine")
    
    # Situation sans achat
    ax.bar(np.arange(N+1)+bar_width,
           patrimoine_sans_achat,
           bottom=0,
           width=bar_width, align="edge",
           color='mediumturquoise',
           label="Patrimoine sans achat")



    ax.set_title("Variations du patrimoine au cours du remboursement de l'emprunt")
    ax.set_xlabel('Périodes')
    ax.set_ylabel('Patrimoine (€)')
    ax.legend()

    # Major grid every 1000, minor ticks every 100
    y_major_ticks = np.arange(0, B+emprunt, 1000)
    y_minor_ticks = np.arange(0, B+emprunt, 100)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    ax.set_xticks(np.arange(N+1))
    # Different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    plt.arrow(N+0.6, patrimoine_sans_achat[-1],
              0, -(patrimoine_sans_achat[-1]-patrimoine[-1]),
              length_includes_head=True,
              color="black",
              width=0.01,
              head_width=0.03,
              head_length=0.06*abs(patrimoine_sans_achat[-1]-patrimoine[-1]),
              overhang=0)
    
    plt.text(N+0.8, (patrimoine_sans_achat[-1]-patrimoine[-1])/2+patrimoine[-1],
             f"Coût: {cout_achat:.1f} €",
             fontsize="xx-small",
             rotation="horizontal",
             verticalalignment="center_baseline")
    
    plt.text(4*N/5, 9*(B+emprunt)/10,
             f"Valeur du bien: {B:.1f} €\n"
             f"Apport personnel: {apport:.1f} €\n"
             f"Somme empruntée: {emprunt:.1f} €\n"
             f"Durée: {N} mois\n"
             f"Annuités: {annuites:.1f} €\n"
             f"TAEG emprunt: {100*Ra_e:.2f} %\n"
             f"Taux livret: {100*Ra_b:.2f} %\n\n"
             f"Coût de l'achat sur le patrimoine: {cout_achat:.1f} €",
             fontsize="small",
             rotation="horizontal",
             horizontalalignment="center",
             verticalalignment="center_baseline")
    
    
    plt.show()






