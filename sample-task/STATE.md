# STATE — the modular black box

## Why this is the only answer
The box is fully determined by the pair (a, b) under the known modulus. Two clean
observations at x=0 and x=1 pin both constants exactly: f(0) gives b, and f(1) - f(0)
gives a (mod the modulus). No other (a, b) pair reproduces those two outputs. The answer
is therefore unique and stable — it does not depend on which extra points you sample.

## Order of decisions
1. Establish the modulus is known and the form is (a*x + b) mod m. (given in problem.md)
2. Recover b first (it is the output at x=0).
3. Recover a from the change between x=0 and x=1, reduced by the modulus.
4. Validate against one more point before committing.

## State
CALIBRATED — intended solver passes, naive shortcut fails, preview recorded at 1/8.
