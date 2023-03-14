
"""

if row["location"] == "3" and "1530" in self.getAllLaneletId(list(set(curgroup["laneletId"].unique()))) and \
        (row["laneletId"] == "1422"):
    return self.initTracks(tracksdata, row)

if row["location"] == "3" and row["laneletId"] == "1530":
    return False

"""


