import pysmile
import pysmile_license

def setNodoDecisione(net, nome_nodo):
    net.update_beliefs()
    utilita_attese = net.get_node_value(nome_nodo)
    stati = net.get_outcome_ids(nome_nodo)

    print(f"\n--- Decisione: {nome_nodo} ---")
    for i, stato in enumerate(stati):
        print(f"{i + 1}. {stato} (Utilità Attesa: {utilita_attese[i]:.2f})")
    
    while True:
        try:
            scelta = int(input(f"Seleziona l'azione (1-{len(stati)}): ")) - 1
            if 0 <= scelta < len(stati):
                stato_scelto = stati[scelta]
                break
            print(f"Errore: inserisci un numero tra 1 e {len(stati)}.")
        except ValueError:
            print("Errore: inserisci un valore numerico.")

    net.set_evidence(nome_nodo, stato_scelto)
    net.update_beliefs()
    print(f"Decisione impostata: {stato_scelto}\n")
    return stato_scelto

def setNodoChance(net, nome_nodo):
    net.update_beliefs()
    probabilita = net.get_node_value(nome_nodo)
    stati = net.get_outcome_ids(nome_nodo)
    opzioni_valide = []
    
    print(f"\n--- Evento: {nome_nodo} ---")
    for i in range(len(stati)):
        if probabilita[i] > 0:
            opzioni_valide.append(stati[i])
            print(f"{len(opzioni_valide)}. {stati[i]} -> {probabilita[i]:.2%}")

    while True:
        try:
            scelta = int(input(f"Seleziona l'esito (1-{len(opzioni_valide)}): ")) - 1
            if 0 <= scelta < len(opzioni_valide):
                esito_scelto = opzioni_valide[scelta]
                break
            print(f"Errore: inserisci un numero tra 1 e {len(opzioni_valide)}.")
        except ValueError:
            print("Errore: inserisci un valore numerico.")
    
    net.set_evidence(nome_nodo, esito_scelto)
    net.update_beliefs()
    print(f"Evento impostato: {esito_scelto}\n")
    return esito_scelto

def mostraRisultati(net):
    valore_finale = net.get_node_value("guadagno")
    print("----- esito -----")
    print(f"Guadagno: {valore_finale[0]:.2f}")

    costo_ricerca = net.get_node_value("costo_ricerca")[0]
    costo_prototipo = net.get_node_value("costo_prototipo")[0]
    costo_produzione = net.get_node_value("costo_produzione")[0]
    vendite = net.get_node_value("vendite")[0]
    print("\n--- variabili ---")
    print(f"Costo Ricerca: {costo_ricerca:.2f}")
    print(f"Costo Prototipo: {costo_prototipo:.2f}")
    print(f"Costo Produzione: {costo_produzione:.2f}")
    print(f"Vendite: {vendite:.2f}")

net = pysmile.Network()
net.read_file("es1.xdsl")

scelta = input("Seleziona Domanda Mercato (1: alta, 2: bassa): ")
stato_scelto = "alta" if scelta == "1" else "bassa"
net.set_evidence("domanda_mercato", stato_scelto)
net.update_beliefs()
setNodoDecisione(net, "ricerca_marketing")
setNodoChance(net, "esito_ricerca")
setNodoDecisione(net,"sviluppare_prototipo")
setNodoChance(net,"qualita_prodotto")
setNodoDecisione(net,"produrre")
setNodoChance(net,"probabilita_di_profitto")

mostraRisultati(net)