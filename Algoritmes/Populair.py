import psycopg2
import datetime
import csv

c = psycopg2.connect("dbname=(naam van je database) user=postgres password=(je wachtwoord)") # Voer zelf in
cursor = c.cursor()


def populair(cursor):
    """In dit algoritme kijken we wat de meest populaire dagen van de afgelopen vijf dagen zijn"""
    with open('populair.csv', 'w', newline='') as csvout:
        fieldnames = ['productid', 'productnaam']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        now = 1548242043 # Dit is de timestamp van de laatste sessie van de website. Als de website nog aan was zou je hier
                         # om de timestamp van dit moment te vragen. Dit doe je met datetime.datetime.now(). Maar voor nu is dit beter.
        now -= 604800‬ # Hier krijgen we een timestamp van vijf dagen gelden. (432000 seconden in vijf dagen)

        cursor.execute('Select producten_id from sessies as b, product_gekocht as a where b.id = a.sessies_id and b.eindtijd > (%s)', (now, ))
        alleproducten = cursor.fetchall() # Selecteer alle producten die gekocht werden tussen vijf dagen geleden en nu.

        cursor.execute("""select id from producten""")
        producten = cursor.fetchall()

        populair = []
        optellen = []

        for i in producten:
            populair.append(i[0]) # Product_id
            optellen.append(alleproducten.count(i)) # Hoe vaak dit product voorkomt

        top = []

        for i in range(0, 20): # Stopt de meest populaire producten in 'top'
            x = optellen.index(max(optellen))
            top.append(populair[x])
            optellen.remove(optellen[x])
            populair.remove(populair[x])

        for i in top: # Bekijkt wat de naam van het product_id is en schrijft alles weg in een csv bestand
            cursor.execute("""select naam from producten where id = (%s)""", (i,))
            naam = cursor.fetchall()

            writer.writerow({
                'productid': i,
                'productnaam': naam[0][0]
            })


populair(cursor)
