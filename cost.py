def estimate_roi(total_kw, cost_per_watt, electricity_rate, sunlight_hours):
    total_cost = total_kw * 1000 * cost_per_watt  # convert kW to W

    annual_output_kwh = total_kw * sunlight_hours * 365

    annual_savings = annual_output_kwh * electricity_rate

    payback_years = round(total_cost / annual_savings, 2) if annual_savings > 0 else None

    return {
        "installation_cost": int(total_cost),
        "annual_output_kwh": int(annual_output_kwh),
        "annual_savings": int(annual_savings),
        "payback_years": payback_years
    }
