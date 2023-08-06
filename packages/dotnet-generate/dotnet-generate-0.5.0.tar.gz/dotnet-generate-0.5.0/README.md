# Dotnet generate
[![PyPI](https://img.shields.io/pypi/v/dotnet-generate.svg?style=flat-square)](https://pypi.org/project/dotnet-generate/)
> Script generator for dotnet core 2.x


Tool for making it easier to generate MVC and API controllers in Asp.NET Core applications.
Helps also with managing DB migrations and updates.

## Installation

I have tested it with Python 3.6 only

Install it via pip/pip3 `pip install dotnet-generate`.


## Examples

Examples executed in dotnet core 2.1 solution folder, with the following structure

```
├── DAL
│   └── AppDbContext.cs
├── Domain
│   ├── BaseEntity.cs
│   ├── Contact.cs
│   ├── ContactType.cs
│   ├── Domain.csproj
│   ├── Identity
│   │   ├── AppRole.cs
│   │   └── AppUser.cs
│   └── Person.cs
└── WebApp
    ├── Startup.cs
    ├── Program.cs
    ...
```

### Migrations

To make new migrations run:
```
dotnet-generate migrate MigrationName
```

Migrate command has some additional options:
- `-u`, `-update` for updating DB to latest migration.
- `-m`, `--mvc` for creating MVC controllers.
- `-a`, `--api` for creating API controllers.
- `-t`, `--try` this option runs the tool without actually executing any commands, instead it will print those commands to console.

You can also combine these flags, for example you can generate shell script with all the commands as follows:

```
dotnet-generate migrate MigrationName -umat > script.sh
```

Which will produce the following script.sh

```bash
dotnet ef migrations add MigrationName --project DAL --startup-project WebApp
dotnet ef database update --project DAL --startup-project WebApp
cd WebApp/
dotnet aspnet-codegenerator controller -name PersonsController -actions -m Person -dc AppDbContext -outDir Controllers --useDefaultLayout --useAsyncActions --referenceScriptLibraries -f
dotnet aspnet-codegenerator controller -name ContactsController -actions -m Contact -dc AppDbContext -outDir Controllers --useDefaultLayout --useAsyncActions --referenceScriptLibraries -f
dotnet aspnet-codegenerator controller -name ContactTypesController -actions -m ContactType -dc AppDbContext -outDir Controllers --useDefaultLayout --useAsyncActions --referenceScriptLibraries -f
cd ../
cd WebApp/
dotnet aspnet-codegenerator controller -name PersonsController -actions -m Person -dc AppDbContext -outDir Api/Controllers -api --useAsyncActions -f
dotnet aspnet-codegenerator controller -name ContactsController -actions -m Contact -dc AppDbContext -outDir Api/Controllers -api --useAsyncActions -f
dotnet aspnet-codegenerator controller -name ContactTypesController -actions -m ContactType -dc AppDbContext -outDir Api/Controllers -api --useAsyncActions -f
cd ../


```

### Db updating

For updating db run
```
dotnet-generate update
```

### MVC controllers.

For generating MVC controllers run
```
dotnet-generate mvc
```

### API controllers.

For generating API controllers run
```
dotnet-generate api
```

-----
## Installation for local build

If you want to make this tool better,
then you can make local releases like this:

1. Fork/Clone this project.
2. Navigate to project dir.
3. Edit the code.
4. Install the CLI tool. `pip3 install --editable .`
5. Check that tool is installed `dotnet-generate --help`
6. If everything works, make new pull request?


## Built with

- [Click](https://github.com/pallets/click)
