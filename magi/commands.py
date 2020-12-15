import click
from rich.console import Console
from rich.table import Table

# `magi [OPTIONS] <number>
# `magi 200`
# `magi 0xEF` or `magi -hex EF`  (0b, 0o, 0x)
# `magi --base=22 44` for giving a base 44 number
import magi.numbers as nbrs  # todo: better name


# todo: give random number quote
# `--no bin,hex` to exclude
# `--only bini,dec` to show only
# todo: Save configurations to add commands `magi -f mw 200` => magi --only=bin,hex --binary-index=no 200`
# magi save-format
# todo: choose Endiness
# todo: Split into bytes
# todo: binary into groups
# todo: calculator
# todo: logical operations (shift, &, |)
# todo: themes
# todo: arbitrary bases
# todo: list bases with notes
# todo: teach `magi --list`
# todo: magi --teach all
# todo: magi --teach hex,bin
# todo: `magi --steps 200`  # Show the conversion steps
# todo: add negative encodings
# todo: Allow context to be given to the bases
# todo: allow expressions `magi '200 + 3'` or magi '10001 << 5' or magi '0x4A | 0xB2'
# todo: maybe allow 0[3]13 vor base 3


@click.command()
@click.option('--base', default=None, help='base of the given value')
@click.argument('value')
def main(base, value):
    if base is None:
        for _, base in nbrs.bases.items():  # todo: rename this item and better export
            if not base.can_be_inferred():
                continue

            inferred = base.is_inferred(value)
            valid = base.is_valid(value)

            if inferred:
                if valid:
                    base = base.key()
                    break
                else:
                    print(f"Looks like a `{base.key()}`, but does not seem to be valid")
                    break

    # todo: try and parse that value
    value = nbrs.bases[base].parse(value)
    value.is_given = True

    # todo: do all conversions from `Base` that was parsed
    conversions = []
    for _, base in nbrs.bases.items():
        if base.key() == value.key():
            conversions.append(value)
            continue

        conversions.append(
            base.parse(
                value.as_decimal()
            )
        )

    console = Console()

    # Print the Primary Table
    table = Table(
        title="Formatted Number Conversions",
        show_lines=True
    )

    table.add_column("Title", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    independent_displays = []
    for value in conversions:
        if value.show_in_table():
            table.add_row(value.title(), value.display())
        else:
            independent_displays.append(value)

    console.print(table)

    # Print any others
    for value in independent_displays:
        console.print(value.title())
        value.display(console)
