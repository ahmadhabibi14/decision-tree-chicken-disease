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


# penyakitItems = df[COL_PENYAKIT]

# print(penyakitItems.items())

# for idx, gv in gangguanSyaraf.items():
#   match penyakitItems[idx]:
    

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

def getPenyakitTotal(col: str, penyakit: int, ya: bool = True) -> int:
  state: int = 1 if ya else 0
  return df[(df[col] == state) & (df[COL_PENYAKIT] == penyakit)].shape[0]

# def getGain(fields: list[int], total: int, ) -> float:

# ============================================
ENTROPY_TOTAL: float = 0.0
PENYAKIT_LIST_TOTAL: list[int] = []

for idx in pk.PENYAKIT.keys():
  jumlahKasusYa: int = df[df[COL_PENYAKIT] == idx].shape[0]
  PENYAKIT_LIST_TOTAL.append(jumlahKasusYa)

ENTROPY_TOTAL: float  = getEntropy(PENYAKIT_LIST_TOTAL, df.shape[0], toRound=6)
TOTAL_ROW: int        = df.shape[0]

print("+----------------------------+")
print(f"+ Total Kasus = {TOTAL_ROW}")
print(f"+ Entropy Total = {ENTROPY_TOTAL}")
print("+ ---------------------------+\n")

# =======================================================

for gk, gv in gj.GEJALA.items():
  penyakitListYa: list[int] = [getPenyakitTotal(gk, idx, ya=True) for idx in pk.PENYAKIT.keys()]
  penyakitListTidak: list[int]  = [getPenyakitTotal(gk, idx, ya=False) for idx in pk.PENYAKIT.keys()]
  
  jumlahKasusYa: int    = sum(penyakitListYa)
  jumlahKasusTidak: int = sum(penyakitListTidak)
  
  entropyYa: float    = getEntropy([x for x in penyakitListYa if x != 0], jumlahKasusYa)
  entropyTidak: float = getEntropy([x for x in penyakitListTidak if x != 0], jumlahKasusTidak)
  
  gain = round(ENTROPY_TOTAL - (
    ((jumlahKasusYa / TOTAL_ROW) * entropyYa) +
    ((jumlahKasusTidak / TOTAL_ROW) * entropyTidak)
  ), 6)
  
  print(f"{gv}")
  print("-------------------------")
  print(f"Penyakit      (Ya)    = {penyakitListYa}")
  print(f"Penyakit      (Tidak) = {penyakitListTidak}")
  print(f"Jumlah Kasus  (Ya)    = {jumlahKasusYa}")
  print(f"Jumlah Kasus  (Tidak) = {jumlahKasusTidak}")
  print(f"Entropy       (Ya)    = {entropyYa}")
  print(f"Entropy       (Tidak) = {entropyTidak}")
  print(f"Gain                  = {gain}")
  print("-------------------------\n")
  