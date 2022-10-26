#  Nepgeardam

Nepgeardam is an API using mongodb in order to do miscellaneous things

It is made to be the core of multiple application that will talk with it.

# Requirements

This application is made using python and fastAPI.
All library used are in the requirements.txt

A Dockerfile is provided.

The application need mongodb, the url and port need to be indicated int the config.json file (Do not work at this moment, the informations are in the common/mongo.py file)

# Usage

The application come with fastAPI and, therefore, swagger in order to test the different parts.

Currently, the application has the following part:
- Anniversary: Can save date for something, attach him a tag (use for an image on safebooru) and check if today is the day
- Echo: Attach a message to a tag and retrieve it with the tag
- Quotation: Save quote from someone and get one randomly
- Scheduler: Call a webservice when it must be call (Only save the information, this application will not check by himself)
- Misc: Other actions that don't fit anywhere else

For each main part, when you create a collection, you will get two id, the id of the collection needed to access it, and another one that will be needed if you want to do modification to the collection

For the scheduler, the key is currently directly in the class (Probably need to be place in the config.json file)