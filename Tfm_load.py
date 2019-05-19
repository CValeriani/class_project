from handler.data_handler import data_process as handle
from os.path import join

# Program starts here:
# -------------------------------------
# Fetch Data
handle().fetch_data(folder=join("datasets"))