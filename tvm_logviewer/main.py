import re
import multiprocessing as mp
from pyparsing import (
    Word, Literal, Combine, Optional, Regex, Suppress, restOfLine, ParserElement, StringEnd, MatchFirst, alphas, alphanums
)

ParserElement.setDefaultWhitespaceChars(" ")
langle  = Suppress("<")
rangle  = Suppress(">")

timestamp = Word("0123456789:.", exact=12).setResultsName("timestamp")
log_level = Word("ABCDEFGHIJKLMNOPQRSTUVWXYZ*").setResultsName("log_level")
tag = Word(alphas, alphanums + "_").setResultsName("tag")
pid_part = Word("0123456789:")
pid = Combine(pid_part + Literal(" ") + pid_part).setResultsName("PID")
first_block = langle + timestamp + log_level + tag + pid + rangle

optional_id_block = Optional(langle + Regex(r"\d+").setResultsName("optional_id") + rangle)
module = langle + Regex(r"[^>]+").setResultsName("module") + rangle
function = Optional(Suppress("[") + Regex(r"[^\]]+").setResultsName("function") + Suppress("]"))
message_basic = Optional(restOfLine.setResultsName("message"))

tail_alternative = optional_id_block + module + function + message_basic
message_multiline = Regex(r".*", re.DOTALL).setResultsName("message")

tail = MatchFirst([tail_alternative, message_multiline])
log_parser = first_block + tail + StringEnd()

def log_error(error_msg):
    with open("./logfile.txt", "a") as file: 
        file.write(error_msg)

def parse_line(line):
    if not re.match(r"^<\d{2}:\d{2}:\d{2}\.\d{3}", line):
        return {
            "timestamp": "", 
            "log_level": "",
            "tag": "",
            "PID": "",
            "optional_id": "", 
            "module": "", 
            "function": "", 
            "message": line.strip()
        }
    return log_parser.parseString(line.strip(), parseAll=True)

def parse_worker(lines): 
    results = []
    for line in lines: 
        try: 
            results.append(parse_line(line))
        except Exception as e: 
            log_error(f"Error: {e} in line: {line}")
    
    return results

logfiles = [
    "./IMS.log_20250409081706.log",
    "./IMS.log_20250409081724.log",
    "./IMS.log_20250409082908.log",
    "./IMS.log_20250409085500.log"
    ]

if __name__ == "__main__": 
    for file in logfiles:
        log_error(file + "\n")
        with open(file, "r") as log: 
            all_lines = log.readlines()

        n_workers = mp.cpu_count()
        chunks = [all_lines[i::n_workers] for i in range(n_workers)]

        with mp.Pool(n_workers) as pool: 
            results = pool.map(parse_worker, chunks)

        all_results = [item for sublist in results for item in sublist]

        log_error("\nParsing finished\n")
        log_error("Parsed lines: " + str(len(all_results)) + "\n\n")

    print("finished")

