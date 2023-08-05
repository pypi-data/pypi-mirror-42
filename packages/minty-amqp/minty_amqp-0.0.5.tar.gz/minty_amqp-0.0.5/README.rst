.. _readme:

Introduction
============

AMQP Consumer service framework.

Getting started
---------------

Main::
  
  def main():
      amqp = AMQPLoader(
          domains=[insert_domains_here],
          command_wrapper_middleware=[insert_wrapper_classes_here],
          config_path="application_config.json",
      )
      amqp.start_client()

Create consumer::

  from minty_amqp.consumer import BaseConsumer

  class ConsumerPrint(BaseConsumer):
    def __call__(self, message):
        print("Message:", message.body, "consumer_touch")
        message.ack()

application_config.json example::

  {
  "config_file": "config.json",
  "url": "http://rabbitmq_url:6782",
  "consumers": [
    {
      "routing_key": "zs.*.base.*",
      "queue_name": "message_print_queue",
      "exchange": "amq.topic",
      "qos_prefetching": 1,
      "class": "package_name.consumer.ConsumerPrint",
      "number_of_channels": 1
    }
  ]
  }



More documentation
------------------

Please see the generated documentation via CI for more information about this
module and how to contribute in our online documentation. Open index.html
when you get there:
`<https://gitlab.com/minty-python/minty_amqp/-/jobs/artifacts/master/browse/tmp/docs?job=qa>`_


Contributing
------------

Please read `CONTRIBUTING.md <https://gitlab.com/minty-python/minty_amqp/blob/master/CONTRIBUTING.md>`_
for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning. For the versions
available, see the
`tags on this repository <https://gitlab.com/minty-python/minty_amqp/tags/>`_

License
-------

Copyright (c) 2018, Minty Team and all persons listed in
`CONTRIBUTORS <https://gitlab.com/minty-python/minty_amqp-cqs/blob/master/CONTRIBUTORS>`_

This project is licensed under the EUPL, v1.2. See the
`EUPL-1.2.txt <https://gitlab.com/minty-python/minty_amqp/blob/master/LICENSE>`_
file for details.
