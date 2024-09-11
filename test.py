import apache_beam
import weatherbench2
import xarray as xr
from weatherbench2 import config
from weatherbench2.metrics import SpatialMSE, MSE, MADp, SpatialMAE
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

# the merging messes up with spatially-averaged measurements and time-averaged ones.
# particularly, MSE vector (lead_time,) is repeated (init_time,) times to match
# the dimension of SpatialMSE.
# it is better to consider two separate datasets to avoid confusion.
eval_configs = {
  'deterministic': config.Eval(
      metrics={
          'madp' : MADp(),
          'mae' : SpatialMAE()
      },
  )}

evaluate_in_memory(data_config, eval_configs)   # Takes around 5 minutes
