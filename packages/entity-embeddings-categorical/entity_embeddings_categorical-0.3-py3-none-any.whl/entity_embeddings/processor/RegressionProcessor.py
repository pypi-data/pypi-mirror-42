from typing import List

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from entity_embeddings.processor.BaseProcessor import TargetProcessor


class RegressionProcessor(TargetProcessor):
    def process_target(self, y: List) -> np.ndarray:
        return MinMaxScaler().fit_transform(pd.DataFrame(y))
