import apache_beam
import weatherbench2
import xarray as xr
from weatherbench2 import config
from weatherbench2.metrics import SpatialMSE
from weatherbench2.evaluation import evaluate_in_memory, evaluate_with_beam

forecast_path = '/data01/benassi/wavegraph/wavegraph/swh/long_run_48_16/preds_2022_96h_new.zarr'
obs_path = '/data01/benassi/wavegraph/data-adriatic/processed_training_set/6years/zarr/mesh_data_2022.zarr'

paths = config.Paths(
    forecast=forecast_path,
    obs=obs_path,
    output_dir='./',   # Directory to save evaluation results
)

selection = config.Selection(
    variables=[
        'swh'
    ],
    levels=[],
    time_slice=slice('2022-01-01', '2022-12-31'),
)

data_config = config.Data(selection=selection, 
                          paths=paths,
                          rename_variables={
                                            'deltat' : 'prediction_timedelta'})

eval_configs = {
  'deterministic': config.Eval(
      metrics={
          'mse': SpatialMSE(), 
      },
  )}

evaluate_in_memory(data_config, eval_configs)   # Takes around 5 minutes
