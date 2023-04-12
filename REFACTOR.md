# Refactoring details
## Usage:
### Cyclomatic complexity:
```
radon cc path .
```
### Maintainability index:
```
radon mi path .
```

## Key:
### Cyclomatic complexity:
| Block type | Letter |
| --- | --- |
| Function | F |
| Method | M |
| Class | C |

| CC score | Rank | Risk | 
| --- | --- | --- |
| 1 - 5	| A | low - simple block |
| 6 - 10 | B | low - well structured and stable block |
| 11 - 20 | C | moderate - slightly complex block |
| 21 - 30 | D | more than moderate - more complex block |
| 31 - 40 | E | high - complex block, alarming |
| 41+ | F | very high - error-prone, unstable block |

### Maintainability index
| MI score | Rank | Maintainability |
| --- | --- | --- |
| 100 - 20 | A | Very high |
| 19 - 10 | B | Medium |
| 9 - 0 |	C | Extremely low |

## Pre-refactor (commit number 06d7ce6d3ca8bfda81c5564289f6debbf18597c3):
### Cyclomatic complexity:
```
    F 16:0 download_file - A
website/auth.py
    F 39:0 permissions - C
    F 14:0 user_redirect - A
website/backend.py
    C 13:0 EmailBackend - A
    M 19:4 EmailBackend.send_messages - A
    M 31:4 EmailBackend._send - A
    M 16:4 EmailBackend.__init__ - A
website/models.py
    F 135:0 parse_csv - C
    C 16:0 Hawkins - A
    C 27:0 User - A
    C 59:0 Role - A
    C 69:0 UserRoles - A
    C 85:0 Team - A
    C 94:0 Note - A
    C 101:0 Nutrition - A
    C 111:0 Sleep - A
    C 124:0 Readiness - A
website/__init__.py
    F 105:0 populate - A
    F 94:0 create_database - A
    F 36:0 create_app - A
website/forms.py
    C 6:0 NameRegisterForm - A
website/views.py
    F 422:0 teamView - D
    F 51:0 adminView - D
    F 654:0 adduser - C
    F 266:0 athleteView - C
    F 745:0 upload - B
    F 614:0 changeRole - A
    F 628:0 permissions - A
    F 409:0 changingTeamView - A
    F 737:0 allowed_file - A
    F 33:0 home - A
    F 42:0 dashboard - A
    F 772:0 remove_users - A
    F 789:0 remove - A
website/decorators.py
    F 7:0 protect_athlete_view - A
```

### Maintainability Index:
```
main.py - A
download_file.py - A
website/auth.py - A
website/backend.py - A
website/models.py - A
website/__init__.py - A
website/forms.py - A
website/views.py - A
website/decorators.py - A
```