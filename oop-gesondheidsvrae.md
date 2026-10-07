# Two open health questions — South African official sources

Checked 28 September 2026. Subject: Grade 7 Life Orientation, health and social
responsibility. The two claims under test are (1) that at a public clinic the visit, the
TB test and the medicine for TB and HIV all cost nothing, and (2) that a cough of two
weeks is the point at which a person should be tested for TB.

---

## What was reachable and what was not

Report this honestly, because one earlier attempt at these questions found every South
African source unreachable and left both claims unverified.

| Source | Result |
|---|---|
| `www.health.gov.za` (National Department of Health main site) | **Unreachable.** Expired TLS certificate (`SEC_E_CERT_EXPIRED`). Every file under it failed, including the department's own TB screening poster, the Uniform Patient Fee Schedule page, TB Recovery Plan 4.0 (2025/26), the End TB Campaign 2025/26 plan and the RR-TB guidelines. |
| `knowledgehub.health.gov.za` (NDoH Knowledge Hub) | Reachable. Guidelines downloaded. |
| `www.nicd.ac.za` (National Institute for Communicable Diseases) | Reachable. Also mirrors NDoH documents that the main site could not serve. |
| `www.gov.za` (South African Government) | Reachable for pages and for the Act PDFs. One older document path (`/sites/default/files/gcis_document/201706/…`) failed with a TLS error. |
| `www.westerncape.gov.za` (Western Cape Department of Health and Wellness) | Reachable. |
| `sanac.org.za` (South African National AIDS Council) | Reachable. |
| `www.idealclinic.org.za` (hosts the 2014 National TB Management Guidelines) | HTTP 522. Not retrieved. |
| `www.saflii.org` (legislation) | HTTP 403. The Act was obtained from gov.za instead. |

So the national department's own website is down, but its guidelines were obtained
elsewhere — two of the three key documents below came through the Knowledge Hub and the
NICD rather than through `health.gov.za`.

---

## Question 1 — what is free at a public clinic

Short answer: all three are free, but they are free under **two different mechanisms**,
not one. The consultation is free under the National Health Act. The TB test, the TB
medicine and antiretroviral treatment are free under a **separate, diagnosis-based fee
exemption** that applies regardless of what the patient would otherwise have to pay. The
1996 free primary health care decision covers the consultation only.

### 1a. The consultation at a public primary health care clinic — established, free

**Authority: National Health Act 61 of 2003, section 4(3)(b)**, published in *Government
Gazette* No. 26595, 23 July 2004 (retrieved from gov.za):

> "Subject to any condition prescribed by the Minister, the State and clinics and
> community health centres funded by the State must provide … all persons, except
> members of medical aid schemes and their dependants and persons receiving compensation
> for compensable occupational diseases, with free primary health care services".

The same section, 4(3)(a), separately gives free health services to "pregnant and
lactating women and children below the age of six years, who are not members or
beneficiaries of medical aid schemes".

Conditions attached:

* It is **primary** care, at state clinics and community health centres — not hospital
  care.
* Two groups are excluded by name: medical aid scheme members and their dependants, and
  people receiving compensation for a compensable occupational disease.
* The whole subsection opens "Subject to any condition prescribed by the Minister".
* There is **no means test and no nationality or documentation condition in the statute**.
  The words are "all persons".

The 1996 date: free primary health care for all users of public primary level services
was announced with effect from 1 April 1996, extending free care given in 1994 to
under-sixes and to pregnant and breastfeeding women. I could confirm that date and
sequence only from academic literature (the *South African Health Review* and a
*Development Southern Africa* review of the user-fee abolition), **not** from a
government source — `health.gov.za` was unreachable. The binding authority today is the
2003 Act, so nothing rests on the 1996 date.

