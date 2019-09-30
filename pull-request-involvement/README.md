This is a set of two scripts fetching and creating data for
BIDS involved in pull requests on the numpy repository (master
branch).
The `fetch-pr-data.py` script will download and store a
`pr_data.pkl` pickle file. `ananlyze-pr-info.py` prints out
a markdown file with the.

To run, fix the fetching script to include a github login/token
and run it. When it is done, call
`./analyze-pr-info.py > analysis.md`, to create/udpate the
`analysis.md` file.
