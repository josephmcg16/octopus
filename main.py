from yaml import safe_load
from octopus import OctopusEnergyAPI


if __name__ == "__main__":
    with open("config.yaml", encoding="utf-8") as file:
        config = safe_load(file)

    octopus = OctopusEnergyAPI(
        config["api_key"],
        config["electricity_meterpoint_mpan"],
        config["electricity_serial_number"],
        config["gas_meterpoint_mpan"],
        config["gas_serial_number"],
    )
    octopus.get_electricity_consumption()
    octopus.get_gas_consumption()

    fig_electricity = octopus.px_bar("electricity")
    fig_gas = octopus.px_bar("gas")
    fig_electricity.show()
    fig_gas.show()
