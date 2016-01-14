import pandas as pd

_population = [5970688.5, 6125275.0, 6289205.5, 6439041.5,
              6570000.0, 6689700.0, 6809000.0, 6930100.0,
              7053700.0, 7180100.0, 7308800.0, 7485600.0,
              7623600.0, 7765800.0, 7910500.0, 8059500.0,
              8215700.0, 8400000.0]
print map(str,range(1998,2016))
population = {k: v for (k,v) in zip(map(str,range(1998,2016)),_population)}

# print pd.DataFrame(population)