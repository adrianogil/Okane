# Okane (お金)
> Personal Finance Manager via Command Line.

Manage your personal finance using a simple and effective command line interface.

## Table of Contents

- [Command Line Options](#command-line-options)
- [Installation](#how-to-install)
- [Planned Features](#planned-features)
- [Contributing](#contributing)
- [Development Status](#development-status)

## Command Line Options

Save a register

```
okane -s <description> <amount> -dt <date> -cs <category> -ac <account>
```

Update a register

```
okane -u <register-id> <description> <amount> -dt <date> -cs <category>
```

Delete a register

```
okane -d <register-id>
```

Save a category
```
okane -sc <category>
```

Update a category
```
okane -uc <category-id> <new-category-name>
```

Delete a category
```
okane -dc <category-id>
```

List categories
```
okane -lc
```

List financial registers
```
okane -l
```

List financial registers while showing balance of current selection
```
okane -l --format balance
```

List financial registers with some description
```
okane -l <description>
```

Create an account
```
okane -sa <account-name>
```

List accounts
```
okane -la
```

Update an account
```
okane -ua <account-id> <account-name>
```

Delete an account by id
```
okane -da <account-id>
```

Delete an account by name
```
okane -da <account-name>
```

List financial registers in a specific time interval
```
okane -l -since=<date1> -until=<date2>
```

List financial registers with specific categories
```
okane -l -cs <category1> <category2>..<categoryN>
```

List financial registers from specific accounts
```
okane -l -ac <account1> <account2>..<accountN>
```

List financial registers with a offset <offset> and a limit <limit>. Very useful for paging content.
```
okane -l +<offset> and -<limit>
```

Show a balance
```
okane -b
```

Balance per account
```
okane -ba
```

Balance per category
```
okane -bc
```

Load data from xls. Mapping fields according to:
- "Data Ocorrência" as "register date"
- "Descrição" as "description"
- "Valor" as "amount"
- "Categoria" as category
- "Conta" as "account"
```
okane -xls
```

Export data as CSV
```
okane -e <file.csv>
```

- Load data from CSV
```
okane -csv <file.csv>
```

Transfer between accounts
```
okane -t <value> <account1> <account2> -dt <date>
```

## Planned features
- List all registers that are in given accounts.
- List all registers in a specific time interval.
- Capability to plot charts.

# How to Install

You can use [gil-install](https://github.com/adrianogil/gil-tools/blob/master/src/python/gil_install.py):
```
gil-install -i
```

Or you can add the following lines to your bashrc:
```
export OKANE_DIR=<path-to-okane>/Okane/
source $OKANE_DIR/src/bashrc.sh
```

## Contributing

Contributions are welcome! Please submit your PRs. They will be reviewed, and if they align with the project's goals, they will be merged.

## Development Status

This is currently in its alpha stage. The code was written without strict adherence to coding standards and architecture. Refactoring is in consideration.
