def generate_summary(data):
    prompt = f"""
You are a solar energy assistant. Summarize the following technical data into a user-friendly solar recommendation:

- Rooftop Area: {data['area']} m²
- Number of Panels: {data['panels']}
- Panel Wattage: {data['panel_wattage']} W
- Estimated System Size: {data['system_kw']} kW
- Installation Cost: ₹{data['installation_cost']}
- Annual Output: {data['annual_output']} kWh
- Annual Savings: ₹{data['annual_savings']}
- Payback Period: {data['payback_years']} years

Make suggestions about panel types, cleaning tips, and government subsidy options. Write in 4-5 lines.
"""
    return prompt
