#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.r)
        writable: true
inputs:
  r: File
  script:
    type: File
    default:
      class: File
      location: updateval.py
outputs:
  out:
    type: File
    outputBinding:
      glob: $(inputs.r.basename)
arguments: [python, $(inputs.script), $(inputs.r.basename)]