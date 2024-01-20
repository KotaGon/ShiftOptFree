
# プロジェクト名
シフトスケジューリング最適化の無償版
## 概要
- プロジェクトの簡潔な説明  
無償でご利用頂けるシフトスケジューリング最適化ツールになります。  
複数の従業員の休日希望を回避しながら、勤務表を作成します。  
以下、仮設定した制約条件になります。  
   - 各シフトには必要従業数を定義しており、その数の従業員が割り付く必要あります。
   - さらに、従業員は連続した勤務はできない  
  
## インストール方法
```bash
# pip install -r requirements.txt
```

## 入力情報(sample_input.csv)
| 氏名 | シフト1 | .... | シフトN |
|---------|---------|---------|---------|
| Aさん | 0 or 1 or -1 | .... | 0 or 1 or -1|
| Bさん | 0 or 1 or -1 | .... | 0 or 1 or -1|
| 必要従業員数 | 4 | .... | 5 |                  

 ※ 必要な従業員数は最終に書く  
0  : 休み希望無し  
1  :　休み希望  
-1 :　必ず休み  

## 出力情報(sample_output.csv)
| 氏名 | シフト1 | .... | シフトN |
|---------|---------|---------|---------|
| Aさん | 0 or 1 or -1 | .... | 0 or 1 or -1|
| Bさん | 0 or 1 or -1 | .... | 0 or 1 or -1|

0  : 勤務無し  
1  :　勤務  

## 実行方法
```bash
# python main.py
```
ノートブックも用意しておりますので、GoogleColaboratoryでも実行できます。　　
ノートブックをDrive上へ保存し、上から実行していけばOKです。