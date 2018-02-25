# Okane
お金: Personal finance manager via command line


# Command line options

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

Show a balance
```
okane -b
```

## Planned features
- Save financial registers with accounts
- List all registers in a specific time interval
- Load data from XLS
- Plot charts

## Installation

Add the following lines to your bashrc:
```
export OKANE_DIR=<path-to-okane>/Okane/
source $OKANE_DIR/src/bashrc.sh
```
(WIP I am going to create a better setup)

## Contributing

Feel free to submit PRs. I will do my best to review and merge them if I consider them essential.

## Development status

This is a very alpha software. The code was written with no consideration of coding standards and architecture. A refactoring would do it good...