#!/usr/bin/env python3

import datetime

import github
import pickle


# Using a token/login is required to download these statistics:
g = github.Github()
numpy = g.get_repo('numpy/numpy')


# Closed will ignore PRs that are not yet merged...
merged_pulls = numpy.get_pulls(state="closed")


def is_bids_associated(author, time):
    if author == "mattip" and time > datetime.datetime(2018, 3, 11):
        return True
    if author == "tylerjereddy" and time > datetime.datetime(2018, 6, 8):
        return True
    if author == "seberg" and time > datetime.datetime(2019, 4, 24):
        return True
    if author == "WarrenWeckesser" and time > datetime.datetime(2019, 8, 1):
        return True
    if author == "stefanv":
        # Within the past year, no need to filter.
        return True

    return False


pr_list = []
for pr in merged_pulls:
    # The PRs are sorted (as far as I know), so once we find an old one, stop
    if pr.created_at < datetime.datetime(2018, 10, 1):
        break

    if not pr.base.label == "numpy:master":
        # skip non-master (usually not interesting w.r.t. review)
        continue

    if not pr.merged:
        continue

    bids_merged = is_bids_associated(pr.merged_by.login, pr.merged_at)
    pr_author = pr.user.login
    bids_created = is_bids_associated(pr_author, pr.merged_at)

    bids_comments = 0
    other_comments = 0

    # Pool review and non-review comments, but ignore those by the PR author
    for comm in pr.get_review_comments():
        user = comm.user.login
        if user == pr_author:
            continue
        if is_bids_associated(user, comm.created_at):
            bids_comments += 1
        else:
            other_comments += 1

    for comm in pr.get_issue_comments():
        user = comm.user.login
        if user == pr_author:
            continue
        if is_bids_associated(user, comm.created_at):
            bids_comments += 1
        else:
            other_comments += 1

    info = {
        "title": pr.title,
        # There is probably a better way to get the URL...
        "url": pr.url.replace("//api.", "//").replace("/pulls/", "/pull/").replace("/repos/", "/"),
        "bids_merged": bids_merged,
        "created_at": pr.created_at,
        "merged_at": pr.merged_at,
        "bids_comments": bids_comments,
        "other_comments": other_comments,
        "bids_created": bids_created,
        "author": pr_author,
        }
    print(info)
    pr_list.append(info)


num_bids = len([pr for pr in pr_list if pr_list[2]])

with open("pr_data.pkl", "wb") as pickle_file:
    pickle.dump(pr_list, pickle_file)
