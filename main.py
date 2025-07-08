import os
import csv
import re
from tqdm import tqdm
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from pyfiglet import figlet_format

console = Console()


def menu():
    titre = figlet_format("DB SEARCHER", font="slant")
    console.print(Text(titre, style="bold green"))
    console.print(Panel.fit("Recherche dans le dossier 'db'", style="bold green"))

def file_detect(fichier):
    if fichier.endswith(".csv"):
        return "csv"
    elif fichier.endswith(".txt"):
        return "txt"
    elif fichier.endswith(".sql"):
        return "sql"
    else:
        return "inconnu"

def search(critere):
    chemin_dossier = "./db"
    fichiers = [f for f in os.listdir(chemin_dossier) if f.endswith((".csv", ".txt", ".sql"))]
    resultats = []

    total_lignes = 0
    for nom_fichier in fichiers:
        try:
            with open(os.path.join(chemin_dossier, nom_fichier), encoding="utf-8") as f:
                total_lignes += sum(1 for _ in f)
        except:
            continue

    with tqdm(total=total_lignes, desc="Scan en cours", ncols=70, colour="green") as pbar:
        for nom_fichier in fichiers:
            chemin = os.path.join(chemin_dossier, nom_fichier)
            type_fichier = file_detect(nom_fichier)

            try:
                with open(chemin, encoding="utf-8") as f:
                    if type_fichier == "csv":
                        reader = csv.reader(f)
                        for ligne in reader:
                            pbar.update(1)
                            if any(critere.lower() in champ.lower() for champ in ligne):
                                resultats.append((nom_fichier, ', '.join(ligne)))
                    else:
                        for ligne in f:
                            pbar.update(1)
                            if critere.lower() in ligne.lower():
                                resultats.append((nom_fichier, ligne.strip()))
            except:
                continue

    return resultats

def show_les_results(resultats, critere):
    if not resultats:
        console.print("[bold yellow]Aucun résultat trouvé.[/bold yellow]")
        return

    table = Table(title="Resultats", title_style="bold green")
    table.add_column("Fichier", style="cyan", no_wrap=True)
    table.add_column("Ligne", style="white")

    pattern = re.compile(re.escape(critere), re.IGNORECASE)

    for fichier, ligne in resultats:
        texte_ligne = Text()
        last_index = 0
        for match in pattern.finditer(ligne):
            start, end = match.span()
            texte_ligne.append(ligne[last_index:start])
            texte_ligne.append(ligne[start:end], style="bold green")
            last_index = end
        texte_ligne.append(ligne[last_index:])
        table.add_row(fichier, texte_ligne)

    console.print(table)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    menu()
    critere = Prompt.ask("Mot-clé à rechercher")
    resultats = search(critere)
    show_les_results(resultats, critere)


if __name__ == "__main__":
    main()
