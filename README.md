# Harsh Thumar

**I build AI systems that sit close to money and personal data. Underneath that work is one question: how do you let an AI agent act for someone without handing it the keys?**

Founding engineer at an Indian credit-fintech startup · Ahmedabad, India
Focus: **agent identity and delegated authorization** (OAuth 2.1, token exchange, WIMSE) and **MCP security**

---

### Now

- **[mcp-auth-tamarin](https://github.com/HarshThumar/mcp-auth-tamarin)**: a formal model of MCP authorization in the Tamarin prover, built for the IETF 127 Hackathon (remote).
  - Model 01 asks one question: can an untrusted MCP server get a client to send its credentials to the wrong authorization server? The model rediscovers a published, already-fixed MCP SDK advisory on its own ([GHSA-qx49-fqc8-xw99](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-qx49-fqc8-xw99)).
  - In the vulnerable variant Tamarin finds the attack. With the fix applied, the property is proven. CI runs the proofs on every push.
  - Next: PKCE, resource indicators (RFC 8707) and issuer identification (RFC 9207), then client ID metadata documents and enterprise token exchange (ID-JAG).
- Remote participant in the IETF **OAuth** and **WIMSE** working groups; following the AAIF Identity & Trust WG.

### Production work

The rule I build by: **the model recommends, deterministic code decides, and a human signs off on anything that matters.**

The code below is private (employer and client work), so this section describes what I built. I'm happy to walk through the designs.

| What I built | How it is kept safe and correct |
|---|---|
| **A credit-appraisal API and loan-origination backend for lenders.** It takes a borrower's bank-statement, GST and credit-bureau data plus the lender's own credit-policy PDF. It runs 30+ deterministic forensic checks, then an LLM drafts the appraisal memo, citing every finding to the exact clause or cell it came from. | <ul><li>Tenants are isolated with Postgres row-level security.</li><li>Personal data is encrypted field by field (AES-256-GCM) and stays searchable through blind indexes.</li><li>The audit log is hash-chained and append-only.</li><li>LLM calls are pinned to an India region.</li><li>585 tests.</li></ul> |
| **An LLM analyst with a guarded SQL tool.** An agent answers research questions using 12 domain tools plus a read-only SQL tool. Every number in an answer has to come from a tool result. | <ul><li>Each query is parsed (sqlglot) and only a single SELECT is allowed, against a 25-table allow-list with a row limit.</li><li>It runs under a read-only DB role with a statement timeout.</li><li>Each user has a token quota.</li><li>A 30-question eval suite grades answers against live data.</li></ul> |
| **A data platform for mutual-fund research.** I was the main engineer. Scrapers cover 55 fund houses and 10+ years of data: 7.7M holdings rows, 8.6M NAV rows and 64K source documents, each with recorded provenance. | <ul><li>Every fund house passes 7 quality gates, for example holdings summing to 100% ± 0.1% and no invented IDs.</li><li>Load testing found the bottleneck. The fix cut p95 latency from 27.5 s to 1.5 s and raised throughput 9×.</li><li>CI/CD has no stored keys (Workload Identity Federation).</li></ul> |
| **An underwriting app for borrowers with informal income.** It covers 46 business types, with income methods rebuilt from a lender's Excel workbooks. | <ul><li>Golden tests check every method against the workbook's own figures.</li><li>Each number can be traced back to its source cell.</li><li>4-role access control.</li><li>The rules recommend; a credit manager signs off.</li><li>A server-side guard refuses to store personal data.</li></ul> |

<details>
<summary><b>More production work</b></summary>
<br>

- **Compliant content engine.** It writes financial posts and messages in 4 Indian languages from a fact pack. A deterministic checker re-extracts every number from the output and blocks any number that isn't in the source. A versioned rule engine checks the text, then an LLM reviewer. A spend cap and an audit trail are on throughout.
- **Multi-agent application evaluator.** CrewAI agents draft a scoring rubric and a human approves it. The agents then use retrieval over applicants' documents to score each one, with a justification for every criterion. Runs on Cloud Run and Cloud Tasks, with LangSmith tracing.
- **Document AI for project finance.** It extracts facts from PDF, DOCX and XLSX deal documents and reconciles conflicts between sources. It then drafts memoranda in which each citation points to a bounding box in the source document.
- **Real-time computer-vision edge box (team project).** I built the scoring, highlights, analytics and live-broadcast overlay layers on top of a YOLO + pose-estimation pipeline. I also packaged the GPU deployment in containers, and found a container setting that had been silently forcing inference onto the CPU.
- **Infrastructure.** I wrote Terraform for GCP: Cloud Run, private Cloud SQL, Secret Manager, Cloud Tasks, monitoring and Workload Identity Federation. I also built a cloud-agnostic backend template (AWS / Azure / GCP) with MFA, scoped JWTs and field-level encryption built in.

</details>

### Open source

- **[zero-cost-gaia-agent](https://github.com/HarshThumar/zero-cost-gaia-agent)**: a LangGraph research agent that scored **90% (18/20) on GAIA Level 1** with **$0** spent on models (free-tier Cloudflare Workers AI). It repairs malformed tool calls and takes a majority vote over 3 runs.
- **[BillExtraction](https://github.com/HarshThumar/BillExtraction)**: turns invoice PDFs into Google Sheets rows (Docling + FastAPI on Cloud Run). It uses keyless service-account impersonation, so there is no long-lived JSON key.

### Tools

Python · TypeScript · FastAPI · React / Next.js · PostgreSQL · GCP (Cloud Run, Cloud SQL, Vertex AI) · Terraform · Docker · LangGraph · CrewAI · Tamarin

### Contact

[LinkedIn](https://www.linkedin.com/in/harsh-thumar-357037251/) · harshthummar1000@gmail.com

If you work on agent authorization, MCP security or OAuth for agents, I'd like to hear from you.
