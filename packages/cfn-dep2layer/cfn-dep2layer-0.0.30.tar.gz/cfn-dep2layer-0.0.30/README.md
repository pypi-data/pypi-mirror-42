# No longer manually download dependencies for your lambda
For each of your Lambda in Cloudformation template, this tool can download dependencies and package them to layer.

Support runtime:

- Python 3.7
- Python 3.6
- Python 2.7
- Node.js 8.10
- Node.js 6.10

## How to use
```
pip3 install -U cfn-dep2layer
cd cloudformation-project-rootdir
dep2layer download --template-file template.yaml --out-template-file .dep2layer-template.yaml
```
