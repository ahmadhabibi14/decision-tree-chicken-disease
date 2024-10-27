import datasource.gejala as gj
import datasource.penyakit as pk
import pandas as pd

df: pd.DataFrame = pd.read_csv(
  filepath_or_buffer="penyakit-ayam.csv"
)

COL_KASUS: str = "Kasus"
COL_G1: str = "G1"
COL_G2: str = "G2"
COL_G3: str = "G3"
COL_G4: str = "G4"
COL_G5: str = "G5"
COL_G6: str = "G6"
COL_G7: str = "G7"
COL_G8: str = "G8"
COL_PENYAKIT: str = "Penyakit"

# for key, value in gj.GEJALA.items():

g1 = df[df[COL_G1] == 1]

result = g1[COL_PENYAKIT].value_counts()

result