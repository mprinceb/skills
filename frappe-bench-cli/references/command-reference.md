# Bench Command Reference

Use these forms as canonical syntax patterns.

## Bench-level

```bash
bench --help
bench setup --help
bench update --help
bench restart --help
bench start --help
```

## Site-scoped framework commands

```bash
bench --site <site> list-apps
bench --site <site> version
bench --site <site> install-app <app_name>
bench --site <site> uninstall-app <app_name> --dry-run
bench --site <site> migrate
bench --site <site> reload-doc <module> doctype <doctype_name>
bench --site <site> clear-cache
bench --site <site> backup --with-files
bench --site <site> restore <sql_file_path>
bench --site <site> execute <module.function> --args '["arg1"]'
bench --site <site> execute <module.function> --kwargs '{"k":"v"}'
```

## Dev-oriented commands

```bash
bench new-app <app_name>
bench --site <site> install-app <app_name>
bench --site <site> run-tests --app <app_name>
bench --site <site> run-tests --doctype "<DocType Name>"
bench --site <site> data-import --file <path.csv|xlsx> --doctype "<DocType Name>" --type Insert
bench --site <site> export-fixtures
```

## Typical sequencing

1. `bench --site <site> backup --with-files`
2. `bench --site <site> install-app <app_name>` or migration/change
3. `bench --site <site> migrate`
4. `bench --site <site> list-apps`
5. targeted verification (`bench execute`, app checks)
