import datetime
import time
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivy.animation import Animation
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock
import backend

class Body(MDBoxLayout):

    """
    enreg_infos and enreg_inputs are used to cancel enregstrement...
    """
    enreg_infos = [
        "enreg_firstName_infos",
        "enreg_surname_infos",
        "enreg_lastName_infos",
        "enreg_infos"
        ]

    enreg_inputs = [
        "enreg_firstName_input",
        "enreg_surname_input",
        "enreg_lastName_input"
        ]

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    start, end = (0, 4)

    def saveRecords(self):
        prenomValue = self.ids["enreg_firstName_input"].text.capitalize()
        surnomValue = self.ids["enreg_surname_input"].text.capitalize()
        nomValue = self.ids["enreg_lastName_input"].text.capitalize()
        if prenomValue=="" or len(prenomValue)<2:
            self.ids["enreg_firstName_infos"].text = "[color=#ffff00]Le champ prénom est obligatoire...[/color]"
            Clock.schedule_once(self.hideFirstNameInfos, 3)
        elif prenomValue.isalpha()==False:
            self.ids["enreg_firstName_infos"].text = "[color=#ffff00]Le prenom ne devrait contenir que des alphabets.[/color]"
            Clock.schedule_once(self.hideFirstNameInfos, 3)
        elif nomValue=="" or len(nomValue)<2:
            self.ids["enreg_lastName_infos"].text = "[color=#ffff00]Le champ nom est obligatoire...[/color]"
            Clock.schedule_once(self.hideLastNameInfo, 3)
        elif nomValue.isalpha()==False:
            self.ids["enreg_lastName_infos"].text = "[color=#ffff00]Le nom ne devrait contenir que des alphabets.[/color]"
            Clock.schedule_once(self.hideLastNameInfo, 3)
        elif backend.DataBase.isSaved(prenomValue, surnomValue, nomValue)==True:
            self.ids["enreg_infos"].text = "[color=#ffff00]Ce nom existe déjà dans la base de donnée...[/color]"
            Clock.schedule_once(self.hideInfo, 3)
        else:
            backend.DataBase.inscription(prenomValue, surnomValue, nomValue)
            for textInput in self.enreg_inputs:
                self.ids[textInput].text = ""
            self.ids["enreg_infos"].text = "[color=#00ff00]Enregistrement réussi...[/color]"
            Clock.schedule_once(self.hideInfo, 3)

    def cancelEnregistrement(self):
        for textInput in self.enreg_inputs:
            self.ids[textInput].text = ""
        self.ids[self.enreg_infos[-1]].text = "[color=#ffff00]Enregistrement annulé[/color]"
        Clock.schedule_once(self.hideInfo, 3)

    def hideFirstNameInfos(self, event):
        self.ids["enreg_firstName_infos"].text = ""

    def hideSurNameInfo(self, event):
        self.ids["enreg_surname_infos"].text = ""
    
    def hideLastNameInfo(self, event):
        self.ids["enreg_lastName_infos"].text = ""

    def hideInfo(self, event):
        self.ids["enreg_infos"].text = ""
    
    def hideTitle(self):
        self.animation = Animation(size=(self.size[0], 0), t="in_quad")
        self.animation.start(self.ids["title"])
    
    def showTitle(self):
        self.animation = Animation(size=(self.size[0], 64), t="in_quad")
        self.animation.start(self.ids["title"])

