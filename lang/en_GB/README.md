# British English

The game's own text is American English, shown as **American English** in the language menu. **British English** (`en_GB`) is an ordinary gettext catalogue, [`lang/po/en_GB.po`](../po/en_GB.po), generated from that text by [`make_en_GB_po.py`](make_en_GB_po.py). Gettext shows the game's own text for any string a catalogue leaves out, so `en_GB.po` holds only the strings whose British form differs: about 8,100 of the 111,000.

With the language option set to "System language", the game picks British English for English set to the United Kingdom, Ireland, Australia or New Zealand, and American English for any other English.

## What it changes

* **Spelling**, from [`spelling.tsv`](spelling.tsv): the common British forms with *-ise* (armour, colour, centre, defence, grey, realise, travelled, aluminium, tyre, metre). Oxford *-ize* spelling is not used.
* **Vocabulary**, from [`vocabulary.tsv`](vocabulary.tsv): only swaps whose British word has no second meaning in the game, such as pants → trousers, gasoline → petrol, parking lot → car park, zucchini → courgette and canned → tinned. Words that would clash with another item in British English stay American: a *flashlight* is not called a *torch* because the game has burning torches, and *vest*, *jumper*, *tin*, *rubber*, *flat*, *pavement*, *silencer*, *paraffin*, *chemist*, *spirits*, *biscuit*, *boot* and *bonnet* are not swapped for the same reason.
* **Exceptions**, from [`keep.txt`](keep.txt): text left exactly as it is, such as American proper nouns (Department of Defense, Centers for Disease Control, Springfield Armory, Bar Harbor), American idioms (freedom fries, dumpster fire) and words whose other sense keeps the American form (a pH meter, an EMP blast that fries a circuit).

Markup tags (`<color_red>`, `<npcname>`), printf placeholders (`%s`, `%1$d`) and `{braced}` fields are never changed. Matching is by whole word, ignores case and keeps the original's capitalisation (Armor → Armour, ARMOR → ARMOUR).

## Regenerating it

`en_GB.po` must be regenerated whenever the game's text changes, or new and changed strings appear in American English. CI warns when it is out of date. From the repository root, with gettext and Python 3 with [polib](https://pypi.org/project/polib/) installed (`pip install polib`):

```bash
lang/update_en_GB.sh
```

This rebuilds the translation template `lang/po/cataclysm-dda.pot` with `lang/update_pot.sh` and converts it. To convert an existing template only, run `lang/en_GB/make_en_GB_po.py`. Commit the new `lang/po/en_GB.po`.

To change a spelling or word, edit the list (one `american<TAB>british` pair per line; longer phrases in `vocabulary.tsv` win over shorter ones), add a phrase to `keep.txt` to leave it alone, then regenerate. Do not edit `en_GB.po` by hand: the next regeneration overwrites it.

## VarCon

`spelling.tsv` was derived from VarCon (Variant Conversion Info) version 2016.01.19, from <http://wordlist.aspell.net/varcon/>, and modified: it keeps only entries for words that occur in the game's text, drops some of those by hand (sense-dependent words such as *inquire*, *spoiled* and *whiskey*, and names) and adds a few VarCon lacks or marks as sense-dependent (tyre, metre, licence, chequered, flyer). VarCon's copyright and permission notice:

```
COPYRIGHT:

Copyright 2000-2010 by Kevin Atkinson

Permission to use, copy, modify, distribute and sell this array, the
associated software, and its documentation for any purpose is hereby
granted without fee, provided that the above copyright notice appears
in all copies and that both that copyright notice and this permission
notice appear in supporting documentation. Kevin Atkinson makes no
representations about the suitability of this array for any
purpose. It is provided "as is" without express or implied warranty.

Since the original words lists come from the Ispell distribution:

Copyright 1993, Geoff Kuenning, Granada Hills, CA
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All modifications to the source code must be clearly marked as
   such.  Binary redistributions based on modified source code
   must be clearly marked as modified versions in the documentation
   and/or other materials provided with the distribution.
(clause 4 removed with permission from Geoff Kuenning)
5. The name of Geoff Kuenning may not be used to endorse or promote
   products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY GEOFF KUENNING AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL GEOFF KUENNING OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
```