**Where practice narrows the statute.** Fee administration is done through the Uniform
Patient Fee Schedule and the NDoH's classification policy, and there the consultation is
a chargeable item for some patients. The Limpopo Department of Health's *Departmental
Revenue Circular 13 of 2025 on UPFS 2025-2026* (`ldoh.gov.za`) reproduces the NDoH *UPFS
User Guide* and the NDoH *Policy Guidelines for Administration and Classification of
Users accessing healthcare and services at public healthcare facilities*, the latter
citing a "Circular to all Provincial Health Departments, 15/05/2023". It says:

> "MANDATORY DOCUMENTS REQUESTED FROM ALL USERS WHEN VISITING STATE HEALTHCARE FACILITY
> • Identity Document • Birth Certificate • National Passport • Visa/Permit (Immigration
> Act 13, 2002; Refugee Act 130,1998) …"

and

> "In case the patient refuses to complete the forms as indicated in 2 above, such
> patient must be classified as full paying patient (PP/H3) and requested to pay the full
> applicable fees."

and, of the Hospital Gratis free-service conditions:

> "These conditions apply to South African citizens, permanent residents with a valid
> permit and refugees with a valid permit."

The *Uniform Patient Fee Schedule Regulations for Health Care Services Rendered by the
Department of Health and Wellness, 2026* (Western Cape Provincial Gazette Extraordinary
9216, 31 March 2026, in force 1 April 2026) likewise has a chargeable primary health care
consultation tariff —

> "1.2.26.1 The tariff for a consultation at a primary health care centre applies when
> the health care professional personally takes down a patient's clinical history,
> performs an appropriate clinical examination or prescribes or administers treatment or
> assists the patient with advice."

— and classifies as full-paying "foreign nationals not assessed according to the
prescribed means test".

So: the consultation is free as a matter of law for everyone except scheme members and
occupational-disease compensation cases, and the fee regulations assume most clinic
patients pay nothing; but the fee machinery does contain a clinic consultation tariff,
and classification depends on paperwork.

### 1b. The TB test — established, free

Three South African official sources say so in terms.

**NICD, "TB Frequently Asked Questions"** (`nicd.ac.za/tb-frequently-asked-questions/`;
page undated, cites 2019 burden figures):

> "TB testing is free at all public health facilities in South Africa. Private laboratory
> groups are also able to test for TB."

**Western Cape Department of Health and Wellness, "Tuberculosis", dated 13 February
2026:**

> "Good news! Free TB testing and treatment. TB testing and treatment are FREE at public
> clinics and hospitals. You don't need an appointment, just walk in."

**South African Government, "What is TB and where can I get treatment?"**
(`gov.za/faq/health/…`; no publication date shown on the page):

> "Free TB testing and treatment are available at public clinics and hospitals."

**What the current first-line test actually is.** The lesson's "sputum test" needs care.
The *TB Screening and Testing Standard Operating Procedure*, Department of Health, South
Africa 2022, version dated June 2022 (obtained from `nicd.ac.za`, since `health.gov.za`
is down), says:

> "All people must be tested using the Xpert MTB RIF Ultra as a first line test."

and, of smear microscopy:

> "Smear microscopy is used as a baseline test following a positive RS-TB test result and
> as a monitoring test at 7 and 23 weeks."

So sputum is still what the person produces, but the first-line **test** run on it is a
molecular test (Xpert MTB/RIF Ultra), not smear microscopy. Smear microscopy is now a
baseline and monitoring test. The lesson must not present the sputum smear as the
diagnostic test.

**The fee basis, and one caveat I could not close.** The exemption that makes TB free is
diagnosis-based rather than income-based. From the NDoH free-services table as
reproduced in the Limpopo circular:

> "There exist certain circumstances/ diagnosis under which patients will receive
> services free of charge independently of their classification as full paying or
> subsidized patients. These circumstances have a statutory basis and apply only to the
> episode of care directly related to the circumstances under which the patient has
> qualified for free services."

and under "Infectious, formidable and/or notifiable Diseases":

> "2. All tuberculosis including Pulmonary tuberculosis."

