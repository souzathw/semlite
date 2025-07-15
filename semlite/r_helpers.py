import subprocess
import os
import pandas as pd
import tempfile

def run_lavaan_sem(model_desc, df, estimator="WLSMV", ordered_vars=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "modelo.txt")
        data_path = os.path.join(tmpdir, "dados.csv")
        output_path = tmpdir

        df.to_csv(data_path, index=False)

        with open(model_path, "w", encoding="utf-8") as f:
            f.write(model_desc)

        r_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "lavaan_runner.R"))

        cmd = ["Rscript", r_script_path, output_path, estimator]
        if ordered_vars:
            cmd.append(",".join(ordered_vars))

        subprocess.run(cmd, check=True)

        estimates = pd.read_csv(os.path.join(tmpdir, "estimates.csv"))
        indices = pd.read_csv(os.path.join(tmpdir, "indices.csv")).set_index("metric")["value"].to_dict()
        with open(os.path.join(tmpdir, "summary.txt"), encoding="utf-8") as f:
            summary = f.read()

        return {
            "indices": indices,
            "estimates": estimates,
            "summary": summary
        }
