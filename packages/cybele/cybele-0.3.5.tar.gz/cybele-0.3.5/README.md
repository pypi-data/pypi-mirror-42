Cybele
======

Cybele is a simple CLI password manager.  
It's based on python (3.6) and json.


Getting started
===============
## Installation
```bash
git clone https://gitlab.com:dithyrambe/cybele
pip install ./cybele
```

## Configuration
First you'll need to set up a database and a passphrase to encrypt your creds.  
By default, database will be stored at `~/.cybele/<$USERNAME>.cybeledb`
```bash
cybele init
Enter passphrase:
Enter same passphrase again:
```

## Adding entries
To add entries, you need to type your password, as most of `cybele` subcommands.
```bash
cybele add gitlab
Enter passphrase:
Username: my_gitlab_username
Enter passphrase:
Enter same passphrase again:
```

## Listing entries
At any time you may check your stored credentials
```
cybele ls
Enter passphrase:
┌────────┬────────────────────┬────────────┐
│ ENTRY  │ USERNAME           │ PASSPHRASE │
├────────┼────────────────────┼────────────┤
│ gitlab │ my_gitlab_username │ ********** │
│ entry1 │ my_entry1_username │ ********** │
│ entry2 │ my_entry2_username │ ********** │
└────────┴────────────────────┴────────────┘
```

## Copy-Paste tools
Typing passphrase is painfull. To copy passphrase 
of an entry in your clipboard type `cybele cp gitlab`.  
Clipboard is flush after a few seconds, so you only
have a reasonable time to paste it in a form.

> Note: if you want to copy username instead of passphrase
> type `cybele cp -u gitlab`