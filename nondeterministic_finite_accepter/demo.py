import argparse
from nfa import NFA


# parse argument
parser = argparse.ArgumentParser(
    description="Run input strings through a provided NFA and output the resulting states and whether they are accepted",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "filename",
    metavar="NFA_JSON",
    help="""path to a .json file containing the NFA.
The JSON object must contain the following properties:
"initial_state", "final_states" and "transition".

E.g.
{
  "initial_state": "q0",
  "final_states": ["q1"],
  "transition": {
    "q0": { "a": "q1" },
    "q1": { "a": "q1", "": "q2" },
    "q2": { "b": "q0" }
  }
}

A lambda symbol is represented as an empty string "".
A transition can result in many states (an array)
or no state (null, empty array or not specified).

E.g.
"transition": {
  "q0": {
    "": "q1",          // lambda transition
    "a": ["q0", "q1"], // more than one resulting state

    "b": null,
    "c": []
    // transition["q0"]["b"] is an empty set because null is provided
    // transition["q0"]["c"] is an empty set because empty array [] is provided
    // transition["q0"]["d"] is an empty set because no transition for symbol "d" is provided
  }
}
""",
)

args = parser.parse_args()


# parse nfa object
try:
    with open(args.filename) as f:
        import json

        try:
            nfa_json = json.load(f)
        except json.decoder.JSONDecodeError:
            parser.error("invalid JSON")
except FileNotFoundError:
    parser.error(f"file not found: '{args.filename}'")

if (
    not isinstance(nfa_json, dict)
    or "initial_state" not in nfa_json
    or "final_states" not in nfa_json
    or "transition" not in nfa_json
):
    parser.error(f"invalid nfa object in '{args.filename}'")


nfa = NFA(nfa_json)


# user input
print("Input strings to run through the NFA (Ctrl + C to stop the loop):\n")

try:
    while True:
        string = input(">> ")

        result = nfa.delta_star(nfa.initial_state, string)
        accepted = "accepted ✔️" if nfa.accepts(string) else "rejected ❌"

        print(f"delta_star({nfa.initial_state}, {string}) = {result}")
        print(f"'{string}' {accepted}\n")
except KeyboardInterrupt:
    pass
