# bran-agent-skills

我的 Codex 共用能力庫，包含任務路由、研究、Coding、Prompt 與品質驗證 Skills。

## 安裝

Windows PowerShell：

```powershell
cd "C:\Users\<你的使用者名稱>\Downloads\Bran\Git\bran-agent-skills"
.\bootstrap\setup.ps1
```

macOS/Linux：

```sh
cd /path/to/bran-agent-skills
./bootstrap/setup.sh core coding research knowledge composite
```

安裝後重新啟動 Codex。Windows 若無法建立連結，請開啟 Developer Mode 或使用系統管理員 PowerShell。

## 使用

直接用繁體中文描述工作即可，Codex 會依照對話與目前專案自動選擇 Skill：

```text
請接手這個專案，先了解架構，再修正登入問題並執行測試。
```

也可以指定 Skill：

```text
請使用 quality-gate 審查這次修改。
```

常用路由：

- 不確定要用什麼：`personal-ai-task-router`
- 接手既有專案：`existing-project-takeover`
- 需求不清楚：`requirement-refinement`
- 需要研究資料：`evidence-first-research`
- 實作完成後：`implementation-validator`
- 交付前審查：`quality-gate`

## 驗證

```powershell
.\scripts\validate-skills.ps1
```

Skills 檔案維持英文，方便跨環境維護；Codex 對使用者的提問、說明、驗證結果與最終回覆，預設使用繁體中文。

## 專案 AGENTS.md

每個專案的 `AGENTS.md` 只放該專案自己的規則，例如技術棧、測試指令、命名方式與禁止事項。不需要複製全部 Skills 或全域 System Prompt。

內容來源依序為：

1. 專案現有文件與設定，例如 README、package.json、Build 與測試設定
2. 實際程式碼與測試
3. 你對該專案的特殊要求
4. 本 Repository 的通用工程規範

可從以下範本開始：

```markdown
# Project instructions

## Language

- 使用繁體中文回覆。
- 程式碼、變數名稱與 commit message 使用英文。

## Technology

- 使用既有專案指定的套件管理工具。
- 優先沿用現有 component、utility 與架構。

## Workflow

- 修改前先閱讀 README、相關程式碼與測試。
- 修改後執行專案指定的測試與 build。

## Safety

- 不要提交 secrets 或修改 `.env`。
- 未經要求不要 deploy、push 或修改 production data。
```

若專案沒有特殊規則，可以不建立 `AGENTS.md`。

## 指令優化判斷

Codex 會先判斷指令是否已經可以直接執行：

- 指令清楚：保留原意，直接執行，不過度改寫。
- 缺少重要條件或驗收標準：使用 `requirement-refinement` 協助釐清。
- 不確定要走哪個能力：使用 `personal-ai-task-router`。

這樣可以兼顧自動優化與最低必要修改，避免每個簡單請求都被改寫成冗長 Prompt。
