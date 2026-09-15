# QPFP ProTool Formula Bible — Complete (Batch 15)

**What this is.** A portable, device-independent replacement for opening the ProTool workbooks. Every entry is the *live cell logic* extracted from the official Network FP ProTool .xlsx files — sheet, cell, exact Excel formula, and the cached value the workbook itself produced. Answering from this file reproduces the tool's figure on any device, in any Claude session, with no connected folder.

**Coverage.** All 36 sessions. 34 workbook ProTools extracted at formula level; ProTool 22 and 35 are Word templates (structure documented); ProTool 09, 11, 12, 13 are frameworks with no formulas (structure documented).

**Verification.** Every calculation tool below was independently re-computed in Python and matched the workbook's own cached result to full float precision. Figures marked *Verified* carry that guarantee.

**Status:** Internal / organisation use. Contains Trainers Sheet worked answers and Case Study answer keys.

---

# PART 0 — Replication kernel

Use these before anything else. Sign conventions matter.

```python
def FV(r,n,pmt=0.0,pv=0.0,typ=0):
    if r==0: return -(pv+pmt*n)
    return -(pv*(1+r)**n + pmt*(1+r*typ)*(((1+r)**n-1)/r))

def PV(r,n,pmt=0.0,fv=0.0,typ=0):
    if r==0: return -(fv+pmt*n)
    return -(pmt*(1+r*typ)*((1-(1+r)**-n)/r) + fv*(1+r)**-n)

def PMT(r,n,pv=0.0,fv=0.0,typ=0):
    if r==0: return -(pv+fv)/n
    return -(pv*(1+r)**n + fv)/((1+r*typ)*(((1+r)**n-1)/r))

def EFFECT(nom,n):  return (1+nom/n)**n - 1
def NOMINAL(eff,n): return n*((1+eff)**(1/n) - 1)
# RATE / NPER / IRR / XIRR: solve numerically (bisection or Newton) on the same equations.

def fy(d):   # date -> Indian financial year "YYYY-YY"
    return f"{d.year-1}-{str(d.year)[2:]}" if d.month <= 3 else f"{d.year}-{str(d.year+1)[2:]}"
```

**The four periodic-rate conventions.** These are not interchangeable, and picking the wrong one lands you on a manufactured distractor:

| Convention | Formula | Input rate is | Used by |
|---|---|---|---|
| A | `EFFECT(NOMINAL(r,I),J)/I` → `r/I` when I=J | nominal | ProTool 05, 10 |
| B | `NOMINAL(r,12)/12` | effective | ProTool 17, 18, 19, 28, 30 (EPF) |
| C | `(1+r)^(1/12) − 1` | effective | ProTool 27, 33 |
| D | plain `r/12` | nominal | ProTool 32, 33 (EMI), 34 |

---

# PART 1 — LEVEL I: Personal Finance Foundations

## ProTool 01 — The REAL Statement
**Session 01 · `ProTool 01 - Real Statement.xlsx`** · Sheets: Case Study, Trainers Sheet, Candidate Sheet

A complete cashflow + net-worth statement. Structure:

| Block | Rows | Contents |
|---|---|---|
| Income (net of tax) | 7–12 | Salary (H+W), Annual Bonus, Business, Rental, Investment income |
| Household Expenses | 17–27 | Rent, society/maintenance, food & grocery, vehicle, healthcare, utilities, domestic help, telecom, subscriptions, others |
| Lifestyle Expenses | 29–39 | Clothes, shopping, dining, personal care, travel, coaching/advisor/CA, hobbies, courses, charity, others |
| Dependent Expenses | 41–44 | Children's schooling, contribution to parents, siblings/relatives |
| Insurance Premiums | 46–49 | Life (term), health, general |
| Loan EMIs | 51–54 | Home, vehicle, other |
| Savings | 59–66 | Income − Expenses = Savings; less ongoing investments = Surplus for new investments |
| Assets & Liabilities | 70+ | Present value of assets (H + W + dependent children), liabilities, net worth |

**Formulas**
```
D7:D11  =E7/12                     ' monthly = annual / 12
E12     =SUM(E7:E11)               ' total income
F7:F66  =E7/$E$12                  ' every line as % of TOTAL INCOME (not of expenses)
E17:E64 =D17*12                    ' annual = monthly x 12
D27     =SUM(D17:D26)              ' household subtotal
D55     =D27+D39+D44+D49+D54       ' total expenses = the five expense blocks
D61     =D59-D60                   ' savings = income - expenses
D66     =D61-D65                   ' surplus = savings - ongoing investments
```
**Convention:** the `% of Income` column always divides by **total income**, so expense-block percentages are read against income, not against total expenses. *Verified (Trainer):* income ₹19,30,000 p.a. (₹1,60,833 p.m.), expenses ₹9,66,000 (₹80,500 p.m.), savings ₹9,64,000 = **49.95% savings rate**.

---

## ProTool 02 — PFP Capability Analyzer
**Session 02 · `ProTool 02 - PFP Capability Analyzer.xlsx`** · Sheets: Trainer Sheet, Candidate Sheet

Self-assessment across **30 capability areas**, each rated 1–10. Section A = Personal Finance Solutions (Retirement, Children's Education, House Purchase, Wills & Succession, Income Tax, NRI Investment & Taxation, Life Planning & Behavioural Coaching, …). Further sections cover products, practice management and client engagement. Output is a score profile identifying the candidate's development gaps. No financial mathematics — 8 aggregation formulas only.

---

## ProTool 03 — Ethics @ Heart
**Session 03 · `ProTool 03 - Ethics @ Heart - Tool.xlsx`** · Sheets: QPFP Ethics Oath, Trainer Sheet, Candidate Sheet

Personal ethics checklist built on the **ETHICS** acronym — **E**xpertise, **T**ransparency, **H**olistic, **I**ntegrity, **C**lientFirst, **S**olutions. Each pillar carries statements rated 1–10.

*Expertise (E)* — "My clients trust me for being an expert in the field of personal finance. I shall keep myself updated…" Sample statements: undergone a professional education program on managing personal finance holistically; proactively update on new products & market changes; keep acquiring/sharpening skills.

The `QPFP Ethics Oath` sheet is the signable declaration: *"As a Qualified Personal Finance Professional, I shall follow & abide by the following Code of Ethics and Professional Responsibility."* Cite this sheet for any ethics-code MCQ.

---

## ProTool 04 — Financial Health Indicators
**Session 04 · `ProTool 04 - Financial Health Indicators.xlsx`**

**Seven ratios. All use the same formula `E = D(numerator) / D(denominator)`. Memorise the optimum thresholds — they are directly examinable.**

| # | Ratio | Numerator ÷ Denominator | **Optimum** |
|---|---|---|---|
| 1 | Savings Ratio | Annual Savings ÷ Annual Income | **More than 20%** |
| 2 | Investments-to-Savings | Annual Ongoing Investments ÷ Annual Savings | **More than 80%** |
| 3 | Emergency Funds Ratio | Emergency Funds ÷ Monthly Expenses | **More than 6** (months) |
| 4 | Debt-to-Assets (DTA) | Total Debt (Liabilities) ÷ Total Assets | **Less than 50%** |
| 5 | Debt-to-Income (DTI) | Total Monthly EMIs ÷ Net Monthly Income | **Less than 40%** |
| 6 | Physical Assets Ratio | Physical Assets ÷ Total Assets | **Less than 40%** |
| 7 | Retirement Savings Ratio | Annual Retirement Savings ÷ **Gross** Annual Income | **More than 10%** |

Note ratio 3 returns a count of months, not a percentage. Ratio 5 uses **net** monthly income; ratio 7 uses **gross** annual income. *Verified:* savings ₹8,40,000 ÷ income ₹24,00,000 = **35%**.

---

## ProTool 05 — One TVM Calculator
**Session 05 · `ProTool 05 - One TVM Calculator.xlsx`** · Sheets: Case Study, Trainers Sheet, Candidates Sheet, Practice Questions, Practice Questions & Solutions

### Layout (identical on both working sheets)
| Find | Row | Rate | NPER | PV | FV | PMT | Type | Pmts/yr | Comp/yr |
|---|---|---|---|---|---|---|---|---|---|
| PMT | 6 | C6 | D6 | E6 | F6 | **G6** | H6 | I6 | J6 |
| FV | 9 | C9 | D9 | E9 | **F9** | G9 | H9 | I9 | J9 |
| PV | 12 | C12 | D12 | **E12** | F12 | G12 | H12 | I12 | J12 |
| NPER | 15 | C15 | **D15** | E15 | F15 | G15 | H15 | I15 | J15 |
| Rate | 18 | **C18** | D18 | E18 | F18 | G18 | H18 | I18 | J18 |

Type legend on the sheet: `L5=0 → end of period`, `L6=1 → begin of period`.

### Embedded formulas (verbatim)
```
G6  =PMT(EFFECT(NOMINAL(C6,I6),J6)/I6, D6*I6, E6, F6, H6)
F9  =FV (EFFECT(NOMINAL(C9,I9),J9)/I9, D9*I9, G9, E9, H9)
E12 =PV (EFFECT(NOMINAL(C12,I12),J12)/I12, D12*I12, G12, F12, H12)
D15 =NPER(EFFECT(NOMINAL(C15,I15),J15)/I15, G15, E15, F15, H15) / I15
C18 =NOMINAL(EFFECT(RATE(D18*I18,G18,E18,F18,H18)*I18, I18), J18)
```

### The convention that decides the answer
Periodic rate = `EFFECT(NOMINAL(C,I),J)/I` — **convention A**. When payments/yr = compounding/yr (I=J, the common case) this collapses to **`C/I`**: the entered rate is treated as **nominal**. Contrast ProTool 19, which uses `NOMINAL(r,12)/12` and treats the same input as **effective**. Using B where A applies is a ~2.3% error — exactly the size of a plausible wrong option.

Also note `D15` divides the NPER result by `I15` to return **years**, not periods.

### Verified worked cases (Trainers Sheet)
| Row | Inputs | Output |
|---|---|---|
| PMT | 8.5%, 20 yrs, PV 65,00,000, FV 0, Type 0, 12/12 | **−56,408.51** |
| FV | 12.5%, 20 yrs, PV −15,00,000, PMT 0, Type 1, 1/1 | **1,58,17,640.76** |
| PV | 10%, 24 yrs, FV 4,00,00,000, Type 1, 1/1 | **−40,61,023.92** |
| NPER | 2.83%, PV −4,00,00,000, PMT 25,00,000, Type 1 | **20.7985 yrs** |
| RATE | 12 yrs, PV −30,00,000, FV 75,54,510, Type 1 | **8.00%** |

**Case Study answers:** Q1 PMT 56,409 · FV 1.58 Cr · PV 40.61 L · NPER 20.80 yrs · Rate 8%. Q2 = 69,79,039. Q3 = 23.79 years.

---

## ProTool 06 — One ROR Calculator
**Session 06 · `ProTool 06 - One ROR Calculator.xlsx`**

### Nine blocks
| # | Block | Output | Formula |
|---|---|---|---|
| 1 | CAGR | D9 | `=RATE(D6,D7,D4,D5,D8)` — PV entered negative |
| 2 | Absolute Returns | D14 | `=(D13-D12)/D12` |
| 3 | Effective Rate | D19 | `=EFFECT(D17,D18)` |
| 4 | Nominal Rate | D24 | `=NOMINAL(D22,D23)` |
| 5 | Tax Adjusted Return | D29 | `=D27*(1-D28)` |
| 6 | Real Rate (inflation adj.) | D34 | `=((1+D32)/(1+D33))-1` |
| 7 | Tax-Adj Real Rate | D39→D41 | `D39 =D37*(1-D38)`; `D41 =((1+D39)/(1+D40))-1` |
| 8 | IRR | D52 | `=IRR(D45:D51)` — annual flows, rows 45–51 |
| 9 | XIRR | D63 | `=XIRR(D56:D62, C56:C62)` — dated flows, rows 56–62 |

**Rules encoded:** real return is always `[(1+r)/(1+i)]−1`, never `r−i`. Tax-adjusted real rate is **sequenced** — tax first, then inflation, never combined. CAGR uses `RATE(...)` (so PMT and Type are honoured), not `(FV/PV)^(1/n)−1`.

**Verified:** CAGR −35,00,000→1,75,00,000 over 20 yrs Type 1 = **8.3798%**; −7,20,000→14,50,000 over 7 yrs = **10.5182%**; Absolute 35L→175L = **400%**; EFFECT(8%,12) = **8.2999%**; XIRR of the six dated flows = **36.188%**.

**Practice Solutions cached:** IRR = 8.5992% · XIRR(Q2) = 6.4198% · EFFECT(4%,4) = 4.0604% · tax-adj 12% @10% = 10.8% · real (12%, 8%) = 3.7037% · absolute 20L→80L = 300% · `RATE(12,,-2000000,8000000)` = 12.2462% · XIRR(Q9) = 7.1378% · tax-adj 14.5% @10% = 13.05%.

**Case Study:** Q1 → 36.19%, 10.52%, 8.30%, 400% & 8.38%, 0.57%. Q2 = 28.29%. Q3 = 10.47%.

---

## ProTool 07 — Macro Economics Tracker
**Session 07 · `ProTool 07 - Macro Economics Tracker.xlsx`**

A tracking grid: Indicator | Description | Data. Candidates populate current readings for the macro indicators taught in Session 07 (GDP growth, CPI/WPI inflation, repo rate, IIP, fiscal deficit, currency, crude, FII/DII flows, etc.) and interpret the direction of impact on investors. No embedded calculations — cite the Session 07 Handout/PPT for any macro-theory MCQ.

---

## ProTool 08 — Best Practices Checklist for PFPs
**Session 08 · `ProTool 08 - Best Practices Checklist for PFPs.xlsx`**

Compliance self-audit **prepared with reference to SEBI and AMFI Guidelines**. Four-state legend:

| Mark | Meaning |
|---|---|
| ✅ | Yes, in place |
| 🚧 | Partially in place |
| ❌ | Not in place |
| 🚫 | Not applicable to me / firm |

**Section A — Client First & Fiduciary Responsibility** (verbatim items):
1. I always place the client's interest above my revenue, incentives, or any targets.
2. I recommend financial products based on client suitability and not based on commissions or incentives.
3. I avoid conflicts of interest in my recommendations, and where unavoidable, I disclose them clearly to clients.
4. I do not engage in unnecessary transactions or churning to increase my income.
5. I do not split transactions or applications to earn higher commissions or charges.
6. I do not offer any rebates, gifts, or inducements.

Subsequent sections cover disclosure, documentation, KYC, record-keeping and grievance redressal. This sheet is the citation source for conduct/compliance MCQs.

---

## ProTool 09 — Product Suitability Matrix
**Session 09 · `ProTool 09 - Product Suitability Matrix.xlsx`**

Purpose (verbatim): *"This matrix can be used by the Advisor to allocate the various products available in the market, as per the Risk Profile, Goal Tenure and their Investment Philosophy."*

Rows = risk profile (Aggressive / Moderate / Conservative investor) × goal tenure. The **product master list** (column O) is the examinable content:

1. Fixed Deposits (FDs) · 2. National Savings Certificate (NSC) · 3. Senior Citizen Savings Scheme (SCSS) · 4. Monthly Income Scheme (MIS) · 5. Public Provident Fund (PPF) · 6. Voluntary Provident Fund (VPF) · 7. Bonds, NCDs, MLDs · 8. Debt Mutual Funds (Liquid / Ultra ST / Short Term / Medium Term / Income / Duration) · 9. Equity Mutual Funds (Large / Multi-Flexi / Mid / Small Cap / Sectoral / Thematic) · 10. Hybrid Mutual Funds (Equity Oriented / Debt Oriented / Dynamic) · 11. Equity Shares · 12. Portfolio Management Services (PMS) · 13. ULIPs · 14. Traditional Insurance Policies (Endowment / Money-back …)

No formulas — a placement framework.

---

## ProTool 10 — Asset Class Performance Calculator
**Session 10 · `ProTool 10-Asset Class Performance.xlsx`**

Four blocks, each run across **Equity / Real Estate / Gold / Debt** columns.

```
Block 1 (rows 4-8)   Investment potential:
  C8 =FV(EFFECT(NOMINAL(C7,1),1)/1, $D$5*1, 0, -$D$4, 1)      ' Type 1
Block 2 (rows 11-15) Target amount -> lumpsum needed today:
  C15 =PV(EFFECT(NOMINAL(C14,1),1)/1, $D$12*1, 0, -$D$11, 1)
Block 3 (rows 17-20) Years to double:
  C20 =72/(C19*100)                                            ' RULE OF 72
Block 4 (rows 22-28) Actual realised return:
  C28 =NOMINAL(EFFECT(RATE(C27*1,0,-C25,C26,1)*1,1),1)         ' CAGR from PV/FV/years
```

**Conventions:** convention A rates with I=J=1 (so the rate passes through unchanged); **Type = 1** throughout; years-to-double uses the **Rule of 72** on the rate expressed as a percentage.

*Verified:* ₹1,00,000 for 10 yrs → Equity @12% **3,10,585** · Real Estate @10% **2,59,374** · Gold @8% **2,15,892** · Debt @6% **1,79,085**. Target ₹1.25 Cr in 12 yrs → lumpsum today: Equity @15% **23,36,339** · RE @12% **32,08,439** · Gold @10% **39,82,885** · Debt @6% **62,12,117**. Years to double: 15% → **4.8** · 10% → **7.2** · 6% → **12**. Actual CAGR 2014→2024: Equity 25,000→80,000 = **12.33%** · RE 40,00,000→55,00,000 = **3.24%** · Gold 28,000→76,000 = **10.50%**.

---

## ProTool 11 — Financial Consultancy Process Matrix
**Session 11 · `ProTool 11 - Consultancy Process Matrix.xlsx`**

The **six-stage consultancy process**, each stage carrying Particulars + Timeline columns:

**Establish Need → 1) Understand → 2) Analyse → 3) Recommend → 4) Execute → 5) Monitor → 6) Review**

