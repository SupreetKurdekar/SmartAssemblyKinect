import graph_utils as gUtils


parts = ["L","R","C","M","T","S","E"]
feasible_edges = [("L","R"),("L","C"),("C","R"),("L","T"),("T","R"),("L","E"),("R","E"),("T","S"),("L","M"),("R","M")]

gUtils.get_AO_graph(parts,feasible_edges)
