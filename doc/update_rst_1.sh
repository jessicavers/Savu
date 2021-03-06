#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

# Add the relevant savu libraries into your path
module load savu/4.0

# Create pages for savu_config commands and plugin template documentation
python -m doc.create_arg_parser_doc
python -m doc.create_plugin_template_doc

# Remove directory for plugin doc so that there are no obsolete files
rm -rf $DIR/source/reference/plugin_documentation/

# Create contents for plugin api and plugin tools documentation
python -m doc.create_plugin_doc api_plugin plugin_autosummary.rst
python -m doc.create_plugin_doc plugin_documentation plugin_documentation.rst

# Remove the directory containing all plugin guide tests
# rm -rf $DIR/../savu/test/travis/doc_tests/plugins/

# Remove directory for plugin guide testing logs so that there are no obsolete files
# rm -rf $DIR/../savu/test/travis/doc_tests/logs/

# Create the test file from each individual plugin guide
# This is made by collecting the command prompt lines and process lists from each plugin guide
# python -m doc.create_individual_doc_test

# Run documentation tests for process list refresh and process list command execution
# Log files containing the resulting output from each command will be created
# Errors should be raised here if there is a problem with a plugin reference
# python -m unittest savu.test.travis.framework_tests.plugin_doc_test_runner

module unload savu/4.0