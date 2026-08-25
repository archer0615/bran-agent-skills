# AI Development Orchestrator V1 — Phase 01

本目錄是 `bran-agent-skills` 的 Orchestrator 架構與規格來源。Phase 01 只定義協作邊界、狀態、artifact contract、安全閘門與 Phase 02 路線；不包含 runtime、API adapter 或自動化 loop。

## Operating model

`Planner → Executor → Reviewer → Finish / Re-plan`

程式負責狀態轉移、重試上限、artifact persistence 與 gate enforcement；模型負責需求理解、分解、實作判斷與審查推理。Reviewer 必須獨立於 Executor，且只能根據 task、diff 與可重現 evidence 判定完成。

## Documents

- [Architecture](architecture.md)：角色、邊界、target repository 與 context model。
- [State machine](state-machine.md)：正式狀態、轉移、owner、輸入輸出與 retry semantics。
- [Artifact contracts](artifact-contracts.md)：Goal、Plan、Task、Execution Result、Review Result 的 JSON contract。
- [Safety and human gates](safety-and-human-gates.md)：Git policy、核准條件、失敗分類與證據規則。
- [Phase 02 plan](phase-02-plan.md)：最小 local CLI prototype 的分階段實作順序。
- [ADR 0001](adr/0001-orchestrator-boundary.md)：為何協調層不做成單一 Skill。

## Source of truth

執行中的 state 與 artifact 必須可由 target repository 的檔案及其 Git revision 重建；聊天記憶只可作為非權威 context。Target repository 的 `AGENTS.md`、README、build/test 設定與 project-specific Skills 優先於 generic defaults。
