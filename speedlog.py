from argparse import ArgumentParser
from cProfile import Profile
from pathlib import Path

parser = ArgumentParser()

parser.add_argument("file", type=str)
parser.add_argument("function", type=str)
parser.add_argument("--decimal_places", type=int, default=5)
args = parser.parse_args()
code_file = args.file
function_name = args.function
decimal_places = args.decimal_places

file_name = Path(code_file).stem

exec(f"import {file_name}")

profile = Profile().run(f"{file_name}.{function_name}()")

profile.snapshot_stats()


class Stat:
    def __init__(self, file, line_num, function, calls, time, cum_time, callers=None):
        self.calls = calls
        self.time = round(time, decimal_places)
        self.cum_time = round(cum_time, decimal_places)

        self.callers: list[Stat] = callers or []

        self.built_in = None
        if file == "~":
            built_in_method = function[function.find(".") + 1 : -1]
            self.built_in = f"built-in method '{built_in_method}'"
            self.desc = self.built_in
            return

        self.file = file
        self.line_num = line_num
        self.function = function

        self.link = file + " :" + str(line_num)
        self.desc = "file:///" + self.link + " (" + self.function + ")"

    def __repr__(self):
        return f"{str(self.calls)} {str(self.time)} {str(self.cum_time)} {self.desc}"


def get_stats(method, stats):
    file, line_num, function = method

    if (
        file == "<string>"
        or function.startswith("<method '")
        or function == "<built-in method builtins.exec>"
    ):
        return None

    if len(stats) == 5:
        calls, _, time, cum_time, callers = stats

        if callers:
            stat = Stat(
                file,
                line_num,
                function,
                calls,
                time,
                cum_time,
            )
            for method, stats in callers.items():
                sat = get_stats(method, stats)
                if sat is not None:
                    stat.callers.append(sat)
            return stat

    else:
        calls, _, time, cum_time = stats

    return Stat(file, line_num, function, calls, time, cum_time)


results: list[Stat] = []
for method, stats in profile.stats.items():
    stat = get_stats(method, stats)

    if stat:
        results.append(stat)

string = f"Ran {code_file} in {round(sum([stat.time for stat in results]), decimal_places)} seconds...\nCalls | Time | Total-Time | File\n\n"
for result in sorted(results, key=lambda x: x.cum_time):
    string += str(result) + "\n"
    for i, caller in enumerate(result.callers):
        string += " " + ("-" if i + 1 % 2 == 0 else "#") + " " + str(caller) + "\n"

with open(r"time.log", "w") as f:
    f.write(string)
