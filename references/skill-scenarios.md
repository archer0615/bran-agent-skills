# Skill routing scenarios

這些情境用來檢查 Skill 的觸發與交接是否符合預期。測試重點不是要求固定措辭，而是確認路由、順序、輸出與驗證行為。

## 1. 陌生 Repository 接手

### Prompt

```text
請接手這個陌生 Repository，先了解架構、啟動方式與測試，再找出登入流程的問題。
```

### Expected route

`existing-project-takeover` → `implementation-validator` → `quality-gate`

### Required behavior

- 先讀取 README、AGENTS、設定與測試
- 先建立架構與風險摘要，再開始修改
- 修改後執行針對登入流程的驗證

## 2. 需求不完整

### Prompt

```text
幫我加一個匯出功能。
```

### Expected route

`requirement-refinement`

### Required behavior

- 釐清匯出格式、資料範圍、權限、錯誤處理與驗收條件
- 不應直接猜測完整產品行為
- 問題應限制在會改變實作或風險的事項

## 3. 研究與方案決策

### Prompt

```text
請比較三個目前可用的資料庫方案，根據成本、效能、維運與可退出性給建議。
```

### Expected route

`evidence-first-research` → `option-comparison` → `decision-researcher`

### Required behavior

- 查找目前且可追溯的來源
- 分開事實、估計、假設與判斷
- 以一致標準比較所有方案
- 說明什麼新證據會改變建議

## 4. Prompt 改善

### Prompt

```text
請檢查這個 Prompt 是否穩定，並用幾個案例測試它。
```

### Expected route

`prompt-evaluation` → `prompt-curator`

### Required behavior

- 建立代表性輸入、預期行為與失敗案例
- 檢查模糊、缺資料、對抗性與語言要求
- 只做必要的 Prompt 修改，保留原始目的

## 5. 知識轉 SOP

### Prompt

```text
請把這段對話整理成新人可以照做的 SOP。
```

### Expected route

`conversation-skill-miner` → `sop-generator` → `quality-gate`

### Required behavior

- 區分事實、決策、步驟與未確認事項
- 產出前置條件、例外處理、檢查點與完成標準
- 不把對話中的猜測寫成正式規則

## 6. 高風險 AI 流程

### Prompt

```text
請設計一個 AI 自動審核財務資料的流程。
```

### Expected route

`ai-governance` → `human-review-workflow` → `quality-gate`

### Required behavior

- 分析資料敏感度、影響程度、權限、稽核與保存
- 對高影響決策保留人工審查與升級條件
- 不直接宣稱法律或合規結論
- 包含拒絕、修正、回滾與事故處理路徑

## Review checklist

- 是否選擇最窄且足夠的 Skill
- 多個 Skill 是否依賴關係排序
- 是否保留使用者原始目的
- 是否明確標示假設與未解問題
- 是否提出可實際執行的驗證方法
- 是否使用繁體中文回覆使用者
