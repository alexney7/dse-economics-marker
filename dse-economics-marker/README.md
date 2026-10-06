# DSE 經濟閱卷 Skill

面向教師、新教師及學生自評的 DSE 經濟中文卷批改流程。輸入題目、對應評分參考及答卷圖片／PDF，輸出逐點建議分、具體改進及教師待確認項；有足夠證據時提供 Level 1–5 參考估計。

## 快速使用

將整個 `dse-economics-marker` 資料夾放入 Codex 的 skills 目錄（通常為使用者目錄下 `.codex/skills`；如有設定 `CODEX_HOME`，使用該目錄內的 `skills`）。不要只複製 SKILL.md。

開新任務後可這樣說：

> 使用 $dse-economics-marker，教師模式。請批改附件中 2025 年經濟卷二第 1 題，評分參考與教材位於我的经济資料夾。列出學生證據、逐點建議分及需要我確認的地方。

學生自評：

> 使用 $dse-economics-marker，學生模式。根據我提供的題目與評分標準批改，解釋失分原因及如何補足論證。

新模考沒有細則：

> 使用 $dse-economics-marker。這是新模考題，請先建立評分細則供我確認，確認前不要給正式分數。

教師裁定續接：

> 裁定 T02：學生此處寫的是「供應減少」，不是「需求減少」。請依原評分參考更新相關得分點，其他疑點繼續待確認。

## 接入你的本地資料

此套件不附教材、官方試卷、學生答卷或教材全文 OCR。可以直接在對話提供路徑／附件，也可以在 skill 根目錄建立 `library.local.json`：

```json
{"root": "D:/你的資料/经济"}
```

也可設環境變量 `ECON_MARKER_LIBRARY`。該路徑指向包含 `经济学教材` 和 `dse經濟真题` 的「经济」資料夾。

檢查目錄匹配（在 skill 資料夾執行；python 指 Python 3.10+ 解譯器）：

```powershell
python scripts/check_library.py --root "D:/你的資料/经济"
```

此檢查只證明索引文件存在，**不代表每年評分材料完整或內容已全面核實**。新題可直接提供題目和細則，不受 2021–2025 索引限制。

## PDF 輔助工具

如果執行環境已能直接讀圖或 PDF，可不安裝這個依賴。需要本地渲染時：

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe scripts/pdf_pages.py inspect --pdf "D:/資料/試卷.pdf"
.venv/Scripts/python.exe scripts/pdf_pages.py render --pdf "D:/資料/試卷.pdf" --pages 1,3-5 --out "work/batch-01"
```

PDF 頁碼由 1 起算，與印刷頁碼可能不同。若畫面方向錯誤，在新的輸出資料夾重跑並加 `--rotation 0`、`90`、`180` 或 `270`，查看結果後選正確方向。工具不改原檔，不覆蓋已有輸出，不提供 OCR；圖像內容仍需模型或其他可用 OCR 工具閱讀並核對。

## 第一版的實際範圍

- 已有：完整閱卷指令、教師裁定流程、50 份本地文件清單、七冊教材的章節定位、掃描頁讀取工具及 GitHub 發布指引。
- 教材共有 1,337 個 PDF 頁面；已核對目錄與部分內容，沒有聲稱全文識別完成。
- 2023 年評分參考在本次索引目錄尚未找到；2024 年第 5(c) 必須讀取勘誤。
- 參考等級是證據比較，不是固定百分比換算，也不是官方成績；樣本比較不自行細分 5/5*/5**；另可按 DSE00 歷年 cutoff 規則提供有條件的第三方星級參考。
- 尚未完成教師逐點標註的準確率驗證。校內正式成績仍由教師逐題確認。

## GitHub 發布

詳見 [GITHUB-GUIDE.md](GITHUB-GUIDE.md)。本套件可直接作為倉庫根目錄，`SKILL.md` 留在根層。發布的是 skill 指令、工具和索引；本地資料與學生答卷留在你的電腦。

本套件未替你選定開源授權。若要允許他人修改、再發布，發布前選擇適合的授權並添加 LICENSE；本地參考材料的權利不隨 skill 的授權改變。


## 歷年 cutoff（2026-10-01 更新）

已加入 [DSE00 經濟科 2012–2026 數據與使用規則](references/cutoffs-dse00.md)，並提供 CSV／JSON。保留網站推算標記，未把第三方資料稱為官方分界。網頁滿分口徑尚未確認，因此不能直接套入原始試卷分數；完整模考可作明確假設下的歷年情景比較。
