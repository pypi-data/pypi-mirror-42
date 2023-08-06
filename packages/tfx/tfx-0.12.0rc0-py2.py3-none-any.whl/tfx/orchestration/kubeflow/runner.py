# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFX runner for Kubeflow."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

from kfp import compiler
from kfp import dsl
from tfx.orchestration import tfx_runner
from tfx.orchestration.kubeflow import base_component


# TODO(ajaygopinathan): Add tests to ensure components are compiled into a
# valid Kubeflow pipeline.
class KubeflowRunner(tfx_runner.TfxRunner):
  """Kubeflow Pipelines runner.

  Constructs a pipeline definition YAML file based on the TFX logical pipeline.
  """

  def _prepare_output_dict(self, outputs):
    return dict((k, v.get()) for k, v in outputs.get_all().items())

  def _construct_pipeline_graph(self, pipeline):
    """Constructs a Kubeflow Pipeline graph.

    Args:
      pipeline: The logical TFX pipeline to base the construction on.
    """
    # producers is a map from an output Channel, to a Kubeflow component that
    # is responsible for the named output represented by the Channel.
    # Assumption: Channels are unique in a pipeline.
    producers = {}

    # Assumption: There is a partial ordering of components in the list, i.e.,
    # if component A depends on component B and C, then A appears after B and C
    # in the list.
    for component in pipeline.components:
      input_dict = {}
      for input_name, input_channel in component.input_dict.items():
        if input_channel in producers:
          output = getattr(producers[input_channel].outputs,
                           input_channel.channel_name)

          if not isinstance(output, dsl.PipelineParam):
            raise ValueError(
                'Component outputs should be of type dsl.PipelineParam.'
                ' Got type {} for output {}'.format(type(output), output))
          input_dict[input_name] = output
        else:
          input_dict[input_name] = json.dumps(
              [x.json_dict() for x in input_channel.get()])

      kfp_component = base_component.BaseComponent(
          component_name=component.component_name,
          input_dict=input_dict,
          output_dict=self._prepare_output_dict(component.outputs),
          exec_properties=component.exec_properties)

      for channel in component.outputs.get_all().values():
        producers[channel] = kfp_component

  def run(self, pipeline):
    """Compiles and outputs a Kubeflow Pipeline YAML definition file.

    Args:
      pipeline: The logical TFX pipeline to use when building the Kubeflow
        pipeline.
    """

    def _construct_pipeline():
      """Constructs a Kubeflow pipeline.

      Creates Kubeflow ContainerOps for each TFX component encountered in the
      logical pipeline definition.
      """
      output_dir = os.path.join(pipeline.kwargs['pipeline_root'],
                                pipeline.kwargs['pipeline_name'])

      beam_pipeline_args = []
      if 'additional_pipeline_args' in pipeline.kwargs:
        beam_pipeline_args = pipeline.kwargs['additional_pipeline_args'].get(
            'beam_pipeline_args', [])

      base_component.ExecutionProperties(
          output_dir=output_dir,
          log_root=pipeline.kwargs['log_root'],
          beam_pipeline_args=beam_pipeline_args,
      )

      self._construct_pipeline_graph(pipeline)

    pipeline_name = pipeline.kwargs['pipeline_name']
    dsl.Pipeline.add_pipeline(pipeline_name,
                              pipeline.kwargs.get('description', ''),
                              _construct_pipeline)

    compiler.Compiler().compile(_construct_pipeline, pipeline_name + '.tar.gz')
