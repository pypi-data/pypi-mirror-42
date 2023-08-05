==================================================================
PyAlexa: Python module to help in the building of Alexa skill sets
==================================================================

PyPI Package to search for is: pyalexa-skill
============================================


``PyAlexa-Skill`` is an Open Source licensed Python package with a base class that support the necessary methods for an Alexa
Skill set and two scripts to help with the creation of the main entry point and the packaging
of the AWS Lambda Function for the Alexa Skill Set.


AlexaBaseHandler class
----------------------

The AlexaBaseHandler class is an abstract class that provides the necessary
framework to build the response hooks for an Alexa application.

It has a single abstract method, and it will dynamically call methods based on the
Alexa intent or request.

Alexa Requests
--------------
For Alexa requests, this class will look for methods of the form:

    def on_<request name>

For example, the LaunchRequest will look for a method of the name:

    def on_launchrequest(self, launch_request, session):

Alexa/Amazon Intents
--------------------
For Alexa intents, this class will look for methods of the form:

    def on_<intentname>_intent

For example,

AMAZON.YesIntent

will look for a method of the name:

    def on_yes_intent(intent_request, session)

AMAZON.HelpIntent

will look fr a method of the name:

    def on_help_intent(intent_request, session)

Application Defined Intents
---------------------------

And intents that are application defined will follow the form:

    def on_<application intent name>_intent(intent_request, session)


abstract method
---------------
The only abstract method that has to be implemented is the following:


    def on_processing_error(self, event, context, exc):



process_request
---------------
This method will take the 2 parameters that are sent to the lambda function
and determine which of the Alexa handlers to invoke.

For the Amazon Built-in requests such as AMAZON.YesIntent, process request will
call a method of the form:  on_<intentname>_intent, e.g. on_yes_intent().  It is expected
that the concrete implementation will have a the necessary methods to support the
built-in intents.

For custom intents, such as, MyCustomIntent, process request will
call a method of the form:  on_<intentname>_intent, e.g. on_mycustomintent_intent().
In this case, no assumption is made about the custom intent name, so the entire
name is lower cased, then used in the creation of the dynamic method call.

For Amazon Built-in requests such as AudioPlayer.PlaybackStarted, process request will
call a method of the form:  on_<major name>_<minor name>, e.g.
on_audioplayer_playbackstarted().

If any of the dynamically called methods is not found, a NotImplementedError exception
is raised.

_build_speechlet_response
-------------------------
This method ( from the Alexa color example ) will put together the speechlet portion
into a properly formatted json message.  This is typically called by the
concrete implementations of the AlexaBaseHandler.

_build_response
---------------
This method (from the Alexa color example ) will construct a properly formatted
response message so the Amazon Echo knows what to respond with.

AlexaDeploymentHandler class
----------------------------
This class is a reference implementation that does nothing useful.  All Alexa
handlers are handled the same way.

To create the concrete implementation use the following: ::

  from pyalexaskill import AlexaBaseHandler
  class MyConcreteAlexaHandler(AlexaBaseHandler.AlexaBaseHandler):
      # implement the abstract methods

main.py
-------
This file contains the main entry point of the lambda function that is called
for the Alexa skill.

lambda_handler(event, context)
------------------------------
This method ( which can be called anything, you just need to configure it in
the lambda handler ), is the method that is called with the 2 parameters.

This method will typically instantiate an concrete implementation of the
AlexaBaseHandler and delegate to the process_request method.

requirements.txt
----------------
This file is the standard Python requirements file.  This file is used by the
create_deployment.py script to install the necessary 3rd party libraries that
your Alexa skill might need.  Any library specified in the requirements.txt
file will be installed into your deployment directory.

Create a zip file of all code necessary for AWS Lambda
======================================================

create_aws_lambda.py
--------------------
This script creates a zip file per the Amazon lambda specification, such that
it is suitable to upload as your lambda function implementation.

activate your virtualenv and execute like: ::

  create_aws_lambda.py -r <rootdir> -i "list,of,all,python,files,to,include"


create_aws_main.py
------------------
This script creates a template main entry point

All deployments are stored in the deployments subdirectory and follow the naming
convention of 'deployment_n' and 'deployment_n.zip', where 'n' is automatically
calculated to the next largest 'n' in the directory.  Right now it does this
based on the name of the subdirectories of deployments - NOT - the names of
the zip files.

The deployment script will create a deployment directory and zip file for
everything in the requirements.txt file AND the files in the deployment_files
variable in the create_deployment.py file.

When this script is done running, there should be a 'deployment_n.zip' file in the deployments directory.
It is that file that needs to be upload to the Amazon Lambda console.

activate your virutal env and execute like: ::

    create_aws_main.py


create_alexa_handler.py
-----------------------
This script creates a template concrete handler class.

This template can be used as the starting point to create the necessary implementation
details for the handler.

activate your virtualenv and execute like: ::

    create_alexa_handler.py


create_alexa_test_skills.py
---------------------------
This script creates a template utterance and intent schema.

This template can be used as the starting point to create the necessary implementation
details for an actual utterance and intent schema.

activate your virtualenv and execute like: ::

    create_alexa_test_skills.py


create_test_deployment.py
-------------------------
This script calls all of the necessary scripts to create a sample deployment ready to
upload to AWS Lambda, and it creates sample utterances and intent schema.


Test Project
------------
https://github.com/youngsoul/PyAlexaSkillTest
