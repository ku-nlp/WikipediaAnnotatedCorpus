# Developer Guide

## Procedures to add new documents

- Copy and filter newly annotated files

```shell
make -f scripts/Makefile pull CORPUS=WAC
fd -t f knp --exec sed -i "s/undefined<NE/<NE/g" {}
fd -t f knp --exec sed -i "s/NIL undefined/NIL/g" {}
p scripts/filter.py knp
```

- Update `inappropriate.id`

```shell
cat id/inappropriate.id | sort | uniq > tmp
mv tmp id/inappropriate.id
g add id/inappropriate.id
g commit id/inappropriate.id
```

- Commit annotated files

```shell
# Make sure the appended lines in `.gitignore` are deduplicated.
cat id/inappropriate.id | sd '(wiki\d{4})(\d{4})' 'knp/$1/$1$2.knp' >> .gitignore
g add ...
g commit ...
```

- Update `all.id`

```shell
fd . -t f knp | cut -d'/' -f3 | cut -d'.' -f1 | sort > id/all.id
# or
ls knp/wiki0020 | cut -d'.' -f1 >> id/all.id
...
difference <(cat id/all.id | sort | uniq) <(cat id/inappropriate.id | sort | uniq) > tmp
mv tmp id/all.id
```
