{
    "$graph": [
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "StepInputExpressionRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "kerstenbreuer/bowtie2:2.2.6-2",
                    "class": "DockerRequirement"
                },
                {
                    "coresMin": 4,
                    "ramMin": 30000,
                    "class": "ResourceRequirement"
                }
            ],
            "baseCommand": [
                "bowtie2"
            ],
            "arguments": [
                {
                    "valueFrom": "--very-sensitive",
                    "position": 1
                },
                {
                    "valueFrom": "$(runtime.cores)",
                    "prefix": "-p",
                    "position": 1
                },
                {
                    "position": 10,
                    "valueFrom": "${\n  if ( inputs.is_paired_end ){\n     return \"-1\";\n  }\n  else {\n    return \"-U\";\n  }\n}\n"
                },
                {
                    "valueFrom": "$(inputs.fastq1.nameroot + \".sam\")",
                    "prefix": "-S",
                    "position": 6
                }
            ],
            "stderr": "$( inputs.fastq1.nameroot + \".bowtie2_stderr\")",
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 11
                    },
                    "id": "#bowtie2.cwl/fastq1"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "valueFrom": "${\n    if ( inputs.is_paired_end ){\n        return self;\n    }\n    else {\n      return null;\n    }\n}  \n",
                        "position": 12,
                        "prefix": "-2"
                    },
                    "id": "#bowtie2.cwl/fastq2"
                },
                {
                    "doc": "path to the FM-index files for the chosen genome genome",
                    "type": "File",
                    "secondaryFiles": [
                        ".fai",
                        "^.1.bt2",
                        "^.2.bt2",
                        "^.3.bt2",
                        "^.4.bt2",
                        "^.rev.1.bt2",
                        "^.rev.2.bt2"
                    ],
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-x",
                        "valueFrom": "$(self.path.replace(/\\.fa/i,\"\"))"
                    },
                    "id": "#bowtie2.cwl/genome_index"
                },
                {
                    "type": "boolean",
                    "id": "#bowtie2.cwl/is_paired_end"
                },
                {
                    "doc": "usefull for very long fragments, as expected for ATAC",
                    "type": [
                        "null",
                        "long"
                    ],
                    "inputBinding": {
                        "prefix": "--maxins",
                        "position": 1
                    },
                    "id": "#bowtie2.cwl/max_mapping_insert_length"
                }
            ],
            "outputs": [
                {
                    "type": "stderr",
                    "id": "#bowtie2.cwl/bowtie2_log"
                },
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.sam"
                    },
                    "id": "#bowtie2.cwl/sam"
                }
            ],
            "id": "#bowtie2.cwl"
        },
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "StepInputExpressionRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "kerstenbreuer/trim_galore:0.4.4_1.14_0.11.7",
                    "class": "DockerRequirement"
                },
                {
                    "coresMin": 1,
                    "ramMin": 5000,
                    "class": "ResourceRequirement"
                }
            ],
            "baseCommand": "fastqc",
            "arguments": [
                {
                    "valueFrom": "$(runtime.outdir)",
                    "prefix": "-o"
                },
                {
                    "valueFrom": "--noextract"
                }
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#fastqc.cwl/bam"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#fastqc.cwl/fastq1"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#fastqc.cwl/fastq2"
                }
            ],
            "outputs": [
                {
                    "doc": "html report showing results from zip",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputBinding": {
                        "glob": "*_fastqc.html"
                    },
                    "id": "#fastqc.cwl/fastqc_html"
                },
                {
                    "doc": "all data e.g. figures",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputBinding": {
                        "glob": "*_fastqc.zip"
                    },
                    "id": "#fastqc.cwl/fastqc_zip"
                }
            ],
            "id": "#fastqc.cwl"
        },
        {
            "doc": "Sort a bam file by read names.",
            "class": "CommandLineTool",
            "hints": [
                {
                    "dockerPull": "kerstenbreuer/samtools:1.7",
                    "class": "DockerRequirement"
                },
                {
                    "coresMin": 4,
                    "ramMin": 15000,
                    "class": "ResourceRequirement"
                }
            ],
            "baseCommand": [
                "samtools",
                "sort"
            ],
            "arguments": [
                {
                    "valueFrom": "$(runtime.cores)",
                    "prefix": "-@"
                }
            ],
            "inputs": [
                {
                    "doc": "aligned reads to be checked in sam or bam format",
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#samtools_sort.cwl/bam_unsorted"
                }
            ],
            "stdout": "$(inputs.bam_unsorted.basename)",
            "outputs": [
                {
                    "type": "stdout",
                    "id": "#samtools_sort.cwl/bam_sorted"
                }
            ],
            "id": "#samtools_sort.cwl"
        },
        {
            "class": "CommandLineTool",
            "hints": [
                {
                    "dockerPull": "kerstenbreuer/samtools:1.7",
                    "class": "DockerRequirement"
                },
                {
                    "coresMin": 1,
                    "ramMin": 10000,
                    "class": "ResourceRequirement"
                }
            ],
            "baseCommand": [
                "samtools",
                "view"
            ],
            "inputs": [
                {
                    "doc": "aligned reads to be checked in sam or bam format",
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#samtools_view_sam2bam.cwl/sam"
                }
            ],
            "arguments": [
                {
                    "valueFrom": "-h",
                    "position": 1
                },
                {
                    "valueFrom": "-b",
                    "position": 1
                }
            ],
            "stdout": "$(inputs.sam.nameroot).bam",
            "outputs": [
                {
                    "type": "stdout",
                    "id": "#samtools_view_sam2bam.cwl/bam_unsorted"
                }
            ],
            "id": "#samtools_view_sam2bam.cwl"
        },
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "kerstenbreuer/trim_galore:0.4.4_1.14_0.11.7",
                    "class": "DockerRequirement"
                },
                {
                    "coresMin": 1,
                    "ramMin": 7000,
                    "class": "ResourceRequirement"
                }
            ],
            "baseCommand": "trim_galore",
            "inputs": [
                {
                    "doc": "Adapter to be trimmed from first reads. Cab be one of the following: \\n\n- \"nextera\" for the Nextera adapter (CTGTCTCTTATA)\\n\n- \"illumina\" for the Illumina universal adapter (AGATCGGAAGAGC)\\n\n- \"small_rna\" for the Illumina Small RNA 3-prime Adapter (TGGAATTCTCGG)\\n\n- \"auto\" to automatically detect the write setting\n",
                    "type": {
                        "type": "enum",
                        "symbols": [
                            "#trim_galore.cwl/adapter1/nextera",
                            "#trim_galore.cwl/adapter1/illumina",
                            "#trim_galore.cwl/adapter1/small_rna",
                            "#trim_galore.cwl/adapter1/auto"
                        ]
                    },
                    "id": "#trim_galore.cwl/adapter1"
                },
                {
                    "doc": "Adapters to be trimmed from second read. Cab be one of the following: \\n\n- \"nextera\" for the Nextera adapter (CTGTCTCTTATA)\\n\n- \"illumina\" for the Illumina universal adapter (AGATCGGAAGAGC)\\n\n- \"small_rna\" for the Illumina Small RNA 3-prime Adapter (TGGAATTCTCGG)\\n\n- \"auto\" to automatically detect the write setting\n",
                    "type": {
                        "type": "enum",
                        "symbols": [
                            "#trim_galore.cwl/adapter2/nextera",
                            "#trim_galore.cwl/adapter2/illumina",
                            "#trim_galore.cwl/adapter2/small_rna",
                            "#trim_galore.cwl/adapter2/auto"
                        ]
                    },
                    "id": "#trim_galore.cwl/adapter2"
                },
                {
                    "doc": "raw reads in fastq format; can be gzipped;\nif paired end, the file contains the first reads;\nif single end, the file contains all reads\n",
                    "type": "File",
                    "inputBinding": {
                        "position": 10
                    },
                    "id": "#trim_galore.cwl/fastq1"
                },
                {
                    "doc": "(optional) raw reads in fastq format; can be gzipped;\nif paired end, the file contains the second reads;\nif single end, the file does not exist\n",
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 11
                    },
                    "id": "#trim_galore.cwl/fastq2"
                },
                {
                    "doc": "minimum overlap with adapter seq in bp needed to trim",
                    "type": "int",
                    "default": 1,
                    "inputBinding": {
                        "prefix": "--stringency",
                        "position": 1
                    },
                    "id": "#trim_galore.cwl/min_adapter_overlap"
                },
                {
                    "doc": "discard reads that get shorter than this value",
                    "type": "int",
                    "default": 20,
                    "inputBinding": {
                        "prefix": "--length",
                        "position": 1
                    },
                    "id": "#trim_galore.cwl/min_read_length"
                },
                {
                    "doc": "if only one read of a pair passes the qc and adapter trimming,\nit needs at least this length to be rescued\n",
                    "type": "int",
                    "default": 35,
                    "id": "#trim_galore.cwl/min_unpaired_read_rescue_length"
                },
                {
                    "doc": "trim all base with a phred score lower than this valueFrom",
                    "type": "int",
                    "default": 20,
                    "inputBinding": {
                        "prefix": "--quality",
                        "position": 1
                    },
                    "id": "#trim_galore.cwl/qual_trim_cutoff"
                }
            ],
            "arguments": [
                {
                    "prefix": "--fastqc_args",
                    "valueFrom": "\"--noextract\"",
                    "position": 1
                },
                {
                    "prefix": "--gzip",
                    "position": 1
                },
                {
                    "valueFrom": "${\n  if ( inputs.adapter1 == \"illumina\" ){ return \"--illumina\" }\n  else if ( inputs.adapter1 == \"nextera\" ){ return \"--nextera\" }\n  else if ( inputs.adapter1 == \"small_rna\" ){ return \"--small_rna\" }\n  else { return null }\n}\n",
                    "position": 1
                },
                {
                    "prefix": "--adapter",
                    "valueFrom": "${\n  if ( inputs.apdater1 != null && inputs.adapter1 != \"illumina\" && inputs.adapter1 != \"nextera\" && inputs.adapter1 != \"small_rna\" ){\n    return inputs.adapter1\n  } else {\n    return null\n  }\n}\n",
                    "position": 1
                },
                {
                    "prefix": "--adapter2",
                    "valueFrom": "${\n  if ( inputs.fastq2 != null && inputs.apdater2 != null && inputs.adapter1 != \"illumina\" && inputs.adapter1 != \"nextera\" && inputs.adapter1 != \"small_rna\" ){\n    return inputs.adapter2\n  } else {\n    return null\n  }\n}\n",
                    "position": 1
                },
                {
                    "valueFrom": "${\n  if ( inputs.fastq2 == null ){ return null }\n  else { return \"--paired\" }\n}\n",
                    "position": 1
                },
                {
                    "valueFrom": "${\n  if ( inputs.fastq2 == null ){ return null }\n  else { return \"--retain_unpaired\" }\n}\n",
                    "position": 1
                },
                {
                    "prefix": "--length_1",
                    "valueFrom": "${\n  if ( inputs.fastq2 == null ){ return null }\n  else { return inputs.min_unpaired_read_rescue_length }\n}\n",
                    "position": 1
                },
                {
                    "prefix": "--length_2",
                    "valueFrom": "${\n  if ( inputs.fastq2 == null ){ return null }\n  else { return inputs.min_unpaired_read_rescue_length }\n}\n",
                    "position": 1
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "${\n    if ( inputs.fastq2 == null  ){ return \"*trimmed.fq*\" }\n    else { return \"*val_1.fq*\" }\n}\n"
                    },
                    "id": "#trim_galore.cwl/fastq1_trimmed"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "outputBinding": {
                        "glob": "*unpaired_1.fq*"
                    },
                    "id": "#trim_galore.cwl/fastq1_trimmed_unpaired"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "outputBinding": {
                        "glob": "*val_2.fq*"
                    },
                    "id": "#trim_galore.cwl/fastq2_trimmed"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "outputBinding": {
                        "glob": "*unpaired_2.fq*"
                    },
                    "id": "#trim_galore.cwl/fastq2_trimmed_unpaired"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputBinding": {
                        "glob": "*trimming_report.txt"
                    },
                    "id": "#trim_galore.cwl/trim_galore_log"
                },
                {
                    "doc": "html report of post-trimming fastqc",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputBinding": {
                        "glob": "*fastqc.html"
                    },
                    "id": "#trim_galore.cwl/trimmed_fastqc_html"
                },
                {
                    "doc": "all data of post-trimming fastqc e.g. figures",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputBinding": {
                        "glob": "*fastqc.zip"
                    },
                    "id": "#trim_galore.cwl/trimmed_fastqc_zip"
                }
            ],
            "id": "#trim_galore.cwl"
        },
        {
            "class": "Workflow",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "ScatterFeatureRequirement"
                },
                {
                    "class": "StepInputExpressionRequirement"
                },
                {
                    "class": "SubworkflowFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": {
                        "type": "enum",
                        "symbols": [
                            "#main/adapter1/nextera",
                            "#main/adapter1/illumina",
                            "#main/adapter1/small_rna",
                            "#main/adapter1/auto"
                        ]
                    },
                    "id": "#main/adapter1"
                },
                {
                    "type": {
                        "type": "enum",
                        "symbols": [
                            "#main/adapter2/nextera",
                            "#main/adapter2/illumina",
                            "#main/adapter2/small_rna",
                            "#main/adapter2/auto"
                        ]
                    },
                    "id": "#main/adapter2"
                },
                {
                    "type": "File",
                    "id": "#main/fastq1"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "id": "#main/fastq2"
                },
                {
                    "type": "File",
                    "secondaryFiles": [
                        ".fai",
                        "^.1.bt2",
                        "^.2.bt2",
                        "^.3.bt2",
                        "^.4.bt2",
                        "^.rev.1.bt2",
                        "^.rev.2.bt2"
                    ],
                    "id": "#main/genome"
                },
                {
                    "type": "boolean",
                    "id": "#main/is_paired_end"
                },
                {
                    "type": [
                        "null",
                        "long"
                    ],
                    "id": "#main/max_mapping_insert_length"
                }
            ],
            "steps": [
                {
                    "doc": "trim galore - adapter trimming using trim_galore",
                    "run": "#trim_galore.cwl",
                    "in": [
                        {
                            "source": "#main/adapter1",
                            "id": "#main/adaptor_trimming_and_qc_trimmed/adapter1"
                        },
                        {
                            "source": "#main/adapter2",
                            "id": "#main/adaptor_trimming_and_qc_trimmed/adapter2"
                        },
                        {
                            "source": "#main/fastq1",
                            "id": "#main/adaptor_trimming_and_qc_trimmed/fastq1"
                        },
                        {
                            "source": "#main/fastq2",
                            "id": "#main/adaptor_trimming_and_qc_trimmed/fastq2"
                        }
                    ],
                    "out": [
                        "#main/adaptor_trimming_and_qc_trimmed/fastq1_trimmed",
                        "#main/adaptor_trimming_and_qc_trimmed/fastq2_trimmed",
                        "#main/adaptor_trimming_and_qc_trimmed/fastq1_trimmed_unpaired",
                        "#main/adaptor_trimming_and_qc_trimmed/fastq2_trimmed_unpaired",
                        "#main/adaptor_trimming_and_qc_trimmed/trim_galore_log",
                        "#main/adaptor_trimming_and_qc_trimmed/trimmed_fastqc_html",
                        "#main/adaptor_trimming_and_qc_trimmed/trimmed_fastqc_zip"
                    ],
                    "id": "#main/adaptor_trimming_and_qc_trimmed"
                },
                {
                    "doc": "bowite2 - mapper, produces sam file",
                    "run": "#bowtie2.cwl",
                    "in": [
                        {
                            "source": "#main/adaptor_trimming_and_qc_trimmed/fastq1_trimmed",
                            "id": "#main/mapping/fastq1"
                        },
                        {
                            "source": "#main/adaptor_trimming_and_qc_trimmed/fastq2_trimmed",
                            "id": "#main/mapping/fastq2"
                        },
                        {
                            "source": "#main/genome",
                            "id": "#main/mapping/genome_index"
                        },
                        {
                            "source": "#main/is_paired_end",
                            "id": "#main/mapping/is_paired_end"
                        },
                        {
                            "source": "#main/max_mapping_insert_length",
                            "id": "#main/mapping/max_mapping_insert_length"
                        }
                    ],
                    "out": [
                        "#main/mapping/sam",
                        "#main/mapping/bowtie2_log"
                    ],
                    "id": "#main/mapping"
                },
                {
                    "doc": "fastqc - quality control for trimmed fastq",
                    "run": "#fastqc.cwl",
                    "in": [
                        {
                            "source": "#main/fastq1",
                            "id": "#main/qc_raw/fastq1"
                        },
                        {
                            "source": "#main/fastq2",
                            "id": "#main/qc_raw/fastq2"
                        }
                    ],
                    "out": [
                        "#main/qc_raw/fastqc_zip",
                        "#main/qc_raw/fastqc_html"
                    ],
                    "id": "#main/qc_raw"
                },
                {
                    "doc": "samtools view - convert sam to bam",
                    "run": "#samtools_view_sam2bam.cwl",
                    "in": [
                        {
                            "source": "#main/mapping/sam",
                            "id": "#main/sam2bam/sam"
                        }
                    ],
                    "out": [
                        "#main/sam2bam/bam_unsorted"
                    ],
                    "id": "#main/sam2bam"
                },
                {
                    "doc": "samtools sort - sorts unsorted bam file by coordinates.",
                    "run": "#samtools_sort.cwl",
                    "in": [
                        {
                            "source": "#main/sam2bam/bam_unsorted",
                            "id": "#main/sort_bam/bam_unsorted"
                        }
                    ],
                    "out": [
                        "#main/sort_bam/bam_sorted"
                    ],
                    "id": "#main/sort_bam"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/sort_bam/bam_sorted",
                    "id": "#main/bam"
                },
                {
                    "type": "File",
                    "outputSource": "#main/mapping/bowtie2_log",
                    "id": "#main/bowtie2_log"
                },
                {
                    "type": "File",
                    "outputSource": "#main/adaptor_trimming_and_qc_trimmed/fastq1_trimmed",
                    "id": "#main/fastq1_trimmed"
                },
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "outputSource": "#main/adaptor_trimming_and_qc_trimmed/fastq2_trimmed",
                    "id": "#main/fastq2_trimmed"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputSource": "#main/qc_raw/fastqc_html",
                    "id": "#main/raw_fastqc_html"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputSource": "#main/qc_raw/fastqc_zip",
                    "id": "#main/raw_fastqc_zip"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputSource": "#main/adaptor_trimming_and_qc_trimmed/trim_galore_log",
                    "id": "#main/trim_galore_log"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputSource": "#main/adaptor_trimming_and_qc_trimmed/trimmed_fastqc_html",
                    "id": "#main/trimmed_fastqc_html"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "outputSource": "#main/adaptor_trimming_and_qc_trimmed/trimmed_fastqc_zip",
                    "id": "#main/trimmed_fastqc_zip"
                }
            ],
            "id": "#main"
        }
    ],
    "cwlVersion": "v1.0"
}