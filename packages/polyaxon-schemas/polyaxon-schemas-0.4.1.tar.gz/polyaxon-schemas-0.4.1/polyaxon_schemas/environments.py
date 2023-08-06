# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.utils import UUID, FloatOrStr, IntOrStr, NotebookBackend


class TensorflowClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    ps = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowClusterConfig


class TensorflowClusterConfig(BaseConfig):
    """
    Tensorflow cluster config.

    Args:
        master: list(str). The list of master host in a tensorflow cluster.
        worker: list(str). The list of worker host in a tensorflow cluster.
        ps: list(str). The list of ps host in a tensorflow cluster.
    """
    IDENTIFIER = 'tensorflow_cluster'
    SCHEMA = TensorflowClusterSchema

    def __init__(self, master=None, worker=None, ps=None):
        self.master = master
        self.worker = worker
        self.ps = ps


class HorovodClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return HorovodClusterConfig


class HorovodClusterConfig(BaseConfig):
    """
    Horovod cluster config.

    Args:
        master: list(str). The list of master host in a Horovod cluster.
        worker: list(str). The list of worker host in a Horovod cluster.
    """
    IDENTIFIER = 'horovod_cluster'
    SCHEMA = HorovodClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class PytorchClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return PytorchClusterConfig


class PytorchClusterConfig(BaseConfig):
    """
    Pytorch cluster config.

    Args:
        master: list(str). The list of master host in a Pytorch cluster.
        worker: list(str). The list of worker host in a Pytorch cluster.
    """
    IDENTIFIER = 'pytorch_cluster'
    SCHEMA = PytorchClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class MXNetClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    server = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return MXNetClusterConfig


class MXNetClusterConfig(BaseConfig):
    """
    MXNet cluster config.

    Args:
        master: list(str). The list of master host in a tensorflow cluster.
        worker: list(str). The list of worker host in a tensorflow cluster.
        server: list(str). The list of server host in a tensorflow cluster.
    """
    IDENTIFIER = 'mxnet_cluster'
    SCHEMA = MXNetClusterSchema

    def __init__(self, master=None, worker=None, server=None):
        self.master = master
        self.worker = worker
        self.server = server


class K8SResourcesEntrySchema(BaseSchema):
    cpu = FloatOrStr(allow_none=True)
    memory = IntOrStr(allow_none=True)
    gpu = fields.Int(allow_none=True)
    tpu = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return K8SResourcesEntryConfig


class K8SResourcesEntryConfig(BaseConfig):
    SCHEMA = K8SResourcesEntrySchema
    REDUCED_ATTRIBUTES = ['cpu', 'memory', 'gpu', 'tpu']

    def __init__(self, cpu=None, memory=None, gpu=None, tpu=None):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.tpu = tpu


