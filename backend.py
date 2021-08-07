# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 08:00:00 2020

@author: Ibrahim Kelly
@contact: hello99world99@gmail.com
"""

import sqlite3

class DataBase:
    global connection
    global curseur

    connection = sqlite3.connect("BaseDeDonnee.db")
    curseur = connection.cursor()
    
    employee_table = """CREATE TABLE IF NOT EXISTS EMPLOYEE
    (
        ID_EMPLOYEE INTEGER PRIMARY KEY AUTOINCREMENT,
        PRENOM VARCHAR(57) NULL,
        SURNOM VARCHAR(57) NULL,
        NOM VARCHAR(57) NULL
    )"""

    mois_table = """CREATE TABLE IF NOT EXISTS MOIS
    (
        ID_MOIS INTEGER,
        ANNEE INTEGER NULL,
        JANVIER INTEGER NULL DEFAULT 0,
        FEVRIER INTEGER NULL DEFAULT 0,
        MARS INTEGER NULL DEFAULT 0,
        AVRIL INTEGER NULL DEFAULT 0,
        MAI INTEGER NULL DEFAULT 0,
        JUIN INTEGER NULL DEFAULT 0,
        JUILLET INTEGER NULL DEFAULT 0,
        AOUT INTEGER NULL DEFAULT 0,
        SEPTEMBRE INTEGER NULL DEFAULT 0,
        OCTOBRE INTEGER NULL DEFAULT 0,
        NOVEMBRE INTEGER NULL DEFAULT 0,
        DECEMBRE INTEGER NULL DEFAULT 0
    )"""

    tutuer_table = """CREATE TABLE IF NOT EXISTS TUTEUR_INFOS
    (
        ID_TUTEUR_INFOS INTEGER PRIMARY KEY AUTOINCREMENT,
        T_FNAME VARCHAR(19),
        T_LNAME VARCHAR(19),
        T_NUMBER INTEGER,
        T_ADRESS VARCHAR(19)
    )"""

    date_table = """CREATE TABLE IF NOT EXISTS DATE_INFOS
    (
        ID_DATE_INFOS INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE_IN DATETIME NULL,
        DATE_OUT DATETIME NULL,
        SALAIRE DATETIME NULL
    )
    """

    dette_table = """CREATE TABLE IF NOT EXISTS DETTE
    (
        ID_DETTE INTEGER,
        MONTANT INTEGER DEFAULT 0
    )"""

    somme_table = """CREATE TABLE IF NOT EXISTS SOMME
    (
        ID_SOMME INTEGER PRIMARY KEY AUTOINCREMENT,
        TOTAL INTEGER NULL
    )"""

    somme_d_table = """CREATE TABLE IF NOT EXISTS SOMME_DETTE
    (
        ID_SOMME_DETTE INTEGER PRIMARY KEY AUTOINCREMENT,
        TOTAL INTEGER NULL
    )"""

    curseur.execute(employee_table)
    curseur.execute(mois_table)
    curseur.execute(tutuer_table)
    curseur.execute(date_table)
    curseur.execute(dette_table)
    curseur.execute(somme_table)
    curseur.execute(somme_d_table)
    connection.commit()

    def inscription(prenom, surnom, nom):
        query = """INSERT INTO EMPLOYEE(PRENOM, SURNOM, NOM)
        VALUES(?, ?, ?)"""
        curseur.execute(query, (prenom, surnom, nom))
        DataBase.insertIntoDateInfo()
        DataBase.insertIntoTuteur()
        DataBase.insertIntoSomme()
        DataBase.insertIntoSommeDette()
        connection.commit()

    def laListe(filtre_value):
        if filtre_value=="Tous":
            query = "SELECT * FROM EMPLOYEE"
            curseur.execute(query)
            rows = curseur.fetchall()
            return rows
        else:
            query = "SELECT * FROM EMPLOYEE WHERE NOM = ?"
            curseur.execute(query, (filtre_value,))
            rows = curseur.fetchall()
            return rows
    
    def isSaved(prenom, surnom, nom):
        query = "SELECT * FROM EMPLOYEE WHERE PRENOM = ? AND SURNOM = ? AND NOM = ?"
        curseur.execute(query, (prenom, surnom, nom))
        if curseur.fetchall():
            return True
        else:
            return False

    def insertIntoSomme():
        query = """INSERT INTO SOMME(TOTAL)
                VALUES(NULL)
                """
        curseur.execute(query)
        connection.commit()

    def insertIntoDateInfo():
        query = """INSERT INTO DATE_INFOS(DATE_IN, DATE_OUT, SALAIRE)
                VALUES('', '', '')
                """
        curseur.execute(query)
        connection.commit()

    def insertIntoTuteur():
        query = """INSERT INTO TUTEUR_INFOS(T_FNAME, T_LNAME, T_NUMBER, T_ADRESS)
                VALUES('', '', '', '')
                """
        curseur.execute(query)
        connection.commit()

    def insertIntoSommeDette():
        query = """INSERT INTO SOMME_DETTE(TOTAL)
                VALUES(NULL)
                """
        curseur.execute(query)
        connection.commit()
       
    def getNomListe():
        query = "SELECT DISTINCT NOM FROM EMPLOYEE"
        result = list()
        curseur.execute(query)
        rows = curseur.fetchall()
        for i in range(len(rows)):
            result.append(rows[i][0])
        result.sort()
        return result

    def getPaiementValue(ID, year):
        query = f"""SELECT JANVIER, FEVRIER, MARS, AVRIL, MAI, JUIN, JUILLET, AOUT,
                SEPTEMBRE, OCTOBRE, NOVEMBRE, DECEMBRE
                FROM MOIS
                WHERE ID_MOIS = {ID}
                AND ANNEE = {year}
                """
        curseur.execute(query)
        result = curseur.fetchall()
        return result
    
    def updatePaiement(ID, year, mois, salaire):
        if (ID=="" or len(str(year))!=4) or str(salaire)=="":
            pass
        else:
            query = f"""UPDATE MOIS SET {mois}={salaire} WHERE ID_MOIS={ID} AND ANNEE={year}
                    """
            curseur.execute(query)
            connection.commit()

    def insertIntoMois(ID, year):
        query = f"""INSERT INTO MOIS(ID_MOIS, ANNEE)
                    VALUES({ID}, {year})
                """
        curseur.execute(query)
        connection.commit()

    def checkYear(ID, year):
        query = f"""SELECT ID_MOIS, ANNEE
                    FROM MOIS
                    WHERE ID_MOIS = {ID}
                    AND ANNEE = {year}
                """
        curseur.execute(query)
        result = curseur.fetchall()
        return result
    
    def isPaied(ID, mois, year):
        query = f"""SELECT {mois}
                    FROM MOIS
                    WHERE ID_MOIS = {ID}
                    AND ANNEE = {year}
                """
        curseur.execute(query)
        result = curseur.fetchall()
        return result

    def updateSomme(id):
        query = """UPDATE SOMME
        SET TOTAL =
        (
            SELECT SUM(JANVIER)+SUM(FEVRIER)+SUM(MARS)+
                    SUM(AVRIL)+SUM(MAI)+SUM(JUIN)+
                    SUM(JUILLET)+SUM(AOUT)+SUM(SEPTEMBRE)+
                    SUM(OCTOBRE)+SUM(NOVEMBRE)+SUM(DECEMBRE)
            FROM MOIS
            WHERE ID_MOIS IS ?
        )
        WHERE ID_SOMME IS ?
                """
        curseur.execute(query, (id, id))
        connection.commit()

    def updateSommeDette(id):
        query = """UPDATE SOMME_DETTE
        SET TOTAL =
        (
            SELECT SUM(MONTANT)
            FROM DETTE
            WHERE ID_DETTE IS ?
        )
        WHERE ID_SOMME_DETTE IS ?
        """
        curseur.execute(query, (id, id))
        connection.commit()

    def getSommeUpdate(id):
        query = """SELECT TOTAL
                    FROM SOMME
                    WHERE ID_SOMME IS ?
                """
        curseur.execute(query, (id,))
        rows = curseur.fetchall()
        return rows

    def getSommeDette(id):
        query = f"""SELECT TOTAL
        FROM SOMME_DETTE
        WHERE ID_SOMME_DETTE = ?
        """
        curseur.execute(query, (id,))
        rows = curseur.fetchall()
        return rows

    def getEmployeeByID(id):
        employee_infos = f"""SELECT PRENOM, SURNOM, NOM
        FROM EMPLOYEE
        WHERE ID_EMPLOYEE = {id}
        """
        date_infos = f"""SELECT DATE_IN, DATE_OUT, SALAIRE
        FROM DATE_INFOS
        WHERE ID_DATE_INFOS = {id}
        """

        tuteur_infos = f"""SELECT T_FNAME, T_LNAME, T_NUMBER, T_ADRESS
        FROM TUTEUR_INFOS
        WHERE ID_TUTEUR_INFOS = {id}
        """

        curseur.execute(employee_infos)
        employee_infos_result = curseur.fetchall()
        curseur.execute(date_infos)
        date_infos_result = curseur.fetchall()
        curseur.execute(tuteur_infos)
        tuteur_infos_result = curseur.fetchall()
        result = employee_infos_result + date_infos_result + tuteur_infos_result
        return result

    def setDette(id, montant):
        query = """INSERT INTO DETTE(ID_DETTE, MONTANT)
                    VALUES(?, ?)
                """
        curseur.execute(query, (id, montant))
        connection.commit()


    def setUpdate(uId, uPrenom, uSurnom, uNom, uDateIn, uDateOut, uSalaire, uAdresse, uTPrenom, uTNom, uTContact):
        query = """UPDATE EMPLOYEE
        SET PRENOM = ?, SURNOM = ?, NOM = ?
        WHERE ID_EMPLOYEE = ?
        """
        query2 = """UPDATE DATE_INFOS
        SET DATE_IN = ?, DATE_OUT = ?, SALAIRE = ?
        WHERE ID_DATE_INFOS = ?
        """
        query3 = """UPDATE TUTEUR_INFOS
        SET T_FNAME = ?, T_LNAME = ?, T_NUMBER = ?, T_ADRESS = ?
        WHERE ID_TUTEUR_INFOS = ?
        """
        curseur.execute(query,(uPrenom, uSurnom, uNom, uId))
        curseur.execute(query2, (uDateIn, uDateOut, uSalaire, uId))
        curseur.execute(query3, (uAdresse, uTPrenom, uTNom, uTContact, uId))
        connection.commit()

if __name__ == "__main__":
    launch = DataBase()