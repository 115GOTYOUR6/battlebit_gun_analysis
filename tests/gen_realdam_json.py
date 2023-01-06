from json import dump


def exact_check(x, gun_name):
    for i in range(len(x) - 1):
        current = x[i]
        ne = x[i+1]
        if current < ne:
            raise ValueError(f"Problem at index {i} for gun {gun_name}")


guns = {}
# these are the distance values used in measuring each of the damage values
# below.
guns['dist'] = [i for i in range(50, 301, 10)]
# please ensure the keys given here match those in the gen_arsenal module
guns["AK74_HB"] = [36.30, 36.18, 35.84, 35.32, 34.68,
                   33.81, 32.78, 31.74, 30.54, 29.25,
                   27.99, 26.49, 25.13, 23.69, 22.35,
                   20.91, 19.63, 18.34, 17.15, 16.06,
                   15.11, 14.25, 13.59, 13.12, 12.81,
                   12.71]
guns["HK419_HB"] = [34.10, 33.98, 33.67, 33.17, 32.51,
                    31.76, 30.88, 29.80, 28.70, 27.49,
                    26.27, 24.96, 23.60, 22.26, 21.02,
                    19.62, 18.47, 17.39, 16.11, 15.13,
                    14.23, 13.45, 12.82, 12.33, 12.04,
                    11.94]
guns["MP5"] = [26.00, 25.73, 24.97, 23.96, 22.57,
               20.87, 19.02, 17.09, 15.27, 13.27,
               11.54, 9.88,  8.67,  7.41,  6.73,
               6.5,   6.5,   6.5,   6.5,   6.5,
               6.5,   6.5,   6.5,   6.5,   6.5,
               6.5]

###########################################################################
# deleting keys in this loop will RunTimeError so we do it after.
keystokill = []
for g_name in guns:
    if g_name == 'dist':
        continue
    try:
        assert len(guns[g_name]) == len(guns['dist'])
        exact_check(guns[g_name], g_name)
    except ValueError as e:
        print(f"There is a damage value in the {g_name} list that violates"
              " decending order. This weapon will be removed from the"
              f" dictionary.\n{e}")
        keystokill.append(g_name)
    except AssertionError:
        print(f"The number of damage values provided for {g_name} is not the"
              " same as the number of distance values. This gun will be"
              " removed from the dictionary.\n")
        keystokill.append(g_name)

for key in keystokill:
    del guns[key]
if len(guns.keys()) < 1:
    raise ValueError("No valid damage data has been provided, exiting")

with open("./realgundam.csv", 'w') as fp:
    dump(guns, fp)