#================================Paiement==========================================

    def getUserInfosForPaiement(self, ID):
        userID = ID
        to_be_used = list() #Used to keep the different month value for a while
        if (userID==""):
            self.ids["pFirstName"].text = ""
            self.ids["pSurname"].text = ""
            self.ids["pLastName"].text = ""
            self.hideButton()
            self.clearPaiement()
        else:
            userID = backend.DataBase.getEmployeeByID(ID)
            if (userID!=[]):
                self.ids["pFirstName"].text = f"[b]{userID[0][0]}[/b]"
                self.ids["pSurname"].text = f"[b]{userID[0][1]}[/b]"
                self.ids["pLastName"].text = f"[b]{userID[0][2]}[/b]"
                if (len(str(self.ids["year"].text))==4):
                    ID = self.ids["idForPaiement"].text
                    year = self.ids["year"].text
                    self.table = backend.DataBase.getPaiementValue(ID, year)
                    if (self.table==[]):
                        self.clearPaiement()
                        self.ids["addYear"].text = "[b]Ajouter[/b]"
                        self.ids["addYear"].size_hint = (0.5, 0.8)
                        self.ids["addYear"].bind(
                            on_press = lambda x: self.insertIntoMois(ID, year)
                        )
                    else:
                        for i in range(len(self.table[0])): #Code slow for about 2.20 seconds
                            self.ids[Body.MONTH[i]].text = str(self.table[0][i])
                else:
                    self.hideButton()
                    for i in range(len(Body.MONTH)):
                            self.ids[Body.MONTH[i]].text = ""
            else:
                self.ids["pFirstName"].text = ""
                self.ids["pSurname"].text = ""
                self.ids["pLastName"].text = ""
                self.hideButton()

    def updatePaiement(self, ID, year, mois, salaire):
        backend.DataBase.updatePaiement(ID, year, mois, salaire)

    def hideButton(self):
        self.ids["addYear"].text = ""
        self.ids["addYear"].bind(
            on_press = lambda x: None
        )


    def insertIntoMois(self, ID, year):
        checking = backend.DataBase.checkYear(ID, year)
        if checking:
            pass
        else:
            backend.DataBase.insertIntoMois(ID, year)
            self.hideButton()

    def updateSomme(self, ID):
        try:
            userID = ID
            if (userID==""):
                pass
            else:
                backend.DataBase.updateSomme(userID)
                infos = self.getSommeUpdate(userID)
                dette = self.getSommeDette(userID)
                #To avoid soustraction with None error...
                infos = 0 if infos[0][0] is None else infos[0][0] #print("Infos is different to none and numbers...")
                #To avoid soustraction with None error...
                if (dette[0][0]=="" or dette[0][0]==None):
                    dette = 0
                else:
                    dette = dette[0][0] #print("Dette is different to none and numbers...")
                #To avoid soustraction with str error...
                #dette = 0 if dette[0][0] is '' else dette[0][0]
                self.ids["paiementInfos"].text = f"[b]Total des paiements : [color=#ffff00]{infos} F[/color][/b]"
                self.ids["paiementDetteInfos"].text = f"[b]Total de dettes accordées : [color=#ffff00]{dette} F[/color][/b]"
                self.ids["paiementCaisseInfos"].text = f"[b]Total restant : [color=#ffff00]{infos-dette} F[/color][/b]"
                
                if (len(str(self.ids["year"].text))!=4):
                    self.ids["paiementInfos"].text = ""
                    self.ids["paiementInfos"].text = ""
                    self.ids["paiementDetteInfos"].text = ""
                    self.ids["paiementCaisseInfos"].text = ""
        except (IndexError, TypeError):
            #Pour les identifiants non dans la base de donnée,
            #Empeche l'ecriture dans les cases textuelles
            self.clearPaiement()

    def clearPaiement(self):
        for textInput in Body.MONTH:
            self.ids[textInput].text = ""
        self.ids["paiementInfos"].text = ""
        self.ids["paiementDetteInfos"].text = ""
        self.ids["paiementCaisseInfos"].text = ""

    def getSommeUpdate(self, ID):
        userID = ID
        result = str()
        if (userID==""):
            pass
        else:
            result = backend.DataBase.getSommeUpdate(userID)
        return result

