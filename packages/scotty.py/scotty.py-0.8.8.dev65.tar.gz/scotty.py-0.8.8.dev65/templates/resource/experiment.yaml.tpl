description: > 
  This is a minimal working example for a scotty experiment that generates the resource $resource_name from the current directory. 
  Be shure that you run this example from the directory which contains the resource_gen.py.
   
  Run this resource on the comando line with: "scotty experiment perform -c example/experiment.yaml" 
  
#############
# Resources #
#############

resources:
  - name: my_$resource_name
    generator: file:.
    params:
      user: myuser
      # Use environment parameter
      passwd: <%= ENV['mysecret'] %> 

#############
# Workloads #
#############
# The minimal example runs without any workload. 
# This is best praxis to develop new resource components. 
# To test your implementation with a workload, please uncomment this lines and spezify your parameters.

#workloads:
#  - name: my_workload
#    generator: git:git@gitlab.gwdg.de:scotty/workload/my_workload[master]
#    params:
#      my_param1: value
#    resources:
#      $resource_name: my_$resource_name
