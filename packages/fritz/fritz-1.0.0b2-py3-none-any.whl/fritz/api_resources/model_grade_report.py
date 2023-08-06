"""
fritz.api_resources.model_grade_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
from termcolor import colored

import fritz
from fritz.api_resources import fritz_object
from fritz.api_client import FritzClient


class ModelGradeReport(fritz_object.FritzObject):
    """Model Benchmark report."""

    OBJECT_NAME = "ModelGradeReport"

    @classmethod
    def get(cls, version_uid, api_key=None):
        """Get model grade report for version_uid

        Args:
            version_uid (str): UID of ModelVersion
            api_key (str): Optional API Key

        Returns: ModelGradeReport if report has succeeded.
        """
        url = "/model/version/{version_uid}/grader".format(
            version_uid=version_uid
        )

        client = FritzClient(api_key or fritz.api_key)
        response = client.get(url)
        return fritz.utils.convert_to_fritz_object(response)

    def summary(self):
        """Print summary of model grade report."""
        if self.fail_at:
            self._error_summary()
            return

        self.layer_summary()

        stats = []
        # Check Core ML Compatibility
        incompatible_layers = [
            layer
            for layer in self.layers
            if not layer["is_coremltools_compatible"]
        ]
        compatible = len(incompatible_layers) == 0
        color = "green" if compatible else "red"
        stats.append(("Core ML Compatible", colored(str(compatible), color)))

        # Calculate Predicted Runtime
        if self.predicted_runtime < 1.0:
            runtime = f"{self.predicted_runtime * 1000:.1f} ms"
        else:
            runtime = f"{self.predicted_runtime:.3}s"

        runtime = f"{runtime} ({1 / self.predicted_runtime:,.1f} fps)"
        stats.append(("Predicted Runtime (iPhone X)", runtime))

        # FLOPS, Parameters, Version UID.
        stats.append(("Total MFLOPS", f"{self.total_flops / 1.0e6:,.2f}"))
        stats.append(("Total Parameters", f"{self.total_parameters:,d}"))
        stats.append(("Fritz Version ID", self.version_uid))

        max_title_length = max(len(title) for title, _ in stats)
        summary_str = "Fritz Model Grade Report"
        print("\n" + "-" * len(summary_str))
        print(summary_str)
        print("-" * len(summary_str) + "\n")
        for title, value in stats:
            title = title + ":"
            format_str = "{title:%s}{value}" % str(max_title_length + 5)
            print(format_str.format(title=title, value=value))

    def layer_summary(self):
        """Print summary of layers from report."""
        summary_str = "Model Layer Summary"
        print("\n" + "-" * len(summary_str))
        print(summary_str)
        print("-" * len(summary_str) + "\n")

        layers = [
            (
                "Layer (type)",
                "Output Shape",
                "MFLOPS",
                "Weights",
                "Core ML Compatible",
            )
        ]
        layers.extend(self._summarize_layer(layer) for layer in self.layers)
        max_lengths = [
            max(len(value) for value in values) for values in zip(*layers)
        ]
        for i, fields in enumerate(layers):
            line = []
            for j, field in enumerate(fields):
                format_str = "{value:%s}" % str(max_lengths[j] + 5)
                line.append(format_str.format(value=field))

            line_length = len("".join(line))

            if i == 0:
                print("-" * line_length)
                print("".join(line))
                print("=" * line_length)
            else:
                print("".join(line))
                print("-" * line_length)

    @staticmethod
    def _summarize_layer(layer):
        layer_type = f"{layer['name']} ({layer['layer_cls_name']})"
        output_shape = f"{layer['output_shape']}"
        mflops = f"{layer['flops'] / 1.0e6:,.2f}"
        weights = f"{layer['num_weights']:,d}"
        color = "green" if layer["is_coremltools_compatible"] else "red"
        compatible = colored(layer["is_coremltools_compatible"], color)

        return (layer_type, output_shape, mflops, weights, compatible)

    def _error_summary(self):
        message = "Model Grade Report Failed"
        print(colored(message, "red"))
        print(colored("-" * len(message), "red"))
        print(f"Error Message: {self.error_message}")
