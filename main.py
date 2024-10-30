from typing import Dict
import pandas as pd
import datasource.gejala as gj
import datasource.penyakit as pk
import math

df: pd.DataFrame = pd.read_csv(
  filepath_or_buffer="penyakit-ayam.csv"
)

COL_PENYAKIT: str = "Penyakit"
# STATE for recursive
prevEntropyNum: float = 0.0
prevEntropyName: str  = ""
curNode: int = 1

KeyPenyakitYa: str = "penyakit_ya"
KeyPenyakitTidak: str = "penyakit_tidak"
KeyJumlahKasusYa: str = "jml_kasus_ya"
KeyJumlahKasusTidak: str = "jml_kasus_tidak"
KeyEntropyYa: str = "entropy_ya"
KeyEntropyTidak: str = "entropy_tidak"
KeyGain: str = "gain"

RootNode: str = "TOTAL"

AlreadyBeenCalculated: list[str] = [RootNode]

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

PENYAKIT_LIST_TOTAL: list[int] = []
TOTAL_ROW: int = df.shape[0]

for idx in pk.PENYAKIT.keys():
  jumlahKasusYa: int = df[df[COL_PENYAKIT] == idx].shape[0]
  PENYAKIT_LIST_TOTAL.append(jumlahKasusYa)

def CalculateNode(entropyNum: float, entropyName: str) -> None:
  global curNode
  global prevEntropyName
  global prevEntropyNum
  global AlreadyBeenCalculated
  
  if entropyName == prevEntropyName:
    return
  
  if entropyNum == 0.0:
    entropyNum = getEntropy(PENYAKIT_LIST_TOTAL, df.shape[0], toRound=6)
  
  nodeDict: Dict[str, Dict[str, any]] = {
    entropyName: {
      KeyPenyakitYa: [],
      KeyPenyakitTidak: [],
      KeyJumlahKasusYa: 0,
      KeyJumlahKasusTidak: 0,
      KeyEntropyYa: entropyNum,
      KeyEntropyTidak: 0.0,
      KeyGain: 0.0
    }
  }
  
  for gk, gv in gj.GEJALA.items():
    if gv in AlreadyBeenCalculated:
      continue
    
    penyakitListYa: list[int] = [getPenyakitTotal(gk, idx, ya=True) for idx in pk.PENYAKIT.keys()]
    penyakitListTidak: list[int]  = [getPenyakitTotal(gk, idx, ya=False) for idx in pk.PENYAKIT.keys()]
    
    jumlahKasusYa: int    = sum(penyakitListYa)
    jumlahKasusTidak: int = sum(penyakitListTidak)
    
    entropyYa: float    = getEntropy([x for x in penyakitListYa if x != 0], jumlahKasusYa)
    entropyTidak: float = getEntropy([x for x in penyakitListTidak if x != 0], jumlahKasusTidak)
    
    gain = round(entropyNum - (
      ((jumlahKasusYa / TOTAL_ROW) * entropyYa) +
      ((jumlahKasusTidak / TOTAL_ROW) * entropyTidak)
    ), 6)
    
    nodeDict[gv] = {
      KeyPenyakitYa: penyakitListYa,
      KeyPenyakitTidak: penyakitListTidak,
      KeyJumlahKasusYa: jumlahKasusYa,
      KeyJumlahKasusTidak: jumlahKasusTidak,
      KeyEntropyYa: entropyYa,
      KeyEntropyTidak: entropyTidak,
      KeyGain: gain
    }
    
    print(f"{gv}")
    print("-------------------------")
    if curNode == 1:
      print(f"Penyakit      (Ya)    = {penyakitListYa}")
      print(f"Penyakit      (Tidak) = {penyakitListTidak}")
      print(f"Jumlah Kasus  (Ya)    = {jumlahKasusYa}")
      print(f"Jumlah Kasus  (Tidak) = {jumlahKasusTidak}")
    print(f"Entropy       (Ya)    = {entropyYa}")
    print(f"Entropy       (Tidak) = {entropyTidak}")
    print(f"Gain                  = {gain}")
    print("-------------------------\n")
  
  entropyThatHasMaxGain: float | int = max(
    nodeDict, key=lambda k: nodeDict[k][KeyGain]
  )
  
  newRootNodeObject: Dict[str, any] = nodeDict[entropyThatHasMaxGain]
  newEntropyNumObtained: float | int = (
    newRootNodeObject[KeyEntropyYa]
    if newRootNodeObject[KeyEntropyYa] > newRootNodeObject[KeyEntropyTidak]
    else newRootNodeObject[KeyEntropyTidak]
  )
  
  print(f"[ Node {curNode} ] Entropy {entropyName} = {entropyNum}")
  print(f"[ Node {curNode} ] Gain terbesar didapatkan dari \"{entropyThatHasMaxGain}\" = {newRootNodeObject[KeyGain]}")
  print("-------------------------\n")
  
  prevEntropyName = entropyName
  prevEntropyNum = entropyNum
  
  curNode += 1
  
  AlreadyBeenCalculated.append(entropyThatHasMaxGain)
  
  CalculateNode(newEntropyNumObtained, entropyThatHasMaxGain)

CalculateNode(0.0, RootNode)