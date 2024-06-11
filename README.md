# F-F

5584550 & 5585031

## Quellen
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

Extremfall für unendliche Pfade in Ford-Fulkerson mit irrationalen Kapazität (U. Zwick, The smallest networks on which the Ford–Fulkerson maximum flow procedure may fail to terminate, Theoret. Comput. Sci. 148(1) (1995),165–170. doi:10.1016/0304-3975(95)00022-O.):

   -Bei der Erstellung der 3. Instanz wurde die Logik mehrerer vom Autor gegebener Beispiele berücksichtigt.(F-F/Data/Irrelational_Kapa.json)
   -Eine spezielle rekursive Sequenz in Ford &Fulkerson verwenden, um sicherzustellen, dass die verbleibende Kapazität niemals auf null abnimmt, was dazu führt, dass der Ford-Fulkerson Algorithmus nicht terminiert.(F-F/lib/FF_irrelational_Kapazität.py)

## Verwendete Repositories:
Algorithms (https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java) von williamfiset
    - Generell dient dieser Code, in Verbindung mit dessen Code-Aufklärung auf YouTube (https://www.youtube.com/watch?v=Xu8jjJnwvxE), als essentielle Unterstützung der Implementierung des Ford-Fulkerson Algorithmus und Edmonds–Karp Algorithmus(mit BFS) sowie zum Verständnis des Codes und des Worst-Cases.
    - DFS-Umsetzung
    - Visited-Variable zur Umsetzung von DFS

Maxflow-Algorithms (https://github.com/anxiaonong/Maxflow-Algorithms/tree/master) von anxiaonong
    - Idee des Stacks für DFS


Generell wurde Copilot intensiv genutzt, um Code zu ergänzen bzw. zu generieren. Die Visualisierungen wurden durch verschiedene Prompts in ChatGPT durchgeführt. Codes abseits der Algorithmen, so z.B. für die Visualisierungen, wurden anfangs von Copilot generiert und anschließend individuell angepasst durch entsprechende Recherche in den Documentations der Libraries.

## Struktur:
Wir haben uns dazu entschieden 3 verschieden Modi zu erstellen für den F&F-Algorithmus. Alle 3 Modi berechnen den Max-Flow, dienen jedoch anderen Zwecken:
    1) **Flow:** Dient dazu, den Max-Flow in kürzest möglicher Laufzeit zu ermitteln. Es werden keine Zwischenschritte ausgegeben, um die Laufzeit zu minimieren.
    2) **Debug:** Printet die Zwischenschritte des Algorithmus, um Nachvollziehbarkeit für den Algorithmus zu gewähren.
    3) **Graph:** Speicher die Zwischenschritte in einer JSON ab, sodass Visualisierungen der Zwischenschritte erstellt werden können. Darüber hinaus wird außerdem der finale Graph abgespeichert, welcher dann auch visualisiert werden kann.

Um den Extremfall mit dem randomisierten Stack auszuführen (vgl. dazu Output_Übersicht), muss in lib/WIP_FF.py dem Kommentar bei der FordFulkerson_Debug angepasst werden; siehe dazu den passenden Code in der Datei.

## Output:
Wir haben ein Jupyter-Notebook erstellt, welches die zentralen Ergebnisse zusammenfasst --> "Output_Overview.ipynb"