The caveat: that exemption is written for a person who **has** the disease, and a person
being tested has not yet been diagnosed. Against that, the Western Cape UPFS 2026
contains a rule that cuts the other way for full-paying patients:

> "4.9 Full-paying patients will be charged by the National Health Laboratory Service
> (NHLS) for laboratory services rendered by the NHLS irrespective of where the services
> are rendered (including primary health care centres)."

I found no source applying that to TB tests, and three official sources say TB testing is
free without qualification. So the finding stands, but the mechanism for the pre-diagnosis
test is the public messaging rather than a fee-schedule line I could quote.

### 1c. The medicine

**TB treatment — established, free.**

South African Government, "What is TB and where can I get treatment?":

> "Drug-susceptible TB: A 6-month treatment course provided at no cost"

and "Drug-resistant (MDR/XDR) TB: Treated using shorter (6-9 month) all-oral regimens,
per updated WHO guidelines." Western Cape (13 February 2026): "TB testing and treatment
are FREE at public clinics and hospitals." And the NDoH free-services list names "All
tuberculosis including Pulmonary tuberculosis" as free independently of the patient's
financial classification.

**Antiretroviral treatment — established free, with two conditions.**

The NDoH free-services list, in the "Other exempt conditions" row (Limpopo circular
reproducing the NDoH policy guidelines):

> "Patients on antiretroviral therapy at identified sites are exempted from paying fees
> excluding those who are members of medical schemes/privately funded."

and, in the infectious-diseases row:

> "HIV/Aids related diseases when accessible at designated ARV sites"

The two conditions are therefore: **the site must be a designated ART site**, and
**medical scheme members and privately funded patients are excluded**.

Western Cape Department of Health and Wellness, "HIV", dated 28 October 2025:

> "We offer a comprehensive, free HIV care system designed to support you at every stage,
> from testing to treatment."

> "Free HIV testing: Available at all our clinics."

with "Antiretroviral therapy (ART)" listed among those services.

Checked and found silent on fees: the *2023 ART Clinical Guidelines for the Management of
HIV in Adults, Pregnancy and Breastfeeding, Adolescents, Children, Infants and Neonates*,
NDoH, June 2023, Version 4 (Knowledge Hub) — it contains nothing about cost. So the
fee authority for ART is the Uniform Patient Fee Schedule exemption above, not the
clinical guideline.

**Not obtained.** The frequently cited 2007 NDoH Revenue Directive
"Refugees/Asylum Seekers With or Without a Permit" could not be retrieved from any
official host. It exists only in NGO summaries in what I could reach (Scalabrini,
SECTION27, GroundUp). **Its exact wording is unconfirmed** and nothing below rests on it.

### 1d. A person without documentation

The law and the government's own statements say documentation does not govern access;
the fee-administration policy partly says otherwise. Both are true at once, and the
distinction matters.

In favour of access regardless of documentation:

* The National Health Act, s4(3)(b), says "all persons". No nationality or documentation
  condition.
* South African Government media statement, **5 July 2025**, "Government on blocking of
  access to healthcare services":

  > "Section 27(1) of the Constitution of the Republic of South Africa, 1996, clearly
  > provides that: 'Everyone has the right to have access to healthcare services'. This
  > right is not subject to an individual's nationality or immigration status."

* Minister of Health's reply to parliamentary question **NW3669, 25 June 2025** (read via
  the Parliamentary Monitoring Group, which mirrors official replies): patients are asked
  for proof of identification, but "services are not withheld from those who are unable
  to do so"; and the department "does not classify or record individuals as 'illegal
  immigrants'". Foreign elective patients are required to pay upfront.
* Decisively for our three services: the TB and ART exemptions sit in the list that
  applies "independently of their classification as full paying or subsidized patients".
  Whatever a person's paperwork does to their classification, it does not reach a
  diagnosis-based exemption.

Cutting the other way:

