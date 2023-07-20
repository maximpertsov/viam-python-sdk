from viam.resource.registry import Registry, ResourceRegistration

from .client import MotionClient
from .motion import Motion
from .service import MotionRPCService

__all__ = ["MotionClient", "Motion", "MotionRPCService"]

Registry.register_subtype(ResourceRegistration(Motion, MotionRPCService, lambda name, channel: MotionClient(name, channel)))