Worked row — *Investment Consultancy, "Want to Invest ₹3 Lakh Lumpsum"*:
- **Understand:** what's the purpose/goal, when is the money needed back, one-off or recurring, return expectation
- **Analyse:** which asset class is suitable, which product is suitable, what return expectation is realistic
- **Recommend:** strategy — asset class, product basket, specific names, Growth/Dividend, source of investment, basis of recommendation
- **Execute:** check KYC, do KYC, other documentation, platform account, bank transaction
- **Monitor:** monthly/quarterly reports, track recommended product performance, return-expectation tracking
- **Review:** anticipate client reactions to markets and communicate proactively, manage withdrawal requests

Memorise the six stage names in order — directly examinable.

---

## ProTool 12 — Client Goals Matrix
**Session 12 · `ProTool 12 - Client Goals Matrix.xlsx`**

Two-axis classification. **Tenure:** Short-Term (<3 years) · Medium-Term (3–7 years) · Long-Term (>7 years). **Priority:** Needs (High Priority) · Wants (Medium Priority) · Wishes (Low Priority).

Worked placement:
- **Short-term / Needs:** Emergency Funding, Health Insurance Upgrade, Term Life Insurance, Parents Medical Fund, Insurance Premium Fund
- **Short-term / Wants:** Domestic Vacations, Car Purchase/Upgrade, Tax Saving Investments, Lifestyle Contingency Fund, Children's Other Costs
- **Medium-term / Wants:** House Purchase, Home Interiors/Renovation
- **Long-term / Needs:** Children's Education
- **Long-term / Wants:** Children's Marriage, Retirement Funds, Wealth Creation Fund

**Priority order (worked list):** 1 Emergency Funding · 2 Retirement Funds · 3 Children's Education · 4 House Purchase · 5 International Vacations · 6 Car Purchase/Upgrade · 7 Children's Marriage · 8 New Venture/Start Up · 9 Sabbatical from Work · 10 Home Interiors/Renovation.

Note the tool ranks **Retirement second, above Children's Education** — a common exam point.


---

# PART 2 — LEVEL II: Personal Finance Solutions

## ProTool 13 — Family FIDOK Organizer
**Session 13 · `ProTool 13 - Family FIDOK Organizer.xlsx`** · Sheets: Trainer Sheet, Candidate Sheet

**FIDOK = Financial Information and Documents Organizer Kit.** No formulas — a structured record. Sections in order:

1. **Details of Family Members** — Couple, Dependent Children, Dependent Parents, Dependent Relatives (Relation, Name, DOB)
2. **Important Contacts** — Family Doctor, Financial Advisor, Lawyer, Chartered Accountant, Office HR, Friend/Colleague, Relative/Neighbour
3. **Important Financial Documents** — PAN, Passport, Aadhaar, **Will**, Birth Certificate, Marriage Certificate, Locker Key, Insurance Policies, Property Papers, Home Loan documents, Cheque books, Other Loan documents, Income Tax Returns, Investment documents, Voter ID, ATM/Credit Cards (with holder, number, physical location, virtual location)
4. **Documents Validity** — name, document, number, valid till, changes required
5. **Locker Details** — bank & branch, account number, locker no., in the name of, code, nominee
6. **Online Passwords** — Personal Email, Password Manager, Mobile Phone Unlock (and *who is aware of the password*)
7. **Life Insurance Policies** — company & policy, policy no., amount insured, valid till, premium, nominee, agent/PFP + contact
8. **Health and Other Insurance Policies**
9. **Bank Account Details** — holder, bank & branch, account no., type, nominee, registered email/mobile, login username

The design principle being tested: a family must be able to reconstruct the complete financial picture without the earning member present.

---

## ProTool 14 — Risk Profiling Tool
**Session 14 · `ProTool 14 - Risk Profiling Tool.xlsx`** · Sheets: Risk Profiler, Results, Scores Working

**Scoring:** 12 questions, options A/B/C/D worth **10 / 20 / 30 / 40** points. Client's Risk Profile % = points scored ÷ total possible points.

### The band table (examinable verbatim)
| Score % | Risk Profile | Investor Type | Equity | Debt |
|---|---|---|---|---|
| 0–20% | Low | Very Cautious / Very Conservative Investor | 05%–25% | 75%–95% |
| 20–35% | Low to Moderate | Cautious / Conservative Investor | 20%–35% | 65%–80% |
| 35–50% | Moderate | Moderate Investor | 35%–50% | 50%–65% |
| 50–65% | Moderate to High | Moderately Aggressive Investor | 50%–65% | 35%–50% |
| 65–80% | High | Aggressive Investor | 65%–80% | 20%–35% |
| 80–100% | Very High | Very Aggressive Investor | 80%–100% | 0%–20% |

`O11 =100-N11` — debt is always the complement of equity. Note the tool carries two naming conventions for the same bands (Very Cautious / Very Conservative); either may appear in options.

---

## ProTool 15 — Life Insurance Calculator (Need Analysis)
**Session 15 · `ProTool 15 - Life Insurance Calculator.xlsx`** · Sheets: Case Study, Trainer Sheet, Candidate Sheet