#================================Employees==========================================
    

    def showEmployeesList(self, filtre):
        self.ids["employees_list"].clear_widgets()
        to_find = filtre.capitalize()
        employees = []
        if (to_find==""):
            pass
        else:
            employees = backend.DataBase.laListe(to_find)
        if (employees==[]):
            pass
        else:
            to_display = employees[Body.start:Body.end]
            self.limit = len(employees)
            content = list(range(len(employees)))
            for i in range(len(to_display)):
                userDateIn = self.getUserDateIn(to_display[i][0])
                content[i] = Icontent()
                content[i].ids["identifiant"].text = f"{to_display[i][0]}"
                content[i].ids["icontent_user"].text = f"[b]{to_display[i][1]} {to_display[i][2]} {to_display[i][3]}[/b]"
                content[i].ids["icontent_salaire"].text = f"[b]{userDateIn[1][2]} F CFA[/b]"
                content[i].ids["icontent_user_date"].text = f"[i]{userDateIn[1][0]}[/i]"
                content[i].ids["icontent_tuteur"].text = f"[b]{userDateIn[2][0]} {userDateIn[2][1]}[/b]"
                content[i].ids["icontent_tuteur_contact"].text = f"[b]{userDateIn[2][2]}[/b]"
                content[i].ids["icontent_tuteur_adress"].text = f"[i]{userDateIn[2][3]}[/i]"
                self.ids["employees_list"].add_widget(
                    content[i]
                )
                try:
                    ID = employees[i][0]
                    userDay = userDateIn[1][0].split("-")[0]
                    localtime = time.localtime()
                    today = localtime[2]
                    mois = Body.MONTH[localtime[1]-1]
                    mois_precedent = Body.MONTH[localtime[1]-2]
                    annee = localtime[0]
                    thisMonth = backend.DataBase.isPaied(ID, mois, annee)
                    query_of_pre_month = backend.DataBase.isPaied(ID, mois_precedent, annee)
                    if (userDay=="" or userDay=="00"):
                        #Enter date not defined...
                        content[i].ids["identifiant"].md_bg_color = (1, 0, 0, 1)
                        content[i].ids["identifiant"].text_color = (1, 1, 1, 1)
                    elif thisMonth==[]:
                        #Aucun paiement n'est effectue pour l'année actuelle...
                        content[i].ids["identifiant"].md_bg_color = (1, 1, 1, 1)
                        content[i].ids["identifiant"].text_color = (0, 0, 0, 1)
                    elif thisMonth[0][0]!=0:
                        #Le paiement est effectué pour le mois...
                        pass
                    elif (int(userDay)>=today and thisMonth[0][0]==0):
                        if (query_of_pre_month[0][0]!=0):
                            content[i].ids["identifiant"].md_bg_color = (1, 1, 0, 1)
                            content[i].ids["identifiant"].text_color = (0, 0, 0, 1)
                        elif (query_of_pre_month[0][0]==0):
                            content[i].ids["identifiant"].md_bg_color = (1, 1, 1, 1)
                            content[i].ids["identifiant"].text_color = (0, 0, 0, 1)
                        else:
                            pass
                    elif (int(userDay)<today and thisMonth[0][0]==0):
                        if (query_of_pre_month[0][0]!=0):
                            content[i].ids["identifiant"].md_bg_color = (1, 1, 0, 1)
                            content[i].ids["identifiant"].text_color = (0, 0, 0, 1)
                        elif (query_of_pre_month[0][0]==0):
                            content[i].ids["identifiant"].md_bg_color = (1, 1, 1, 1)
                            content[i].ids["identifiant"].text_color = (0, 0, 0, 1)
                        else:
                            pass
                    else:
                        print("Autre cas non specifier...")
                except (IndexError, ValueError):
                    pass

    def getUserDateIn(self, ID):
        userID = backend.DataBase.getEmployeeByID(ID)
        return userID
    
    def next(self):
        try:
            if (Body.end >= self.limit):
                self.ids["svt"].stat = "Desabled"
            else:
                Body.start = Body.end
                Body.end += 4
                self.showEmployeesList(self.ids.searchId.text)
        except AttributeError:
            pass

    def preview(self):
        if Body.end <= 4:
            self.ids["prv"].end = "Desabled"
        else:
            Body.end -= 4
            Body.start -= 4
            self.showEmployeesList(self.ids.searchId.text)

#================================Dette==========================================

    def getUserInfosForDette(self, ID):
        userID = ID
        if (userID==""):
            self.clearDette()
        else:
            userID = backend.DataBase.getEmployeeByID(ID)
            if (userID!=[]):
                self.ids["dFirstName"].text = f"[b]{userID[0][0]}[/b]"
                self.ids["dSurname"].text = f"[b]{userID[0][1]}[/b]"
                self.ids["dLastName"].text = f"[b]{userID[0][2]}[/b]"
            else:
                self.ids["dFirstName"].text = ""
                self.ids["dSurname"].text = ""
                self.ids["dLastName"].text = ""
                self.ids["detteMontant"].text = ""

    def setDette(self, ID):
        userID = self.ids["idForDette"].text
        montant = self.ids["detteMontant"].text
        userInfos = str()
        if (userID==""):
            self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)
        else:
            userInfos = backend.DataBase.getEmployeeByID(userID)
            if (userID=="" or userInfos==[]):
                self.ids["detteInfos"].text = "[color=#ffff00]Aucun(e) employée trouvée...[/color]"
                Clock.schedule_once(self.hideDetteInfos, 3)
            elif (userID!="" and montant.isnumeric() and userInfos!=[]):

                if (int(montant)<1000):
                    self.ids["detteInfos"].text = "[color=#ffff00]Montant inférieur à (1 000 F)[/color]"
                    Clock.schedule_once(self.hideDetteInfos, 3)
                else:
                    backend.DataBase.setDette(userID, montant)
                    self.updateSommeDette(userID)
                    self.clearDette()
                    self.ids["detteInfos"].text = "[color=#00ff00]Dette accorder avec succès...[/color]"
                    Clock.schedule_once(self.hideDetteInfos, 3)

            else:
                self.ids["detteInfos"].text = "[color=#ffff00]Montant invalide...[/color]"
                Clock.schedule_once(self.hideDetteInfos, 3)

    def updateSommeDette(self, ID):
        userID = ID
        if (userID==""):
            pass
        else:
            backend.DataBase.updateSommeDette(userID)
    
    def getSommeDette(self, ID):
        userID = ID
        result = ""
        if (userID==""):
            pass
        else:
            result = backend.DataBase.getSommeDette(userID)
        return result

    def clearDette(self):
        self.ids["idForDette"].text = ""
        self.ids["dFirstName"].text = ""
        self.ids["dSurname"].text = ""
        self.ids["dLastName"].text = ""
        self.ids["detteMontant"].text = ""
    
    def hideDetteInfos(self, instence):
        self.ids["detteInfos"].text = ""

