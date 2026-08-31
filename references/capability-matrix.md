# Capability Matrix

本矩陣是 Skill 路由與維護的摘要；各 Skill 的 `SKILL.md` 才是完整規則來源。

| Skill | 主要輸入 | 主要產物 | 不負責事項 | 可交接對象 |
|---|---|---|---|---|
| `existing-project-takeover` | Repository、目標問題 | 專案地圖、風險與基線 | 不直接猜測修改方案 | `implementation-validator` |
| `implementation-validator` | 變更、驗收條件、命令 | 驗證報告與證據 | 不做最終交付決策 | `quality-gate` |
| `requirement-refinement` | 原始需求、上下文 | 澄清需求與驗收條件 | 不直接實作 | 主要執行 Skill |
| `ai-governance` | AI 用例、資料、影響 | 風險分類與控制清單 | 不宣稱法律合規結論 | `human-review-workflow` |
| `ai-playbook-maintainer` | Repository 來源、發布面 | 同步維護報告 | 不虛構能力或直接發布 | `implementation-validator` |
| `codex-project-bootstrap` | 專案設定與指引 | 專案指引與初始化變更 | 不自行部署或發布 | `implementation-validator` |
| `context-management` | 任務狀態、證據、檔案 | 精簡狀態或交接包 | 不把未驗證狀態當成功 | `project-tracking` |
| `decision-researcher` | 決策問題、證據、選項 | 決策簡報與建議 | 不把偏好當事實 | `quality-gate` |
| `human-review-workflow` | 自動輸出、審查權限、門檻 | 審查、拒絕、升級與回滾流程 | 不取代授權人工決策 | `quality-gate` |
| `option-comparison` | 選項、標準、證據 | 比較矩陣與敏感度分析 | 不單獨負責最終治理決策 | `decision-researcher` |
| `personal-ai-task-router` | 使用者需求、上下文 | 路由與交接契約 | 不執行被選 Skill 的程序 | 主要執行 Skill |
| `project-tracking` | 更新、風險、阻塞、證據 | 狀態報告、風險與行動清單 | 不捏造進度 | `context-management` |
| `prompt-evaluation` | Prompt、測試集、輸出契約 | 測試矩陣、結果與回歸狀態 | 不負責單純文案整理 | `prompt-curator` |
| `prompt-skill-publisher` | 素材、格式、目標 | 驗證過的發布素材 | 依規格處理 | `quality-gate` |
| `scenario-planning` | 焦點問題、 горизон、變數 | 情境、訊號與穩健行動 | 不把情境當預測 | `decision-researcher` |
| `closed-loop-task-solver` | 目標、驗收條件、目前狀態 | 執行、驗證、修正閉環 | 不取代路由選擇 | `implementation-validator` |
| `quality-gate` | 最終產物、驗收條件、證據 | Ready / Not-ready 決策 | 不重複所有執行測試 | 交付或修正迴圈 |
| `conversation-skill-miner` | 對話、任務歷史 | 可重用模式或 Skill 草稿 | 不把一次性猜測定稿 | `sop-generator` |
| `knowledge-base-organizing` | 文件、筆記、連結、檢索目標 | 知識架構與維護規則 | 不靜默解決來源衝突 | `sop-generator` |
| `prompt-curator` | Prompt、版本、測試結果 | 整理或修訂後 Prompt | 不宣稱未測試的穩定性 | `prompt-evaluation` |
| `skill-curator` | Skill library、規則、驗證器 | Inventory、邊界與維護建議 | 不無記錄刪除或合併 | `implementation-validator` |
| `sop-generator` | 流程證據、受眾、完成條件 | 可交接 SOP | 不把猜測寫成規則 | `quality-gate` |
| `evidence-first-research` | 問題、範圍、時效與來源 | 可追溯研究結果 | 不提供無來源結論 | `option-comparison` / `decision-researcher` |
