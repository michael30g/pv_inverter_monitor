import tkinter as tk
from tkinter import ttk

from devices.inverter_manager import InverterManager
from devices.inverter_factory import InverterFactory
from pathlib import Path


class InverterDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PV Inverter Monitor")
        self.geometry("400x300")

        # ---- Backend ----
        config_path = Path(__file__).parent.parent / "config" / "inverter_map.json"
        factory = InverterFactory(config_path)

        self.manager = InverterManager()

        for inv in factory.config["inverters"]:
            inverter = factory.create_inverter(inv)
            self.manager.add_inverter(inv["id"], inverter)

        # ---- UI ----
        self.labels = {}
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        for inv in factory.config["inverters"]:
            inv_id = inv["id"]

            label = ttk.Label(
                container,
                text=f"Inverter {inv_id}\nWaiting...",
                relief="solid",
                padding=10
            )
            label.pack(fill="x", pady=5)

            self.labels[inv_id] = label

        # Start update loop
        self._update_data()

    def _update_data(self):
        data = self.manager.get_snapshot()

        for inv_id, values in data.items():
            if "error" in values:
                text = f"Inverter {inv_id}\nERROR: {values['error']}"
            else:
                state_map = {
                    0: "OFF",
                    1: "ON",
                    2: "FAULT"
                }

                state_txt = state_map.get(values["state"], "UNKNOWN")

                text = (
                    f"Inverter {inv_id}\n"
                    f"Power: {values['power_w']} W\n"
                    f"Battery V: {values['battery_voltage_v']} V\n"
                    f"Battery I: {values['battery_current_a']} A\n"
                    f"State: {state_txt}"
                )

            self.labels[inv_id].config(text=text)

        # refresh every 2 seconds
        self.after(2000, self._update_data)


if __name__ == "__main__":
    app = InverterDashboard()
    app.mainloop()