### Structure — the A + B + C method
| Cell | Field | Trainer value |
|---|---|---|
| D8–D12 | Home / Vehicle / Personal / Education / Other loans | 40L / 5L / 3L / 0 / 2L |
| **D13 (A)** | Total Outstanding Liability `=SUM(D8:D12)` | 50,00,000 |
| D15–D18 | Children's Higher Education & Marriage (PV), Children's Primary Education (PV), Contribution to Parents (PV), House Purchase (first house only) | 80L / 15L / 10L / – |
| **D19 (B)** | Total Family Goals & Commitments `=SUM(D15:D18)` | 1,05,00,000 |
| D21–D22 | Household / Lifestyle expenses | 7,80,000 / 3,00,000 |
| D23 | Total Expenses `=SUM(D21:D22)` | 10,80,000 |
| D24 | **Discounting Factor — Personal Expense** | 20% |
| D25 | Current Annual Expenses `=D23*(1-D24)` | 8,64,000 |
| D26 | Remaining Life Expectancy of **Spouse** | 30 |
| D27 | Inflation on Expenses | 6% |
| D28 | Tax on Investment Income | 10% |
| D29 | Expected Return on insurance claim | 8% |
| D30 | Tax Adjusted Return `=D29*(1-D28)` | 7.20% |
| D31 | **Net (Real) Return** `=(1+D30)/(1+D27)-1` | 1.13208% |
| **D32 (C)** | Corpus for Regular Expenses `=PV(D31,D26,-D25,,1)` | 2,21,21,024 |
| **D33** | **Total Life Insurance Required `=D13+D19+D32`** | **3,76,21,024** |
| D35–D37 | Existing Sum Assured / Current Investment Assets / PV of spouse's future earnings | 60L / 25L / 0 |
| D38 | Total Resources `=SUM(D35:D37)` | 85,00,000 |
| **D39** | **Additional Cover Required `=D33-D38`** | **2,91,21,024** |

### Conventions
1. The **discounting factor (D24)** removes the deceased's *own* personal consumption from household expenses — apply it before inflating.
2. Horizon is the **spouse's remaining life expectancy**, not the client's.
3. Expense corpus is an **annuity-due (Type 1)** — the first year's expenses are needed immediately on claim.
4. Return chain: tax first, then inflation. Real rate ≈ 1.13%, not 2%.
5. Goals enter at **present value**, liabilities at **outstanding value** — neither is inflated; only the expense stream is.
6. House Purchase counts **first house only**.

**Case Study:** Q1 Total ₹3.76 Cr / Additional ₹2.91 Cr · Q2 Additional ₹2.51 Cr · Q3 Additional ₹2.55 Cr.

---

## ProTool 16 — Emergency Funds Calculator
**Session 16 · `Protool 16 - Emergency Funds Calculator.xlsx`**

| Cell | Field | Formula | Trainer |
|---|---|---|---|
| D8–D13 | Household, Lifestyle, Dependent, Insurance Premiums, **Loan EMI Servicing**, Ongoing Investments | inputs | 50k/20k/15k/5k/30k/10k |
| D14 | Total Monthly Expenses | `=SUM(D8:D13)` | 1,30,000 |
| D16 | Emergency months to prepare for | input | 6 |
| D17 | Emergency Funds Required | `=D14*D16` | 7,80,000 |
| D18 | **Round-off** | `=ROUND(D17,-4)` | 7,80,000 |
| D20 | Months of expenses in Savings A/c | input | 2 |
| D21 | Savings Account Bank Balance | `=D$14*D20` | 2,60,000 |
| D22 | Remaining months in other liquid assets | `=D16-D20` | 4 |
| D23 | Other Liquid Assets | `=D$14*D22` | 5,20,000 |
| D24 | Total Allocated | `=D21+D23` | 7,80,000 |
| D26–D29 | Savings balance, FDs, Liquid MFs, Other liquid | inputs | 1.5L/2L/1L/0.5L |
| D30 | Total Existing Assets | `=SUM(D26:D29)` | 5,00,000 |
| D32 | Deficit | `=D18-D30` | 2,80,000 |
| D33 | No. of months in savings period | input | 10 |
| **D34** | **Monthly Savings Required** | `=D32/D33` | **28,000** |

**Conventions:** the expense base **includes loan EMIs and ongoing investments** — a frequent trap, since candidates often exclude them. `ROUND(x,-4)` rounds to the nearest ₹10,000 and the *rounded* figure (D18) is what feeds the deficit. The final step is plain division — no TVM, no interest on the savings.

**Case Study:** Q1 ₹28,000 · Q2 ₹34,000 · Q3 ₹92,000 (round off).

---

## ProTool 17 — Children's Future Calculator
**Session 17 · `ProTool 17 - Children's Future Calculator.xlsx`**

Three goal columns run in parallel: **D = Graduation, E = PG, F = Marriage**.

| Row | Field | Formula | D / E / F (Trainer) |
|---|---|---|---|
| 8 | Present Value of Goal | input | 6,00,000 / 7,00,000 / 8,00,000 |
| 9 | Goal Age | input | 18 / 22 / 28 |
| 10 | Current Age | input | 7 / 7 / 7 |
| 11 | Remaining Years | `=D9-D10` | 11 / 15 / 21 |
| 12 | Goal Planning Year | input | 2026 |
| 13 | Goal Target Year | `=D12+D11` | 2037 / 2041 / 2047 |
| 14 | **Expected Inflation of Goal** | input | 10% / 10% / **8%** |
| 15 | Future Value of Goal | `=FV(D14,D11,,-D8)` | 17,11,870 / 29,24,074 / 40,27,067 |
| 17–21 | Endowment / MF / FD / Gold / Stocks (FV at goal) | inputs | FD 3L / Stocks 4L / MF 5L |
| 22 | Current Assets Utilized | `=SUM(D17:D21)` | 3L / 4L / 5L |
| 23 | % of Goal on Track | `=D22/D15` | 17.52% / 13.68% / 12.42% |
| 25 | Deficit | `=D15-D22` | 14,11,870 / 25,24,074 / 35,27,067 |
| 26 | Start investment after (yrs) | input | 0 |
| 27 | **Stop investing before (yrs)** | input | 0 |
| 28 | Expected Investment Returns | input | 12% |
| 29 | Lumpsum Funding Required | `=PV(D28,D11-D26,,-D25)` | 4,05,879 / 4,61,139 / 3,26,464 |
| 30 | **Monthly Investment (Fixed SIP)** | see below | **5,405 / 5,354 / 3,414** |
| 31 | StepUp Rate | input | 10% |
| 32 | **Monthly Investment (StepUp SIP)** | see below | **3,570 / 3,079 / 1,639** |

```
D30 =-PMT(NOMINAL(D28,12)/12, (D11-D26-D27)*12, , -PV(D28,D27,,D25,1), 0)
D32 =-PMT(NOMINAL(D28,12)/12, 12, ,
          (-PV(D28,D27,,D25,1)*(D28-D31)) /
          ((1+D28)^(D11-D26-D27) - (1+D31)^(D11-D26-D27)), 0)
```
The sheet also states the step-up formula in words (cell B40):
`Step Up SIP = FV / ((1+Rate) * (((1+Rate)^Nper − (1+Growth)^Nper) / (Rate − Growth))) / 12`

### Conventions
1. **Each goal carries its own inflation** — education inflation (10%) differs from marriage inflation (8%). Do not apply one rate across all three.
2. Assets are entered **already grown to the goal date** ("FV at time of Goal"), so they are not compounded again.
3. `D27` (stop investing before) discounts the deficit back from the goal date to the last SIP date via `PV(rate, D27, , D25, 1)`. With D26 = D27 = 0 this is just the deficit.
4. Investing window = `Remaining years − start delay − stop-early`.
5. Convention B rate (`NOMINAL(r,12)/12`).
6. StepUp SIP is materially cheaper — 3,570 vs 5,405, a **34% lower opening instalment**.

**Case Study:** Q1 without StepUp — Graduation 5,405 / PG 5,354 / Marriage 3,414; with StepUp — 3,570 / 3,079 / 1,639. Q2 = 24,503. Q3 = 21,833.

---

## ProTool 18 — House Purchase Calculator
**Session 18 · `ProTool 18 - House Purchase Calculator.xlsx`** · Sheets include hidden `House_Candidates` and `Assignment Guidelines`

| Cell | Field | Formula | Trainer |
|---|---|---|---|
| D8 | Present Value of House | input | 1,50,00,000 |
| D9 | Additional Costs (reg., interiors, taxes) % | input | 8% |
| D10 | Total PV of House | `=D8*(1+D9)` | 1,62,00,000 |
| D11 | Growth Rate of Real Estate | input | 5% |
| D12 | Years to Goal | input | 8 |
| D13 | **FV incl. additional costs** | `=FV(D11,D12,,-D10)` | 2,39,34,778 |
| D14 | **FV excl. additional costs (for loan)** | `=FV(D11,D12,,-D8,1)` | 2,21,61,832 |
| D16 | Home Loan Funding % | input | 80% |
| D17 | Home Loan Amount | `=D14*D16` | 1,77,29,465 |
| D18 | Down-payment Funding % | `=1-D16` | 20% |
| D19 | Down-payment Amount | `=D14*D18` | 44,32,366 |
| **D20** | **Total to be accumulated** | `=D19+(D13-D14)` | **62,05,313** |
| D22 | Current Monthly Income | input | 2,50,000 |
| D23 | Expected Monthly Income at purchase | `=FV(8%,D12,,-D22)` | 4,62,733 |
| D24 | Ideal EMI % of Income | input | 35% |
| D25 | Ideal EMI Limit | `=D24*D23` | 1,61,956 |
| D26/D27 | Home Loan Rate / Tenure | inputs | 8.5% / 25 yrs |
| D28 | **Expected EMI** | `=PMT(NOMINAL(D26,12)/12,D27*12,-D17)` | 1,39,028 |
| D33 | Total Current Assets (FV) | `=SUM(D30:D32)` | 3,00,000 |
| D34 | % of Goal on Track | `=D33/D20` | 4.83% |
| D36 | Deficit | `=D20-D33` | 59,05,313 |
| D37 | Start investment after (yrs) | input | 3 |
| D38 | Expected Investment Returns | input | 9% |
| D39 | Lumpsum Required | `=PV(D38,(D12-D37),,-D36)` | 38,38,048 |
| **D40** | **Fixed SIP** | `=-PMT(NOMINAL(D38,12)/12,(D12-D37)*12,0,D36,0)` | **79,019** |
| D41 | StepUp Rate | input | 4% |
| **D42** | **StepUp SIP** | `=-PMT(NOMINAL(D38,12)/12,12,,(D36*(D38-D41))/((1+D38)^(D12-D37)-(1+D41)^(D12-D37)),0)` | **73,439** |

### The subtlety that decides the answer
There are **two different future values**:
- `D13` inflates the **cost-inclusive** price as an ordinary annuity (Type 0)
- `D14` inflates the **bare** price with **Type 1**, and this is the one used for the loan and down-payment split

The amount to accumulate is then `down-payment + (the additional-cost gap)` = `D19 + (D13 − D14)`, **not** simply 20% of D13. Getting this wrong is the tool's signature distractor.

Also: income grows at a **hard-coded 8%** in D23 (not the investment return, not inflation). EMI affordability is a separate feasibility check — it does not feed the SIP calculation.

**Case Study:** Q1 Monthly SIP ₹73,439 · Q2 ₹2,12,126 · Q3 ₹4,54,978 (round off).

*Assignment Guidelines sheet:* candidates fill the Candidates Sheet, save as `<Name-AssignmentNo-QPFP>`, upload to their coach's link; **60% assignment submission is required to qualify for QPFP Final Exams.**

---

## ProTool 19 — Retirement Accumulation Calculator
**Session 19 · `Protool 19 - Retirement Accumulation Calculator.xlsx`**

