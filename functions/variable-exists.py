try:
  thevariable
except NameError:
  print("well, it WASN'T defined after all!")
else:
  print("sure, it was defined.")