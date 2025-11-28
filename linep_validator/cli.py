import click
import xarray as xr
from .config import load_config
from .validators import (
    validate_dims,
    validate_vars,
    validate_coords,
    validate_units,
)
from tabulate import tabulate


# Add a main group option for dataset type
@click.group()
@click.option(
    "--dataset-type",
    type=click.Choice(["ctd", "bgc", "stretch"], case_sensitive=False),
    default="ctd",
    help="Specify which dataset type to validate (default: ctd).",
)
@click.pass_context
def main(ctx, dataset_type):
    """LineP dataset validator CLI."""
    # Store dataset_type in context so subcommands can access it
    ctx.obj = {"dataset_type": dataset_type}


def get_config(ctx):
    """Helper to select the correct config file based on dataset type."""
    dataset_type = ctx.obj.get("dataset_type", "CTD")
    config_file = f"config_{dataset_type}.yaml"
    return load_config(config_file)


@main.command()
@click.argument("dataset", type=click.Path(exists=True))
@click.pass_context
def validate(ctx, dataset):
    """Validate a dataset against the built-in schema."""
    click.echo(f"📦 Loading dataset: {dataset}")
    ds = xr.open_dataset(dataset)

    cfg = get_config(ctx)
    click.echo(f"🔍 Running validators using {ctx.obj['dataset_type']} schema...")

    validate_dims(ds, cfg["correct_dimensions"])
    validate_vars(
        ds,
        cfg["required_vars"],
        alternative_groups=cfg.get("alternative_groups", []),
    )
    validate_coords(ds, cfg["required_coords"])
    validate_units(ds, cfg["expected_units"])

    click.echo("\n🎉 Validation complete.")


@main.command()
@click.pass_context
def schema(ctx):
    """Show the expected schema for the LineP dataset."""
    cfg = get_config(ctx)
    dataset_type = ctx.obj["dataset_type"]
    click.echo(f"LineP {dataset_type} Dataset Schema:\n")

    # Dimensions
    dims_table = list(cfg.get("correct_dimensions", {}).items())
    click.echo("Expected Dimensions:")
    click.echo(tabulate(dims_table, headers=["Dimension", "Size"], tablefmt="github"))
    click.echo("")

    # Required Variables
    vars_table = [(v,) for v in cfg.get("required_vars", [])]
    click.echo("Required Variables:")
    click.echo(tabulate(vars_table, headers=["Variable"], tablefmt="github"))
    click.echo("")

    # Alternative Groups
    # Alternative Groups
    alt_table = [[", ".join(group)] for group in cfg.get("alternative_groups", [])]
    click.echo("Alternative Variable Groups:")
    click.echo(tabulate(alt_table, headers=["Group"], tablefmt="github"))
    click.echo("")

    # Coordinates
    coords_table = list(cfg.get("required_coords", {}).items())
    click.echo("Required Coordinates:")
    click.echo(
        tabulate(
            coords_table,
            headers=["Coordinate", "Expected Dimension"],
            tablefmt="github",
        )
    )
    click.echo("")

    # Units
    units_table = [
        (var, ", ".join(units)) for var, units in cfg.get("expected_units", {}).items()
    ]
    click.echo("Expected Units:")
    click.echo(
        tabulate(
            units_table,
            headers=["Variable / Coord", "Accepted Units"],
            tablefmt="github",
        )
    )
    click.echo("")


if __name__ == "__main__":
    main()
