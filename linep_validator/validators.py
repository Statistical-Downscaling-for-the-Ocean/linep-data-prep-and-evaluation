import warnings


def validate_dims(ds, expected_dims, *, name="dataset", raise_error=True):
    actual_dims = dict(ds.sizes)

    missing = {d: expected_dims[d] for d in expected_dims if d not in actual_dims}
    unexpected = {d: actual_dims[d] for d in actual_dims if d not in expected_dims}
    size_mismatches = {
        d: (actual_dims[d], expected_dims[d])
        for d in expected_dims
        if d in actual_dims and actual_dims[d] != expected_dims[d]
    }

    identical = not missing and not unexpected and not size_mismatches

    if raise_error and not identical:
        lines = [f"Dimension mismatch in {name}:"]
        if missing:
            lines.append("  ❌ Missing expected dimensions:")
            lines.extend(f"      - {d}: expected {sz}" for d, sz in missing.items())
        if unexpected:
            lines.append("  ❌ Unexpected dimensions present:")
            lines.extend(f"      - {d}: actual {sz}" for d, sz in unexpected.items())
        if size_mismatches:
            lines.append("  ❌ Incorrect dimension sizes:")
            lines.extend(
                f"      - {d}: actual {a}, expected {e}"
                for d, (a, e) in size_mismatches.items()
            )
        raise ValueError("\n".join(lines))

    print(f"Dimension validation: {'✅ PASSED' if identical else '❌ FAILED'}")
    return {
        "missing_dims": missing,
        "unexpected_dims": unexpected,
        "size_mismatches": size_mismatches,
        "identical": identical,
    }


def validate_vars(
    ds, required_vars=None, *, alternative_groups=None, name="dataset", raise_error=True
):
    required_vars = required_vars or []
    alternative_groups = alternative_groups or []
    ds_vars = set(ds.data_vars)

    missing_vars = [v for v in required_vars if v not in ds_vars]
    missing_groups = [
        group for group in alternative_groups if all(v not in ds_vars for v in group)
    ]

    identical = not missing_vars and not missing_groups

    if raise_error and not identical:
        lines = [f"Variable validation failed for {name}:"]
        if missing_vars:
            lines.append("  ❌ Missing required variables:")
            lines.extend(f"      - {v}" for v in missing_vars)
        if missing_groups:
            lines.append("  ❌ Missing one of the required alternatives:")
            lines.extend("      - One of: " + ", ".join(g) for g in missing_groups)
        raise ValueError("\n".join(lines))

    print(f"Variable validation: {'✅ PASSED' if identical else '❌ FAILED'}")
    return {
        "missing_vars": missing_vars,
        "missing_groups": missing_groups,
        "identical": identical,
    }


def validate_coords(ds, required_coords=None, *, name="dataset", raise_error=True):
    required_coords = required_coords or {}

    missing = []
    wrong_dim = {}

    for coord, expected_dim in required_coords.items():
        if coord not in ds.coords:
            missing.append(coord)
            continue

        dims = ds[coord].dims
        if len(dims) != 1 or dims[0] != expected_dim:
            wrong_dim[coord] = {"actual": dims, "expected": (expected_dim,)}

    identical = not missing and not wrong_dim

    if raise_error and not identical:
        lines = [f"Coordinate validation failed for {name}:"]
        if missing:
            lines.append("  ❌ Missing coordinates:")
            lines.extend(f"      - {c}" for c in missing)
        if wrong_dim:
            lines.append("  ❌ Incorrect coordinate dimension(s):")
            lines.extend(
                f"      - {c}: actual {d['actual']} expected {d['expected']}"
                for c, d in wrong_dim.items()
            )
        raise ValueError("\n".join(lines))

    print(f"Coordinate validation: {'✅ PASSED' if identical else '❌ FAILED'}")
    return {
        "missing_coords": missing,
        "wrong_dim_coords": wrong_dim,
        "identical": identical,
    }


def validate_units(ds, expected_units):
    for var, acceptable in expected_units.items():
        if var not in ds.variables:
            continue

        actual = ds[var].attrs.get("units")

        if actual is None:
            print(f"⚠️ [units] '{var}' missing units (expected {acceptable})")
            continue

        actual_norm = actual.lower()
        acceptable_norm = [u.lower() for u in acceptable]

        if actual_norm not in acceptable_norm:
            print(f"⚠️ [units] {var} has '{actual}', expected one of {acceptable}")
