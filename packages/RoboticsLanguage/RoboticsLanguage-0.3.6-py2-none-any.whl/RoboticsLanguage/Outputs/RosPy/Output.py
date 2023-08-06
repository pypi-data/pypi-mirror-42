#
#   This is the Robotics Language compiler
#
#   Output.py: Generates ROS c++ code
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates

import os
import sys
import subprocess


def runPreparations(code, parameters):

  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # get the path to deploy the code
  if 'RosPy' in parameters['globals']['deployOutputs'].keys():
    deploy_path = parameters['globals']['deployOutputs']['RosPy']
  else:
    deploy_path = parameters['globals']['deploy']

  return code, parameters, node_name_underscore, deploy_path


def output(code, parameters):

  # ############ generate code #####################################################
  # check if node tag is present
  if len(code.xpath('/node')) < 1:
    Utilities.logging.warning('No `node` element found. ROS Python will not generate code!')
    return

  # preprocess the code to provide information for templares
  code, parameters, node_name_underscore, deploy_path = runPreparations(code, parameters)

  # run template engine to generate node code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  # ############ create ros message if needed file if needed ############################################
  namespace = {'namespaces': {'rosm': 'rosm'}}

  messages = code.xpath('//rosm:message', **namespace)

  if len(messages) > 0:
    folder =  Utilities.myOutputPath(parameters) + '/' + node_name_underscore + '/msg'
    Utilities.createFolder(folder)

    for message in messages:
      name = message.xpath('.//rosm:name', **namespace)[0].text
      definition =  message.xpath('.//rosm:definition', **namespace)[0].text

      with open(folder + '/' + name + '.msg', 'w') as file:
        file.write(definition)

        Utilities.logging.debug('Wrote file ' + folder + '/' + name + '.msg ...')


  # ############ beautify code #####################################################
  # if the flag beautify is set then run uncrustify
  if parameters['globals']['beautify']:
    try:
      with open(os.devnull, 'w') as output_file:
        list_of_python_files = ['scripts/' + node_name_underscore + '.py']
        for file in list_of_python_files:
          process = subprocess.Popen(['autopep8' deploy_path + '/' + node_name_underscore + '/scripts/' + node_name_underscore + '.py'],
                                     cwd=deploy_path + '/' + node_name_underscore,
                                     stdout=output_file,
                                     stderr=subprocess.STDOUT)
          process.wait()
          if process.returncode > 0:
            Utilities.logger.error("Error beautifying code. autopep8 has returned an error.")
    except:
      # open HTML in different platforms
      if 'darwin' in sys.platform:
        Utilities.logger.error(
            "Error beautifying code. You may need to install autopep8:\n\n  brew install autopep8")

      if 'linux' in sys.platform:
        Utilities.logger.error(
            "Error beautifying code. You may need to install autopep8:\n\n  sudo apt install autopep8")

  # ############ compile code #####################################################
  # if the flag compile is set then run catkin
  if parameters['globals']['compile']:
    if parameters['Outputs']['RosPy']['useColcon']:
      command = ['colcon', 'build', '--packages-select', node_name_underscore]
    else:
      command = ['catkin', 'build', node_name_underscore]

    Utilities.logger.debug("Compiling with: `" + ' '.join(command) + "` in folder " + deploy_path + '/..')
    process = subprocess.Popen(command, cwd=deploy_path +'/..')
    process.wait()

    if process.returncode > 0:
      Utilities.logger.error("Compilation failed!!!")

  # ############ run code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:
    Utilities.logger.debug("launching: `roslaunch " + node_name_underscore + " " + node_name_underscore + '.launch`')
    process = subprocess.Popen(['roslaunch', node_name_underscore, node_name_underscore + '.launch'])
    process.wait()

  return 0
