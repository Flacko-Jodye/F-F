# F-F

Dieses Projekt orientiert sich zu großen Teilen an den folgenden Quellen:

Ford-Fulkerson Algorithm (https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs) von Alex Chumbley, Karleigh Moore, Tim Hor, Jimin Khim und Eli Ross
    - Die generelle Struktur des F&F baut auf der Struktur der Autoren auf.
    - Verschiedene Anpassungen wurden jedoch vorgenommen:
        - addEdge() wurde nicht übernommen.
        - Es wurden mehrere Modi hinzugefügt, um verschiedenen Aufgabenstellungen gerecht zu werden:
            - Flow --> Max-Flow Berechnung in kürzest möglicher Zeit
            - Debug --> Detaillierte Ausgabe der ausgeführten Aktionen des Algorithmus. Dieser Modus dient für ein besseres Verständnis.
            - Graph --> Erstellt eine JSON für jeden Zwischenschritt des Algorithmuses, um letztendlich eine Animation des Algorithmus zu erstellen
            --> Ausführung der Algorithmen in seperaten Files (X_Appl.py)
        - Viele verschiedene Auswertungen hinzugefügt: CPU-Auslastung, Speicherverbrauch, Laufzeit, etc.
        - Stack für DFS hinzugefügt, um flußvergrößernde Pfade zu erstellen.

Verwendete Repositories:
Algorithms (https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java) von williamfiset
    - Generell dient dieser Code, in Verbindung mit dessen Code-Aufklärung auf YouTube (https://www.youtube.com/watch?v=Xu8jjJnwvxE), als essentielle Unterstützung der Implementierung des Algorithmus sowie zum Verständnis des Codes.
    - DFS-Umsetzung
    - Visited-Variable zur Umsetzung von DFS

Maxflow-Algorithms (https://github.com/anxiaonong/Maxflow-Algorithms/tree/master) von anxiaonong
    - Idee des Stacks für DFS


Generell wurde Copilot intensiv genutzt, um Code zu ergänzen bzw. zu generieren. Die Visualisierungen wurden durch verschiedene Prompts in ChatGPT durchgeführt.