import requests
import pandas as pd
import plotly.express


class OctopusEnergyAPI:
    def __init__(
        self,
        api_key,
        electricity_meterpoint_mpan,
        electricity_serial_number,
        gas_meterpoint_mpan,
        gas_serial_number,
    ):
        self.api_key = api_key
        self.electricity_meterpoint_mpan = electricity_meterpoint_mpan
        self.electricity_serial_number = electricity_serial_number
        self.gas_meterpoint_mpan = gas_meterpoint_mpan
        self.gas_serial_number = gas_serial_number

    def get_electricity_consumption(self):
        url = f"https://api.octopus.energy/v1/electricity-meter-points/{self.electricity_meterpoint_mpan}/meters/{self.electricity_serial_number}/consumption/"
        electricity_consumption = pd.DataFrame()
        for page in range(1, 99):
            response = requests.get(url=f"{url}?page={page}", auth=(self.api_key, ""))
            output_dict = response.json()
            if "detail" in output_dict:
                break
            electricity_consumption = pd.concat(
                [electricity_consumption, pd.DataFrame(output_dict["results"])]
            )
        electricity_consumption["interval_start"] = pd.to_datetime(
            electricity_consumption["interval_start"]
        )
        electricity_consumption["interval_end"] = pd.to_datetime(
            electricity_consumption["interval_end"]
        )
        electricity_consumption_by_day = (
            electricity_consumption.groupby(
                electricity_consumption["interval_start"].dt.date
            )["consumption"]
            .mean()
            .reset_index()
        )

        self.electricity_consumption = electricity_consumption
        self.electricity_consumption_by_day = electricity_consumption_by_day
        return electricity_consumption, electricity_consumption_by_day

    def get_gas_consumption(self):
        url = f"https://api.octopus.energy/v1/gas-meter-points/{self.gas_meterpoint_mpan}/meters/{self.gas_serial_number}/consumption/"
        gas_consumption = pd.DataFrame()
        for page in range(1, 99):
            response = requests.get(url=f"{url}?page={page}", auth=(self.api_key, ""))
            output_dict = response.json()
            if "detail" in output_dict:
                if output_dict["detail"] != "Invalid page.":
                    raise ValueError(output_dict["detail"])
                break
            gas_consumption = pd.concat(
                [gas_consumption, pd.DataFrame(output_dict["results"])]
            )
        gas_consumption["interval_start"] = pd.to_datetime(
            gas_consumption["interval_start"]
        )
        gas_consumption["interval_end"] = pd.to_datetime(
            gas_consumption["interval_end"]
        )
        gas_consumption_by_day = (
            gas_consumption.groupby(gas_consumption["interval_start"].dt.date)[
                "consumption"
            ]
            .mean()
            .reset_index()
        )

        self.gas_consumption = gas_consumption
        self.gas_consumption_by_day = gas_consumption_by_day
        return gas_consumption, gas_consumption_by_day

    def px_bar(self, energy_type: str):
        if energy_type == "electricity":
            title = f"{self.electricity_serial_number} Electricity Consumption"
            data_to_plot = self.electricity_consumption_by_day
        elif energy_type == "gas":
            title = f"{self.gas_serial_number} Gas Consumption"
            data_to_plot = self.gas_consumption_by_day
        else:
            raise ValueError("energy_type must be one of:\n['electricity', 'gas']")
        fig = plotly.express.bar(
            data_to_plot,
            x="interval_start",
            y="consumption",
            title=title,
        )
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Consumption (kWh)")
        return fig
