import subprocess
import os
import pandas as pd
import tempfile

R_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "lavaan_runner.R")

def run_lavaan_sem(model_desc, df, estimator="WLSMV", ordered_vars=None):
    if not os.path.isfile(R_SCRIPT_PATH):
        raise FileNotFoundError(f"⚠️ Arquivo lavaan_runner.R não encontrado em: {R_SCRIPT_PATH}")

    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "modelo.txt")
        data_path = os.path.join(tmpdir, "dados.csv")
        output_path = tmpdir
        log_path = os.path.join(tmpdir, "lavaan_error.log")

        df.to_csv(data_path, index=False)

        with open(model_path, "w", encoding="utf-8") as f:
            f.write(model_desc)

        cmd = ["Rscript", R_SCRIPT_PATH, output_path, estimator]
        if ordered_vars:
            cmd.append(",".join(ordered_vars))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            error_log = f"\n📤 STDOUT:\n{e.stdout}\n\n📥 STDERR:\n{e.stderr}\n"
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(error_log)
            raise RuntimeError(f"Erro ao rodar Rscript:{error_log}\n📄 LOG {log_path}:\n")

        estimates = pd.read_csv(os.path.join(tmpdir, "estimates.csv"))
        indices = pd.read_csv(os.path.join(tmpdir, "indices.csv")).set_index("metric")["value"].to_dict()
        with open(os.path.join(tmpdir, "summary.txt"), encoding="utf-8") as f:
            summary = f.read()

        return {
            "indices": indices,
            "estimates": estimates,
            "summary": summary.splitlines()
        }
