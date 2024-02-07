import csv

with open("Elenco Movies definitivo.csv", "r", encoding="utf-8") as file:
    lettore = csv.reader(file)
    next(file)
    for elem in lettore:
        titolo_separato = elem[1][:elem[1].rfind("(")].strip()
        anno_separato = elem[1].split("(")[-1].strip(" )")
        genere_separato = elem[2].split("|")
        print(titolo_separato, anno_separato, genere_separato)