class K8SContainerResourcesSchema(BaseSchema):
    limits = fields.Nested(K8SResourcesEntrySchema, allow_none=True)
    requests = fields.Nested(K8SResourcesEntrySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return K8SContainerResourcesConfig


class K8SContainerResourcesConfig(BaseConfig):
    """
    K8S container resources config.

    Args:
        limits: `K8SResourcesEntry`.
        requests: `K8SResourcesEntry`.
    """
    IDENTIFIER = 'resources'
    SCHEMA = K8SContainerResourcesSchema
    REDUCED_ATTRIBUTES = ['limits', 'requests']

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests


class K8SResourcesSchema(BaseSchema):
    limits = fields.Float(allow_none=True)
    requests = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return K8SResourcesConfig


class K8SResourcesConfig(BaseConfig):
    """
    K8S resources config.

    Args:
        limits: `float`.
        requests: `float`.
    """
    IDENTIFIER = 'resources'
    SCHEMA = K8SResourcesSchema

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests

    def __add__(self, other):
        if not other:
            return self

        if self.requests:
            if other.requests:
                self.requests += other.requests
        elif other.requests:
            self.requests = other.requests

        if self.limits:
            if other.limits:
                self.limits += other.limits
        elif other.limits:
            self.limits = other.limits

        return self


class PodResourcesSchema(BaseSchema):
    cpu = fields.Nested(K8SResourcesSchema, allow_none=True)
    memory = fields.Nested(K8SResourcesSchema, allow_none=True)
    gpu = fields.Nested(K8SResourcesSchema, allow_none=True)
    tpu = fields.Nested(K8SResourcesSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return PodResourcesConfig


class PodResourcesConfig(BaseConfig):
    """
    Pod resources config.

    Args:
        cpu: `K8SResourcesConfig`.
        memory: `K8SResourcesConfig`.
        gpu: `K8SResourcesConfig`.
        tpu: `K8SResourcesConfig`.
    """
    IDENTIFIER = 'pod_resources'
    SCHEMA = PodResourcesSchema

    def __init__(self, cpu=None, memory=None, gpu=None, tpu=None):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.tpu = tpu

    def __add__(self, other):
        if not other:
            return self

        if self.cpu:
            if other.cpu:
                self.cpu += other.cpu
        elif other.cpu:
            self.cpu = K8SResourcesConfig()
            self.cpu += other.cpu

        if self.memory:
            if other.memory:
                self.memory += other.memory
        elif other.memory:
            self.memory = K8SResourcesConfig()
            self.memory += other.memory

        if self.gpu:
            if other.gpu:
                self.gpu += other.gpu
        elif other.gpu:
            self.gpu = K8SResourcesConfig()
            self.gpu += other.gpu

        if self.tpu:
            if other.tpu:
                self.tpu += other.tpu
        elif other.gpu:
            self.tpu = K8SResourcesConfig()
            self.tpu += other.tpu
        return self


class GPUOptionsSchema(BaseSchema):
    gpu_memory_fraction = fields.Float(allow_none=True)
    allow_growth = fields.Bool(allow_none=True)
    per_process_gpu_memory_fraction = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return GPUOptionsConfig


class GPUOptionsConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = GPUOptionsSchema

    def __init__(self,
                 gpu_memory_fraction=None,
                 allow_growth=True,
                 per_process_gpu_memory_fraction=None):
        self.gpu_memory_fraction = gpu_memory_fraction
        self.allow_growth = allow_growth
        self.per_process_gpu_memory_fraction = per_process_gpu_memory_fraction


class SessionSchema(BaseSchema):
    gpu_options = fields.Nested(GPUOptionsSchema, allow_none=True)
    log_device_placement = fields.Bool(allow_none=True)
    allow_soft_placement = fields.Bool(allow_none=True)
    intra_op_parallelism_threads = fields.Int(allow_none=True)
    inter_op_parallelism_threads = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return SessionConfig


class SessionConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = SessionSchema

    def __init__(self,
                 log_device_placement=True,
                 gpu_options=GPUOptionsConfig(),
                 allow_soft_placement=True,
                 intra_op_parallelism_threads=None,
                 inter_op_parallelism_threads=None):
        self.gpu_options = gpu_options
        self.log_device_placement = log_device_placement
        self.allow_soft_placement = allow_soft_placement
        self.intra_op_parallelism_threads = intra_op_parallelism_threads
        self.inter_op_parallelism_threads = inter_op_parallelism_threads


class TFRunSchema(BaseSchema):
    tf_random_seed = fields.Int(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)

    session = fields.Nested(SessionSchema, allow_none=True)
    cluster = fields.Nested(TensorflowClusterSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return TFRunConfig


class TFRunConfig(BaseConfig):
    IDENTIFIER = 'run'
    SCHEMA = TFRunSchema

    def __init__(self,
                 tf_random_seed=None,
                 save_summary_steps=100,
                 save_checkpoints_secs=None,
                 save_checkpoints_steps=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000,
                 session=None,
                 cluster=None):
        self.tf_random_seed = tf_random_seed
        self.save_summary_steps = save_summary_steps
        self.save_checkpoints_secs = save_checkpoints_secs
        self.save_checkpoints_steps = save_checkpoints_steps
        self.keep_checkpoint_max = keep_checkpoint_max
        self.keep_checkpoint_every_n_hours = keep_checkpoint_every_n_hours
        self.session = session
        self.cluster = cluster


class PodEnvironmentSchema(BaseSchema):
    # To indicate which worker/ps index this session config belongs to
    index = fields.Int(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return PodEnvironmentConfig


class PodEnvironmentConfig(BaseConfig):
    """
    Pod environment config.

    Args:
        index: `int | None`. The index of the pod.
        resources: `PodResourcesConfig`.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
    """
    IDENTIFIER = 'pod_environment'
    SCHEMA = PodEnvironmentSchema
    REDUCED_ATTRIBUTES = ['index', 'resources', 'node_selector', 'affinity', 'tolerations']

    def __init__(self,
                 index=None,
                 resources=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 ):
        self.index = index
        self.resources = resources
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations


class TensorflowPodEnvironmentSchema(PodEnvironmentSchema):
    config = fields.Nested(SessionSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowPodEnvironmentConfig


class TensorflowPodEnvironmentConfig(PodEnvironmentConfig):
    IDENTIFIER = 'pod_environment'
    SCHEMA = TensorflowPodEnvironmentSchema
    REDUCED_ATTRIBUTES = PodEnvironmentConfig.REDUCED_ATTRIBUTES + ['config']

    def __init__(self,
                 index=None,
                 config=None,
                 resources=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 ):
        self.config = config
        super(TensorflowPodEnvironmentConfig, self).__init__(
            index=index,
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )


class FrameworkEnvironmentMixin(object):
    @staticmethod
    def _get_env_indexed_property(obj, getter):
        if not obj:
            return {}
        return {o.index: getter(o) for o in obj if getter(o)}

    @property
    def default_worker_config(self):
        return self.default_worker.config if self.default_worker else None

    @property
    def default_worker_resources(self):
        return self.default_worker.resources if self.default_worker else None

    @property
    def default_worker_node_selector(self):
        return self.default_worker.node_selector if self.default_worker else None

    @property
    def default_worker_affinity(self):
        return self.default_worker.affinity if self.default_worker else None

    @property
    def default_worker_tolerations(self):
        return self.default_worker.tolerations if self.default_worker else None

    @property
    def default_ps_config(self):
        return self.default_ps.config if self.default_ps else None

    @property
    def default_ps_resources(self):
        return self.default_ps.resources if self.default_ps else None

    @property
    def default_ps_node_selector(self):
        return self.default_ps.node_selector if self.default_ps else None

    @property
    def default_ps_affinity(self):
        return self.default_ps.affinity if self.default_ps else None

    @property
    def default_ps_tolerations(self):
        return self.default_ps.tolerations if self.default_ps else None

    @property
    def worker_configs(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.config)

    @property
    def worker_resources(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.resources)

    @property
    def worker_node_selectors(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.node_selector)

    @property
    def worker_affinities(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.affinity)

    @property
    def worker_tolerations(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.tolerations)

    @property
    def ps_configs(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.config)

    @property
    def ps_resources(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.resources)

    @property
    def ps_node_selectors(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.node_selector)

    @property
    def ps_affinities(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.affinity)

    @property
    def ps_tolerations(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.tolerations)


class TensorflowSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    delay_workers_by_global_step = fields.Bool(allow_none=True)
    run_config = fields.Nested(TFRunSchema, allow_none=True)
    default_worker = fields.Nested(TensorflowPodEnvironmentSchema, allow_none=True)
    default_ps = fields.Nested(TensorflowPodEnvironmentSchema, allow_none=True)
    worker = fields.Nested(TensorflowPodEnvironmentSchema, many=True, allow_none=True)
    ps = fields.Nested(TensorflowPodEnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowConfig


class TensorflowConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Tensorflow environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        n_ps: `int`. The number of ps requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        default_ps: `PodEnvironment`. The default pod environment to use for all ps.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
        ps: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific ps.
    """
    IDENTIFIER = 'tensorflow'
    SCHEMA = TensorflowSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 delay_workers_by_global_step=False,
                 run_config=None,
                 default_worker=None,
                 default_ps=None,
                 worker=None,
                 ps=None,
                 ):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.run_config = run_config
        self.default_worker = default_worker
        self.default_ps = default_ps
        self.worker = worker
        self.ps = ps


class HorovodSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    default_worker = fields.Nested(PodEnvironmentSchema, allow_none=True)
    worker = fields.Nested(PodEnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return HorovodConfig


class HorovodConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Horovod environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
    """
    IDENTIFIER = 'horovod'
    SCHEMA = HorovodSchema

    def __init__(self,
                 n_workers=0,
                 default_worker=None,
                 worker=None,
                 ):
        self.n_workers = n_workers
        self.default_worker = default_worker
        self.worker = worker


class PytorchSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    default_worker = fields.Nested(PodEnvironmentSchema, allow_none=True)
    worker = fields.Nested(PodEnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return PytorchConfig


class PytorchConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Pytorch environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
    """
    IDENTIFIER = 'pytorch'
    SCHEMA = PytorchSchema

    def __init__(self,
                 n_workers=0,
                 default_worker=None,
                 worker=None,
                 ):
        self.n_workers = n_workers
        self.default_worker = default_worker
        self.worker = worker


class MXNetSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    default_worker = fields.Nested(PodEnvironmentSchema, allow_none=True)
    default_ps = fields.Nested(PodEnvironmentSchema, allow_none=True)
    worker = fields.Nested(PodEnvironmentSchema, many=True, allow_none=True)
    ps = fields.Nested(PodEnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return MXNetConfig


class MXNetConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    MXNet environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        n_ps: `int`. The number of ps requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        default_ps: `PodEnvironment`. The default pod environment to use for all ps.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
        ps: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific ps.
    """
    IDENTIFIER = 'mxnet'
    SCHEMA = MXNetSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 default_worker=None,
                 default_ps=None,
                 worker=None,
                 ps=None,
                 ):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.default_worker = default_worker
        self.default_ps = default_ps
        self.worker = worker
        self.ps = ps


def validate_frameworks(frameworks):
    if sum([1 for f in frameworks if f is not None]) > 1:
        raise ValidationError('Only one framework can be used.')


class PersistenceSchema(BaseSchema):
    data = fields.List(fields.Str(), allow_none=True)
    outputs = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceConfig


class PersistenceConfig(BaseConfig):
    """
    Persistence config.

    Defines the list of persistent volumes to mount for this specific run.

    Args:
        data: `list(str)`. The list of the names of data persistence to mount.
        outputs: `list(str)`. The list of the names of outputs persistence to mount.
    """
    IDENTIFIER = 'persistence'
    SCHEMA = PersistenceSchema

    def __init__(self, data=None, outputs=None):
        self.data = data
        self.outputs = outputs


class OutputsSchema(BaseSchema):
    jobs = fields.List(IntOrStr(), allow_none=True)
    experiments = fields.List(IntOrStr(), allow_none=True)

    @staticmethod
    def schema_config():
        return OutputsConfig


class OutputsConfig(BaseConfig):
    """
    Outputs config.

    Defines the list of previous jobs/experiments outputs paths
    to make available to other experiments/jobs.

    Args:
        jobs: `list(str)`. The list of the names of jobs to make available for the current run.
        experiments: `list(str)`. The list of the names of experiments
            to make available for the current run.
    """
    IDENTIFIER = 'outputs'
    SCHEMA = OutputsSchema

    def __init__(self, jobs=None, experiments=None):
        self.jobs = jobs
        self.experiments = experiments


class EnvironmentSchema(PodEnvironmentSchema):
    cluster_uuid = UUID(allow_none=True)
    persistence = fields.Nested(PersistenceSchema, allow_none=True)
    outputs = fields.Nested(OutputsSchema, allow_none=True)
    secret_refs = fields.List(fields.Str(), allow_none=True)
    configmap_refs = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return EnvironmentConfig


class EnvironmentConfig(PodEnvironmentConfig):
    """
    Environment config.

    Args:
        cluster_uuid: `str`. The cluster uuid.
        persistence: `PersistenceConfig`. The persistence config definition.
        outputs: `OutputsConfig`. The outputs config definition.
        resources: `PodResourcesConfig`. The resources config definition.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
    """
    IDENTIFIER = 'environment'
    SCHEMA = EnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 persistence=None,
                 outputs=None,
                 resources=None,
                 secret_refs=None,
                 configmap_refs=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None):
        self.cluster_uuid = cluster_uuid
        self.persistence = persistence
        self.outputs = outputs
        self.secret_refs = secret_refs
        self.configmap_refs = configmap_refs
        super(EnvironmentConfig, self).__init__(
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )


class ExperimentEnvironmentSchema(EnvironmentSchema):
    tensorflow = fields.Nested(TensorflowSchema, allow_none=True)
    horovod = fields.Nested(HorovodSchema, allow_none=True)
    mxnet = fields.Nested(MXNetSchema, allow_none=True)
    pytorch = fields.Nested(PytorchSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentEnvironmentConfig

    @validates_schema
    def validate_frameworks(self, data):
        validate_frameworks([data.get('tensorflow'),
                             data.get('mxnet'),
                             data.get('pytorch'),
                             data.get('horovod')])


class ExperimentEnvironmentConfig(EnvironmentConfig):
    """
    Environment config.

    Args:
        cluster_uuid: `str`. The cluster uuid.
        persistence: `PersistenceConfig`. The persistence config definition.
        outputs: `OutputsConfig`. The outputs config definition.
        resources: `PodResourcesConfig`. The resources config definition.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
        tensorflow: `TensorflowConfig`.
        horovod: `HorovodConfig`.
        pytorch: `PytorchConfig`.
        mxnet: `MXNetConfig`.
    """
    IDENTIFIER = 'environment'
    SCHEMA = ExperimentEnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 persistence=None,
                 outputs=None,
                 resources=None,
                 secret_refs=None,
                 configmap_refs=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 tensorflow=None,
                 horovod=None,
                 pytorch=None,
                 mxnet=None):
        super(ExperimentEnvironmentConfig, self).__init__(
            cluster_uuid=cluster_uuid,
            persistence=persistence,
            outputs=outputs,
            resources=resources,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        validate_frameworks([tensorflow, horovod, pytorch, mxnet])
        self.tensorflow = tensorflow
        self.horovod = horovod
        self.pytorch = pytorch
        self.mxnet = mxnet


def validate_notebook_backend(backend):
    if backend and backend not in NotebookBackend.VALUES:
        raise ValidationError('Notebook backend `{}` not supported'.format(backend))


class NotebookEnvironmentSchema(EnvironmentSchema):
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return NotebookEnvironmentConfig

    @validates_schema
    def validate_backend(self, data):
        validate_notebook_backend(data.get('backend'))


class NotebookEnvironmentConfig(EnvironmentConfig):
    """
    Environment config.

    Args:
        cluster_uuid: `str`. The cluster uuid.
        persistence: `PersistenceConfig`. The persistence config definition.
        outputs: `OutputsConfig`. The outputs config definition.
        resources: `PodResourcesConfig`. The resources config definition.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
        backend: `str`.
    """
    IDENTIFIER = 'environment'
    SCHEMA = NotebookEnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 persistence=None,
                 outputs=None,
                 resources=None,
                 secret_refs=None,
                 configmap_refs=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 backend=None):
        super(NotebookEnvironmentConfig, self).__init__(
            cluster_uuid=cluster_uuid,
            persistence=persistence,
            outputs=outputs,
            resources=resources,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        validate_notebook_backend(backend)
        self.backend = backend
