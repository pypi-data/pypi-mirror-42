# Propose

Build truthtables with your command line.

![capture](https://user-images.githubusercontent.com/13420273/53683290-4d235900-3cff-11e9-9e1f-3ee883a91b8b.PNG)

### Operands

```
F <-> G | biconditional
F -> G  | implication
F xor G | exclusive or
F + G   | or
F * G   | and
!F      | not
```

## Installation

Install Propose with PIP

    $ pip3 install propose

## Usage

Pass an inline formula:

    $ propose "a * b"

Pass a file instead:

    $ propose --file formula.propose

To get a list of all available commands and options:

    $ propose --help

## Development

1. Clone this repository

    ```
    $ git clone git@github.com:jonhue/propose.git
    ```

2. Install Propose with Pip. You may want to use a virtualenv

    ```
    $ make setup
    ```

Rebuild & reinstall Propose:

    $ make reload

Run tests:

    $ make spec