* The NDoH classification policy ties the free-service categories to "South African
  citizens, permanent residents with a valid permit and refugees with a valid permit",
  lists identity document, passport and visa/permit as mandatory documents, and says a
  patient who does not complete the forms is classified as full-paying.

**Marked unconfirmed:** search results repeatedly quoted a ministerial reply saying that
emergency care, maternal and child health, and "notifiable and communicable diseases, such
as TB and HIV" are provided irrespective of nationality. I could not locate, open or quote
that document, so I am not asserting it. The position above rests on what I did read.

---

## Question 2 — how long a cough before a person should be tested for TB

**South Africa's own national TB guidance does not use a two-week cough threshold. It
uses a cough of any duration.** The two weeks in South African guidance attaches to
**fever**, not to cough. This is the most important finding in the document, and it goes
the opposite way from what the brief expected.

### Source 1 — the national screening standard operating procedure

*TB Screening and Testing Standard Operating Procedure*, **Department of Health, South
Africa 2022**, document version June 2022, contact Dr L Mvusi, National TB Control and
Management Cluster. Obtained from `nicd.ac.za` because `health.gov.za` is unreachable.

Table 2, headed "Symptoms of TB and Covid-19":

> "TB symptoms in Adolescents and Adults — Cough of any duration — Fever more than 2
> weeks — Loss of weight (>1.5kg in a month) — Drenching night sweats"

> "TB Symptoms in Children — Cough of any duration — Fever — Documented weight loss/
> failure to thrive — Fatigue"

And on what follows from a symptom:

> "All people presenting with any TB symptom must be tested for TB"

The screen is universal, not risk-restricted:

> "TB symptom screening must be conducted for all patients seen in health facilities and
> in targeted community settings."

### Source 2 — the current paediatric and adolescent guideline

*A Clinical Guideline for the Diagnosis and Treatment of Drug-susceptible TB in Children
and Adolescents in South Africa* / *Management of Tuberculosis in Children and
Adolescents*, **National Department of Health, September 2024**, signed by Dr SSS
Buthelezi, Director-General: Health, 6 September 2024. Knowledge Hub.

This is the guideline that covers a thirteen-year-old. It carries the national screening
form:

> "TB SYMPTOMS — 1. ADULTS … Current cough of any duration / Persistent fever for 2
> weeks or more / Unexplained weight loss of >1.5kg in a month, or failure to gain weight
> in pregnant women / Drenching night sweats.
> 2. CHILDREN … Current cough of any duration / Persistent fever for 2 weeks or more /
> Fatigue/less playful / Weight loss or failure to thrive.
> If 'yes' to one or more of these questions, consider TB."

In the body:

> "Symptoms typical of pulmonary TB • Cough of any duration, but especially if it is
> persistent and fails to improve."

Two weeks does appear in this guideline, but as a raised-suspicion marker rather than a
threshold for testing:

> "Most children and adolescents with TB develop unremitting symptoms that persist for
> more than two weeks. There should be a high index of suspicion, especially if symptoms
> persist (> two weeks) without improvement following other appropriate therapies."

### Source 3 — the TB infection (preventive treatment) guideline

*National Guidelines on the Treatment of Tuberculosis Infection*, **National Department
of Health, 2023**. Obtained from `nicd.ac.za`.

> "Symptom screen: current cough of any duration, fever, unexplained weight loss, night
> sweats, haemoptysis, history of previous TB treatment, adherence to ART"

### But South African public messaging does use two weeks

This is where the lesson's number comes from, and it is not invented.

**South African Government, "What is TB and where can I get treatment?"** (gov.za FAQ,
no date on the page; it links to the National TB Recovery Plan 4.0 for 2025-26, so it is
current):

> "Visit your nearest public clinic if you experience any of the following symptoms:
> Persistent cough (≥2 weeks) …"

**Western Cape Department of Health and Wellness, "Tuberculosis", 13 February 2026:**

