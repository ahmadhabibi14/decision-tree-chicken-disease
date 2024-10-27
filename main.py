import pandas as pd
import datasource.gejala as gj
import datasource.penyakit as pk
import math

df: pd.DataFrame = pd.read_csv(
  filepath_or_buffer="penyakit-ayam.csv"
)

# df.index = df.index + 1

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

# row2: pd.Series = df.iloc[1]

# print(row2[COL_G2])

# for idx, row in df.iterrows():
#   print(f"Index: {idx}")
#   print(row)  # Access each row's data as a Series
#   print("------") 

# g1 = df[df[COL_G1] == 1]

# print(g1)

# result = filtered_df['Penyakit'].value_counts()

def getEntropy(daftarPenyakit: list[int], jumlahKasus: int, toRound: int = 6) -> float:
  """
  Hitung entropy dari penyakit berdasarkan gejala.
    
  Args:
    daftarPenyakit (list[int]): daftar penyakit yang didapatkan dari sebuah kolom
    jumlahKasus (int): total berapa gejala yang ada atau bernilai 1
  
  Returns:
    float: entropy hasil dari: Entropy(S) = - Σ pi * log2(pi)
  """
  
  entropyRaw: float = 0.0
  
  for penyakit in daftarPenyakit:
    entropyRaw += (-penyakit / jumlahKasus * math.log2(penyakit / jumlahKasus))
  
  return round(entropyRaw, toRound)

penyakit = df[COL_PENYAKIT]

ENTROPY_TOTAL: float = 0.0
PENYAKIT_LIST_TOTAL: list[int] = []

for pk, pv in pk.PENYAKIT.items():
  jumlahKasusYa: int = df[df[COL_PENYAKIT] == pk].shape[0]
  PENYAKIT_LIST_TOTAL.append(jumlahKasusYa)

ENTROPY_TOTAL = getEntropy(PENYAKIT_LIST_TOTAL, df.shape[0], toRound=9)
print(f"Entropy Total = {ENTROPY_TOTAL}")
print("-------------------------\n")

for gk, gv in gj.GEJALA.items():  
  gejalaYa: pd.DataFrame    = df[df[gk] == 1]
  gejalaTidak: pd.DataFrame = df[df[gk] == 0]
  
  jumlahKasusYa: int    = (df[gk] == 1).sum()
  jumlahKasusTidak: int = (df[gk] == 0).sum()
  
  penyakitListYa: list[int]     = []
  penyakitListTidak: list[int]  = []
  
  for _, v in (gejalaYa[COL_PENYAKIT].value_counts()).items():
    penyakitListYa.append(v)
  
  for _, v in (gejalaTidak[COL_PENYAKIT].value_counts()).items():
    penyakitListTidak.append(v)
  
  entropyYa: float    = getEntropy(penyakitListYa, jumlahKasusYa)
  entropyTidak: float = getEntropy(penyakitListTidak, jumlahKasusTidak)
  
  print(f"{gv}")
  print("-------------------------")
  print(f"Penyakit  (Ya)      = {penyakitListYa}")
  print(f"Penyakit  (Tidak)   = {penyakitListTidak}")
  print(f"Entropy   (Ya)      = {entropyYa}")
  print(f"Entropy   (Tidak)   = {entropyTidak}")
  print("-------------------------\n")
  