# QPFP Genius

A remote MCP server that turns the Network FP QPFP ProTool Formula Bible into a
Claude **custom connector**. Any Claude user adds one URL and gets ProTool-faithful
answers — no project setup, no file uploads, no local course folder.

---

## What it exposes

| Tool | Purpose |
|---|---|
| `qpfp_operating_protocol` | Returns the answering protocol + mandatory 10-section output format. **Called first** — this is what makes the connector self-configuring. |
| `route_question` | Maps question text → ProTool number, level, session, rate convention |
| `get_protool` | Full Formula Bible entry for ProTool 1–36: cell map, live Excel formulas, conventions, verified figures |
| `list_protools` | All 36 tools by number, name, level |
| `get_convention_register` | Part 4 — the cross-tool trap register |
| `get_replication_kernel` | Part 0 — Python equivalents of Excel TVM + the four rate conventions |
| `get_case_study_answers` | Trainers Sheet answer key, per tool or full index |
| `search_formula_bible` | Full-text search (cell refs, rules, scheme terms, figures) |
| `tvm_calculate` | TVM engine with explicit convention A/B/C/D selection; returns the periodic rate used so the convention is auditable |

Plus one prepared prompt: `answer_qpfp_question`.

**Kernel validation.** `tvm_calculate` was checked against ten cached workbook
figures across ProTools 05, 10, 18, 32, 33 and 34 — all match to the rupee
(e.g. PMT 8.5% / 20y / ₹65,00,000 → −56,408.51; ProTool 32 EMI → 61,348.73).

---

## Why a tool call, not just a system prompt

A connector ships **tools**, not personality. Project instructions do not travel
with it. That is why `qpfp_operating_protocol` exists: the server's `instructions`
field tells Claude to call it first, and the tool returns the full workflow and
output format. The connector therefore configures itself in any user's account,
on any plan, with zero onboarding.

---

## Deploy (Railway — ~10 minutes)

1. Push this folder to a GitHub repo.
2. Railway → **New Project → Deploy from GitHub repo**.
3. Railway auto-detects Python, installs `requirements.txt`, runs the `Procfile`.
   No environment variables are required; `PORT` is injected.
4. Settings → Networking → **Generate Domain**.
5. Your connector URL is `https://<your-domain>.up.railway.app/mcp`

Smoke test:

```bash
curl -s -X POST https://<your-domain>.up.railway.app/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'
```

A `200` with `"serverInfo":{"name":"QPFP Genius"}` means you are live.

The transport is Streamable HTTP and the server is **authless** — Claude connects
in one click with no OAuth flow. See the security note below before you keep it that way.

---

## How a learner adds it

**Individual (Free / Pro / Max):**
Claude → **Customize → Connectors → + → Add custom** → Name `QPFP Genius`,
URL `https://<your-domain>.up.railway.app/mcp` → **Add** → **Connect**.

Free-plan users are limited to one custom connector.

**Team / Enterprise:** only an Owner or Primary Owner can add a custom connector
to the organization, via Organization Settings → Connectors. Members then enable it
individually from Customize → Connectors.

**Mobile:** iOS and Android can *use* a connector already added on claude.ai, but
cannot add new ones.

---

## Network requirement

Claude connects to your server **from Anthropic's cloud**, not from the learner's
device — true on claude.ai, Desktop, Cowork and mobile alike. The server must be
reachable over the public internet from Anthropic's IP ranges. A Railway public
domain satisfies this. A server behind a VPN or corporate firewall will not connect
even if it works on your own machine.

---

## Security and IP note — read before publishing

`data/formula_bible.md` carries Trainers Sheet worked answers and Case Study answer
keys, marked internal use. An authless public URL is, functionally, publishing that
answer key to the internet — anyone who learns the URL can query it.

Three options, in ascending control:

1. **Public, trimmed** — remove `get_case_study_answers` and the Case Study lines
   from the Bible before deploy. Keeps the formula engine open, keeps the answer key closed.
2. **Gated** — put the server behind OAuth (Claude supports the 6/18 auth spec and
   Dynamic Client Registration) or a simple bearer token issued only to enrolled
   Batch 15 learners. Preserves full fidelity and makes the connector an enrolment benefit.
3. **Org-internal** — Owner adds it to the Network FP Team/Enterprise workspace only.
   Trainer tool, not learner tool.

Get written sign-off from Network FP Knowledge Solutions on which tier ships before
the URL leaves your machine.

---

## Updating content

Edit `data/formula_bible.md` or `data/operating_protocol.md` and push. Railway
redeploys; learners pick up the change on their next call with no action.

Claude has no in-place edit for a custom connector — if the **URL** changes, users
must remove and re-add it. Treat the domain as permanent from day one.
