import MVVLive

foo = MVVLive.MVVLive()

lines = ["S1", "S2", "S3", "S4", "S6", "S7", "S8", "S20"]
for line in lines:
    print(f"{line}: {foo.get_punctuality(line)} %")
