# The Unofficial Guide

Vaishnavi Veeranki — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers questions about student life at a university, using only a corpus of 88 short posts written by students (`campus_life`): dining halls, residence halls, courses, and the administrative rules nobody explains properly. You ask a plain-language question such as "Until which week can I withdraw from a course?" and the system retrieves the closest posts, answers from them only, and names the file it used. If your question is about something the posts don't cover, it refuses with "I don't have enough information about that" instead of guessing.

## Chunking Strategy

**Chunk size:** one post per chunk, with a ceiling of 700 characters and a floor of 150. Posts in `campus_life` run 178 to 549 characters, so none is ever cut.
**Overlap:** 0

I read a dozen posts first. Each is a title line plus one to three short paragraphs, and the fact someone would ask about sits in one sentence (for example "Withdrawal runs to week ten"). The starter's 800-character window never cut anything: 88 documents came out as 88 chunks. That is the right outcome for these documents, because cutting inside a post would separate a fact from its title and the context around it, which is what makes a chunk answerable on its own.

So my chunker keeps one post as one chunk and only splits when a post passes 700 characters. It splits at a blank line, never mid-sentence, and repeats the title at the top of each piece. Overlap is 0 because cuts fall on paragraph boundaries and there is no half-sentence to repeat. A trailing piece under 150 characters is merged back into the previous one. On this corpus it produces the same 88 chunks as the starter (shortest 178, longest 549 characters), so I did not change my mind about the result. The rule matters if I add a longer document.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_housing_lottery.txt` — produced by: `chunker.py::split_documents`

```
On the housing lottery

The housing lottery is not random in the way most people assume. Rising sophomores get a number drawn at random, but juniors and seniors are ordered by accumulated credit hours first, and only tie-break randomly. That means a senior who took summer courses reliably beats a senior who didn't. Numbers come out the second week of March and selection runs over four evenings.
```

**Chunk 2** — source: `dining_kestrel_commons.txt` — produced by: `chunker.py::split_documents`

```
Kestrel Commons

I'm a junior and I've done this twice now. Wait times: 20 to 25 minutes between 12:15 and 1:00, under 5 minutes before 11:45. The thing worth going for is the stir-fry station, made to order. The thing to know is that the salad bar wilts after 1:30.

Hours are 7:00am to 9:00pm weekdays, 9:00am to 8:00pm weekends. Costs one meal swipe, or $12.50 cash.
```

**Chunk 3** — source: `course_cs_210_exams.txt` — produced by: `chunker.py::split_documents`

```
CS 210 Data Structures — assessment

Two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Do the labs even though they're only 10% — the exams reuse the lab problems.
```

**Chunk 4** — source: `housing_tamsin_court_laundry.txt` — produced by: `chunker.py::split_documents`

```
Laundry in Tamsin Court

Machines take in-unit washer-dryer. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.

Best time to do laundry here is Tuesday or Wednesday morning. Sunday after 6pm you will wait.
```

**Chunk 5** — source: `transit_shuttle.txt` — produced by: `chunker.py::split_documents`

```
The campus shuttle

Runs a loop every 20 minutes from 7am to 11pm on weekdays and every 40 minutes on weekends. The published timetable is optimistic by about five minutes in the morning and accurate the rest of the day.

It's free with a student ID. The stop outside Fenwick Court is the one that gets skipped when the driver is behind, which is worth knowing if you live there.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How are juniors and seniors ordered in the housing lottery?

**Answer:**

```
$ python app.py ask "How are juniors and seniors ordered in the housing lottery?"

  (best distance 0.225, cutoff 0.6)

Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used only when necessary.

Source: admin_housing_lottery.txt

Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, housing_old_brewhouse.txt, housing_tamsin_court.txt
```

**My relevance cutoff:** 0.6, the starter's default, kept on purpose.

