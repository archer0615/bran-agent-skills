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

### Local Orchestrator prototype

The provider-neutral local prototype is available through the Python module:

```powershell
python -m orchestrator.cli run . "<goal>"
python -m orchestrator.cli plan . "<goal>"
python -m orchestrator.cli status .
python -m orchestrator.cli artifacts .
python -m orchestrator.cli doctor .
```

It defaults to deterministic fake providers. Real providers must be configured explicitly and remain behind the Planner／Executor／Reviewer interfaces. Runtime state is stored under `.orchestrator/`, which is ignored by Git.

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

已納入的 Playbook 能力：`sop-generator`、`knowledge-base-organizing`、`option-comparison`、`project-tracking`、`human-review-workflow`、`scenario-planning`、`context-management`、`prompt-evaluation`、`ai-governance`。

## 安裝後設定

### Codex 全域「自訂指令」

在 Codex 設定的自訂指令欄位，貼上以下內容。這些規則適用於所有專案：

```text
請以繁體中文回覆，包括必要提問、進度、驗證結果與最終結論。

## 工作原則

根據使用者指令、目前專案、`AGENTS.md`、專案文件與可用 Skills，自動選擇最適合且最窄的 Skill；只有任務相關時才使用 Skill。

優先順序：

`使用者指令 → AGENTS.md → 適用 Skills → 專案文件與慣例`

遵循流程：

`Understand → Select Skill → Inspect → Modify → Verify → Correct → Report`

## Understand

指令與驗收條件清楚時直接執行。

只有缺少會實質影響範圍、限制、風險或驗收的重要資訊，且無法從專案合理判斷時，才提問。

不要為了改善措辭而重寫使用者 Prompt。

## Inspect

修改前檢查任務相關的：

- 程式碼
- `AGENTS.md`
- Skills
- 設定
- 測試
- 文件
- 既有架構與慣例

## Modify

只做最小且完整的必要修改，保留既有架構、命名、API、Dependency、Coding Style 與使用者變更。

避免無關重構、格式化、依賴升級或架構變更。

## Verify

依變更風險選擇驗證深度：

- 低風險：語法、格式或靜態檢查
- 中風險：相關測試、Lint、Type Check 或受影響範圍檢查
- 高風險：完整回歸、相容性、人工確認與 rollback 評估

單純問答、單檔案小修改或不涉及外部狀態的低風險任務，可採用精簡驗證。

不得聲稱未實際執行的命令或測試成功。

## Correct

驗證失敗時遵循：

`Identify → Fix → Re-verify`

區分本次修改造成的問題、既有問題、環境限制與未驗證項目。能安全修正就修正並重跑；否則停止擴大範圍並說明原因。

## Report

完成後簡潔回報：

- 修改內容
- 驗證結果
- 未解決問題或限制

不要重複完整推理過程。

## 安全與版本控制

除非明確要求，不要自行：

- commit
- push
- merge
- deploy
- release

避免破壞性操作、大範圍修改、資料遺失與重大相容性變更。不可逆或高風險操作前先確認。
```

### 各專案的 `AGENTS.md`

只有專案有特殊規則時才需要建立。請在專案根目錄新增 `AGENTS.md`，貼上以下範本，再依專案實際內容修改：

```markdown
# Project instructions

## Language

- 使用繁體中文回覆。
- 程式碼、變數名稱與 commit message 使用英文。

## Technology

- 使用本專案既有的套件管理工具與技術棧。
- 優先沿用現有 component、utility 與架構。

## Workflow

- 修改前先閱讀 README、相關程式碼與測試。
- 修改後執行本專案指定的測試與 build。

## Safety

- 不要提交 secrets 或修改 `.env`。
- 未經要求不要 deploy、push 或修改 production data。
```

全域自訂指令負責共通工作方式；專案 `AGENTS.md` 只負責該專案的技術棧、測試指令與特殊限制。不需要把所有 Skills 或完整 System Prompt 複製到每個專案。

## 驗證

```powershell
.\scripts\validate-skills.ps1
```

Skills 檔案維持英文，方便跨環境維護；Codex 對使用者的提問、說明、驗證結果與最終回覆，預設使用繁體中文。

目前驗證範圍包含 23 個 Skills 的 frontmatter 與必要章節、10 條代表性路由情境，以及 5 個可機器讀取的情境測試案例：

```powershell
.\scripts\validate-skills.ps1
.\scripts\validate-scenarios.ps1
.\scripts\validate-library.ps1
.\scripts\validate-powershell.ps1
.\scripts\validate-markdown.ps1
.\scripts\validate-consistency.ps1
.\scripts\prepare-release.ps1 -Version vX.Y.Z
```

## 跨電腦延續

完整的目前狀態、換電腦安裝步驟、Codex 自訂指令、專案 `AGENTS.md` 說明與下一步，請閱讀 [`references/continuation-handoff.md`](references/continuation-handoff.md)。

### 新電腦／新對話延續指令

換電腦或開啟新的 Codex 對話時，直接貼上以下內容：

```text
請閱讀 Repository 內的 references/continuation-handoff.md，接續目前 bran-agent-skills 的開發。
先檢查 git status、AGENTS.md、README.md 與目前 Skills 狀態，再依「下一步優先順序」繼續工作。
所有回覆使用繁體中文，並遵守 Repository 內的 AGENTS.md。
```

如果尚未取得 Repository，先執行：

```text
請先從 https://github.com/archer0615/bran-agent-skills 取得 Repository，閱讀 references/continuation-handoff.md，然後依文件完成安裝與狀態確認，再繼續目前工作。
```

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

## 路由情境測試

代表性路由情境與預期 Skill 順序收錄於 [`references/skill-scenarios.md`](references/skill-scenarios.md)，目前涵蓋 10 條情境，可用來檢查新增或修改 Skill 後的實際行為。

跨 Skill 的邊界檢查由 `scripts/validate-library.ps1` 執行；實際情境測試資料請參閱 [`references/scenario-test-cases.md`](references/scenario-test-cases.md)；發布前檢查清單請參閱 [`references/release-checklist.md`](references/release-checklist.md)。GitHub Actions 會在 `main` push 與 Pull Request 時自動執行五項驗證。

Windows PowerShell 可執行：

```powershell
.\scripts\validate-scenarios.ps1
```
