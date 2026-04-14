import pysmile
import pysmile_license

def mostra_influenza(net, node_id):
    node_handle = net.get_node(node_id)           # prende il nodo
    ids = net.get_outcome_ids(node_handle)        # prende gli stati del nodo
    parent_handles = net.get_parents(node_handle) # prende i genitori del nodo
    params = net.get_node_definition(node_handle) # P(si),P(no) per ogni genitore
    
    print(f"\n--- Analisi per {node_id} ---")
    
    param_idx = 0                               # Indice per scorrere la lista parametri
    for p_handle in parent_handles:             # Per ogni genitore...
        p_id = net.get_node_id(p_handle)        # Prende il nome del genitore
        p_stati = net.get_outcome_ids(p_handle) # Prende gli stati del genitore
        # evidenza: lo stato del genitore se è osservato, altrimenti None
        evidenza = net.get_evidence(p_handle) if net.is_evidence(p_handle) else None
        
        for i, s_id in enumerate(p_stati): # Per ogni stato del genitore...
            current_probs = params[param_idx : param_idx + len(ids)] # Prende le probabilità corrispondenti a questo stato del genitore
            if evidenza == i: # se è uno stato osservato, mostralo
                #crazione riga
                prob_str = ""
                for j in range(len(ids)):
                    prob_str += f"{ids[j]}: {current_probs[j]:.1%}"
                    if j < len(ids) - 1:
                        prob_str += ", "
                #stampa riga
                print(f" - Poiché {p_id} è {s_id} -> Influenza: {prob_str}")
            param_idx += len(ids) # sposta l'indice per il prossimo stato del genitore

    leak_probs = params[-len(ids):] # l'ultimo valore è il leak 
    if leak_probs[0] > 0.05: 
        leak_str = ""
        for j in range(len(ids)):
            leak_str += f"{ids[j]}: {leak_probs[j]:.1%}"
            if j < len(ids) - 1:
                leak_str += ", "
        print(f" - Cause Esterne (Leak) -> Influenza: {leak_str}")

def gestisci_step(net, t_suffix=""):
    # questi sono i nomi dei nodi per questo step
    n_pos = f"Posizione{t_suffix}"
    n_tempo = f"Tempo{t_suffix}"
    n_terr = f"Terreno{t_suffix}"
    n_guasto = f"Guasto{t_suffix}"
    n_acc = f"Accuratezza{t_suffix}"
    n_pos_ril = f"Posizione_rilevata{t_suffix}"
    n_azione = f"Azione{t_suffix}"

    print(f"\n{'='*30}\n STEP {t_suffix if t_suffix else '0'}\n{'='*30}") 

    net.update_beliefs()

    # 1. Posizione del veicolo
    stati_p = net.get_outcome_ids(n_pos) # centro, destra, sinistra
    probs_p = net.get_node_value(n_pos)  # probabilità
    
    if t_suffix == "": # primo step, posizione è sicuramente centro
        print("Posizione: centro")
        net.set_evidence(n_pos, "centro")
    else: 
        print(f"\nPosizione Reale :")
        for i, s in enumerate(stati_p): # mostra le probabilità per ogni posizione (data vecchia posizione e azione scelta)
            print(f"{i+1}: {s} (Prob: {probs_p[i]:.1%})")
        scelta_p = int(input("In quale posizione si trova il veicolo? ")) - 1
        net.set_evidence(n_pos, stati_p[scelta_p]) # imposta la posizione scelta
    net.update_beliefs() 

    # 2. Tempo e Terreno
    for node_id in [n_tempo, n_terr]:
        stati = net.get_outcome_ids(node_id)     # umido, secco
        probs = net.get_node_value(node_id)      # probabilità
        print(f"\nSelezione {node_id}:")
        for i, s in enumerate(stati):            #mostra
            print(f"{i+1}: {s} (Prob: {probs[i]:.1%})")
        scelta = int(input("Scelta: ")) - 1      #seleziona
        net.set_evidence(node_id, stati[scelta]) #setta
        net.update_beliefs()                     #aggiorna

    # 3. Guasto
    mostra_influenza(net, n_guasto)    # mostra l'influenza dei vari parametri
    stati_g = net.get_outcome_ids(n_guasto)  # stati
    probs_g = net.get_node_value(n_guasto)   # probabilità
    # mostro le probabilità
    testo_prob = ""
    for i in range(len(stati_g)):
        testo_prob += f"{stati_g[i]}: {probs_g[i]:.1%}"
        if i < len(stati_g) - 1:
            testo_prob += ", "
    print(f"\nEsito Guasto (Prob. calcolata: {testo_prob})")
    
    scelta_g = int(input(f"Seleziona esito osservato (1:{stati_g[0]}, 2:{stati_g[1]}): ")) - 1
    net.set_evidence(n_guasto, stati_g[scelta_g])
    net.update_beliefs()
    
    # 4. Accuratezza
    mostra_influenza(net, n_acc)
    stati_a = net.get_outcome_ids(n_acc)
    probs_a = net.get_node_value(n_acc)
    # mostro le probabilità
    testo_acc = ""
    for i in range(len(stati_a)):
        testo_acc += f"{stati_a[i]}: {probs_a[i]:.1%}"
        if i < len(stati_a) - 1:
            testo_acc += ", "
    print(f"\nEsito Accuratezza (Prob. calcolata: {testo_acc})")
    #input, setta, aggiorna
    scelta_a = int(input(f"Seleziona esito (1:{stati_a[0]}, 2:{stati_a[1]}, 3:{stati_a[2]}): ")) - 1
    net.set_evidence(n_acc, stati_a[scelta_a])
    net.update_beliefs()

    # 5. Posizione Rilevata
    stati_r = net.get_outcome_ids(n_pos_ril)    # centro, destra, sinistra
    probs_r = net.get_node_value(n_pos_ril)     # probabilità
    print(f"\nProbabilità Posizione Rilevata:")
    for i, s in enumerate(stati_r):             # mostra
        print(f"{i+1}: {s} ({probs_r[i]:.1%})")
    ril_scelta = stati_r[int(input("Cosa leggi sul sensore? ")) - 1] # seleziona
    net.set_evidence(n_pos_ril, ril_scelta)                          # setta
    net.update_beliefs()                                             # aggiorna

    # 6. Dove andare 
    suggerimento = "Stay"
    if ril_scelta == "destra": suggerimento = "Left" # se sei a destra vai a sinistra...
    elif ril_scelta == "sinistra": suggerimento = "Right"

    stati_az = net.get_outcome_ids(n_azione) # Stay, Left, Right
    print(f"\nIl sensore indica {ril_scelta} -> Dovresti fare {suggerimento}.")
    for i, az in enumerate(stati_az): # mostra le opzioni
        print(f"{i+1}. {az}")
    net.set_evidence(n_azione, stati_az[int(input("Azione: ")) - 1]) 
    net.update_beliefs()

net = pysmile.Network()
net.read_file("Es2_Unrolled.xdsl")

for s in ["", "_1", "_2", "_3", "_4"]:
    gestisci_step(net, s)

net.update_beliefs()
print(f"\nPunteggio Totale: {net.get_node_value(net.get_node('Punteggio'))[0]:.2f}")