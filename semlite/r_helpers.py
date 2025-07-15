import os
import pandas as pd
import tempfile
import subprocess

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

        # 🔧 Redireciona stdout/stderr para arquivos para evitar [WinError 6]
        stdout_path = os.path.join(tmpdir, "stdout.txt")
        stderr_path = os.path.join(tmpdir, "stderr.txt")

        with open(stdout_path, "w") as out, open(stderr_path, "w") as err:
            result = subprocess.call(cmd, stdout=out, stderr=err)

        if result != 0:
            with open(stderr_path, "r", encoding="utf-8") as errf:
                raise RuntimeError(f"Erro ao rodar Rscript:\n{errf.read()}")

        estimates = pd.read_csv(os.path.join(tmpdir, "estimates.csv"))
        indices = pd.read_csv(os.path.join(tmpdir, "indices.csv")).set_index("metric")["value"].to_dict()
        with open(os.path.join(tmpdir, "summary.txt"), encoding="utf-8") as f:
            summary = f.read()

        return {
            "indices": indices,
            "estimates": estimates,
            "summary": summary
        }
