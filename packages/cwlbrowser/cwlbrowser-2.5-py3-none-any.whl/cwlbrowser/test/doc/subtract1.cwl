#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

doc: Subtracts two numbers

inputs: 
  subtract_op1:
    type: File
    default: sum.txt

  subtract_op2:
    type: string
    default: "2 "

outputs:
  difference: 
    type: File
    outputSource: subtraction/result

steps:
  subtraction:
    run: 
      class: CommandLineTool
      inputs:
        statement:
          type: string
          default: "3"
          inputBinding: 
            position: 0

      baseCommand: echo
      stdout: subtract.txt

      outputs:
        result:
          type: stdout

    in: []
    out: [result]
