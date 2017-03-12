# coding: utf-8

# **** MOISSONNAGE DE DONNÉES SUR LE SITE WEB DE L'AGENCE DE LA SANTÉ PUBLIQUE DU CANADA ****

# Objectif du script : 

    # L'Agence de la santé publique du Canada donne accès, sur son site web, à des informations concernant les subventions et les contributions supérieures 
    # à 25 000$ qu'elle a octroyé depuis 2006 (divulgations proactives). Ces informations sont accèssibles à partir de la page web suivante : 
    # http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbyperiodF?OpenView&Count=1000&ExpandAll&lang=fra&.
    # Cette page web donne accès à l'ensemble des subventions et des contributions qui ont été octroyé chaque année depuis 2006, et ce, en fonction des différents trimestres.
    
    # L'objectif du script est de recueillir l'information disponible pour chacune des subventions et des contributions octroyées par l'Agence.
    # On procédra de la manière suivante:
    #   1) Trouver l'url de chacun des « trimestres » sur cette page web : 
    #    http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbyperiodF?OpenView&Count=1000&ExpandAll&lang=fra&
    #   2) Sur la page web de chacun des «trimestres», trouver l'url du «nom du bénéficiaire»
    #    (par exemple 3e trimestre de 2016-2017 : http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbypurposeF?OpenView&RP=2016-2017~3&Start=1&Count=20&lang=fra&)
    #   3) Sur chacune des pages web du «nom du bénéficiaire», extraire les informations suivantes : nom, endroit, date, valeur, type, objectif, observations.
    #     (par exemple 3e trimestre de 2016-2017, le premier bénéficiaire est : Aboriginal Head Start Association of British Columbia. Les informations concernant ce bénéficiaire se retrouve ici :
    #       http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbydetails/15EA5794EEDB8190852580D5007229BD?OpenDocument&lang=fra&)
    #   4) Écrire le tout dans un fichier csv.

#  Avant de débuter, il faut préparer Cloud9 (3 étapes) : 

    # Étape 1 : Créer un environnement virtuel
    # virtualenv -p /usr/bin/python3 moissonnageEnv
    
    # Étape 2 : Activer l'environnement virtuel
    # source moissonnageEnv/bin/activate
    
    # Étape 3 : Ajouter les modules externes nécessaires : 
    # sudo pip install requests
    # sudo pip install BeautifulSoup4
    
# **DÉBUT DU SCRIPT PYTHON** 

# 1) Voici les importations nécessaires : 
import csv
import requests
from bs4 import BeautifulSoup

# 2) Déclaration des variables, qui contiendront l'information disponible pour chacun des bénificiaires d'une subvention ou d'une contribution :
nom = ""
endroit = ""
date = ""
valeur = ""
typeSubvention = ""
objectif = ""
observations = ""

# 3) Créer une variable de départ, contenant l'URL où se trouve l'information recherchée (liste des trimestres selon les années) :
url1 = "http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbyperiodF?OpenView&Count=1000&ExpandAll&lang=fra&"

# 4) Créer un fichier csv dans lequel l'information sera enregistrée :
#   (Cette étape comprend la création de la variable «fichier», qui contient le nom du fichier csv qui sera créé.)
fichier = "subventions-SantePublique.csv"

# 5) Faire une en-tête, afin de s'identifier : 
entetes = {
    "User-Agent":"Isabelle Neveu - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM",
    "From":"isa.neveu@hotmail.com"
}

# 6) Utiliser « Request » pour établir une connexion avec l'URL indiqué plus haut : 
#   (Cette étape comprend la création de la variable «contenu1».)
contenu1 = requests.get(url1,headers=entetes)

# 7) Demander à Beautifulsoup d'aller chercher le contenu de la page web, de l'analyser et de placer l'information dans la variable «page»:
#   (Cette étape comprend la création de la variable «page».)
page = BeautifulSoup(contenu1.text,"html.parser")

# 8) AVANT D'ENTRER DANS LES BOUCLES, créer l'en-tête des colones du fichier csv:
f = open(fichier,"a")    
final = csv.writer(f)
final.writerow(["Nom","Endroit","Date","Valeur","Type subvention","Objectif","Observations"])

# 9) **NIVEAU 1** : Créer une première boucle pour aller chercher tous les URL de chacun des trimestres de 2005-2006 à 2016-2017:
    
    # 9.1) Aller inspecter le code html de la page web. Je m'apperçois que les URL des trimestres se retrouvent tous dans un élément html <li>.

    # 9.2) Faire une boucle, afin d'aller chercher tous les <li> de cette page web et y récueillir le contenu de l'élément html <href>. 
    #      (Utiliser «find_all» pour réunir dans une liste tous les <li> de la page web de départ)
    #      (Utiliser «.a.get» pour aller chercher le contenu du <href>.)
    
    # 9.3) Créer un compteur  :
i = 0   

