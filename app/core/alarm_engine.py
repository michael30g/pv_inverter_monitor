from core.logger import get_logger


class AlarmEngine:
    def __init__(self, limits: dict):
        self.limits = limits
        self.logger = get_logger("AlarmEngine")

    def evaluate(self, parsed_data: dict) -> dict:
        """
        parsed_data:
        {
          inverter_id: {
            signal: { value, unit }
          }
        }
        """

        alarms = {}

        for inv_id, signals in parsed_data.items():
            alarms[inv_id] = []

            for signal, info in signals.items():
                if signal not in self.limits:
                    continue

                limits_cfg = self.limits[signal]
                value = info["value"]

                # Estado tipo enum (FAULT, ON, OFF)
                if isinstance(value, str):
                    state_cfg = limits_cfg.get(value)
                    if state_cfg:
                        alarms[inv_id].append({
                            "signal": signal,
                            "value": value,
                            "severity": state_cfg["severity"]
                        })
                        self.logger.warning(
                            f"Inverter {inv_id} | {signal}={value} "
                            f"({state_cfg['severity']})"
                        )
                    continue

                # Valores numéricos
                min_v = limits_cfg.get("min")
                max_v = limits_cfg.get("max")

                if min_v is not None and value < min_v:
                    alarms[inv_id].append({
                        "signal": signal,
                        "value": value,
                        "limit": min_v,
                        "type": "LOW",
                        "severity": limits_cfg["severity"]
                    })
                    self.logger.warning(
                        f"Inverter {inv_id} | {signal} LOW: {value}"
                    )

                if max_v is not None and value > max_v:
                    alarms[inv_id].append({
                        "signal": signal,
                        "value": value,
                        "limit": max_v,
                        "type": "HIGH",
                        "severity": limits_cfg["severity"]
                    })
                    self.logger.warning(
                        f"Inverter {inv_id} | {signal} HIGH: {value}"
                    )

        return alarms
