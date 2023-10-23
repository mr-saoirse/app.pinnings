import sys, requests

key = sys.argv[1]
sha = sys.argv[2]
changed_files_str = " ".join(sys.argv[3:])
changed_files = changed_files_str.split(",")

# changed folder extract

print("Changed Files: {}".format(changed_files_str))
