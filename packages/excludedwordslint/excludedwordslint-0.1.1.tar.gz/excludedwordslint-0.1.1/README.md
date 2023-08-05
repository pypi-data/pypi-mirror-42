# Excluded Words Lint

[![Build Status](https://travis-ci.org/dgarcia360/excludedwords-lint.svg?branch=master)](https://travis-ci.org/dgarcia360/excludedwords-lint)

Automate the search of unnecessary words in your project.

Inspired in Jim's Fisher talk [Don’t Say “Simply”](http://www.writethedocs.org/videos/prague/2018/don-t-say-simply-jim-fisher/) (Write The Docs 2018).

# Installation

    $ pip install excludedwordslint

# Usage    
    
excluded-words-lint [OPTIONS] WORDS

| Options               | Description                                         |
|-----------------------|-----------------------------------------------------|
| -e, --extensions TEXT | File extensions to consider, separated by commas.   |
| -c, --match_case      | Matches case sensitive words.                       |
| -w, --match_word      | Matches complete words.                             |
| -r, --regex           | Argument is a custom regular expression.            |
| -p, --path TEXT       | Changes the root directory.                         |
| -t, --throw           | Throws an exception if some of the words are found. |
| --help                | Show this message and exit.                         |

# Examples
    
## Search for substrings

Matches any line that contains the substrings "simply" or "simple". It only takes into account files inside "docs" folder with rst or md extensions. 

    $> excluded-words-lint simply,simple --path 
    docs --extensions rst,md 
    
## Search for complete words

Matches any line that contains the word "Simply" or "simply".

    $> excluded-words-lint simply,simple --match-word

## Search for case sensitive words

Matches any line that contains the word "Simply".

    $> excluded-words-lint Simply --match-word

## Search for words using a custom regular expression

Matches any line that starts with "Simply".

    $> excluded-words-lint ^Simply --regex
    
## Import words from a config file

Get an example configuration file [here](https://gist.github.com/dgarcia360/f89b0d591882aabb7b8b07c71ae4aad1).

    $> excluded-words-lint --config=config/.excludedwords
    
## Search for words and throw an error when found

Include the option ``throw`` when integrating the command line tool with TravisCI.

    $> excluded-words-lint simply --throw
    
# License

[MIT License](LICENSE.md)
