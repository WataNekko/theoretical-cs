import argparse


parser = argparse.ArgumentParser(
    description="Run the provided strings through the dfa and output whether they are accepted",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "dfa_filename",
    metavar="DFA_JSON",
    help="""path to the .json file containing the dfa.
The JSON object must contain the following properties:
"transition", "initial_state" and "final_states".

For example:
{
  "transition": {
    "q0": { "a": "q1", "b": "q0" },
    "q1": { "a": "q0", "b": "q1" }
  },
  "initial_state": "q0",
  "final_states": ["q1"]
}

""",
)
parser.add_argument("strings", nargs="*", help="the strings to be run through the dfa")
parser.add_argument(
    "-i",
    "--input",
    metavar="FILE",
    dest="input_file",
    help="""file containing strings to be run through the dfa.
Can be either in new line-separated text or in json format

E.g:
   '100
    101'
 or
   '["100", "101"]'""",
)

args = parser.parse_args()

# parse dfa object
try:
    with open(args.dfa_filename) as f:
        import json

        try:
            dfa = json.load(f)
        except json.decoder.JSONDecodeError:
            parser.error("invalid JSON")
except FileNotFoundError:
    parser.error(f"file not found: '{args.dfa_filename}'")

if (
    not isinstance(dfa, dict)
    or "transition" not in dfa
    or "initial_state" not in dfa
    or "final_states" not in dfa
):
    parser.error(f"invalid dfa object in '{args.dfa_filename}'")


# get input strings
if not args.input_file:
    input_strings = args.strings
else:
    try:
        with open(args.input_file) as f:
            content = f.read()
            try:
                input_strings = json.loads(content)
            except json.decoder.JSONDecodeError:
                input_strings = content.splitlines()
    except FileNotFoundError:
        parser.error(f"file not found: '{args.input_file}'")

    input_strings.extend(args.strings)


if not input_strings:
    print("[No string provided]")
    raise SystemExit


# run dfa
trans = dfa["transition"]
initial_state = dfa["initial_state"]
final_states = dfa["final_states"]

for string in input_strings:
    state = initial_state

    for symbol in string:
        try:
            state = trans[state][symbol]  # next state
        except KeyError as ex:
            parser.error(f"invalid dfa or input symbol: {ex}")

    result = "accepted ✔️" if state in final_states else "rejected ❌"
    print(f"'{string}' {result}")
