from rich import print
from rich.console import Console

console = Console()

MAX: int = 17.5
FINAL: int = 10

cotes: str  = input("Cotes: ")

while cotes != "":
    
    total = eval(cotes)
    nombre = cotes.count("+") + 1
    
    print (str(nombre)," cotes")
    #print ("Total:", total)
    print(f"Total: [bold]{total}[/bold]")
    
    resultat = round(total / MAX * FINAL ,1)
   
    style = "bright_green"
    if (resultat < 12):
       style ="orange1"
    elif (resultat < 10):
       style= "red1"

    console.print(" ---> " + str(resultat) + "/" + str(FINAL), style = style + " bold")

    #print (" ---> ", str(round(total / MAX * 100, 1)), "%")
    console.print(" ---> " + str(round(total / MAX * 100, 1)) + "%", style = style)
    cotes  = input("Cotes: ")