| Cell | Field | Formula | Trainer |
|---|---|---|---|
| D8/D9/D10 | Household / Lifestyle / Other annual expenses | inputs | 10.8L / 3L / 1.2L |
| D11 | Total Current Annual Expenses | `=SUM(D8:D10)` | 15,00,000 |
| D12 | Monthly | `=D11/12` | 1,25,000 |
| D14 / D15 | Current age / Retirement age | inputs | 42 / 60 |
| D16 | Years to retirement | `=D15-D14` | 18 |
| D17 | Inflation till retirement | input | 6% |
| D18 | **Drop in expenses after retirement** | input | 15% |
| D19 | Annual Expenses @ Retirement | `=FV(D17,D16,,-D11*(1-D18))` | 36,39,282 |
| D22 | Corpus for Children / Charity | input | 25,00,000 |
| D23 | Life Expectancy | input | 88 |
| D24 | Years post retirement | `=D23-D15` | 28 |
| D25 | Inflation during retirement | input | 6% |
| D26 | Net tax on investment income | input | 10% |
| D27 | Weighted avg return on corpus | input | 9.5% |
| D28 | Tax Adjusted Return | `=D27*(1-D26)` | 8.55% |
| D29 | **Real Return** | `=(1+D28)/(1+D25)-1` | 2.40566% |
| **D30** | **Retirement Corpus Required** | `=PV(D29,D24,-D19,-D22,1)` | **7,65,81,905** |
| D35 / D40 | Employment benefits / own assets | `=SUM(...)` | 1.75 Cr / 1.45 Cr |
| D42 | Total Assets @ Retirement | `=SUM(D35,D40)` | 3,20,00,000 |
| D43 | % of Goal on Track | `=D42/D30` | 41.79% |
| D45 | **Deficit** | `=D30-D42` | 4,45,81,905 |
| D46 | Start investment after (yrs) | input | 1 |
| D47 | Expected Investment Return | input | 12% |
| D48 | Lumpsum Required | `=PV(D47,(D16-D46),,-D45)` | 64,93,102 |
| **D49** | **Fixed SIP** | `=PMT(NOMINAL(D47,12)/12,(D16-D46)*12,,-D45,0)` | **72,115** |
| **D51** | **StepUp SIP** | see below | **72,115** |

```
D51 =PMT(NOMINAL(D47,12)/12, 12, ,
        -((D45 - FV(D47,D16,,)) * (D47-D50)) /
         ((1+D47)^(D16-D46) - (1+D50)^(D16-D46)), 0)
```

### Conventions
1. Expense drop (D18) applies to **today's** expenses *before* inflating.
2. Corpus is an **annuity-due (Type 1)**.
3. Terminal corpus (children/charity) enters `PV` as the `fv` argument, negative.
4. Two different inflation rates may apply — D17 (pre-retirement) and D25 (during retirement). The real return uses **D25**.
5. Convention B rate — the 12% is **effective annual**. This differs from ProTool 05.
6. Delayed start shortens the horizon to `D16 − D46` for both lumpsum and SIP.

**Case Study:** Q1 Required 7.66 Cr / Available 3.20 Cr / Shortfall 4.46 Cr · Q2 6.30 / 2.38 / 3.92 Cr · Q3 7.53 / 2.00 / 5.53 Cr.

---

## ProTool 20 — Retirement Distribution Calculator (Bucket Strategy)
**Session 20 · `Protool 20 - Retirement Distribution Calculator.xlsx`**

This is the **three-bucket** model. Do not solve it as a single annuity.

| Cell | Field | Formula | Trainer |
|---|---|---|---|
| F10 | Age at Retirement | input | 60 |
| F11 | Monthly Expenses | input | 1,20,000 |
| F12 | Annual Expenses | `=F11*12` | 14,40,000 |
| F17 | Life Expectancy | input | 90 |
| F18 | Distribution Phase (yrs) | `=F17-F10` | 30 |
| F19 | Inflation Rate | input | 6% |
| E22 / F22 | **Bucket 1 (Yrs 1–3)** — years, post-tax return | inputs | 3 yrs, **5%** |
| E23 / F23 | **Bucket 2 (Yrs 4–7)** — years, return | inputs | 4 yrs, **7%** |
| E24 / F24 | **Bucket 3 (Yr 8+)** — years, return | `E24 =F18-E22-E23` | 23 yrs, **9%** |
| F25 | Weighted Average Return | `=SUMPRODUCT(E22:E24,F22:F24)/SUM(E22:E24)` | 8.3333% |
| F26 | Real Rate | `=(1+F25)/(1+F19)-1` | 2.2013% |
| F37 | **Total Investment Required** | `=SUM(F34:F36)` | **3,02,69,429** |

### Bucket workings (rows 42–44) — corpus needed at the START of each bucket
```
F42 =PV((1+$F$22)/(1+$F$19)-1, E22, -$F$12, , 1)                        ' 43,61,273
F43 =PV((1+$F$23)/(1+$F$19)-1, E23, -FV($F$19,E22,,-$F$12), , 1)        ' 67,64,678
F44 =PV((1+$F$24)/(1+$F$19)-1, E24,  FV($F$19,E22+E23,,$F$12), , 1)     ' 3,72,66,703
```
### Amount to invest TODAY in each bucket (rows 34–36)
```
F34 =F42                          ' Bucket 1 needed immediately          43,61,273
F35 =-PV(F23, E22, , F43)         ' discount B2's start-corpus back 3 yrs @7%   55,21,992
F36 =-PV(F24, E22+E23, , F44)     ' discount B3's start-corpus back 7 yrs @9%  2,03,86,163
E34 =F34/F$37                     ' allocation %                          14.41% / 18.24% / 67.35%
```

### Conventions
1. Each bucket is discounted at **its own** return rate against inflation — a bucket-specific real rate, not the weighted average. The weighted average (F25) and real rate (F26) are **reported for reference only**; they do not drive F37.
2. Every bucket is an **annuity-due (Type 1)**.
3. Bucket 2 and 3 expense streams start from an **already-inflated** expense: `FV(inflation, prior years, , −annual expense)`.
4. The start-corpus for a later bucket is discounted back to today at that bucket's **nominal** return (no inflation adjustment on that leg) — `-PV(F23,E22,,F43)`.
5. Bucket 3 length is the residual: `total years − 3 − 4`.
6. Basis of allocation: Bucket 1 = **Liquidity**, Bucket 2 = **Safety**, Bucket 3 = **Wealth Creation**.

**Case Study:** Q1 ₹3.02 Cr · Q2 ₹2.77 Cr · Q3 ₹1.90 Cr.

---

## ProTool 21 — Income Tax Calculator (Old vs New Regime)
**Session 21 · `Protool 21 - Income Tax Calculator.xlsx`**

### Basic information
`E6` Metro/Non-Metro · `E7` EPF interest rate (8.25%) · `E8` Basic Salary · `E9` Rent Paid · `E10` Employee PF contribution · `E11` Employer PF contribution.

### 1) Gross Income (rows 14–19)
Salary, Bonus, House property (let out), Income from other sources, plus:
```
E18 =IF(E10<0,0, IF(AND(E11=0,E10>500000), (E10-500000)*E7,
                 IF(AND(E11>0,E10>250000), (E10-250000)*E7, 0)))
E19 =SUM(E14:E18)
```
**Rule:** interest on employee PF contribution above **₹2,50,000** is taxable where the employer also contributes; the threshold rises to **₹5,00,000** where there is **no employer contribution**.

### 2) Deductions
**2.1 HRA u/s 10(13A)** — least of three:
```
E23 = actual HRA received
E24 =IF(E6="Metro", E8*50%, E8*40%)     ' 50% metro / 40% non-metro of Basic
E25 =E9-10%*E8                           ' rent paid less 10% of Basic
E26 =IF(MIN(E23:E25)>=0, MIN(E23:E25), 0)
```
**2.2 Standard Deduction u/s 16** — Old ₹50,000 + Professional Tax ₹2,400 → `E32 =E29+E31`; New **₹75,000** → `E33 =E30` (professional tax not allowed in the new regime).

**2.3 80C** — `E42 =MIN(E41,150000)`. Eligible items: EPF/PPF, ELSS, life insurance premium, housing loan principal repayment, others.

**2.4 80CCD**
```
E46 =IF(E45="",0,MIN(E45,50000))       ' 80CCD(1B) - employee NPS, cap 50,000
E48 =IF(E47=0,0,MIN(E47,10%*E8))       ' 80CCD(2) OLD regime - 10% of Basic
E49 =IF(E47=0,0,MIN(E47,14%*E8))       ' 80CCD(2) NEW regime - 14% of Basic
```
**The 10% vs 14% split is a high-frequency exam point.**

**2.5 80D**
```
E53 =IF(D53="",0,MIN(D53,25000))   ' self/spouse/children, below 60
E54 =IF(D54="",0,MIN(D54,50000))   ' below-60 slot at senior rate
E56 =MIN(parents premium, 25000)   ' parents below 60
E57 =MIN(parents premium, 50000)   ' parents above 60
E58 = health checkup, absorbed within the overall cap:
      both below 60 -> 50,000 total; both above 60 -> 1,00,000; mixed -> 75,000
E59 =SUM(E53:E58)
```
**2.6 80E** — `E63 =E62`, interest on education loan, **no cap**.

**2.7 80TTA / 80TTB** — `E67 =MIN(E66,10000)` non-senior; `E69 =MIN(E68,50000)` senior. Mutually exclusive.

**2.8 80G** — `E75 =(E72*100%)+(E73*50%)`.

**2.9 Section 24 / house property**
```
E80 =30%*(E16)                      ' standard deduction u/s 24A on let-out rent
E81 =IF(E78<200000,E78,200000) + IF(E16>0, IF((E16*70%)>E79, E79, E16*70%), 0)  ' OLD
E82 =IF(E16>0, IF((E16*70%)>E79, E79, E16*70%), 0)                              ' NEW
E83 =E80+E81   ' old regime total
E84 =E80+E82   ' new regime total
```
Self-occupied interest cap **₹2,00,000 (old regime only)**; let-out interest is restricted to 70% of rental income.

**Totals**
```
E86 =SUM(E26,E42,E48,E59,E63,E69,E75,E83,E32,E67,E46)   ' OLD regime deductions
E87 =SUM(E33,E49,E84)                                    ' NEW regime deductions
E90 =E19-E86     ' Taxable income - OLD
E101=E19-E87     ' Taxable income - NEW
```

### 3) Slabs
**Old regime** (`A95` threshold = ₹3,00,000 if Senior, else ₹2,50,000; Super Senior pays 0% in the second band):

| Band | Rate |
|---|---|
| 0 – ₹2,50,000 (₹3,00,000 senior) | 0% |
| ₹2,50,000 – ₹5,00,000 | 5% |
| ₹5,00,000 – ₹10,00,000 | 20% |
| Above ₹10,00,000 | 30% |

**New regime:**

| Band | Rate |
|---|---|
| 0 – ₹4,00,000 | 0% |
| ₹4,00,000 – ₹8,00,000 | 5% |
| ₹8,00,000 – ₹12,00,000 | 10% |
| ₹12,00,000 – ₹16,00,000 | 15% |
| ₹16,00,000 – ₹20,00,000 | 20% |
| ₹20,00,000 – ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

### 4) Final tax
```
E119 =IF(E90<=500000, E117, 0)      ' 87A rebate OLD  - full relief up to 5,00,000
E120 =IF(E101<=1200000, E118, 0)    ' 87A rebate NEW  - full relief up to 12,00,000
D121 =IF(E90<=5000000,0, IF(E90<=10000000,10%, IF(E90<=20000000,15%,
        IF(E90<=50000000,25%, IF(E90>50000000,37%,)))))          ' OLD surcharge, tops at 37%
D122 =IF(E101<=5000000,0, IF(E101<=10000000,10%, IF(E101<=20000000,15%,
        IF(E101>20000000,25%,))))                                ' NEW surcharge, CAPPED AT 25%
E123 =IF(E117=E119, 0, (E117+E121)*4%)     ' cess 4%, nil if fully rebated
E125 =E117-E119+E121+E123                   ' Total OLD
E126 =E118-E120+E122+E124                   ' Total NEW
E128 =IF(E125>E126, "New Regime", "Old Regime")
```
**Surcharge caps at 37% in the old regime but 25% in the new** — examinable.

**Verified (Trainer):** Gross ₹30,30,000 · Old deductions ₹12,96,400 → taxable ₹17,33,600 → tax ₹3,32,580 + cess ₹13,303 = **₹3,45,883**. New deductions ₹4,65,000 → taxable ₹25,65,000 → tax ₹3,49,500 + cess ₹13,980 = **₹3,63,480**. Recommendation: **Old Regime**.

---

## ProTool 22 — Will Template
**Session 22 · `ProTool 22 - Will Template - Blank.docx` / `- Filled.docx`** (Word, not Excel)

