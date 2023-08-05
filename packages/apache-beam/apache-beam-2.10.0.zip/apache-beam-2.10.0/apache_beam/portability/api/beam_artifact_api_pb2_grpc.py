from __future__ import absolute_import
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
from builtins import object
import grpc

from . import beam_artifact_api_pb2 as beam__artifact__api__pb2


class ArtifactStagingServiceStub(object):
  """A service to stage artifacts for use in a Job.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.PutArtifact = channel.stream_unary(
        '/org.apache.beam.model.job_management.v1.ArtifactStagingService/PutArtifact',
        request_serializer=beam__artifact__api__pb2.PutArtifactRequest.SerializeToString,
        response_deserializer=beam__artifact__api__pb2.PutArtifactResponse.FromString,
        )
    self.CommitManifest = channel.unary_unary(
        '/org.apache.beam.model.job_management.v1.ArtifactStagingService/CommitManifest',
        request_serializer=beam__artifact__api__pb2.CommitManifestRequest.SerializeToString,
        response_deserializer=beam__artifact__api__pb2.CommitManifestResponse.FromString,
        )


class ArtifactStagingServiceServicer(object):
  """A service to stage artifacts for use in a Job.
  """

  def PutArtifact(self, request_iterator, context):
    """Stage an artifact to be available during job execution. The first request must contain the
    name of the artifact. All future requests must contain sequential chunks of the content of
    the artifact.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CommitManifest(self, request, context):
    """Commit the manifest for a Job. All artifacts must have been successfully uploaded
    before this call is made.

    Throws error INVALID_ARGUMENT if not all of the members of the manifest are present
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ArtifactStagingServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'PutArtifact': grpc.stream_unary_rpc_method_handler(
          servicer.PutArtifact,
          request_deserializer=beam__artifact__api__pb2.PutArtifactRequest.FromString,
          response_serializer=beam__artifact__api__pb2.PutArtifactResponse.SerializeToString,
      ),
      'CommitManifest': grpc.unary_unary_rpc_method_handler(
          servicer.CommitManifest,
          request_deserializer=beam__artifact__api__pb2.CommitManifestRequest.FromString,
          response_serializer=beam__artifact__api__pb2.CommitManifestResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.model.job_management.v1.ArtifactStagingService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class ArtifactRetrievalServiceStub(object):
  """A service to retrieve artifacts for use in a Job.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetManifest = channel.unary_unary(
        '/org.apache.beam.model.job_management.v1.ArtifactRetrievalService/GetManifest',
        request_serializer=beam__artifact__api__pb2.GetManifestRequest.SerializeToString,
        response_deserializer=beam__artifact__api__pb2.GetManifestResponse.FromString,
        )
    self.GetArtifact = channel.unary_stream(
        '/org.apache.beam.model.job_management.v1.ArtifactRetrievalService/GetArtifact',
        request_serializer=beam__artifact__api__pb2.GetArtifactRequest.SerializeToString,
        response_deserializer=beam__artifact__api__pb2.ArtifactChunk.FromString,
        )


class ArtifactRetrievalServiceServicer(object):
  """A service to retrieve artifacts for use in a Job.
  """

  def GetManifest(self, request, context):
    """Get the manifest for the job
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetArtifact(self, request, context):
    """Get an artifact staged for the job. The requested artifact must be within the manifest
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ArtifactRetrievalServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetManifest': grpc.unary_unary_rpc_method_handler(
          servicer.GetManifest,
          request_deserializer=beam__artifact__api__pb2.GetManifestRequest.FromString,
          response_serializer=beam__artifact__api__pb2.GetManifestResponse.SerializeToString,
      ),
      'GetArtifact': grpc.unary_stream_rpc_method_handler(
          servicer.GetArtifact,
          request_deserializer=beam__artifact__api__pb2.GetArtifactRequest.FromString,
          response_serializer=beam__artifact__api__pb2.ArtifactChunk.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.model.job_management.v1.ArtifactRetrievalService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
