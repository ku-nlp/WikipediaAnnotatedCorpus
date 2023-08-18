# Developer Guide

## Procedures to add new documents

- Commit newly annotated files

```shell
make -f scripts/Makefile pull CORPUS=WAC
fd -t f knp --exec sed -i "s/undefined<NE/<NE/g" {}
fd -t f knp --exec sed -i "s/NIL undefined/NIL/g" {}
p scripts/filter.py knp
g add ...
g commit ...

```

- Update `inappropriate.id`

```shell
l id/inappropriate.id | sort | uniq > tmp
mv tmp id/inappropriate.id
g add id/inappropriate.id
g commit id/inappropriate.id
```

- Update `all.id`

```shell
l knp/wiki0020 | cut -d'.' -f1 >> id/all.id
l knp/wiki0021 | cut -d'.' -f1 >> id/all.id
...
difference <(cat id/all.id | sort | uniq) <(cat id/inappropriate.id | sort | uniq) > tmp
mv tmp id/all.id
```
