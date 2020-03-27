{
  "cwlVersion": "v1.0",
  "class": "CommandLineTool",
  "hints": [
    {
      "coresMin": 1,
      "ramMin": 5000,
      "tmpdirMin": 1000,
      "class": "ResourceRequirement"
    }
  ],
  "baseCommand": [
    "touch"
  ],
  "inputs": [
    {
      "type": "string",
      "inputBinding": {
        "position": 1
      },
      "id": "file:///mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/tests/integration/fixtures/touch.cwl#filename"
    }
  ],
  "outputs": [
    {
      "type": "File",
      "outputBinding": {
        "glob": "$(inputs.filename)"
      },
      "id": "file:///mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/tests/integration/fixtures/touch.cwl#test_file"
    }
  ],
  "id": "file:///mnt/c/Users/kerst/OneDrive/home/C2WL-Rocket/tests/integration/fixtures/touch.cwl"
}