Clause sequence:
1. **Title** — "Will of ______ (Testator)"
2. **Declaration** — "I, ____, son of ____, residing at ____, declare this to be my **LAST WILL** being made on ____."
3. **Revocation** — "I revoke all prior wills, codicils & testamentary dispositions previously made by me."
4. **Capacity** — "I am in good health and of sound mind, and am not making this will under any persuasion or coercion."
5. **Bequest** — "I give, devise and bequeath all remaining movable and immovable assets, financial and physical assets owned by me and belonging to no one else to the following Beneficiaries."
6. **List of Beneficiaries** — S.N. | Name | Relationship to Testator | PAN/Aadhaar | Place of Residence | Age
7. Asset schedules, executor appointment, guardian appointment, witness attestation.

The three legally essential elements the template encodes: **revocation of prior wills**, **declaration of sound mind and absence of coercion**, and **attestation by witnesses**.

---

## ProTool 23 — One Page Financial Report
**Session 23 · `ProTool 23 - One Page Financial Report.xlsx`** · Sheets: Case Study, Workings (Trainer), Report (Trainer), Workings (Candidate), Report (Candidate)

A consolidation deliverable (148 formulas, all aggregation and referencing — no new financial mathematics). Structure: Family Details (names, relation, remarks, age) → Income Expenditure Statement (annual inflows after taxes: salary, spouse salary, rental, investment, other; outflows: household, lifestyle, dependent, insurance premiums, EMIs, taxes) → Assets & Liabilities → Goals → Financial Health Indicators → Recommendations. The `Remarks` column carries "Enter — Ask Client" prompts, marking which fields are client-sourced rather than derived. Every figure on the Report sheet is a link to the Workings sheet.

---

## ProTool 24 — Asset Allocation & Assumptions (AAA Framework)
**Session 24 · `Protool 24 - Asset Allocation & Assumptions.xlsx`**

### Master assumptions block (rows 3–12)
| Assumption | Sub-category | Figure | Sub-category | Figure |
|---|---|---|---|---|
| Inflation | General | **7%** | Education | **10%** |
| Income Growth | Self | 10% | Spouse | 10% |
| Tax Bracket | Self | 30% | Spouse | 30% |
| Loan Rates | Home | 8% | Vehicle | 9% |
| | Education | 10% | Personal | 13% |
| Life Span – Self | Retirement Age | 60 | Life Expectancy | 80 |
| Life Span – Spouse | Retirement Age | 60 | Life Expectancy | 80 |
| **Asset Class Returns (post-tax)** | Liquid | **4%** | Gold | **10%** |
| | Debt | **7%** | Real Estate | **12%** |
| | Equity | **15%** | | |

### The engine
```
E16 =G10 ; F16 =G11 ; G16 =J10 ; H16 =G12 ; I16 =J11   ' return vector: Liquid, Debt, Gold, Equity, RE
J17 =SUM(E17:I17)                                       ' allocation must total 100%
K17 =SUMPRODUCT($E$16:$I$16, $E17:$I17)                 ' PORTFOLIO RETURN
```
Portfolio return is always **SUMPRODUCT(return vector, allocation vector)** — a weighted average, never a simple average.

### Three allocation lenses
**A) By time horizon of goal:** Very Short Term (0–1 yr) = 100% Liquid → portfolio return **4%**. Very Long Term (10+ yrs) = 10% Debt / 10% Gold / 80% Equity → **13.7%**.

**B) By risk profile:** five investor types from Very Cautious to Very Aggressive. Very Aggressive = 10% Debt / 5% Gold / 80% Equity / 5% RE → **13.8%**.

**C) By income-generation requirement:** Retirement Corpus (retirement distribution) = 20% Liquid / 60% Debt / 10% Gold / 10% Equity → **7.5%**. Insurance Corpus (life claims settled) is the second row.

**Case Study:** Q1 — Goal 1 Son's School Admission (8 months) **4%** · Goal 2 Daughter's Marriage **13.70%** · Goal 3 Retirement Corpus **13.80%** · Goal 4 Father's Retirement Distribution **7.50%**. Q2 = 6.30%. Q3 Child's Higher Education = 12.90%.

The exam pattern: given a goal, pick the correct lens (horizon vs risk profile vs income generation), read the allocation row, SUMPRODUCT it against the return vector.


---

# PART 3 — LEVEL III: Personal Finance Products

## ProTool 25 — Life Insurance Recommendation Template
**Session 25 · `ProTool 25 - Life Insurance Recommendation Template.xlsx`** · Sheets: Trainer Sheet, Recommendation (Trainer), Candidate Sheet, Recommendation (Candidate), Annexure, Steps (CSR)

A structured recommendation record — 17 fields, no financial mathematics:

| # | Field | Worked example |
|---|---|---|
| 1–2 | Name, Age | Mr. ABC, 30 |
| 3 | **Ideal Sum Assured** (from ProTool 15) | 2,00,00,000 |
| 4 | Sum Assured recommended | 2,00,00,000 |
| 5 | Policy Term | 30 |
| 6 | Policy ends at age | (derived: age + term = 60) |
| 7–8 | Company, Policy Name | ICICI Prudential Life, iProtect Smart Plus |
| 9 | Critical Illness | Available |
| 10 | Waiver of Premium | Available |
| 11 | Personal Accident | Available |
| 12 | Return of Premium | Not Available |
| 13 | Payout Option | Lumpsum *(options: Lumpsum / Income / Increasing)* |
| 14 | PPT (Premium Payment Term) | Regular *(options: Regular / 5 Yrs / 10 Yrs / 15 Yrs)* |
| 15 | Premium Amount | 17,951 |

**Convention:** field 3 (Ideal Sum Assured) must trace back to a ProTool 15 need analysis — a recommendation is only defensible if the need was computed first. The four riders (CI, WOP, PA, ROP) are the standard comparison set for term-plan MCQs.

---

## ProTool 26 — Health Insurance Recommendation Template
**Session 26 · `ProTool 26 - Health Insurance Recommedation Template.xlsx`**

| # | Field | Worked example |
|---|---|---|
| 1–2 | Name, Age | Mr. ABC, 30 |
| 3 | Family Count | 2 Adult + 2 Children |
| 4 | Single / Family Floater | Family Floater |
| 5–6 | Company, Policy Name | Niva Bupa, ReAssure |
| 7 | **Room Category** | Any Category |
| 8 | **Restoration Benefit** | Covered |
| 9 | **No Claim Bonus / Year** | 50% |
| 10 | **PED Waiting Period** | 36 Months |
| 11 | Unique Features | Unlimited Restore |
| 12 | Maternity Cover | Not Covered |
| 13 | **Co-Pay** | Nil |
| 14 | Free Health Checkup limit | Covered up to ₹10,000 |
| 15 | Insurance Cover | 50,00,000 |
| 16 | Years of premium payment | 1 |
| 17 | Premium | 36,233 |

The eight comparison levers examinable for health-product suitability: room-rent category, restoration, NCB, PED waiting period, maternity, co-pay, sub-limits, and cover amount.

---

## ProTool 27 — All-in-One SIP Calculator
**Session 27 · `Protool 27- SIP Calculator.xlsx`**

Two independent calculators on one sheet: **left (H / J–O) = step-up by percentage**, **right (W / Y–AD) = step-up by fixed rupee amount**.

| Input | Left | Right |
|---|---|---|
| SIP amount p.m. | H7 | W7 |
| SIP duration (yrs) | H8 | W8 |
| Step-up rate (%) / amount (₹) | H9 | W9 |
| Step-up duration (yrs) | H10 | W10 |
| Rate of return | H11 | W11 |
| Horizon after SIP period | H12 | W12 |

### Year table (rows 8–67)
```
K8  =H7
M8  =IF(OR(J8>H$10,J8=0),0,H$9)                          ' step-up only within step-up duration
N8  =IF(J8=0,0,H$11)
O8  =IF(J8=0,0, FV((1+N8)^(1/12)-1, 12, -K8, -L8, 1))
J9  =IF(OR(J8=0,J8>=H$15),0,J8+1)
K9  =IF(AND(J9<=H$8,J9>0), K8*(1+M8), 0)                 ' LEFT: multiply
Z9  =IF(AND(Y9<=W$8,Y9>0), Z8+AB8, 0)                    ' RIGHT: add fixed amount
O9  =IF(J9=0,0, FV((1+N9)^(1/12)-1, 12, -K9, -(O8+L9), 1))
H15 =H8+H12                                               ' total investment duration
H17 =SUM(K8:K67)*12+SUM(L8:L67)                           ' total invested
H19 =VLOOKUP(H$15, J$8:O$67, 6, 0)                        ' <-- THE ANSWER CELL
```

### Conventions
1. **Monthly rate = `(1+annual)^(1/12) − 1`** (convention C) — the effective monthly equivalent, *not* `annual/12`.
2. SIP is **Type = 1 (beginning of month)**.
3. Step-up applies from **year 2**, only while `year ≤ step-up duration`; thereafter the instalment freezes but keeps compounding.
4. Prior year's closing corpus enters the next year as `pv`, with any fresh lumpsum added.
5. Answer read via **VLOOKUP on total duration** (SIP years + post-SIP horizon), column 6 — not the last row.

**Verified:** ₹25,000 p.m., 15 yrs, 6% step-up for 10 yrs, 11% → Yr1 3,17,590.06 · Yr2 6,89,170.42 · **corpus 1,47,65,137**, invested 66,40,510. Right panel: ₹10,000 p.m. + ₹5,000 annual step-up for 15 yrs, 25 yrs, 12%, ₹2,00,000 lumpsum yr 1 → **7,40,33,463**, invested 1,85,00,000.

**Case Study:** Q1 Education 1.47 Cr / Retirement 7.40 Cr · Q2 2.35 Cr · Q3 2.49 Cr.

---

## ProTool 28 — SWP Calculator
**Session 28 · `Protool 28 - SWP Calculator.xlsx`**

Answers **"how long will the corpus last?"** — a duration question, not a corpus question.

### Inputs
`D5` Current Age (62) · `D6` Start Date (01-Apr-2026) · `D7` Rate of Return (8.5%) · `D8` **Step-up SWP Rate (5%)** · `D9` Initial Corpus (₹1,00,00,000) · `D10` Monthly SWP Required (₹50,000). Column K carries ad-hoc **lumpsum withdrawals** (₹5,00,000 entered at row 17).

### Monthly engine (rows 6–605, 50 years)
```
I6  =D9                                    ' beginning value
J6  =D10                                   ' SWP amount
M6  =IF(I6=0, 0, (I6-J6-$K6)*(1+NOMINAL(L6,12)/12))     ' ENDING VALUE
I7  =M6
J7  =IF( IF(MOD(F7,12)=1, J6*(1+$D$8), J6) > I7, I7,
         IF(MOD(F7,12)=1, J6*(1+$D$8), J6) )
G7  =IF(I7=0,"-", DATE(YEAR(G6),MONTH(G6)+1,DAY(G6)))
F7  =IF(I7=0, 0, F6+1)
D12 =(COUNTA($G$6:$G$605)-COUNTIF($G$6:$G$605,"-"))/12   ' SWP DURATION IN YEARS
D13 =SUM(J6:J605, $K$6:$K$605)                            ' total withdrawn
D14 =IF(M605=0, 0, M605)                                  ' residual corpus
```
Annual summary block (O–U) rolls months into years:
```
S6 =SUMIFS($J$6:$J$1000,$H$6:$H$1000,$Q6)+SUMIFS($K$6:$K$1000,$H$6:$H$1000,$Q6)
U6 =IF(S6<=0,0, IFERROR(INDEX($M$6:$M$605, MATCH($T6, $F$6:$F$605, 0)), 0))
```

### Conventions
1. **Withdrawal happens BEFORE growth**: `(opening − SWP − lumpsum) × (1 + monthly rate)`. Reversing the order overstates longevity.
2. Monthly rate is convention B — `NOMINAL(annual,12)/12`.
3. **Step-up fires on month 13, 25, 37…** — `MOD(month,12)=1` — i.e. annually from the second year.
4. The withdrawal **self-caps** at the available balance in the final month, so the corpus lands exactly at zero rather than going negative.
5. Duration is counted as **surviving months ÷ 12** and reported to one decimal.

