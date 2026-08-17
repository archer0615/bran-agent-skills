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
