import pandas as pd

# Make simple dataframe
df = pd.DataFrame({'Data': ('CSV', 'Pickle'), 'Type': ('text', 'binary')})

# Pickle dataframe
df.to_pickle('src/persis/data/df.pkl')
