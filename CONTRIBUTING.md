# Developer Guide

## Requirements

- Python: 3.10+
- Dependencies: See [pyproject.toml](./pyproject.toml) or [requirements.txt](./requirements.txt).

## Setting up the development environment

- Create a virtual environment and install dependencies.

    ```shell
    uv sync
    ```

## Adding new documents

- Copy and filter newly annotated files

```shell
make -f scripts/Makefile pull CORPUS=WAC
python scripts/filter.py knp
```

- Update `inappropriate.id`

```shell
cat id/inappropriate.id | sort | uniq > tmp
mv tmp id/inappropriate.id
git add id/inappropriate.id
git commit -m "update id/inappropriate.id"
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
ls knp/wiki0021 | cut -d'.' -f1 >> id/all.id
...
difference <(cat id/all.id | sort | uniq) <(cat id/inappropriate.id | sort | uniq) > tmp
mv tmp id/all.id
```

- Update `train.id`

...
