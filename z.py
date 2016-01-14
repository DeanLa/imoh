from imoh import download_reports, Disease
import pandas as pd
import matplotlib.pyplot as plt
y = range(2000,2001)
w = range(1,5)
# download_reports(y,w)

# p = pd.DataFrame(data=[[9,1],[0.,2]],columns=["am","C"])
# pertussis = Disease(data=[[9,1],[0.,2]],columns=["am","C"])
p = Disease('pertussis')
d = Disease(8)

print p.name