I ran my five test questions and the five `OUT_OF_SCOPE` questions through retrieval (top-k 5) and recorded the best distance for each. The in-corpus questions all landed between 0.218 and 0.412. The out-of-scope questions all landed between 0.825 and 0.934. The gap runs from 0.41 to 0.82, so 0.6 sits inside it with about 0.2 to spare on each side. I did not need to move it. In all five test questions the chunk containing the `expects` phrase appeared in the top 5, and it ranked first every time. The withdrawal question had the loosest best distance (0.412) because the add/drop and pass/fail posts talk about the same topic. I left top-k at 5. The grounding instruction in `generate.py` (use only the documents, say so when they don't cover it, name the file) already produced a cited answer, so I left it alone.

| Question | In corpus? | Best distance |
|---|---|---|
| How are juniors and seniors ordered in the housing lottery? | yes | 0.225 |
| What happens to dining dollars that are left over in May? | yes | 0.218 |
| How long is the wait at Kestrel Commons around 12:30? | yes | 0.222 |
| What is the latest week I can make a course pass/fail? | yes | 0.266 |
| Until which week can I withdraw from a course? | yes | 0.412 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. The chunker.** I asked Claude to replace the body of `split_documents` after I'd read the corpus and decided one post should stay one chunk. It wrote a paragraph-aware splitter with a 700-character ceiling, a 150-character floor, and the title repeated at the top of any continuation. When I ran it, it produced exactly the same 88 chunks as the starter (shortest 178, longest 549), so on `campus_life` it never splits anything. I kept it anyway: the finding is that the starter was already right for these posts, and the splitter now handles a longer post without cutting mid-sentence. I rewrote the Chunking Strategy section to say this plainly instead of claiming the new code improved the chunks.

**2. The cutoff.** I asked Claude to write five specific test questions from the posts, with an `expects` phrase for each, and then to run them and the five out-of-scope questions through retrieval and print the distances. Retrieval put the right chunk in the top 5 for all five questions, and the two groups of distances were far apart (0.218 to 0.412 against 0.825 to 0.934). I had expected to have to tune the 0.6 default, but there was nothing to tune, so I kept it and recorded the ten numbers as the evidence. The withdrawal question, at 0.412, was the weakest, because the add/drop and pass/fail posts discuss the same topic. That is why criterion 1 allows one miss.

**3. Unit 2: finding something to fix.** After `run_eval.py` came back MET on all five criteria, I asked Claude to write `scorer.py` (the judge function `run_eval.py` looks for) and then, because nothing had failed, to build a harder retrieval-only probe from the near-identical posts in the corpus. It came back with `stress.py` and one number I hadn't expected: "How is MATH 220 curved?" had the right post ranked first but a distance of 0.620, so the gate refused it. I had assumed the fix would be hybrid search, and Claude measured it before building it (`probe_lexical.py`), which showed a keyword score didn't separate answerable from unanswerable questions either. I dropped hybrid search and changed only the cutoff, 0.6 to 0.5. I then had Claude write seven fresh holdout questions after the number was chosen, because I'd picked 0.5 from the same questions I was scoring against. I kept MATH 220 listed as still broken instead of tuning the cutoff until it passed.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Produced by `run_eval.py::main` with `--label before`: three runs of each test question with caching off, 15 model calls. The scorer is `scorer.py::judge`, which I wrote this unit (an answer passes if it contains the `expects` phrase and is not a refusal). It also records, per question and run, whether a retrieved chunk contains the phrase, which files the answer names, and whether those files contain the phrase. Raw data: `results/run_2026-10-04_2320_before.md` and `results/criteria_data_before.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks: all 88 within 150–700 chars and ending on a full stop; 5 sampled chunks stand alone | 88/88 and 5 of 5 | 88/88, 5/5 | 88/88, 5/5 | 88/88, 5/5 | MET |
| 5. Cited file contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 3 is one deterministic pass (retrieval and the gate don't vary), so the same number is in all three columns. Criterion 4 is also deterministic: the chunker doesn't call the model, so it gives the same chunks every run. Its 5 of 5 is the five chunks I read by hand in unit 1 (see Sample Chunks).

**Real output, one per criterion**

Criterion 1 (`scorer.py::judge`, from `results/criteria_data_before.jsonl`, retrieval by `store.py::search`): the chunk containing "week ten" came back first for the withdrawal question.

```
{"question": "Until which week can I withdraw from a course?", "expects": "week ten", "chunk_has_answer": true, "rank_of_answer": 1, "named_a_source": true, "sources_named": ["admin_withdrawal_deadline.txt"], "cited_files_contain_answer": true, "answer_correct": true, "refused": false}
```

Criterion 2 (`generate.py::answer_from_chunks`, run 3 of the Kestrel Commons question):

```
Based on the documents provided, the wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00.

Source: `dining_kestrel_commons.txt` (and also supported by `dining_kestrel_commons_followup.txt`).
```

Criterion 3 (`run_eval.py::check_out_of_scope`, cutoff 0.6 at that point):

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |
```

Criterion 4 (`chunker.py::describe`, via `python app.py index`):

```
88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::split_documents
```

Criterion 5 (the same `criteria_data_before.jsonl` line type, for the Kestrel Commons question, which cites two files):

```
"sources_named": ["dining_kestrel_commons.txt", "dining_kestrel_commons_followup.txt"], "cited_files_contain_answer": true
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer, 4 of 5 | MET | 5/5 in all three runs. In fact the chunk was ranked first for every question. Retrieval doesn't use the model, so the three runs could only differ by chance, and they didn't. |
| 2 | Every answer names a source, 5 of 5 | MET | All 15 answers (5 questions, 3 runs) named at least one retrieved file. Formats varied ("Source: ...", "(file.txt)", "Based on file.txt"), so I matched on the filename, not the format. |
| 3 | Gate stops out-of-corpus questions, 4 of 5 | MET | 5 of 5 refused. The closest was 0.825 against a 0.6 cutoff. This is the criterion I think was too easy; see Diagnoses. |
| 4 | Chunk size, all 88 in bounds and 5 of 5 sampled stand alone | MET | A script check found zero chunks outside 150–700 characters or not ending in punctuation. The 5 I read each answered their own post's question. Close call: none, because this corpus never needs a split. |
| 5 | Cited file contains the answer, 5 of 5 | MET | Every file named in every answer contains the `expects` phrase. The one I watched was withdrawal, which has near-neighbours (add/drop, pass/fail), and the model cited the right post all three times. |

No criterion was revised.

## Diagnoses

I missed nothing, so there is no failure to trace to a stage. The honest reading is that my targets were safe, not that the system is excellent. My five questions each have one obviously relevant post, and my five out-of-scope questions come from a different world (capital of Mongolia, diesel engines), so nearly any cutoff from 0.42 to 0.82 would have passed.

To find out whether that is true, I wrote a harder check, `stress.py`, which uses no model calls. It has eight questions about a specific building or course, where the corpus has seven near-identical laundry posts and seven near-identical exam posts, and five questions that sound like campus life but no post answers. Results at the original cutoff of 0.6:

- **Right file ranked first: 7 of 8**, in the top 3: 8 of 8. The one miss was "Are there exams in HIST 118?", where `course_hist_118.txt` outranked `course_hist_118_exams.txt`. The answer file was still in the top 5, so the model still saw it.
- **A false refusal.** "How is MATH 220 curved?" ranked `course_math_220_exams.txt` first but with a best distance of 0.620, over the 0.6 cutoff, so the gate refused a question the corpus answers. Stage: **embedding/retrieval**. A short question dominated by a course code and a number ("MATH 220") sits far from a post in embedding space even when the right post is nearest. Retrieval got the ranking right and the gate then threw it away.
- **Near-miss questions got through.** The gate let 3 of 5 campus-flavoured, unanswerable questions pass: bike rental (0.565), gym hours (0.517), tuition (0.527). Stage: **retrieval/gate**. These share words like "campus" and "semester" with real posts, so they land well inside the range of real questions.

Together these are one problem, not two: on terse or campus-flavoured questions the two groups of distances overlap (answerable up to 0.620, unanswerable down to 0.517), so a single distance cutoff can't separate them. My unit 1 gap of 0.412 to 0.825 was real but only because my out-of-scope questions were extreme.

**Which criterion I'd tighten:** criterion 3, to use unanswerable questions that sound like the corpus, and to require refusal of at least 4 of 5 of those. On the stress set at 0.6 that criterion would have been MISSED (2 of 5).

## The Improvement

**What I changed:** the relevance cutoff in `config.py`, `THRESHOLD`, from 0.6 to 0.5. Nothing else.

**Why I picked it:** my diagnosis found that the gate let through 3 of 5 near-miss questions at 0.6, and a lower cutoff is the direct fix for that.

**What I tried first and rejected.** I expected to add hybrid search (BM25 keyword matching beside the embeddings), because the MATH 220 failure is a name-and-number question that embeddings handle badly. Before building it I measured whether a keyword signal separates the two groups (`probe_lexical.py`). It doesn't: "How much is tuition per semester?" gets a BM25 score of 7.53 because "per semester" matches the printing-quota post, which is higher than for several questions the corpus does answer ("Until which week can I withdraw from a course?" scores 3.11). The share of query words found in the top chunk is 0.67 for gym hours and 0.50 for the pharmacy question, against 0.50 to 1.00 for answerable ones. So a keyword rule would have rescued MATH 220 and let tuition through too. I did not build it.

**How I chose 0.5.** From the stress-set distances: every answerable question except MATH 220 scores 0.446 or better, and all five near-misses score 0.517 or more. 0.5 lies between them. I then wrote seven fresh questions (3 answerable, 4 unanswerable) after choosing it and ran them without changing anything, as a check that I hadn't just fitted the numbers.

### Run Log — After

`run_eval.py --label after`, same five criteria, three runs each, cutoff 0.5. Raw data: `results/run_2026-10-04_2323_after.md`, `results/criteria_data_after.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks: all 88 within 150–700 chars and ending on a full stop; 5 sampled chunks stand alone | 88/88 and 5 of 5 | 88/88, 5/5 | 88/88, 5/5 | 88/88, 5/5 | MET |
| 5. Cited file contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**On the stress set (`stress.py`, no model calls):**

| Measure | Cutoff 0.6 | Cutoff 0.5 |
|---|---|---|
| Near-miss questions the gate refuses (should be 5) | 2 of 5 | 5 of 5 |
| Answerable specific questions the gate passes (should be 8) | 7 of 8 | 7 of 8 (MATH 220 still refused) |
| Holdout, unanswerable refused (should be 4) | 3 of 4 | 4 of 4 |
| Holdout, answerable passed (should be 3) | 3 of 3 | 3 of 3 |

**Did it help?**

Yes, where I could measure it, but my five criteria cannot show it. All five come out identically before and after, because every answerable question scores 0.412 or better and every out-of-scope question 0.825 or worse, so a move from 0.6 to 0.5 changes nothing for them. The improvement shows only on the harder set: near-miss refusals went from 2 of 5 to 5 of 5, and on the 7 holdout questions I wrote after choosing the number, the gate got 7 of 7 right at 0.5 against 6 of 7 at 0.6 (the cinema-discount question at 0.554 got through at 0.6).

Caveats, plainly: I picked 0.5 using the same 5 near-miss questions I then reported on, so the 5 of 5 is partly fitted. The holdout is only 7 questions. The margins are thin: the lowest unanswerable distance is 0.517, and the highest answerable distance that still passes is 0.446. And the change did not fix MATH 220, which is refused at both cutoffs. It trades nothing for what it gains on my data, but a harder or larger near-miss set would probably find a question in the 0.45 to 0.5 band that it now refuses wrongly.

## What's Still Broken

No criterion is missed, so there is nothing to list against my five targets. Against the harder checks:

- **MATH 220 is still wrongly refused (0.620).** Stage: embedding. Short queries made of a course code and a number sit far from the post in embedding space. The cutoff can't fix it without letting the near-misses back in (gym hours at 0.517 would pass). I looked at a rule that lets a question through when the semantic and keyword retrievers agree on the same top chunk. It would have rescued MATH 220, but tuition also has both retrievers pointing at the printing-quota post, so it would have let that through. Fixing this properly probably needs a better embedding model, which I didn't try, or a reranker. I stopped because the diagnosis showed no simple rule separates them, and one cutoff change was the scope of this unit.
- **HIST 118 ranks the wrong post first.** `course_hist_118.txt` beats `course_hist_118_exams.txt` for "Are there exams in HIST 118?". The right post is in the top 5, so the answer still comes out. I did not fix it.
- **The gate is a single number on a thin margin.** At 0.5 the safe zone is 0.446 to 0.517, so a new corpus post or a new question style could fall into it.

## What I'd Do Differently

I'd write criterion 3 with unanswerable questions that sound like the corpus instead of the five from a different world. I wrote it against the starter's `OUT_OF_SCOPE` list, which any cutoff would clear, so it measured almost nothing. Written that way at the start, it would have been missed (2 of 5) and pointed straight at the gate. I'd also tighten criterion 1 to "the answer chunk is ranked first", since it was 5 of 5 and "somewhere in the top 5" left me no room to be wrong. And I'd add a criterion for false refusals ("every answerable question passes the gate"), which is the one the MATH 220 failure belongs to and none of my five covers.

