import hashlib

h = hashlib.new("md5")
for i in range(10000000):
    h.update(f"iwrupvqb{i}".encode("ascii"))
    if h.hexdigest()[0:6] == "000000":
        break

print(h.hexdigest())
print(i)
