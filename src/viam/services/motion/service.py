from grpclib.server import Stream

from viam.proto.common import DoCommandRequest, DoCommandResponse
from viam.proto.service.motion import MotionServiceBase, MoveOnGlobeRequest, MoveOnGlobeResponse
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

    # async def Move(self, stream: 'grpclib.server.Stream[service.motion.v1.motion_pb2.MoveRequest, service.motion.v1.motion_pb2.MoveResponse]') -> None:
    #     pass
    #
    # @abc.abstractmethod
    # async def MoveOnMap(self, stream: 'grpclib.server.Stream[service.motion.v1.motion_pb2.MoveOnMapRequest, service.motion.v1.motion_pb2.MoveOnMapResponse]') -> None:
    #     pass
    #
    # @abc.abstractmethod
    # async def MoveSingleComponent(self, stream: 'grpclib.server.Stream[service.motion.v1.motion_pb2.MoveSingleComponentRequest, service.motion.v1.motion_pb2.MoveSingleComponentResponse]') -> None:
    #     pass
    #
    # @abc.abstractmethod
    # async def GetPose(self, stream: 'grpclib.server.Stream[service.motion.v1.motion_pb2.GetPoseRequest, service.motion.v1.motion_pb2.GetPoseResponse]') -> None:
    #     pass
    #
    # @abc.abstractmethod
    # async def DoCommand(self, stream: 'grpclib.server.Stream[common.v1.common_pb2.DoCommandRequest, common.v1.common_pb2.DoCommandResponse]') -> None:
    #     pass
