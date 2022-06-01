# Side Channel Analysis on Bitsliced AES
This repository contains the source code for the experiments in the master thesis "Side Channel Analysis on Bitsliced AES" by Stian Husum.

There are five main parts of this code:
- [A fixsliced implementation of AES by Alexandre Adomnicai](https://github.com/aadomn/aes) with driver code to collect traces on a [ChipWhisperer](https://github.com/newaetech/chipwhisperer).
- A jupyter notebook to collect traces.
- A script to compute SNRs from traces.
- A script to compute CPA attacks on the traces using the attacks presented in the thesis.
- A script to compute the success rates from the results of the attacks.

# License
The code derived from the [ChipWhisperer](https://github.com/newaetech/chipwhisperer) project is licenced under GPLv3, as denoted in their files
The rest of the code is licenced under the MIT licence

* GPL-3.0 (https://www.gnu.org/licenses/gpl-3.0.html)
* MIT license ([LICENSE](../LICENSE) or http://opensource.org/licenses/MIT)
