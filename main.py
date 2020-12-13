from rich.console import Console
from rich.table import Table

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

# `magi [OPTIONS] <number>
# `magi 200`
# `magi 0xEF` or `magi -hex EF`  (0b, 0o, 0x)
# `magi --base=22 44` for giving a base 44 number
from bases import bases


def main():
    given = 'AA'
    base_key = 'hex'  # --hex, -0x or --base=15

    if base_key is None:
        for _, base in bases.items():
            if not base.can_be_inferred():
                continue

            inferred = base.is_inferred(given)
            valid = base.is_valid(given)

            if inferred:
                if valid:
                    base_key = base.key()
                    break
                else:
                    print(f"Looks like a `{base.key()}`, but does not seem to be valid")
                    break

    # todo: try and parse that value
    value = bases[base_key].parse(given)
    value.is_given = True

    # todo: do all conversions from `Base` that was parsed
    conversions = []
    for _, base in bases.items():
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
        console.print(value.display(console))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
