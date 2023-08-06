#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

doc: Adds two numbers 

inputs:
  addition_op1:
    type: string
    default: "7 "
  addition_op2:
    type: string
    default: "5 "

outputs:
  sum:
    outputSource: addition/result
    type: File

steps:
  addition:
    run:
      class: CommandLineTool
      inputs: 
        statement:
          type: string
          default: "12"
          inputBinding: 
            position: 0

      baseCommand: echo
      stdout: sum.txt
      outputs:
        result: 
          type: stdout

    in: []

    out: [result]


