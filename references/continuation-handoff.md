# bran-agent-skills 對話交接文件

> 最後更新：2026-08-17
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
請以繁體中文與我溝通，包括提問、進度說明、驗證結果與最終回覆。

請根據目前專案、AGENTS.md、對話內容與可用 Skills，自動選擇最適合的 Skill，不要求我手動指定。

如果指令已經清楚，保留原意並直接執行；只有在缺少重要條件、限制或驗收標準時，才先進行需求釐清與指令優化。

修改前先檢查現有程式碼、測試、設定與文件，只做完成任務所需的最小修改。

修改完成後執行適當驗證，不得聲稱未實際執行的命令成功。除非我明確要求，不要自行 commit、push、merge、deploy 或 release。
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

- 23 個 Skills 已完成 frontmatter 驗證與第一輪正文補強。
- 下一階段應進行跨 Skill 一致性審查、重複能力檢查、README／交接文件同步，以及必要的實例測試。
- 目前所有修改尚未 commit；依專案規則，不應自行 commit 或 push。
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

1. 執行 `scripts/validate-skills.ps1` 並檢查所有 Skill 的結構一致性。
2. 進行相鄰 Skills 的重複與路由衝突審查。
3. 以代表性情境測試主要路由與閉環流程。
4. 同步 README、CHANGELOG 與本交接文件的狀態。
5. 由使用者決定是否 commit；本 Repository 沒有 remote 操作需求。
