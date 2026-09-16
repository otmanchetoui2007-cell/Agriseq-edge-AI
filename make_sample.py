import os
import pod5
import numpy as np
from uuid import uuid4

out_path = os.path.join("real_pod5", "sample.pod5")

if os.path.exists(out_path):
    os.remove(out_path)

os.makedirs("real_pod5", exist_ok=True)

run_info = pod5.RunInfo(
    adc_max=2047,
    adc_min=-2048,
    context_tags={},
    experiment_name="demo",
    flow_cell_id="FA10000",
    flow_cell_product_code="FLO-MIN106",
    protocol_name="demo_protocol",
    protocol_run_id="run_1",
    protocol_start_time=0,
    sample_id="sample_1",
    sequencing_kit="SQK-LSK109",
    sequencer_position="1A",
    sequencer_position_type="MinION",
    software="MinKNOW",
    system_name="MinION",
    tracking_id={},
    acquisition_id="demo",
    acquisition_start_time=0,
    sample_rate=4000,
    system_type="MinION"
)

pore = pod5.Pore(channel=1, well=1, pore_type="r10.4.1")
calibration = pod5.Calibration(offset=0.0, scale=1.0)
end_reason = pod5.EndReason(reason=pod5.EndReasonEnum.SIGNAL_POSITIVE, forced=False)

# Signal synthétique de 10 000 échantillons
signal = (np.random.randn(10000) * 8 + 85).astype(np.int16)

read = pod5.Read(
    read_id=uuid4(),
    read_number=1,
    start_sample=0,
    median_before=0.0,
    end_reason=end_reason,
    calibration=calibration,
    pore=pore,
    run_info=run_info,
    signal=signal
)

with pod5.Writer(out_path) as writer:
    writer.add_read(read)

print("Fichier sample.pod5 régénéré avec succès !")
