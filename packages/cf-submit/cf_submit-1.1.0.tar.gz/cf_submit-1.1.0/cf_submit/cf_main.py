import sys
import re
import os
import argparse
import webbrowser

from . import cf_login
from . import cf_problems
from . import cf_contests
from . import cf_groups
from . import cf_standings
from . import cf_submit
from . import cf_hack
from . import cf_parse
from . import cf_test
from .cf_colors import colors


# print standings

def print_standings(group, contest, verbose, top, sort, showall):
    # requires login
    browser = cf_login.login()
    if group is not None:
        # group contest contest
        url = "http://codeforces.com/group/" + \
            group + "/contest/" + contest + "/standings"
    elif len(str(contest)) >= 6:
        # gym contest
        url = "http://codeforces.com/gym/" + contest + "/standings"
    else:
        # codeforces round
        url = "http://codeforces.com/contest/" + contest + "/standings"
    # check if friends
    if group is not None:
        url += "/groupmates/true"
    elif showall is False:
        url += "/friends/true"
    else:
        url += "/page/1"
    browser.open(url)
    cf_standings.print_st(browser.parsed, verbose, top, sort)


# print problem stats

def print_problems(group, contest, verbose, sort, pretty_off):
    browser = cf_login.login()
    if group is not None:
        url = "http://codeforces.com/group/" + group + "/contest/" + contest
    elif len(str(contest)) >= 6:
        url = "http://codeforces.com/gym/" + contest
    else:
        url = "http://codeforces.com/contest/" + contest
    browser.open(url)
    if sort is None:
        sort = "solves"
    cf_problems.print_prob(browser.parsed, contest, verbose, sort, pretty_off)


# get time

def print_time(group, contest):
    browser = cf_login.login()
    if group is not None:
        url = "http://codeforces.com/group/" + group + "/contest/" + contest + "/submit"
    elif len(str(contest)) >= 6:
        url = "http://codeforces.com/gym/" + contest + "/submit"
    else:
        url = "http://codeforces.com/contest/" + contest + "/submit"
    browser.open(url)
    countdown_timer = browser.parsed.find_all(
        "span", class_="contest-state-regular countdown before-contest-" + contest + "-finish")
    if len(countdown_timer) == 0:
        print("Contest " + contest + " is over")
    else:
        print("%sTIME LEFT: %s%s" %
              (colors.BOLD, str(countdown_timer[0].get_text(strip=True)), colors.ENDC))


# main

