# Matthieu Bouveron, 22/10/2023

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

"""
 HYPOTHESES
 ----------
 - Le bien acheté fait partie du patrimoine de l'acheteur après achat
 - Le bien acheté ne perd pas de valeur entre l'achat et la fin du remboursement de l'emprunt
 - Remboursement de l'emprunt à annuité constante
 - Inflation nulle sur la période

 NOMMAGE DES VARIABLES
 ---------------------
 B Montant du bien à acheter

 alpha Répartition entre apport personnel et emprunt pour l'achat (alpha = apport_personnel / B), compris entre 0 et 1

 Ra_b Taux du compte en banque

 K Montant emprunté (principal)

 N Nombre de périodes (durée du prêt)

 P Nombre de périodes par an

 Ra_e TAEG de l'emprunt (annuel)

 Rp_e Taux périodique équivalent au TAEG
 https://www.compta-online.com/les-taux-equivalents-un-taux-annuel-mensuel-trimestriel-semestriel-ao3193

 Ap Montant des annuités périodiques fixes pour le remboursement de l'emprunt
 Ip Montant des intérêts versés lors d'une annuité (Ap = Ip + remboursement du principal pour cette période)
 https://fr.wikipedia.org/wiki/Emprunt_(finance)#L'emprunt_indivis_à_annuité_constante

"""

def compute_cost(alpha, B, Ra_b, Ra_e, N):
    K = (1-alpha)*B
    Ap = compute_periodic_payment(K, N, Ra_e)
    Rp_b = convert_annual_to_periodic(Ra_b)
    I = compute_interests(K, N, Ra_e)
    interest_rates = (1+Rp_b)**(N-np.arange(N))[:,np.newaxis]
    Iem = I * (interest_rates -1)
    if type(alpha) is float:
        print("Intérêts remboursés par annuité (€):\n", np.hstack((np.arange(N)[:,np.newaxis], I)))
        print("Intérêts manquant par annuité (€):\n", np.hstack((np.arange(N)[:,np.newaxis], Iem)))
    C = (N * Ap - K)                   # Coût de l'emprunt
##    C += np.sum(Iem, axis=0)           # Intérêts manquant à cause du montant des intérêts de l'emprunt
    C += alpha * B * ((1+Rp_b)**N-1)   # Intérêts manquant à cause de l'apport personnel
    return C

def compute_periodic_payment(K, N, Ra_e, P=12): # P=12 : mensualités
    Rp_e = convert_annual_to_periodic(Ra_e)
    Ap = K * (Rp_e)/(1-(1+Rp_e)**(-N))
    return Ap

def compute_interests(K, N, Ra_e):
    Rp_e = convert_annual_to_periodic(Ra_e)
    n = np.arange(N)[:,np.newaxis] # period indices
    Ap = compute_periodic_payment(K, N, Ra_e)
    I = (1+Rp_e)**n * (Rp_e*K-Ap) + Ap
    return I                                   # Tableau des intérêts payés pour chaque période

def convert_annual_to_periodic(Ra, P=12):
    Rp = (1+Ra)**(1/P)-1
    return Rp

def update1(val):
    global Ra_e
    # gamma is the current value of the slider
    Ra_e = loan_rate_slider.val
##    print(f"Updated loan rate : {Ra_e:%}")
    update_fig()

def update2(val):
    global N
    # N is the current value of the slider
    N = periods_slider.val
##    print(f"Updated number of periods : {N} periods")
    update_fig()

def update3(val):
    global Ra_b
    # beta is the current value of the slider
    Ra_b = account_rate_slider.val
##    print(f"Updated account rate : {Ra_b:%}")
    update_fig()

def update4(val):
    global B
    # sigma is the current value of the slider
    B = product_cost_slider.val
##    print(f"Updated purchase amount : {B:,} €".replace(',', ' '))
    update_fig()