**Verified:** ₹1 Cr corpus, ₹50,000 p.m. SWP, 5% annual step-up, 8.5% return, one ₹5,00,000 lumpsum withdrawal → **23.2 years**, total withdrawn ₹2,56,49,283, residual nil.

**Case Study:** Q1 23.2 yrs · Q2 18.1 yrs · Q3 27.1 yrs.

---

## ProTool 29 — Equity MF Whitelist Tracker
**Session 29 · `Protool 29 - Equity MF Whitelist Tracker.xlsx`** · companion data file: `ValueResearch MF Data File.xlsx`

A scoring grid, no formulas — the parameter set is what's examinable:

| Group | Parameters |
|---|---|
| **Scheme Details** | Scheme Name, Launch Date, Sub Category, Benchmark, AUM (Crs.), **Expense Ratio (BER)** |
| **Portfolio** | Portfolio Turnover, Large Cap %, Midcap %, Small Cap %, Others, No. of Stocks, Top 10 holdings concentration |
| **Fund Manager** | tenure / track record |
| **Trailing Returns** | 1Y / 3Y / 5Y / since inception |
| **Risk Ratios** | standard deviation, beta, Sharpe, alpha, Sortino |
| **Score** | composite whitelist score |

The evaluation logic: screen on category fit → check AUM and expense ratio → examine portfolio composition and concentration → assess manager tenure → compare trailing returns against benchmark and category → confirm risk-adjusted ratios → score and whitelist.

---

## ProTool 30 — Employment Benefits Calculator
**Session 30 · `Protool 30 - Employment Benefits Calculator.xlsx`**
Four calculators on one sheet: **EPF (5–72)**, **NPS (74–135)**, **PPF (137–168)**, **Gratuity (170–178)**.

### 1) EPF Accumulation
Inputs: `C6` current age · `D6` retirement age · `E6` monthly salary (Basic+DA) · `F6` salary increase % · `G6` contribution % · `H6` opening EPF balance · `I6` interest rate.
```
J6  =VLOOKUP(D6, $C$9:$J$72, 6, 0)          ' answer: closing balance at retirement-age row
D9  =E6*12                                   ' annual salary
E9  =D9*$G$6                                 ' employee EPF contribution
F9  = VPF (manual entry, 0 by default)
G9  =IF(E9=0, 0, E9-(1250*12))               ' employer EPF = employee share LESS EPS
I9  =SUM(E9:G9)
J9  =FV($I$6,1,,-H9,0) + FV(NOMINAL($I$6,12)/12, 12, -I9/12, , )
D10 =IF(C10>=D$6, 0, D9*(1+$F$6))
H10 =J9
J10 =IF(C10>=D$6, 0, FV($I$6,1,,-H10,0)+FV(NOMINAL($I$6,12)/12,12,-I10/12,,))
```
**Conventions:** (a) the employer's EPF share is reduced by the **EPS diversion of ₹1,250 p.m. = ₹15,000 p.a.** — omit it and the corpus is overstated; (b) the opening balance compounds **annually**, the current year's contributions compound **monthly** at convention B, end-of-month; (c) salary steps up from year 2; (d) rows stop at retirement age.

*Verified:* age 48→60, ₹50,000 p.m. salary, 5% increase, 12% contribution, VPF ₹5,000 p.m. for 12 yrs, opening ₹9,20,000, 8.25% → Yr1 **11,91,944.28**, Yr2 **14,93,792.32**, **corpus at 60 = 69,26,230**.

