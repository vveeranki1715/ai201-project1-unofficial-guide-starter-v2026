"""
Eight harder, retrieval-only questions. The corpus has seven near-identical
laundry posts and seven near-identical exam posts that differ only by building
or course name, so these ask for one specific building or course and check that
the right file comes back first.

    python stress.py                     rank of the right file, and what the gate does
    python stress.py --threshold 0.7     try a different relevance cutoff

It also runs five questions that sound like campus life but that no post
answers. The gate should refuse these, and they are what stops a raised cutoff
from simply letting everything through.
"""

import argparse

import config
import gate
import store

STRESS = [
    ("How much does a dryer cost in Calder Annexe?", "housing_calder_annexe_laundry.txt"),
    ("What do the laundry machines cost at Morrow House?", "housing_morrow_house_laundry.txt"),
    ("Is the Aldridge Hall laundry coin operated?", "housing_aldridge_hall_laundry.txt"),
    ("Is the CS 340 midterm open-book?", "course_cs_340_exams.txt"),
    ("How is MATH 220 curved?", "course_math_220_exams.txt"),
    ("Are there exams in HIST 118?", "course_hist_118_exams.txt"),
    ("How loud is Innisfree Hall?", "housing_innisfree_hall_noise.txt"),
    ("Are the ECON 101 exams multiple choice?", "course_econ_101_exams.txt"),
]


NEAR_MISS = [
    "Where can I rent a bike on campus?",
    "What time does the gym open?",
    "Who is the president of the university?",
    "How much is tuition per semester?",
    "Is there a campus pharmacy?",
]


# Written after I chose the cutoff, and never used to choose it. The first three
# are answered by a post; the last four are campus-flavoured but not covered.
HOLDOUT_IN = [
    ("How often does the campus shuttle run on weekends?", "transit_shuttle.txt"),
    ("When do the housing lottery numbers come out?", "admin_housing_lottery.txt"),
    ("How much printing do I get each semester?", "admin_printing_quota.txt"),
]
HOLDOUT_OUT = [
    "What is the name of the campus mascot?",
    "How do I join a fraternity or sorority?",
    "Is there a student discount at the cinema?",
    "Where is the campus chapel?",
]


def holdout(threshold):
    print("\nholdout, written after the cutoff was chosen:")
    passed = 0
    for question, want in HOLDOUT_IN:
        results = store.search(question, top_k=config.TOP_K)
        decision = gate.check(results, threshold=threshold)
        passed += decision.passed
        print(f"best {decision.best_distance:.3f}  {'passes gate' if decision.passed else 'REFUSED by gate'}  "
              f"{question}  (nearest: {results[0].source}, wanted {want})")
    refused = 0
    for question in HOLDOUT_OUT:
        results = store.search(question, top_k=config.TOP_K)
        decision = gate.check(results, threshold=threshold)
        refused += not decision.passed
        print(f"best {decision.best_distance:.3f}  {'refused' if not decision.passed else 'LET THROUGH'}  "
              f"{question}  (nearest: {results[0].source})")
    print(f"holdout: gate passes {passed} of {len(HOLDOUT_IN)} answerable, refuses {refused} of {len(HOLDOUT_OUT)} unanswerable")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    threshold = config.THRESHOLD if args.threshold is None else args.threshold
    print(f"relevance cutoff: {threshold}\n")

    top1 = top3 = answered = 0
    for question, want in STRESS:
        results = store.search(question, top_k=config.TOP_K)
        decision = gate.check(results, threshold=threshold)
        files = [r.source for r in results]
        rank = files.index(want) + 1 if want in files else None
        top1 += rank == 1
        top3 += rank is not None and rank <= 3
        answered += decision.passed
        verdict = "passes gate" if decision.passed else "REFUSED by gate"
        print(f"rank {rank}  best {decision.best_distance:.3f}  {verdict}  {question}")
        if rank != 1:
            print(f"      top 3 were: {', '.join(files[:3])}")
    print(f"right file ranked first: {top1} of {len(STRESS)}; in top 3: {top3} of {len(STRESS)}")
    print(f"gate lets through: {answered} of {len(STRESS)}  (should be all of them)\n")

    refused = 0
    for question in NEAR_MISS:
        results = store.search(question, top_k=config.TOP_K)
        decision = gate.check(results, threshold=threshold)
        refused += not decision.passed
        verdict = "refused" if not decision.passed else "LET THROUGH"
        print(f"best {decision.best_distance:.3f}  {verdict}  {question}  (nearest: {results[0].source})")
    print(f"gate refuses: {refused} of {len(NEAR_MISS)}  (should be all of them)")
    holdout(threshold)


if __name__ == "__main__":
    main()
