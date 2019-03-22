# Trello2mdtable #

This script converts JSON exports from [Trello](http://trello.com) to Pandoc flavor
Markdown summary table. The resulting file can then be translated further to other
formats such as PDF or HTML a converter (like [Pandoc](http://johnmacfarlane.net/pandoc/)).

To use the script, you need to have installed [Python 3](https://www.python.org/download). Then,
from a terminal, you can type the following:

    python3 ./src/trello2mdtable.py inputfile.json
    
This will generate a file `inputfile.md`, containing a section for each list, and subsections for
each cards. 

Markdown used inside cards is preserved, except that section headings on cards are converted down to
lower subsections to keep the logical structure (although, this is currently only done for
[Atx-style headers](http://johnmacfarlane.net/pandoc/README.html#atx-style-headers)).

The generated table has four columns (customized for product management): Feature (the card title), Description, Drivers (the card labels), Product Manager (the card owners).  It will produce one table per trello column with a section heading for it.

There currently following arguments are supported:

- `--output`/`-o` sets output filename (default is appending `.md` to the input filename)
- `--archived`/`-a` also includes archived lists and cards.
- `--header`/`-i` prepends a header page with general information about the board.
- `--encoding`/`-e` specifies the file encoding to be used (defaults to `utf8`)

## Licence ##

All code is [unlicensed](http://unlicense.org/)