def update_fig():
    # update curves
    cost = compute_cost(alpha, B, Ra_b, Ra_e, N)
    payment = compute_periodic_payment((1-alpha)*B, N, Ra_e)
    payment_line.set_ydata(payment)
    cost_line.set_ydata(-cost)

    # Major grid every 1000, minor ticks every 100
    x_major_ticks = np.arange(0, 1.01, 0.1)
    x_minor_ticks = np.arange(0, 1.01, 0.01)
    m = -np.mean(cost)
    s = max(abs(-np.max(cost)-m), abs(-np.min(cost)-m), 1000)
    
    if s < 2000:
        y_major_ticks = np.arange(100*np.floor((m-1.2*s)/100), 100*np.ceil((m+1.2*s)/100), 100)
        y_minor_ticks = np.arange(100*np.floor((m-1.2*s)/100), 100*np.ceil((m+1.2*s)/100), 25)
    elif s < 20000:
        y_major_ticks = np.arange(1000*np.floor((m-1.2*s)/1000), 1000*np.ceil((m+1.2*s)/1000), 1000)
        y_minor_ticks = np.arange(1000*np.floor((m-1.2*s)/1000), 1000*np.ceil((m+1.2*s)/1000), 250)
    else:
        y_major_ticks = np.arange(10000*np.floor((m-1.2*s)/10000), 10000*np.ceil((m+1.2*s)/10000), 10000)
        y_minor_ticks = np.arange(10000*np.floor((m-1.2*s)/10000), 10000*np.ceil((m+1.2*s)/10000), 2500)

    ax.set_xticks(x_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.set_yticks(y_minor_ticks, minor=True)
    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    
    ax.set_ylim([m-1.2*s, m+1.2*s])
    ax2.set_ylim([-10,1.2*np.max(payment)])
    
    ax.legend(handles=[cost_line, payment_line])
    
    fig.canvas.draw_idle()

    alpha_info = 0.5
    Ap = compute_periodic_payment((1-alpha_info)*B, N, Ra_e)
    print("\n#### NOUVELLE CONFIGURATION ###")
    print(f"Montant de l'achat : {B:.2f} €")
    print(f"Taux du compte en banque : {100*Ra_b:.2f} %")
    print(f"TAEG de l'emprunt : {100*Ra_e:.2f} %")
    print(f"{N} périodes, 12 périodes par an")
    print(f"Pour alpha = {100*alpha_info}% : \n")
    print(f"\tApport personnel : {alpha_info*B:.2f} €\n"
          f"\tMontant de l'emprunt :  {(1-alpha_info)*B:.2f} €\n"
          f"\tPaiement périodique : {Ap:.1f} €\n"
          f"\tCoût du crédit : {N*Ap - (1-alpha_info)*B:.1f} €\n"
          f"\tCoût total de l'achat sur le patrimoine: {compute_cost(alpha_info, B, Ra_b, Ra_e, N):.1f} €\n")


if __name__ == "__main__":
    # create figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    # define variables
    alpha = np.arange(0, 1, 0.001)
    Ra_b = 0.03
    Ra_e = 0.06697
    N = 24
    B = 10000

    # compute the cost (loss after N periods, relatively to situation without purchase)
    cost = compute_cost(alpha, B, Ra_b, Ra_e, N)
    payment = compute_periodic_payment((1-alpha)*B, N, Ra_e)

    # plot the curve with alpha varying
    payment_line, = ax2.plot(alpha, payment, 'g', lw=2, label="Paiement périodique")
    cost_line, = ax.plot(alpha, -cost, 'r', lw=2, label="Cout pour le patrimoine")

    # create the slider for the loan rate
    ax_slider = plt.axes([0.05, .93, 0.35, 0.02])
    loan_rate_slider = Slider(ax_slider, 'TAEG', 0.001, 0.1, valinit=Ra_e, valstep=0.001)

    # create the slider for the number of repayment periods
    ax_slider2 = plt.axes([0.05, .96, 0.35, 0.02])
    periods_slider = Slider(ax_slider2, 'Durée', 6, 15*12, valinit=N, valstep=1)

    # create the slider for the bank account rate
    ax_slider3 = plt.axes([0.50, .93, 0.35, 0.02])
    account_rate_slider = Slider(ax_slider3, 'Taux banque', 0.001, 0.1, valinit=Ra_b, valstep=0.001)

    # create the slider for the price of the good
    ax_slider4 = plt.axes([0.50, .96, 0.35, 0.02])
    product_cost_slider = Slider(ax_slider4, 'Achat', 5000, 200000, valinit=B, valstep=100)


    # call update function on slider value change
    loan_rate_slider.on_changed(update1)
    periods_slider.on_changed(update2)
    account_rate_slider.on_changed(update3)
    product_cost_slider.on_changed(update4)

    update_fig()

    
    
    ax.set_xlabel("Part de l'apport personnel")
    ax.set_ylabel("Évolution du patrimoine à la fin de la durée de l'emprunt (€)")
    ax2.set_ylabel("Montant du paiement périodique (€)")
    
    plt.show()

















