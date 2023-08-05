import dicebag

print(f"D6: {dicebag.roll_d6()}")
print(f"3D6: {dicebag.roll_3d6()}")
print(f"3D20: {dicebag.roll_3d20()}")

# OMG I really didn't expect the following to work:
from dicebag import roll_d6 as d6

print(f"D6 {d6()}")
