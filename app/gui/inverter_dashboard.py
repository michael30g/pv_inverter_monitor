import tkinter as tk
from pathlib import Path
from devices.inverter_manager import InverterManager
from devices.inverter_factory import InverterFactory


class InverterDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PV Inverter Monitor")
        self.geometry("420x250")

        config_path = Path(__file__).parents[1] / "config" / "inverter_map.json"

        self.factory = InverterFactory(config_path)
        self.manager = InverterManager(self.factory.config["register_map"])

        for inv in self.factory.config["inverters"]:
            inverter = self.factory.create_inverter(inv)
            self.manager.add_inverter(inv["id"], inverter)

        self.labels = {}
        self._build_ui()
        self._update_data()

    def _build_ui(self):
        row = 0
        for inv_id in self.manager.inverters.keys():
            label = tk.Label(self, text="", font=("Consolas", 10), anchor="w")
            label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
            self.labels[inv_id] = label
            row += 1

    def _update_data(self):
        data = self.manager.get_snapshot()

        for inv_id, values in data.items():
            if "error" in values:
                text = f"Inverter {inv_id}: ERROR"
                color = "red"
            else:
                state = values["inverter_state"]
                color = "green" if state == "ON" else "orange" if state == "OFF" else "red"

                text = (
                    f"Inverter {inv_id} | "
                    f"P={values['power_w']} W | "
                    f"Vbat={values['battery_voltage']} V | "
                    f"Ibat={values['battery_current']} A | "
                    f"State={state}"
                )

            self.labels[inv_id].config(text=text, fg=color)

        self.after(2000, self._update_data)


if __name__ == "__main__":
    app = InverterDashboard()
    app.mainloop()
