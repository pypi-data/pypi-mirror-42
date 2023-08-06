# get_env_pass

The get_env_pass module returns the environment variable if is exists in the system running the module. If not, it prompts user for the value

## Installation

`pip install get-env-pass`

## Usage

```
from get_env_pass import get_env_pass

# Returns value if environment variable exists
sys_var = get_env_pass('SYS_VAR')

# Prompts user for input if environment variable does not exist
sys_var = get_env_pass('DOES_NOT_EXIST')

# Prompts user for input if no argument is pass into the function
sys_var = get_env_pass()
```

# Bugs/Request

Please submit an issue in [GitHub](https://github.ibm.com/cbcavale/python-getenvpass/issues/new)

# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue in the [python-getenvpass dashboard](https://github.ibm.com/cbcavale/python-getenvpass/issues), or any other method with the owners(info at the bottom of this README) of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
4. For every new component added or changes made, make sure that it's covered by test(see package json for test framework used or use other components as examples.
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
5. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

##### Maintainers
[@cbcavale](https://github.ibm.com/cbcavale)

