import pandas as pd

df = pd.DataFrame({
    'raw':['10x2','approx 10','7-9',]
})

s = df['raw'].astype(str).str.lower().str.strip()

numbers = (
    s.str.extractall(r'(\d+\.?\d*)')[0]
    .astype(float)
    .groupby(level=0)
    .apply(list)
)

print(numbers)