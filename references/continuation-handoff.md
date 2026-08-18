# bran-agent-skills 對話交接文件

> 最後更新：2026-08-18
> Repository：`https://github.com/archer0615/bran-agent-skills`
> 目的：換電腦或更換 Codex 對話後，快速恢復工作上下文。

## 一、目前目標

將這個 Repository 建立成個人的 AI Capability Source of Truth，供 Codex 長期使用：

- 個人 AI 任務路由
- Prompt 管理
- Agent Skills 管理
- Composite Skills
- Codex 專案初始化
- AI Playbook 維護
- Windows、macOS、Linux 同步
- Git 版本控制與未來公開發布

## 二、目前完成狀態

- Repository 已建立基本治理文件：`AGENTS.md`、`.codex/AGENTS.md`、`README.md`
- 已建立跨平台安裝腳本：`bootstrap/setup.ps1`、`bootstrap/setup.sh`
- 已建立 Skill 驗證工具：`scripts/validate-skills.ps1`
- 已建立 authoring 與專案 `AGENTS.md` 指引：`references/`
- 目前共有 23 個 Skills
- Skills 內容以英文維護，對使用者回覆規則為繁體中文
- Windows 安裝腳本會在無法建立 symbolic link 時使用 junction
- 重複執行安裝不會刪除實際 Skill 內容，也不應再跳出刪除確認
- 23 個 Skills 的正文已完成第一輪補強，包含觸發條件、流程、決策規則、驗證與輸出格式
- 最新驗證結果：`Validated 23 skills.`
- 最新遠端同步 commit：以 `git log` 與 `git status` 的實際結果為準
- 已建立代表性路由情境：`references/skill-scenarios.md`
- 已建立情境路由結構檢查：`scripts/validate-scenarios.ps1`
- 已建立跨 Skill 邊界檢查：`scripts/validate-library.ps1`
- 已建立 GitHub Actions 驗證流程：`.github/workflows/validate.yml`
- 已建立發布檢查清單：`references/release-checklist.md`
- 已建立具體情境測試資料：`references/scenario-test-cases.md`
- GitHub Actions 已擴充 PowerShell syntax 與 Markdown 檢查。

## 三、目前 Skills

### Core

- `closed-loop-task-solver`
- `quality-gate`

### Coding

- `requirement-refinement`
- `existing-project-takeover`
- `implementation-validator`

### Research

- `evidence-first-research`

### Knowledge

- `conversation-skill-miner`
- `prompt-curator`
- `skill-curator`
- `sop-generator`
- `knowledge-base-organizing`

### Composite

- `personal-ai-task-router`
- `ai-playbook-maintainer`
- `prompt-skill-publisher`
- `codex-project-bootstrap`
- `decision-researcher`
- `ai-governance`
- `context-management`
- `human-review-workflow`
- `option-comparison`
- `project-tracking`
- `scenario-planning`
- `prompt-evaluation`

## 四、換電腦恢復步驟

### 1. 取得 Repository

```sh
git clone https://github.com/archer0615/bran-agent-skills.git
cd bran-agent-skills
```

### 2. 安裝 Skills

Windows PowerShell：

```powershell
.\bootstrap\setup.ps1
```

macOS/Linux：

```sh
./bootstrap/setup.sh core coding research knowledge composite
```

安裝後重新啟動 Codex。

### 3. 驗證

Windows PowerShell：

```powershell
.\scripts\validate-skills.ps1
```

預期結果：`Validated 23 skills.`

## 五、Codex 全域自訂指令

在 Codex 的全域「自訂指令」貼上：

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

## 六、專案層級設定

不是每個專案都需要 `AGENTS.md`。只有專案有特殊技術棧、測試、部署或安全規則時才建立。

建議內容來源：

1. 專案 README 與設定檔
2. 現有程式碼與測試
3. 專案負責人的特殊要求
4. 本 Repository 的通用規範

範本位於：`references/project-agents.md`

## 七、目前已知狀態與限制

- 23 個 Skills 已完成 frontmatter、必要章節與 Decision rules 一致性補強。
- 已完成初步跨 Skill 路由審查，並補充至 10 條代表性情境，包含多能力請求的 handoff contract。
- 目前 Repository 在最近一次工作結束時為 clean，且已同步至 `origin/main`。
- 不要一次大量複製外部 Playbook Skills；先確認是否與現有能力重複。
- 不要把 Token、密碼、API Key、個資或機器專屬路徑寫入 Repository。

## 八、延續對話的建議開場

在新電腦或新對話貼上：

```text
請閱讀 Repository 內的 references/continuation-handoff.md，接續目前 bran-agent-skills 的開發。
先檢查 git status、AGENTS.md、README.md 與目前 Skills 狀態，再依「下一步優先順序」繼續工作。
所有回覆使用繁體中文，並遵守 Repository 內的 AGENTS.md。
```

## 九、每次工作結束前

1. 執行適當驗證
2. 更新本文件的完成狀態或下一步
3. 檢查 `git status`
4. 依使用者要求 commit／push
5. 回報 Changed、Verified、Notes

## 十、下一步優先順序

1. 以 10 條代表性情境測試主要路由與閉環流程。
2. 持續檢查新增 Skill 是否造成重複能力或路由衝突。
3. 依 `references/release-checklist.md` 進行版本化與發布。