### 2) NPS
Inputs: `C77` current age · `D77` retirement age · `E77` NPS balance · `F77` yearly contribution (year-END) · `G77` step-up · `H77` return · `L77` annuity rate.
```
I77 =VLOOKUP(D$77, $C$80:$D$135, 2, 0)   ' corpus = OPENING balance of retirement-age row
J77 =I77*80%                              ' available for withdrawal
K77 =I77*20%                              ' compulsory annuity purchase
M77 =(K77*L77)/12                         ' monthly annuity, pre-tax
F80 =IF(C80>=$D$77, 0, FV($H$77,1,,-D80,0)+E80)
D81 =IF(C81>D$77, 0, F80)
E81 =IF(C81>=$D$77, 0, E80*(1+$G$77))
```
**Conventions:** contributions are **year-end** (added after the year's growth); the reported corpus is the **opening balance of the retirement-age row** (= closing of the prior year), not the last row; the **80/20 split is hard-coded**; monthly annuity = 20% of corpus × annuity rate ÷ 12.

*Verified:* age 45→60, ₹15,00,000 balance, ₹50,000 p.a., 5% step-up, 10% return, 6% annuity → **corpus 83,64,192 · lumpsum 66,91,354 · annuity corpus 16,72,838 · monthly annuity 8,364**.

### 3) PPF
Inputs: `E138` today's date · `E139` current age · `E140` yearly contribution (END) · `E141` account opening date · `I138` current balance · `I139` rate.
```
I140 =IF(MONTH(E141)<=3, DATE(YEAR(E141)+15,4,1), DATE(YEAR(E141)+16,4,1))   ' MATURITY DATE
I141 = FY string of I140
I142 =VLOOKUP($I141, $D$145:$E$161, 2, 0)     ' answer = OPENING balance of the maturity FY
D145 = FY of today
E145 =I138
F145 =$E$140
G145 =FV($I$139, (DATE(YEAR(E138)+IF(MONTH(E138)<=3,0,1),3,31)-E138)/365, , -E145) + F145
D146 =LEFT(D145,4)+1 & "-" & TEXT(RIGHT(D145,2)+1,"00")
G146 =FV($I$139, 1, , -E146) + F146
```
**Conventions:** (a) **maturity = 1 April, 15 full FYs after the FY of opening** — opened 15-Jan-2021 (FY 2020-21) → matures **1-Apr-2036**; (b) the **first year is a stub**: `(31-March-of-current-FY − today)/365` years of growth on the opening balance, then the contribution is added; (c) contributions are **end-of-year** and earn nothing in the year they are made; (d) the reported value is the **opening balance of the maturity FY** (= closing of FY 2035-36), because PPF earns no interest in the maturity year.

*Verified exactly:* today 04-Jul-2026, balance ₹5,50,000, ₹40,000 p.a., opened 15-Jan-2021, 7.1% → FY 2026-27 closing **6,18,627.055** · FY 2027-28 closing **7,02,549.576** · **maturity value 16,28,039**.

### 4) Gratuity
**Covered under the Payment of Gratuity Act** (row 174):
```
H174 =FV(G174, (D174-C174), , -F174)        ' monthly salary at retirement
I174 =(15/26)*(E174+(D174-C174))*H174       ' 15/26 x total service years x last drawn salary
```
**NOT covered by the Act** (row 178):
```
I178 =(H178 + FV(G178,(D178-C178)-1,,-F178))/2   ' avg of last 10 months ~ mean of final two years
J178 =(1/2)*(E178+(D178-C178))*I178              ' 1/2 (=15/30) x years x average salary
```
**Conventions:** covered → **15/26** of *last drawn* monthly salary; not covered → **1/2** of the *average of the last 10 months'* salary. Total service = years already worked + years to retirement. Statutory exemption cap **₹20,00,000**.

*Verified:* age 40→55, 11 yrs served, ₹35,000 p.m., 10% increase → salary at 55 = 1,46,203.69, **gratuity 21,93,055**, taxable 1,93,055.

**Case Study:** Q1 EPF at 60 = 69,26,230 · NPS total 83,64,192 / lumpsum 66,91,354 · PPF 16,28,039 · Gratuity at 55 = 21,93,055 (taxable 1,93,055). Q2 EPF at 60 = 2,59,37,321. Q3 Gratuity at 58 (not covered) = 26,94,806.

---

## ProTool 31 — Debt MF Whitelist Tracker
**Session 31 · `ProTool 31 - Debt MF Whitelist Tracker.xlsx`** · Sheets: tracker + filled example

| Group | Parameters |
|---|---|
| **Scheme Details** | Scheme Name, Sub Category, Launch Date, AUM, Expense Ratio |
| **Fund Manager** | tenure |
| **Portfolio Aggregates** | **Modified Duration, Average Maturity, YTM**, number of securities |
| **Allocation in High Quality Papers** | Sovereign / AAA / AA+ / below-AA exposure |
| **Trailing Returns** | 1Y / 3Y / 5Y |
| **Score** | composite |

The debt-specific screen that distinguishes this from ProTool 29: **credit quality** (proportion in sovereign and AAA) and **interest-rate risk** (modified duration vs the investor's horizon). YTM net of expense ratio is the realistic return expectation.

---

## ProTool 32 — Loan Amortization Calculator
**Session 32 · `ProTool 32 - Loan Amortization Calculator.xlsx`** · Sheets: Case Study, Loan Calculator (Trainer/Candidate), Step-up EMI (Trainer/Candidate)

### Header block
| Cell | Field | Formula / value |
|---|---|---|
| F5 | Principal | `=9000000*80%` → 72,00,000 (80% LTV) |
| H5 | Interest rate | 8.25% |
| J5 | Tenure (yrs) | 20 |
| **L5** | **EMI** | `=IFERROR(-PMT(H5/12, J5*12, F5,,),0)` → **61,348.73** |
| J9 | First (next) EMI date | 01-Apr-2026 |
| F11 | Tenure in months | `=F10*12` → 240 |
| F12 | **No. of EMIs with prepayments** | `=(COUNT($F$15:$F$414)-COUNTIF($F$15:$F$414,0))-1` → **213** |
| J10 | Loan end date | `=DATE(YEAR(J9),MONTH(J9)+F12-1,DAY(J9))` |

### Schedule (rows 15–414, 400 months max)
| Col | Field | Formula |
|---|---|---|
| C | Sr No | `=+C15+1` |
| D | Month | `=DATE(YEAR(D15),MONTH(D15)+1,DAY(D15))` |
| E | Financial Year | `=IF(MONTH(D15)<=3, YEAR(D15)-1&"-"&RIGHT(YEAR(D15),2), YEAR(D15)&"-"&RIGHT(YEAR(D15)+1,2))` |
| F | Principal opening | `=L15` (prior month's closing) |
| G | EMI | `=IF($F15<=0,0, IF($F15*(1+NOMINAL($F$9,12)/12)<$J$8, $F15*(1+NOMINAL($F$9,12)/12), IF($F15*(1+NOMINAL($F$9,12)/12)>=$J$8, $J$8,)))` |
| H | Interest | `=IF(G15=0,0, F15*($F$9/12))` |
| I | Principal repaid | `=G15-H15` |
| J | Outstanding | `=F15-I15` |
| K | **Prepayment** | manual entry |
| L | Principal closing | `=IF(ROUND(J15-K15,0)<=0, 0, (J15-K15))` |

### Conventions
1. **EMI uses the simple periodic rate `H5/12`** (convention D) — the entered rate is nominal. Interest charged each month is always `opening × rate/12`. (Column G's *cap test* uses `NOMINAL(F9,12)/12`, a marginally different figure used only to detect the final part-EMI.)
2. The final EMI **self-truncates**: if outstanding plus one month's interest is less than the standard EMI, that smaller amount closes the loan.
3. **Prepayments (column K) reduce the closing balance directly** — the EMI is unchanged, the tenure shortens. `F12` counts surviving rows for the actual EMI count (213 vs 240 in the trainer case).
4. FY tagging is on the **EMI month** — "prepayment in FY 2026-27" means Apr-2026 to Mar-2027.
5. Closing balance snaps to 0 once `ROUND(bal,0) <= 0`.

*Verified:* ₹90,00,000 property at 80% LTV = ₹72,00,000, 8.25%, 20 yrs → **EMI 61,348.73**; month 1 interest 49,500, principal 11,848.73, closing 71,88,151.27.

**Case Study:** total EMIs after step-up EMI = **147 months**.

---

## ProTool 33 — SIP to Foreclose Home Loan
**Session 33 · `ProTool 33 - SIP to foreclose Home Loan.xlsx`** · Sheets: Case Study, Input Sheet (Trainers/Candidates), Prepayment Chart (Trainers/Candidates)

Answers two symmetric questions: **Option 1 — what SIP is needed to close the loan in N years?** and **Option 2 — given a SIP I can afford, when will the loan close?**

### Input Sheet
```
C12 =-PMT(C10/C9, C8*C9, C7)                ' EMI - convention D (rate/12)
C14 =C12*C8*C9                               ' total repayment over full tenure
C16 =C14-C7                                  ' total interest
' --- Option 1: fix the year, solve the SIP ---
C22 =INDEX('Prepayment Chart'!$H$11:$H$310, C19*C20)     ' outstanding at target month
C24 =PMT((1+C21)^(1/C20)-1, C19*C20, , -C22, )           ' required SIP - CONVENTION C
C25 =C24/C12                                              ' SIP as % of EMI
' --- Option 2: fix the SIP, solve the year ---
C29 =C28/C12
C33 =(MATCH(TRUE, 'Prepayment Chart'!L11:L310 >= 'Prepayment Chart'!$H$11:$H$310, 0))/12
C34 =INDEX('Prepayment Chart'!$H$11:$H$310, C33*C30)      ' outstanding at that month
C35 =INDEX('Prepayment Chart'!L11:L310, C33*C30)          ' fund value at that month
```
`C33`, `C22`, `C34`, `C35` are **array formulas**.

### Prepayment Chart engine
```
G8  =-ROUND(PMT(G6/12, G7, G5, 0, 0), 0)      ' EMI, ROUNDED TO THE RUPEE
F11 =D11*$G$6/12                               ' interest
G11 =E11-F11                                   ' principal
H11 =D11-G11                                   ' closing
D12 =IF(H11-I11<0, 0, H11-I11)
E12 =IF($D12<E11, $D12+$F12, E11)              ' final part-EMI
K11 =IF($H11<>0, $L$4, $L$4+$G$8)              ' SIP; AFTER the loan closes, EMI is ADDED to the SIP
L11 =K11+(K11*$L$5/12)                         ' fund value, monthly simple accrual
L12 =L11+K12+((L11+K12)*$L$5/12)
```

### Conventions
1. **Option 2's answer is the first month at which fund value ≥ outstanding balance** — `MATCH(TRUE, L>=H, 0)/12`. It is a crossover search, not a formula.
2. **The EMI is rounded to the nearest rupee** before the schedule runs (`ROUND(...,0)`), so a schedule built on the unrounded EMI drifts.
3. Option 1's SIP uses **convention C** (`(1+r)^(1/12)−1`), while the loan side uses **convention D** (`r/12`) — two different rate conventions inside one tool.
4. Once the loan closes (`H = 0`), the freed-up EMI is **redirected into the SIP** (`K = L4 + G8`).
5. Fund value accrues as `balance × rate/12` monthly on the running balance.

*Verified:* ₹60,00,000 loan, 20 yrs, 8.5% → **EMI 52,069.39** (rounded 52,069); total repayment ₹1,24,96,655; total interest ₹64,96,655. Option 1 (close in 12 yrs, 10% return): outstanding at month 144 = ₹36,18,006 → **SIP ₹13,491** = 25.91% of EMI. Option 2 (₹15,000 SIP = 28.81% of EMI): **loan closes in 11.42 years**, outstanding ₹37,97,961 against fund value ₹38,42,723.

**Case Study:** Q1 Option 1 SIP ₹13,491 for 12 yrs / Option 2 11 yrs · Q2 ₹11,355 for 15 yrs / 12 yrs · Q3 ₹14,050 for 10 yrs / 11 yrs.

---

## ProTool 34 — House Rent vs. Purchase Calculator
**Session 34 · `ProTool 34 - House Rent vs. Purchase Calculator.xlsx`** (and `( Filled )` variant) · Sheets: Case Study, Input Sheet, Buy vs Rent, Cash Flow, Buy Later, Buy Later @Inflation, EMI - Rent Invested, Checklist

### Input Sheet
| Cell | Field | Trainer |
|---|---|---|
| C5 | Cost of Property | 92,00,000 |
| C6 | Downpayment % | 25% |
| C7 | Loan Interest | 8.4% |
| C8 | Loan duration (yrs) | 20 |
| C9 | Loan Type (Individual / Joint) | Individual |
| C10 | Duration of Stay (yrs) | 20 |
| C11 | Maintenance Cost (yearly, %) | 0.5% |
| C12 | Annual increase in Maintenance | 6% |
| C13 | Appreciation of House Property | 6% |
| C14 | Incidental Costs % | 8% |
| C15 | Incidental Costs | `=C14*C5` → 7,36,000 |
| C16 | Monthly Rent | 32,000 |
| C17 / C18 | Tax Bracket (self / spouse) | 30% / 30% |
| C19 | Deduction for Taxation (HRA / 80GG) | 18,000 |
| C20 | Average Annual Rental Increment | 6% |
| C21 | Rate of return on Investment | 12% |
| C23 | **Postponement Years** (for Buy Later) | 4 |

### Tax-saving block
```
G8  =G6+G7                                   ' 80C principal 1,50,000 + Sec 24 interest 2,00,000 = 3,50,000
G9  =G8*C17                                  ' tax saving (self) = 1,05,000
G14 =MIN(G9+IF(C9="Joint",G13,0), IF(C9="Joint",210000,105000))     ' CAP: 1,05,000 single / 2,10,000 joint
G15 =G14/12                                  ' monthly tax saving = 8,750
```

### Buy vs Rent sheet
```
' BUY side
C6  =C4*C5                        ' downpayment 23,00,000
C7  =C4-C6                        ' loan 69,00,000
C10 =-PMT(C8/12, C9*12, C7,0,0)   ' EMI 59,443.81   (convention D)
C11 = monthly tax saving 8,750
C12 =C10-C11                      ' effective tax-adjusted EMI 50,693.81
C14 =(C12*12*C9)-C7               ' total NET interest paid 52,66,514
C17 =C4*C16/12                    ' monthly maintenance 3,833.33
C19 =FV(C18,'Input'!C10, -(C17*12), 0,0)   ' total maintenance over period 16,92,137
C21 =C4+C14+C15+C19               ' TOTAL COST OF BUYING 1,68,94,652
C24 = value of property after the period (appreciated at C13)
' RENT side
F7  =F4-(F6*F5)                   ' effective rent = rent - (HRA deduction x tax bracket) = 26,600
F8  =F7*12                        ' effective annual rent 3,19,200
F11 =FV(F10,F9,-F8,0,0)           ' total rent over 20 yrs 1,17,41,961
F12 =C6                           ' downpayment freed up for investment 23,00,000
F13 =C12-F7                       ' monthly saving vs EMI 24,093.81
F21 ='Cash Flow'!I24              ' net benefit of renting, TVM-adjusted 4,07,81,492
```

### Conventions
1. **Effective rent is net of the HRA/80GG tax shield**, and **effective EMI is net of the 80C + Section 24 tax saving** — compare like with like.
2. The buy-side tax saving is **capped** at ₹1,05,000 (individual) or ₹2,10,000 (joint), reflecting 80C ₹1.5L + Sec 24 ₹2L at the 30% bracket.
3. Total cost of buying = property cost + net interest + incidental costs + cumulative maintenance. **Incidental costs (8%) and maintenance are the two components candidates forget.**
4. The renting case invests **both** the freed-up downpayment *and* the monthly EMI-minus-rent differential at C21 (12%) — this is what makes renting win in the worked case.
5. `Buy Later` and `Buy Later @Inflation` sheets test postponing the purchase by C23 years, the second inflating the property price meanwhile.

**Case Study:** Q1a **Renting is better, generating an additional corpus of ₹1.12 Crore**; Q1b if the family wants to buy, **buying now beats buying after 4 years** with property appreciation. Q2 renting better by ₹79 lakhs. Q3 renting better by ₹81 lakhs.

---

## ProTool 35 — Letter of Engagement (Onboarding)
**Session 35 · `ProTool 35- Onboarding - Letter of Engagement.docx`** (Word)

A client-onboarding engagement letter, illustrated for "Wisdom Financial Consultants Pvt Ltd". Structure:

1. **Addressee block** and thanks for the interest shown
2. **Purpose** — "This engagement letter outlines the specific terms of engagement between [firm] and its clients with respect to financial consultancy services."
3. **Long-term framing** — "the real value of our expertise and services accrue over a long term while we help client families achieve complete financial wellbeing"
4. **Financial Consultancy Process** — states the firm follows "the financial consultancy process recommended by **Network FP** – a premier institute for personal finance professionals," and that the team is fully trained in it
5. Scope of services, fee structure and basis, responsibilities of both parties, conflict-of-interest disclosure, confidentiality, term and termination, signatures

Examinable point: the Letter of Engagement is the **documentary anchor of the fiduciary relationship** — scope, fees and conflicts must be disclosed in writing before advice is given (ties back to ProTool 08).

---

## ProTool 36 — Capital Gains Calculator
**Session 36 · `ProTool 36 - Capital Gains Calculator ( Filled ).xlsx`** · Sheets: Case Study, Taxation Rules, Equity, Debt, Hybrid, Other Funds, Gold-Silver ETF, Real Estate, Indexation rates

### The three dates that decide everything
| Excel serial | Date | Meaning |
|---|---|---|
| 43131 | **31-Jan-2018** | Grandfathering cut-off for equity |
| 45017 | **01-Apr-2023** | Debt-fund indexation withdrawal |
| 45495 | **22-Jul-2024** | Budget 2024 — new rates apply to sales **on or after 23-Jul-2024** |

### Equity sheet
```
C10 =DATEDIF(C8,C9,"m")                                   ' holding period, months
C11 =IF(AND(C8<=43131, C10>=12), "Yes","No")              ' grandfathering eligible
C12 =IF(C10<12, "Short Term","Long Term")
C13 =IF(C9<=45495, IF(C12="Long Term",10%,15%),
                   IF(C12="Long Term",12.5%,20%))
C18 =IF(C11="Yes", MIN(C16,C17), "-")     ' min(FMV 31-Jan-18, sale price)
C19 =IF(C11="Yes", MAX(C15,C18), "-")     ' max(actual cost, above)
C20 =IF(C11="Yes", C19, C15)              ' grandfathered cost of acquisition
C25 =C23-C24                               ' capital gain
D36 =IF(SUM(D33:D34,D29:D30)>=125000, 125000, SUM(D33:D34,D29:D30))   ' LTCG exemption cap
D38 =((SUM(D29:D30)-MIN(SUM(D29:D30),D36))*D31)
    +((SUM(D33:D34)-(D36-MIN(SUM(D29:D30),D36)))*D35)
C30 =SUMIFS($C$25:$D$25, $C$9:$D$9,"<=45495", $C$12:$D$12, C$27)   ' pre-23-July slice
C34 =SUMIFS($C$25:$D$25, $C$9:$D$9,">45495",  $C$12:$D$12, C$27)   ' post-23-July slice
```
**Grandfathering chain (s.55(2)(ac)):** cost = `MAX( actual cost , MIN( FMV on 31-Jan-2018 , sale consideration ) )`. Applies only if bought on/before 31-Jan-2018 **and** held ≥12 months.
**LTCG exemption:** ₹1,25,000 per FY (₹1,00,000 for sales before 23-Jul-2024), consumed by the **pre-23-July slice first**, the remainder applied to the post-23-July slice.

### Debt sheet
```
C11 =IF(C9<DATE(2024,7,23), "Yes","No")                      ' old-regime sale
C12 =IF(C8<DATE(2023,4,1), IF(C11="Yes", IF(C10>=36,"Yes","No"), "No"), "No")  ' indexation allowed
C13 =IF(C8<45017, IF(C11="Yes", IF(C10<36,"Short Term","Long Term"),
                                IF(C10<24,"Short Term","Long Term")), "Does not matter")
C14 =IF(C8<45017, IF(C11="Yes", IF(C13="Short Term",$C$4,20%),
                                IF(C13="Short Term",$C$4,12.5%)), $C$4)   ' $C$4 = slab rate
C20 =IFERROR(VLOOKUP(C18,'Indexation rates'!$B$3:$C$28,2,0),"NA")
C22 =((C21/C20)*C16)                       ' indexed cost per unit
C28 =IF(C12="Yes", C25-C27, C25-C26)
C29 =C14*C28
```
**Key rule:** a debt fund bought **on or after 1-Apr-2023 is always taxed at slab rates** — no LTCG, no indexation. Bought before that date, indexation survives only if also sold before 23-Jul-2024 and held ≥36 months.

### Hybrid sheet (35–65% equity)
```
C13 =IF(C9>=DATE(2024,7,23), IF(C10>=24,"Long Term","Short Term"),
                             IF(C10>=36,"Long Term","Short Term"))
C14 =IF(C9>=DATE(2024,7,23), IF(C10>=24,"12.5%",$C$4), IF(C10>=36,"20%",$C$4))
```
Holding threshold moves **36 → 24 months** for sales on/after 23-Jul-2024.

### FY tagging for indexation
`=IF(MONTH(date)>=4, YEAR&"-"&RIGHT(YEAR+1,2), YEAR-1&"-"&RIGHT(YEAR,2))`

### Cost Inflation Index (`Indexation rates` B3:C28)
| FY | CII | FY | CII | FY | CII | FY | CII |
|---|---|---|---|---|---|---|---|
| 2001-02 | 100 | 2007-08 | 129 | 2013-14 | 220 | 2019-20 | 289 |
| 2002-03 | 105 | 2008-09 | 137 | 2014-15 | 240 | 2020-21 | 301 |
| 2003-04 | 109 | 2009-10 | 148 | 2015-16 | 254 | 2021-22 | 317 |
| 2004-05 | 113 | 2010-11 | 167 | 2016-17 | 264 | 2022-23 | 331 |
| 2005-06 | 117 | 2011-12 | 184 | 2017-18 | 272 | 2023-24 | 348 |
| 2006-07 | 122 | 2012-13 | 200 | 2018-19 | 280 | 2024-25 | 363 |
| | | | | | | 2025-26 | 376 |
| | | | | | | 2026-27 | 384 |

### `Taxation Rules` master matrix (verbatim from the sheet)

**Equity-oriented funds (>65% equity)** — Equity Fund, Arbitrage, Aggressive Hybrid, Equity Savings
| Condition | Short term | Long term |
|---|---|---|
| Bought ≤31-Jan-2018, sold ≤22-Jul-2024 | – | >12 m → 10% **with grandfathering** |
| Bought >31-Jan-2018, sold ≤22-Jul-2024 | <12 m → 15% | >12 m → 10% |
| Bought ≤31-Jan-2018, sold ≥23-Jul-2024 | – | >12 m → 12.5% **with grandfathering** |
| Bought >31-Jan-2018, sold ≥23-Jul-2024 | <12 m → 20% | >12 m → 12.5% |

**Debt-oriented funds (>65% debt)** — Debt Fund, Conservative Hybrid, FOF-Debt
| Condition | Short term | Long term |
|---|---|---|
| Bought <01-Apr-2023, sold ≤22-Jul-2024 | <36 m → slab | >36 m → 20% **with indexation** |
| Bought <01-Apr-2023, sold ≥23-Jul-2024 | <24 m → slab | >24 m → 12.5% |
| Bought & sold ≥01-Apr-2023 | slab | slab |

**Non-equity / hybrid (35–65% equity)** — Balanced Hybrid, FOF-Balanced
| Condition | Short term | Long term |
|---|---|---|
| Sold ≤22-Jul-2024 | <36 m → slab | >36 m → 20% with indexation |
| Sold ≥23-Jul-2024 | <24 m → slab | >24 m → 12.5% |

**Other mutual funds** — Gold/Silver MF, FOF-International, FOF-Equity
| Condition | Short term | Long term |
|---|---|---|
| Bought <01-Apr-2023, sold ≤22-Jul-2024 | <36 m → slab | >36 m → 20% with indexation |
| Bought <01-Apr-2023, sold ≥23-Jul-2024 | <24 m → slab | >24 m → 12.5% |
| Bought ≥01-Apr-2023, sold ≤31-Mar-2025 | slab | slab |
| Bought ≥01-Apr-2023, sold ≥01-Apr-2025 | <24 m → slab | >24 m → 12.5% |

**Gold / Silver ETF** — as above, except the final row: sold ≥01-Apr-2025 → **<12 m slab, >12 m 12.5%**.

**Real Estate (property)**
| Condition | Short term | Long term |
|---|---|---|
| Bought & sold before 01-Apr-2017 | <36 m → slab | >36 m → 20% with indexation |
| Bought & sold before 23-Jul-2024 | <24 m → slab | >24 m → 20% with indexation |
| Bought <23-Jul-2024, sold ≥23-Jul-2024 | <24 m → slab | >24 m → **lower of 12.5% without indexation or 20% with indexation** |
| Bought & sold ≥23-Jul-2024 | <24 m → slab | >24 m → 12.5% without indexation |

**Notes from the sheet**
1. LTCG up to **₹1.25 lakh per FY is tax-exempt** for equities.
2. ELSS: 3-year lock-in; deduction up to ₹1.5 lakh (old regime only).
3. Children's Fund & Retirement Fund: 5-year lock-in. Their taxation follows equity allocation — <35% equity → debt treatment; 35–65% → non-equity; >65% → equity.
4. Rules per Union Budget 2024.

---

# PART 4 — Cross-tool convention register

The highest-value page in this file. Most wrong options are manufactured by violating one of these.

| Convention | Applies to | The trap |
|---|---|---|
| Periodic rate `EFFECT(NOMINAL(r,I),J)/I` → `r/I` when I=J | ProTool 05, 10 | Input rate is **nominal** |
| Periodic rate `NOMINAL(r,12)/12` | ProTool 17, 18, 19, 28, 30 (EPF) | Input rate is **effective** |
| Monthly rate `(1+r)^(1/12) − 1` | ProTool 27, 33 (SIP leg) | Effective monthly equivalent |
| Simple `r/12` | ProTool 32, 33 (loan leg), 34 | Plain nominal |
| Real return `(1+r)/(1+i) − 1` | ProTool 06, 15, 19, 20 | Never `r − i` |
| Tax first, then inflation | ProTool 06 blk 7, 15, 19 | Never combined in one step |
| Annuity-due (Type 1) | ProTool 15 corpus, 19 corpus, 20 all buckets, 27 SIP, 10 | Beginning-of-period |
| Ordinary annuity (Type 0) | ProTool 30 NPS & PPF contributions | No interest in the contribution year |
| Stub first year `(31-Mar − today)/365` | ProTool 30 PPF | Whole-year assumption is off by thousands |
| VLOOKUP reports the **opening** balance of the target row | ProTool 30 NPS & PPF | Not the last row of the schedule |
| VLOOKUP on total duration, column 6 | ProTool 27 | Not the last row |
| Withdrawal **before** growth | ProTool 28 SWP | Reversing overstates longevity |
| EPS diversion ₹1,250 p.m. off employer's share | ProTool 30 EPF | Overstates corpus if missed |
| PPF matures 1 April, 15 FYs after the FY of opening | ProTool 30 PPF | Not 15 years from the opening date |
| Gratuity 15/26 (covered) vs 1/2 (not covered); cap ₹20,00,000 | ProTool 30 | Last drawn vs last-10-month average |
| Two different FVs — cost-inclusive vs bare, Type 0 vs Type 1 | ProTool 18 | Accumulate `D19 + (D13 − D14)`, not 20% of D13 |
| Each bucket discounted at **its own** rate | ProTool 20 | The weighted average is reported, not used |
| Each goal carries **its own** inflation | ProTool 17, 24 | Education 10% ≠ general 7% ≠ marriage 8% |
| Expense base **includes** EMIs and ongoing investments | ProTool 16 | Commonly excluded in error |
| `ROUND(x,-4)` then use the rounded figure | ProTool 16 | Deficit is computed off the rounded requirement |
| EMI rounded to the rupee before the schedule runs | ProTool 33 | Unrounded EMI drifts the crossover month |
| Step-up applies from year 2, only within step-up duration | ProTool 17, 18, 19, 27, 28, 30 NPS | Then freezes but keeps compounding |
| Rule of 72 on the rate **as a percentage** | ProTool 10 | `72/(r*100)` |
| Portfolio return = SUMPRODUCT(returns, allocation) | ProTool 24 | Weighted, never simple average |
| 80CCD(2): 10% of Basic old / **14% new** | ProTool 21 | High-frequency exam point |
| 87A rebate: ₹5,00,000 old / **₹12,00,000 new** | ProTool 21 | |
| Surcharge tops at 37% old / **25% new** | ProTool 21 | |
| Standard deduction ₹50,000 + PT old / **₹75,000 new**, no PT | ProTool 21 | |
| 22-Jul-2024 / 01-Apr-2023 / 31-Jan-2018 | ProTool 36 | Every capital-gains question turns on one of these |
| Grandfathering = MAX(cost, MIN(FMV 31-Jan-18, sale)) | ProTool 36 | Three-step chain, not two |
| Horizon = **spouse's** remaining life expectancy | ProTool 15 | Not the client's |
| Discounting factor removes deceased's own consumption | ProTool 15 | Apply before inflating |

---

# PART 5 — Case Study answer index

Fast cross-check when a question resembles a Trainers Sheet case.

| ProTool | Q1 | Q2 | Q3 |
|---|---|---|---|
| 05 TVM | PMT 56,409 · FV 1.58 Cr · PV 40.61 L · NPER 20.80 yrs · Rate 8% | 69,79,039 | 23.79 years |
| 06 ROR | 36.19% · 10.52% · 8.30% · 400% & 8.38% · 0.57% | 28.29% | 10.47% |
| 15 Life Ins. | Total 3.76 Cr / Additional 2.91 Cr | Additional 2.51 Cr | Additional 2.55 Cr |
| 16 Emergency | 28,000 p.m. | 34,000 p.m. | 92,000 p.m. |
| 17 Children | Fixed 5,405 / 5,354 / 3,414; StepUp 3,570 / 3,079 / 1,639 | 24,503 | 21,833 |
| 18 House | SIP 73,439 | 2,12,126 | 4,54,978 |
| 19 Retirement Acc. | 7.66 / 3.20 / 4.46 Cr | 6.30 / 2.38 / 3.92 Cr | 7.53 / 2.00 / 5.53 Cr |
| 20 Retirement Dist. | 3.02 Cr | 2.77 Cr | 1.90 Cr |
| 24 Asset Alloc. | 4% · 13.70% · 13.80% · 7.50% | 6.30% | 12.90% |
| 27 SIP | Education 1.47 Cr / Retirement 7.40 Cr | 2.35 Cr | 2.49 Cr |
| 28 SWP | 23.2 years | 18.1 years | 27.1 years |
| 30 Employment | EPF 69,26,230 · NPS 83,64,192 (lumpsum 66,91,354) · PPF 16,28,039 · Gratuity 21,93,055 | EPF 2,59,37,321 | Gratuity 26,94,806 |
| 32 Loan | 147 months after step-up EMI | | |
| 33 SIP Foreclose | SIP 13,491 for 12 yrs / closes in 11 yrs | 11,355 for 15 yrs / 12 yrs | 14,050 for 10 yrs / 11 yrs |
| 34 Rent vs Buy | Rent better by 1.12 Cr; buy now beats buy-later | Rent better by 79 L | Rent better by 81 L |

---

*Extracted from the Network FP QPFP Batch 15 course files. Every formula is the live cell content of the official ProTool workbook; every figure marked "Verified" is the workbook's own cached result, independently reproduced. © Network FP Knowledge Solutions — internal use.*
