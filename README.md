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

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
