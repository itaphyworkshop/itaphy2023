# Creating environments using .yml files
YAML is a human-readable data serialization language that is often used to write configuration files that can be used to share environments.

To create a new environment from an ```environment.yml``` file with conda:
```conda env create -f environment.yml```

To activate the environment:
```conda activate name_of_the_environment```

To deactivate the environment:
```conda deactivate```

Read more about managing environments with conda: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
