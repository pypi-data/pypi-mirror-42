#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

doc: Adds two numbers then subtracts sum by another number

requirements:
  - class: SubworkflowFeatureRequirement

inputs: 
  operand1:
    type: string
    default: "12"

  operand2:
    type: string 
    default: "7"

  operand3:
    type: string
    default: "2"

outputs:
  result:
    outputSource: subtract/difference
    type: File


steps:
  add:
    run: add1.cwl
    in: 
      addition_op1: operand1
      addition_op2: operand2
    out: [sum]

  subtract:
    run: subtract1.cwl
    in:
      subtract_op1: add/sum
      subtract_op2: operand3
    out:
      [difference]
