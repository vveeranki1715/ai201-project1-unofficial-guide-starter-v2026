# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Several of my questions sit next to near-duplicates: withdrawal (week ten) shares a topic with the add/drop deadline (week six) and the pass/fail option (week eight), and the Kestrel Commons wait time lives in two posts. One of those can lose to a neighbour on a bad phrasing, so I allow one miss. 5 of 5 would grade whether I phrased the five questions well, not whether retrieval works.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Every answer, not most, because the prompt puts a `[from filename]` header on each chunk and tells the model to name the file, so the filename is already in front of it. I count a refusal as naming no source on purpose, since it never reaches the model, and I only check answers. The one thing that breaks it is the model ignoring the instruction and answering without a file name, so a single miss means the grounding prompt needs tightening.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
The gap is clean. My five in-corpus questions had best distances of 0.218 to 0.412, and the five out-of-scope questions had best distances of 0.825 to 0.934, with the cutoff at 0.6. That leaves about 0.2 of margin on each side, so I expect all five to refuse. I wrote 4 of 5 because the out-of-scope set is five questions from a different world, and a question like "where can I park a bike" is campus-flavoured and would land between the groups.

---

## 4. Something about your chunks

Every chunk is between 150 and 700 characters and ends on a full stop or question mark, and in a sample of 5 chunks read by hand, 5 of 5 can answer their post's question without reading any other chunk.

**Why this target:**
The length bounds are checkable by the `app.py index` summary line for all 88 chunks: below 150 characters a chunk is only a title and a fragment, and above 700 it holds more than one post's thought. The hand sample is 5 of 5, not 4 of 5, because in this corpus one post is one chunk, so a chunk that can't stand alone means the chunker cut a post apart, which is a bug and not noise.



---

## 5. Your choice

For each of my 5 test questions, the source file named in the answer is a file whose text contains the `expects` phrase, in 5 of 5 answers.

**Why this target:**
Criterion 2 only checks that a source is named; I care that it is the right one, because a student who follows a wrong citation to the add/drop post for a withdrawal question is worse off than with no citation. It is 5 of 5 because each chunk is exactly one file, so the check is mechanical: look up the cited file and search it for the phrase. The risk is the near-duplicate posts above, where the model could cite the neighbour, so one wrong citation means the prompt or the top-k needs a fix.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
