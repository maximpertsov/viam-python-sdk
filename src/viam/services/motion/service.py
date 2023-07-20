from grpclib.server import Stream

from viam.errors import MethodNotImplementedError
from viam.proto.common import DoCommandRequest, DoCommandResponse
from viam.proto.service.motion import (
    GetPoseRequest,
    GetPoseResponse,
    MotionServiceBase,
    MoveOnGlobeRequest,
    MoveOnGlobeResponse,
    MoveOnMapRequest,
    MoveOnMapResponse,
    MoveRequest,
    MoveResponse,
    MoveSingleComponentRequest,
    MoveSingleComponentResponse,
)
from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.utils import dict_to_struct, struct_to_dict

from .motion import Motion


class MotionRPCService(MotionServiceBase, ResourceRPCServiceBase):
    """
    gRPC Service for a Motion service
    """

    RESOURCE_TYPE = Motion

    async def MoveOnGlobe(self, stream: Stream[MoveOnGlobeRequest, MoveOnGlobeResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None

        motion = self.get_resource(request.name)
        timeout = stream.deadline.time_remaining() if stream.deadline else None

        success = await motion.move_on_globe(
            request.component_name,
            request.destination,
            request.movement_sensor_name,
            request.obstacles,
            request.heading,
            request.linear_meters_per_sec,
            request.angular_deg_per_sec,
            extra=request.extra,
            timeout=timeout,
        )
        response = MoveOnGlobeResponse(success=success)
        await stream.send_message(response)

    async def Move(self, stream: Stream[MoveRequest, MoveResponse]) -> None:
        raise MethodNotImplementedError("Move").grpc_error

    async def MoveOnMap(self, stream: Stream[MoveOnMapRequest, MoveOnMapResponse]) -> None:
        raise MethodNotImplementedError("MoveOnMap").grpc_error

    async def MoveSingleComponent(self, stream: Stream[MoveSingleComponentRequest, MoveSingleComponentResponse]) -> None:
        raise MethodNotImplementedError("MoveSingleComponent").grpc_error

    async def GetPose(self, stream: Stream[GetPoseRequest, GetPoseResponse]) -> None:
        raise MethodNotImplementedError("GetPose").grpc_error

    async def DoCommand(self, stream: Stream[DoCommandRequest, DoCommandResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        motion = self.get_resource(request.name)
        timeout = stream.deadline.time_remaining() if stream.deadline else None
        result = await motion.do_command(command=struct_to_dict(request.command), timeout=timeout, metadata=stream.metadata)
        response = DoCommandResponse(result=dict_to_struct(result))
        await stream.send_message(response)
