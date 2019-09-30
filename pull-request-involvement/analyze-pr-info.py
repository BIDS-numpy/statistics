#!/usr/bin/env python3


import pickle


with open("pr_data.pkl", "rb") as f:
    data = pickle.load(f)


# Fetch first and last day from the PR data
first_day = data[-1]["created_at"].strftime("%Y-%m-%d")


pr_format = "* [``` {title:} ```]({url:})"

prs_created = []
for pr in data:
    if pr["bids_created"]:
        prs_created.append(pr_format.format(**pr))

prs_merged = []
for pr in data:
    if pr["bids_merged"] and not pr["bids_created"]:
        prs_merged.append(pr_format.format(**pr))

prs_most_commented = []
for pr in data:
    if not pr["bids_merged"] and not pr["bids_created"]:
        if pr["bids_comments"] >= pr["other_comments"]:
            prs_most_commented.append(pr_format.format(**pr))

prs_commented = []
for pr in data:
    if not pr["bids_merged"] and not pr["bids_created"]:
        if pr["bids_comments"] >= pr["other_comments"]:
            continue
        if pr["bids_comments"] > 0:
            prs_commented.append(pr_format.format(**pr))


print("# BIDS Contribution to PRs open/merging")
print()
print(f"**Of {len(data)} PRs opened and merged since {first_day}**")
print()
print(f"- **{len(prs_created)} BIDS created.**")
print(f"- **{len(prs_merged)} BIDS merged.**")
print(f"- **{len(prs_most_commented)} BIDS made at least half of non-author comments.**")
print(f"- **{len(prs_commented)} BIDS commented on.**")
print()
involved = len(prs_created) + len(prs_merged) + len(prs_most_commented) + len(prs_commented)
print(f"Thus BIDS was involved in {involved} of the {len(data)} PRs (numbers exclude all previously listed categories).")
print()
print("*See full list below.*")
print("\n")

print(f"## {len(prs_created)} BIDS created")
print()
print("\n".join(prs_created))
print("\n" * 2)

print(f"## {len(prs_merged)} BIDS merged")
print()
print("\n".join(prs_merged))
print("\n" * 2)

print(f"## {len(prs_most_commented)} BIDS made at least half of non-author comments")
print()
print("\n".join(prs_most_commented))
print("\n" * 2)

print(f"## {len(prs_commented)} BIDS commented on")
print()
print("\n".join(prs_commented))
print("\n" * 2)
