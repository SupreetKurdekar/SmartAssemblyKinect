import graph_utils as gUtils


parts = ["F","Tc","Tp","Bc","Bm","L","Tm","S"]
feasible_edges = [("F","Tc"),("F","Tp"),("Fb","Bc"),("F","Bm"),("F","Tm"),("Tm","S"),("Tm","L"),("Bm","S"),("Bm","L")]

gUtils.get_AO_graph(parts,feasible_edges)
