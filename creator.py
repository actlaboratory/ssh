import seens
import pickle
import stage

with open("test.stg", mode = "rb") as f:
	stage = pickle.load(f)
i = 0
for seen in stage:
	newSeen = seens.seen(seen.title, seen.bgm, seen.fadeIn, seen.fadeOut, seen.repeat, seen.fx)
	stage[i] = newSeen
	i += 1
with open("test.stg", mode = "wb") as f:
	pickle.dump(stage, f)
print("done")