> "If you've had any of these for more than 2 weeks, go to your clinic: Cough that won't
> go away / Coughing up blood / Sweating at night / Fever or chills / Feeling tired all
> the time / Losing weight without trying / Not feeling like eating"

**NICD, "TB Frequently Asked Questions"** gives no number at all — "persistent coughing",
and "A doctor should be consulted if you have a fever, unexplained (and unwanted) weight
loss, a persistent cough and night sweats."

### Does it apply to everyone or only to higher risk?

Cough of any duration applies to **everyone**, adults and children alike — it is in both
columns of the 2022 SOP table and in both sections of the 2024 screening form, and the
screen is for all patients seen in health facilities. Higher-risk groups go further
still: the 2022 SOP's facility algorithm has people previously treated for TB, people
living with HIV and household contacts of a TB patient give a sputum sample "irrespective
of symptoms".

### One thing to stop anyone chasing

Search engines attribute "three weeks" to a Western Cape health page. That page
(`d7.westerncape.gov.za/general-publication/tb-what-you-need-know`) now returns 404 and
is only in the search index. The live Western Cape page says two weeks. Three weeks is
the United States CDC's threshold, not South Africa's. The 2014 National TB Management
Guidelines, which would settle the older national position, could not be retrieved —
`idealclinic.org.za` returned HTTP 522.

---

## For whoever decides what a thirteen-year-old reads

**On what a clinic visit costs.** The lesson may safely say that at a government clinic a
child or a family pays nothing for the visit, nothing for the TB test, and nothing for
the medicine for TB or for HIV. All three are established, and the first two are said
plainly by the national institute for communicable diseases and by the provincial health
department in their own public information. The lesson may also safely say that this does
not depend on having papers — the right to health care in this country is not tied to
nationality or immigration status, the government said so publicly last year, and the
rules that make TB and HIV care free are written around the illness rather than around
the patient's circumstances, so they cannot be undone by missing documents. What the
lesson may **not** say is that everything at a government clinic or hospital is free for
everyone: hospital care is not primary care, people on medical aid are treated
differently, and in practice a clinic does ask for identity documents when it works out
what someone owes. It may also not promise that no one is ever turned away or charged —
the law and the practice are not always the same thing, and a child told otherwise who
then watches an adult be refused learns that we were lying. Keep the sentence about
what it still costs to get there and to miss school or work; that is the honest half and
it is already in the lesson.

**On how long a cough.** Two weeks is safe to keep in the sense that it is not false —
two South African government sources, national and provincial, tell the public to go to
the clinic after a cough of two weeks, so a learner who remembers that number is
remembering something her own government told her. But it is the wrong emphasis, and
this is worth a decision rather than leaving it. The country's clinical rule for its own
nurses and doctors is that a cough of **any** length is a reason to test for TB, for
children as much as for adults, and that if you cough at all when you come to the clinic
they should take a sputum sample. The two weeks in South Africa's clinical guidance is
about fever, not about coughing. So the lesson currently teaches a child to wait a
fortnight when the health service's own instruction is not to wait at all. The lesson
already carries the sentence saying you need not wait two weeks and may go earlier if you
are worried, and that sentence is what keeps the number from doing harm — it must not be
cut. The stronger option is to turn the block around: a cough that keeps going is a
reason to go to the clinic, and a cough that has gone on for two weeks or more is a
reason not to leave it any longer. That way the number still anchors the memory but it no
longer reads as permission to wait. The one thing the lesson must not do is present two
weeks as the point at which TB becomes possible, because it is not, and a child who waits
on that is infectious for the whole fortnight.

**One correction not in either question.** If the lesson describes the test itself, it
should not present the sputum smear as the test that finds TB. South Africa's national
procedure is that everyone is tested first with a molecular test on the sputum sample;
looking at the sputum under a microscope is now a baseline and follow-up test, not the
diagnosis. The sputum sample is still right; the microscope is not.
