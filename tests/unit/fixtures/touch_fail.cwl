cwlVersion: v1.0
class: CommandLineTool
hints:
  ResourceRequirement:
    coresMin: 1
    ramMin: 5000
    tmpdirMin: 1000

baseCommand: ["touch"]

inputs:
  filename:
    type: string
    inputBinding:
      position: 1

outputs:
  test_file:
    type: File
    outputBinding:
      glob: $(inputs.filename)_fail.txt
  
  