#================================Update==========================================

    def getUserInfosForUpdate(self, ID):

        userID = ID

        self.update_ids = [
            "updatePrenom", "updateSurnom", "updateNom",
            "updateSalaire", "updateDateEntrer","UpdateDateSortir",
            "updatePrenomTuteur", "updateNomTutuer", "updateTuteurContact",
            "updateAdressTuteur"
        ]

        if (userID==""):
            self.cancelUpdate()
        else:
            userID = backend.DataBase.getEmployeeByID(ID)
            if (userID!=[]):
                self.ids["updatePrenom"].text = str(userID[0][0])
                self.ids["updateSurnom"].text = str(userID[0][1])
                self.ids["updateNom"].text = str(userID[0][2])

                self.ids["updateDateEntrer"].text = str(userID[1][0])
                self.ids["UpdateDateSortir"].text = str(userID[1][1])
                self.ids["updateSalaire"].text = str(userID[1][2])

                self.ids["updatePrenomTuteur"].text = str(userID[2][0])
                self.ids["updateNomTutuer"].text = str(userID[2][1])
                self.ids["updateTuteurContact"].text = str(userID[2][2])
                self.ids["updateAdressTuteur"].text = str(userID[2][3])
                
                self.ids["updateInfos"].text = ""
            else:
                self.ids["updateInfos"].theme_text_color = "Custom"
                self.ids["updateInfos"].text_color = (1, 1, 0, 1)
                self.ids["updateInfos"].text = "Aucun resultat..."
                self.cancelUpdate()
                Clock.schedule_once(self.hideUpdateInfos, 3)
    
    def hideUpdateInfos(self, instence):
        self.ids["updateInfos"].text = ""

    def cancelUpdate(self):
        try:
            for ids in self.update_ids:
                self.ids[ids].text = ""
        except AttributeError:
            pass
    
    def on_save(self, instance, value, date_range):
        self.ids.updateDateEntrer.text = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker() #max_date=datetime.datetime.now()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def clearUpdateID(self):
        self.ids["idToUpdate"].text = ""
        self.cancelUpdate()

    def setUpdate(self, ID):
        userID = ID
        if (userID==""):
            self.ids["updateInfos"].text = "[color=#ffff00]Veuillez entrer un identifiant...[/color]"
            Clock.schedule_once(self.hideUpdateInfos, 3)
        else:
            prenom, surnom, nom = (
                self.ids["updatePrenom"].text,
                self.ids["updateSurnom"].text,
                self.ids["updateNom"].text
            )
            date_in, date_out, salaire = (
                self.ids["updateDateEntrer"].text,
                self.ids["UpdateDateSortir"].text,
                self.ids["updateSalaire"].text
            )
            t_prenom, t_nom, t_contact, t_adress = (
                self.ids["updatePrenomTuteur"].text,
                self.ids["updateNomTutuer"].text,
                self.ids["updateTuteurContact"].text,
                self.ids["updateAdressTuteur"].text
            )
            backend.DataBase.setUpdate(
                userID, prenom, surnom, nom,
                date_in, date_out, salaire,
                t_prenom, t_nom, t_contact, t_adress
            )
            Clock.schedule_once(self.updateSuccess, 1.3)

    def updateSuccess(self, event):
        self.cancelUpdate()
        self.ids["idToUpdate"].text = ""
        self.ids["updateInfos"].text = "[color=#00ff00]Mise en jour effectuée...[/color]"
        Clock.schedule_once(self.hideUpdateInfos, 3)

class Icontent(MDBoxLayout):
    pass

class Main(MDApp):
    title = "GIE"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Body()

if __name__=="__main__":
    Main().run()