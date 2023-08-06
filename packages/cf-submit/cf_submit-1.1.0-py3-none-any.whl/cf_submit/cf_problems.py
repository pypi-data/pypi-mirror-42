from prettytable import PrettyTable

from .cf_colors import colors


def print_prob(raw_html, contest, verbose, sort, pretty_off):
    stats = PrettyTable()

    # header
    header = ["#", "Name", "Solves"]
    stats.field_names = header

    # get problems table
    probraw = raw_html.find_all("table", class_="problems")[0].find_all("tr")
    names = []
    for row in probraw[1:]:
        tablerow = []
        if not verbose and row.has_attr("class") and row["class"][0] == "accepted-problem":
            continue
        cell = row.find_all("td")
        if len(cell) < 4:
            continue
        tablerow.append(str(cell[0].get_text(strip=True)))
        names.append(str(cell[0].get_text(strip=True)))
        tablerow.append(str(cell[1].find("a").get_text(strip=True)))
        numstring = str(cell[3].get_text(strip=True))
        if len(numstring) == 0:
            tablerow.append(int(0))
        else:
            tablerow.append(int(numstring[1:]))
        stats.add_row(tablerow)

    if pretty_off:
        print(*names)
        return

    # printing
    stats.hrules = True
    stats.align["Name"] = "l"
    stats.align["Solves"] = "r"
    if sort == "solves":
        print(stats.get_string(sortby="Solves", reversesort=True))
    elif sort == "index":
        print(stats.get_string(sortby="#"))
    else:
        print(stats)

    # check for countdown timer
    countdown_id = "contest-state-regular countdown before-contest-" + contest + "-finish"
    countdown_timer = raw_html.find_all("span", class_=countdown_id)
    if len(countdown_timer) > 0:
        print("%sTIME LEFT: %s%s" %
              (colors.BOLD, str(countdown_timer[0].get_text(strip=True)), colors.ENDC))
