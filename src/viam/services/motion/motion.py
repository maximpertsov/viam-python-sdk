import abc
from typing import Any, Final, List, Mapping, Optional, Sequence

from viam.proto.common import GeoObstacle, GeoPoint, PoseInFrame, ResourceName
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.utils import ValueTypes, dict_to_struct, struct_to_dict

from ..service_base import ServiceBase


class Motion(ServiceBase):
    """
    Motion represents a Motion service.

    This acts as an abstract base class for any drivers representing specific
    arm implementations. This cannot be used on its own. If the ``__init__()`` function is
    overridden, it must call the ``super().__init__()`` function.
    """

    SUBTYPE: Final = Subtype(RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, "motion")

    @abc.abstractmethod
    async def move_on_globe(
        self,
        component_name: ResourceName,
        destination: GeoPoint,
        movement_sensor_name: ResourceName,
        obstacles: Optional[Sequence[GeoObstacle]],
        heading: Optional[float],
        linear_meters_per_sec: Optional[float],
        angular_deg_per_sec: Optional[float],
        *,
        extra: Optional[Mapping[str, ValueTypes]],
        timeout: Optional[float],
    ) -> bool:
        """Move a component to a specific latitude and longitude, using a ``MovementSensor`` to check the location.

        Args:
            component_name (ResourceName): The component to move
            destination (GeoPoint): The destination point
            movement_sensor_name (ResourceName): The ``MovementSensor`` which will be used to check robot location
            obstacles (Optional[Sequence[GeoObstacle]], optional): Obstacles to be considered for motion planning. Defaults to None.
            heading (Optional[float], optional): Compass heading to achieve at the destination, in degrees [0-360). Defaults to None.
            linear_meters_per_sec (Optional[float], optional): Linear velocity to target when moving. Defaults to None.
            angular_deg_per_sec (Optional[float], optional): Angular velocity to target when turning. Defaults to None.

        Returns:
            bool: Whether the request was successful
        """
        ...