for trimestre in page.find_all("li"):
    if i >= 16:
        lienTrimestre = trimestre.a.get("href")
        
        # 9.4) L'URL que l'on obtient n'est pas complet. Alors, on le complète en ajoutant : http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca : 
        hyperlien1 = "http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca"+ lienTrimestre
        
        # 10) **NIVEAU 2** : Créer une deuxième boucle pour aller chercher tous les URL de chacun des «Nom du bénéficiaire» :
        
        # 10.1) Refaire les étapes 6 et 7 :
        contenu2 = requests.get(hyperlien1, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        # 10.2) Aller inspecter le code html de la page web. Je m'apperçois que les URL des «Nom du bénéficiaire» se retrouvent tous dans un
        #       élément html <tr>, puis dans un élément html <td>.
        
        # 10.3) Faire une boucle, afin d'aller chercher tous les <tr> de cette page web et y récueillir le contenu de l'élément html <href>. 
        #      (Utiliser «find_all» pour réunir dans une liste tous les <tr> de la page web.)
        #      (Utiliser «.a.get» pour aller chercher le contenu du <href>.)
        
        # 10.4) Créer un compteur  :
        j = 0
        
        for beneficiaire in page2.find_all("tr"):
            if j != 0:
                lienBeneficiaire = beneficiaire.a.get("href")
                
                #10.5) L'URL que l'on obtient n'est pas complet. Alors, on le complète en ajoutant :http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca :
                hyperlien2 = "http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca" + lienBeneficiaire

                # 11) **NIVEAU 3** : Créer une troisième boucle pour aller chercher l'information disponible sur chaque page du « Nom du bénéficiaire » :
                
                # 11.1) Refaire les étapes 6 et 7 :
                contenu3 = requests.get(hyperlien2, headers=entetes)    
                page3 = BeautifulSoup(contenu3.text,"html.parser")
                
                # 11.2) Aller inspecter le code html de la page web. Je m'apperçois que chacun des informations dont j'ai besoin se retrouvent dans un
                #       élément html <tr>, puis dans un élément html <td>.
        
                # 11.3) Faire une boucle, afin d'aller chercher tous les <tr> de cette page web et y récueillir séparément l'information se retrouvant dans les éléments
                #       html <td> de chacun des <tr>. Chacune de ces informations est contenue dans une variable (nom, endroit, date...).
                #      (Utiliser «find_all» pour réunir dans une liste tous les <tr> de la page web.)
                #      (Utiliser «.td.» pour aller chercher le contenu du <td>.)
                #      (Indiquer à chaque fois de ne rien afficher ("") si le <td> est vide (None). )
        
                # 11.4) Créer un compteur, qui permet de stocker les informations dans les bonnes variables  :
                k = 0
                
                for caracteristique in page3.find_all("tr"):
                    if k==0:
                        if caracteristique.td is not None:
                            nom = caracteristique.td.text
                        else:
                            nom = ""
                    
                    elif k==1:
                        if caracteristique.td is not None:
                            endroit = caracteristique.td.text
                        else:
                            endroit = ""
                            
                    elif k==2:
                        if caracteristique.td is not None:
                            date = caracteristique.td.text
                        else:
                            date = ""
                    
                    elif k==3:
                        if caracteristique.td is not None:
                            valeur = caracteristique.td.text
                        else:
                            valeur = ""
                            
                    elif k==4:
                        if caracteristique.td is not None:
                            typeSubvention = caracteristique.td.text
                        else:
                            typeSubvention = ""
                            
                    elif k==5:
                        if caracteristique.td is not None:
                            objectif = caracteristique.td.text
                        else:
                            objectif = ""
                            
                    elif k==6:
                        if caracteristique.td is not None:
                            observations = caracteristique.td.text
                        else:
                            observations = ""
                            
                    k = k+1
                
                # 12) **ÉCRIRE DANS LE FICHIER CSV** 
                # Inscrire l'ensemble des informations recueillies pour chacun des bénéficiaires d'une subvention ou d'une contribution dans une nouvelle ligne du fichier csv:
                final.writerow([nom,endroit,date,valeur,typeSubvention,objectif,observations])
            
            j = j+1
    i = i+1
    
    # 13) **SUIVRE LE DÉROULEMENT DANS LE TERMINAL**
    #       13.1) Afin de pouvoir suivre le déroulement (exécution du script) dans le terminal, indiquer lorsque le moissonnage de chaque «trimestre» est terminé :
    if i >= 16:
        print("Moissonnage du " + str(i-15) + "e trimestre est terminé")

# 13.2) Indiquer dans le terminal lors que l'ensemble du moissonnage est complété: 
print("Le moissonnage de la page web http://www.gcdisclosure-divulgationsc.phac-aspc.gc.ca/phac-aspc/pd-dp/gc-oc.nsf/WEBbyperiodF?OpenView&Count=1000&ExpandAll&lang=fra& est terminé")