def main():
    cache_loc = os.path.join(os.environ['HOME'], '.cache', 'cf_submit')
    if os.path.isdir(cache_loc) is False:
        os.mkdir(cache_loc)
    # get default gym contest
    defaultcontest = None
    defaultgroup = None
    contest_loc = os.path.join(cache_loc, "contestid")
    group_loc = os.path.join(cache_loc, "groupid")
    if os.path.isfile(contest_loc):
        contestfile = open(contest_loc, "r")
        defaultcontest = contestfile.read().rstrip('\n')
        contestfile.close()
    if os.path.isfile(group_loc):
        groupfile = open(group_loc, "r")
        defaultgroup = groupfile.read().rstrip('\n')
        groupfile.close()
    # ------------------- argparse --------------------
    parser = argparse.ArgumentParser(
        description="Command line tool to submit to codeforces", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", help="con/gym/gcon -- change contest or gym or group contest id\n" +
                                        "hack -- try to hack all the accepted submissions for a specific given problem\n" +
                                        "ext -- change default file extension\n" +
                                        "ext -- change default file extension\n" +
                                        "info -- current handle and contest id\n" +
                                        "login -- save login info\n" +
                                        "peek -- look at last submission\n" +
                                        "problems -- show number of solves on each problem\n" +
                                        "standings -- show standings of friends in default contest, or specify contest with -p\n" +
                                        "submit -- submit code to problem\n" +
                                        "time -- shows time left in contest\n" +
                                        "watch -- watch last submission\n" +
                                        "open -- open selected problem on default browser\n" +
                                        "parse -- import selected problem samples data\n" +
                                        "test -- test the selected source code with the imported tests data\n"
                        )
    parser.add_argument("option",
                        nargs='*', default=None,
                        help="file to submit"
                        )
    parser.add_argument("--handle",
                        action="store", default=None,
                        help="specify handle, example: --handle _bacali"
                        )
    parser.add_argument("--id",
                        action="store", default=None,
                        help="specify contest or gym id, example: --id 1117"
                        )
    parser.add_argument("-p", "--prob",
                        action="store", default=None,
                        help="specify problem, example: -p 845a"
                        )
    parser.add_argument("--pretty-off",
                        action="store_true", default=False,
                        help="turn pretty print off"
                        )
    parser.add_argument("-l", "--lang",
                        action="store", default=None,
                        help="specify language, example: -l cpp11"
                        )
    parser.add_argument("-c", "--contest",
                        action="store", default=None,
                        help="specify contest when getting standings"
                        )
    parser.add_argument("--group",
                        action="store", default=None,
                        help="specify group"
                        )
    parser.add_argument("-w", "--watch",
                        action="store_true", default=False,
                        help="watch submission status"
                        )
    parser.add_argument("-v", "--verbose",
                        action="store_true", default=False,
                        help="show more when looking at standings"
                        )
    parser.add_argument("-a", "--all",
                        action="store_true", default=False,
                        help="show common standings"
                        )
    parser.add_argument("-t", "--top",
                        type=int, nargs='?', const=10, default=50,
                        help="number of top contestants to print"
                        )
    parser.add_argument("-s", "--sort",
                        choices=["solves", "index", "id"],
                        type=str, nargs='?', const="solves", default=None,
                        help="sort by: solves (default), index (id)"
                        )
    parser.add_argument("-g", "--guru",
                        action="store_true", default=False,
                        help="submit to acmsguru problemset"
                        )
    parser.add_argument("-n", "--number",
                        type=int, action="store", default=10,
                        help="number of tests"
                        )

    args = parser.parse_args()

    # deal with short commands
    if args.command == "st":
        args.command = "standings"
    elif args.command == "pb":
        args.command = "problems"
    if args.sort == "id":
        args.sort = "index"

    # do stuff
    if args.command == "gcon":
        # set group contest
        # check if bad input
        if args.group is None:
            group = input("Group Id: ")
        else:
            group = args.group

        if args.id is None:
            contest = input("Contest number: ")
        else:
            contest = args.id
        groupfile = open(group_loc, "w")
        groupfile.write(group)
        groupfile.close()
        contestfile = open(contest_loc, "w")
        contestfile.write(contest)
        contestfile.close()
        print("Group set to " + group)
        print("Contest set to " + contest)

    elif args.command == "gym" or args.command == "con":
        # set contest
        # check if bad input
        if args.id is not None:
            contest = args.id
        else:
            contest = input("Contest/Gym number: ")
        if os.path.isfile(group_loc):
            os.remove(group_loc)
        contestfile = open(contest_loc, "w")
        contestfile.write(contest)
        contestfile.close()
        if len(contest) >= 6:
            print("Gym set to " + contest)
        else:
            print("Contest set to " + contest)
    elif args.command == "groups":
        if len(args.option) == 0:
            curr = ""
        else:
            curr = str(args.option[0])
        cf_groups.load_groups(args.pretty_off)
    elif args.command == "gcontests":
        if args.group is None:
            group = input("Group Id: ")
        else:
            group = args.group
        cf_groups.load_contests(group, args.pretty_off)
    elif args.command == "contests":
        if len(args.option) == 0:
            curr = ""
        else:
            curr = str(args.option[0])
        cf_contests.load_contests(False, curr, args.pretty_off)
    elif args.command == "gyms":
        if len(args.option) == 0:
            curr = ""
        else:
            curr = str(args.option[0])
        cf_contests.load_contests(True, curr, args.pretty_off)
    elif args.command == "ext":
        if len(args.option) > 1:
            print("Bad input")
            return
        if len(args.option) == 1:
            defext = args.option[0]
        else:
            defext = input("Default file extension: ")
        defext_loc = os.path.join(cache_loc, "default_ext")
        extfile = open(defext_loc, "w")
        extfile.write(defext)
        extfile.close()
        print("Default extension set to " + defext)

    elif args.command == "info":
        handle = cf_login.get_secret(False)
        print("handle: " + handle)
        print("groupID: " + str(defaultgroup))
        print("contestID: " + str(defaultcontest))

    elif args.command == "login":
        # set login info
        if args.handle is None:
            cf_login.set_login()
        else:
            cf_login.set_login(args.handle)

    elif args.command == "peek":
        # look at last submission
        cf_submit.peek(cf_login.get_secret(False))

    elif args.command == "watch":
        cf_submit.watch(cf_login.get_secret(False))

    elif args.command == "time":
        if args.contest is None and args.group is None:
            print_time(defaultgroup, defaultcontest)
        elif args.contest is None:
            print_time(args.group, defaultcontest)
        else:
            print_time(args.group, args.contest)

    elif args.command == "standings":
        # look at standings
        if args.contest is None and args.group is None:
            print_standings(defaultgroup, defaultcontest, args.verbose,
                            args.top, args.sort, args.all)
        elif args.contest is None:
            print_standings(args.group, defaultcontest, args.verbose,
                            args.top, args.sort, args.all)
        else:
            print_standings(args.group, args.contest, args.verbose,
                            args.top, args.sort, args.all)

    elif args.command == "problems":
        # look at problem stats
        if args.contest is None and args.group is None:
            print_problems(defaultgroup, defaultcontest,
                           args.verbose, args.sort, args.pretty_off)
        elif args.contest is None:
            print_problems(args.group, defaultcontest,
                           args.verbose, args.sort, args.pretty_off)
        else:
            print_problems(args.group, args.contest,
                           args.verbose, args.sort, args.pretty_off)

    elif args.command == "submit":
        # get default ext
        defextension = None
        defext_loc = os.path.join(cache_loc, "default_ext")
        if os.path.isfile(defext_loc):
            extfile = open(defext_loc, "r")
            defextension = extfile.read().rstrip('\n')
            extfile.close()
        # get handle
        defaulthandle = cf_login.get_secret(False)
        # open browser
        browser = cf_login.login()
        if args.contest is not None and args.group is not None:
            defaultgroup = args.group
            defaultcontest = args.contest
        elif args.contest is not None:
            defaultcontest = args.contest
        if browser is not None:
            cf_submit.submit_files(
                browser, defaulthandle, defaultgroup, defaultcontest, args.prob, defextension,
                args.lang, args.option, args.watch, args.guru
            )
    elif args.command == "test":
        if not os.path.isdir("files"):
            print("Please import problem testcases first by:\n\tcf parse -p a")
            return
        if len(args.option) == 0:
            print("Please select the source file")
            return
        cf_test.test(args.option[0], args.lang)
    elif args.command == "parse":
        if args.prob is None:
            problem = input("Problem Id: ")
        else:
            problem = args.prob
        if len(problem) < 3:
            cf_parse.parse(defaultgroup, defaultcontest,
                           str(problem).upper())
        else:
            splitted = re.split(r"(\D+)", problem)
            cf_parse.parse(defaultgroup, splitted[0], str(
                splitted[1]+splitted[2]).upper())
    elif args.command == "open":
        if args.prob is None:
            print("Please select problem to open!!")
            return
        if defaultgroup is None:
            if len(args.prob) < 3:
                webbrowser.open("https://codeforces.com/contest/%s/problem/%s"
                                % (defaultcontest, str(args.prob).upper()), 2)
            else:
                splitted = re.split(r"(\D+)", args.prob)
                webbrowser.open("https://codeforces.com/contest/%s/problem/%s"
                                % (splitted[0], str(splitted[1]+splitted[2]).upper()), 2)
        else:
            if len(args.prob) < 3:
                webbrowser.open("https://codeforces.com/group/%s/contest/%s/problem/%s"
                                % (defaultgroup, defaultcontest, str(args.prob).upper()), 2)
            else:
                splitted = re.split(r"(\D+)", args.prob)
                webbrowser.open("https://codeforces.com/group/%s/contest/%s/problem/%s"
                                % (defaultgroup, splitted[0], str(splitted[1]+splitted[2]).upper()), 2)
    elif args.command == "hack":
        if len(args.option) < 3:
            print(
                "Please select your <generator-source> [<tle-generator-source>] <checker-source> <answer-source> !!")
            return
        if args.prob is None:
            print("Please select problem to try!!")
            return

        if len(args.option) == 3:
            cf_hack.begin_hack(defaultcontest, args.prob, args.option[0], None,
                               args.option[1], args.option[2], args.number)
        else:
            cf_hack.begin_hack(defaultcontest, args.prob, args.option[0], args.option[1],
                               args.option[2], args.option[3], args.number)
    else:
        print("UNKNOWN COMMAND")


# END
