from collections import defaultdict,deque
from dataclasses import dataclass
from math import isfinite,sqrt

@dataclass
class MetricObservation:
    timestamp:str
    service:str
    metric:str
    value:float

@dataclass
class DetectionResult:
    observation:MetricObservation
    baseline_mean:float
    baseline_std:float
    z_score: float
    is_anomaly:bool

class StatisticalDetector:
    def __init__(self,window_size:int=10,z_threshold:float=3.0,min_samples:int=5,):
        self.window_size=window_size
        self.z_threshold=z_threshold
        self.min_samples=min_samples
        self.history=defaultdict(lambda:deque(maxlen=window_size))
    def observe(self,observation:MetricObservation)->DetectionResult | None:
        if not isfinite(observation.value):
            raise (ValueError("Metric value miust be finite"))
        key=(observation.service,observation.metric)
        previous=self.history[key]
        if len(previous) < self.min_samples:
            previous.append(observation.value)
            return None
        mean=sum(previous)/len(previous)
        variance=sum((value-mean)**2 for value in previous)/len(previous)
        std=sqrt(variance)
        if std ==0:
            z_score=(0.0 if observation.value==mean else float("inf"))
        else:
            z_score=(observation.value-mean)/std
        result=DetectionResult(observation=observation,baseline_mean=mean,baseline_std=std,z_score=z_score,is_anomaly=z_score>self.z_threshold,)
        if not result.is_anomaly:
            previous.append(observation)
        return result