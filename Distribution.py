from typing import Callable, Union, Any
from scipy import stats
import numpy as np

class Distribution:
    def __init__(self, data: Union[list, np.ndarray]) -> None:
        self.kde = self._generate_kde(data) 
        
    def __call__(self, *args, **kwrds) -> Callable[[Any], np.ndarray]:
        return self.kde(*args, **kwrds)
        
    @staticmethod
    def _generate_kde(
                        data: Union[list, np.ndarray]
                      ) -> Callable[[Any], np.ndarray]:
        return stats.gaussian_kde(data.astype(float))
    
    def sample_data(self, size: int) -> list:
        samples = self.kde.resample(size)[0]
        samples[samples < 0] = 0
        return [sample // 1 for sample in samples]