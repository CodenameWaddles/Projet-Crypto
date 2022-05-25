import random as rd
import numpy as np
#from maths import * 
import matplotlib.pyplot as plt 
from scipy.stats import norm 


class Transaction:
    def __init__(self, val, solde, debiteur, destinataire):
        self.data = val
        self.solde = solde
        self.debiteur = debiteur
        self.destinataire = destinataire
        self.napp = 0 
        self.approved1 = None
        self.approved2 = None
        self.x = None
        self.y = None

class DAG:
    def __init__(self, n, tmax):
        f = open("database.txt", "r")
        self.liste_nom = []
        self.liste_solde = []
        line = 1
        for i in f:
          if line%3 == 1:
            self.liste_nom.append(i)
          elif line%3 == 0:
            self.liste_solde.append(i)
          line += 5
        #print(self.liste_nom)
        #print(self.liste_solde)
        self.genesis = Transaction(0, 1, 'Genesis', 'Genesis')
        self.trans = []
        self.trans.append([self.genesis])
        self.ajouter(n, tmax)
        self.afficher(n, tmax)
        f.close
    
    def afficher(self, n, tmax):
        
        plt.rcParams["figure.figsize"] = (n, tmax)
        
        """for etage in self.trans:
            for t in etage:
                print("[ Débiteur:",t.debiteur)
                print("Destinataire:",t.destinataire)
                print("Valeur de la transaction:",t.data,"]")"""
        x = []
        y = []
        colors = []

        for i in range(n):
            for j in range(len(self.trans[i])):
                x.append(i)
                y.append((((j + 1) * tmax) / (len(self.trans[i]) + 1)))
                self.trans[i][j].x = i
                self.trans[i][j].y = ((((j + 1) * tmax) / (len(self.trans[i]) + 1)))
                if self.valid(self.trans[i][j]) == True:
                	colors.append('black')
                else:	
                	colors.append('red')
        plt.scatter(x, y, c = colors)
        
        for i in range(len(self.trans)):
            #if i == 0:
                #continue
            for t in self.trans[i]:
                if t.approved1 != None:
                    plt.plot([t.x, t.approved1.x], [t.y, t.approved1.y], c="lightblue")
                if t.approved2 != None:
                    plt.plot([t.x, t.approved2.x], [t.y, t.approved2.y], c="lightblue")

    def valid(self, t):
        
        if t.data > int(t.solde) or t.solde == 0 :
            return 0
        else :
            return 1 


    def transac(self, t, n):
        
        if n<=2:
          t1 = self.genesis
          t2 = self.genesis

        else:
            t1 = self.loi_normale(self.recherche_pointes(t, n),n)
            t2 = self.loi_normale(self.recherche_pointes(t, n),n)
          #t1 = rd.choice(self.trans[rd.randint(n-3, n-2)])
          #t2 = rd.choice(self.trans[rd.randint(n-3, n-2)])
        
        if self.valid(t1) == True:
            t1.napp += 1
            t.approved1 = t1
            #print(t.approved1)

        if self.valid(t2) == True:
            t2.napp += 1
            t.approved2 = t2
            #print(t.approved2)
    
    def ajouter(self, n, tmax):
        for i in range(n):
            i+=1
            p1 = rd.randrange(len(self.liste_nom))
            p2 = rd.randrange(len(self.liste_nom))
            t = Transaction(int(rd.expovariate(1/12)+1), self.liste_solde[p1], self.liste_nom[p1], self.liste_nom[p2])
            self.trans.append([t])
            self.transac(t, i)
            for j in range(rd.randint(round(tmax/3), tmax)):
                p1 = rd.randrange(len(self.liste_nom))
                p2 = rd.randrange(len(self.liste_nom))
                p = Transaction(int(rd.expovariate(1/12)+1), self.liste_solde[p1], self.liste_nom[p1], self.liste_nom[p2])
                self.trans[i].append(p)
                self.transac(p, i)
    
    def pourcentage_solde(self, t):
        
        if t.data == 0 : 
          return 0
      
        else :
        
          ratio = int(t.solde) / int(t.data)
          
          if int(t.solde) < 1000:
            return 1
          
          else:
            return 1/ratio


    def recherche_pointes(self, t, n):

        #pointes = [self.trans[n-1], self.trans[n-2]]
        liste_pointes = self.trans[n-2] + self.trans[n-1]
        
        scores_valid = []
        
        
        for i in range(len(liste_pointes)) :
            
            rv = float(self.valid(liste_pointes[i]))
            rpc = rd.random()
            #rpc = float(self.pourcentage_solde(liste_pointes[i]))
            rdv = self.deja_validée(n)[i]

            
            scores_valid.append(int(round(rv * (200*rpc + 800*rdv))))
            

        return scores_valid
        
    

    #def f(x, sigma, mu):

    #    return (1/sigma*np.sqrt(2*np.pi)) * np.exp(-0.5* ( (x-mu)/sigma )**2)
    


    def loi_normale(self, liste_scores, n):
        
        #l = [i for i in range(10000)]
    
        nb = len(liste_scores) #est-ce qu'on prend les non validées dans le nombre de pointes dans la loi normale ?
        #Min = min(liste_scores)
        #Max = max(liste_scores)
        
    
          
        mu = sum(liste_scores)/nb 
        sigma = np.std(liste_scores, ddof = 1) + 1
        #x = l[Min:Max:10]
        
        #print("liste_scores=",liste_scores)
        domain = liste_scores 
        pdf_norm = norm.pdf(domain, loc=mu, scale=sigma)
        #plt.plot(domain, pdf_norm, color='black')
        #plt.show()

        
        prob = []
        loi = []
    
        for i in pdf_norm:
            prob.append(round(i*10000))
        
    
        for i in range(len(liste_scores)):
            for j in range(int(prob[i])):
                loi.append(liste_scores[i])
    
        score_final = rd.choice(loi)
        index = liste_scores.index(score_final)
        liste_pointes = self.trans[n-2] + self.trans[n-1]
        
    
        return liste_pointes[index]

    def deja_validée(self, n):
        
        L = []
        
        for i in self.trans[n-1]:
                
            rdv = i.napp / (len(self.trans[n-2]+self.trans[n-1]))
            
            L.append(int(rdv))
            
        for i in self.trans[n-2]:
                
            rdv = i.napp / len(self.trans[n-1])
                
            L.append(rdv)
            
        return L


A = DAG (10, 10)